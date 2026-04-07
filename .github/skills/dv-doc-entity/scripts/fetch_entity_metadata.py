"""
Fetch Dataverse Entity Metadata and Generate Wiki Documentation

Retrieves entity metadata, attributes, option sets, forms, and views from a live
Dataverse environment and writes output to a staging area for AI-assisted merging:

    wiki/Technical-Reference/entities/.staging/{entity}.json      (raw Dataverse data)
    wiki/Technical-Reference/entities/.staging/{entity}.md        (freshly rendered index)
    wiki/Technical-Reference/entities/.staging/{entity}/forms.md
    wiki/Technical-Reference/entities/.staging/{entity}/views.md

Mechanical files are always written directly (never hand-edited):
    wiki/Technical-Reference/entities/.manifest.json   (first-seen change tracking)
    wiki/Technical-Reference/entities/.order           (ADO wiki nav, alphabetical)
    wiki/Technical-Reference/entities/{entity}/.order  (sub-page nav)

After the script completes, the AI merge step reads the staging files alongside
any existing wiki pages and applies changes without overwriting hand-written content.
See SKILL.md Step 3 for merge instructions.

Usage:
    # Document all entities in a solution
    python fetch_entity_metadata.py --solution IncomeAssistanceCore

    # Document a single entity (with forms + views)
    python fetch_entity_metadata.py --entity mnp_application

    # Specify environment
    python fetch_entity_metadata.py --entity account --environment dev

    # Service principal auth
    python fetch_entity_metadata.py --solution IncomeAssistance --app-id <id> --client-secret <secret>

Environment configuration is loaded from the .env file at the repository root.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Shared scripts path
# ---------------------------------------------------------------------------
_SHARED_SCRIPTS_DIR = Path(__file__).parent.parent.parent.parent / "scripts"
if str(_SHARED_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SHARED_SCRIPTS_DIR))

from config_loader import ConfigurationError, load_dataverse_config
from dataverse_sdk_client import DataverseClient

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MANIFEST_FILENAME = ".manifest.json"

FORM_TYPE_NAMES: Dict[int, str] = {
    0: "Dashboard",
    1: "Mobile Express",
    2: "Main",
    4: "Quick View",
    5: "Card",
    6: "Quick Create",
    7: "Quick Create",
    8: "Power BI Embedded",
    10: "Main (Interactive)",
    11: "Card",
    12: "Quick Create Dialog",
}

QUERY_TYPE_NAMES: Dict[int, str] = {
    0: "Public View",
    1: "Advanced Find",
    2: "Associated View",
    4: "Quick Find",
    64: "Lookup View",
}

ATTRIBUTE_TYPE_MAP: Dict[str, str] = {
    "String": "Text",
    "Memo": "Memo",
    "Integer": "Integer",
    "BigInt": "Big Integer",
    "Decimal": "Decimal",
    "Double": "Float",
    "Money": "Currency",
    "Boolean": "Yes/No",
    "DateTime": "DateTime",
    "Lookup": "Lookup",
    "Owner": "Owner",
    "Customer": "Customer",
    "Uniqueidentifier": "Unique Identifier",
    "Picklist": "Option Set",
    "MultiSelectPicklist": "Multi-Select Option Set",
    "Status": "Status",
    "State": "State",
    "Virtual": "Virtual",
    "EntityName": "Entity Name",
    "ManagedProperty": "Managed Property",
    "File": "File",
    "Image": "Image",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def get_display_name(label_obj: Any) -> str:
    """Extract English (1033) display name from a Dataverse LocalizedLabels object."""
    if not label_obj:
        return ""
    if isinstance(label_obj, str):
        return label_obj
    labels = label_obj.get("LocalizedLabels", [])
    for lbl in labels:
        if lbl.get("LanguageCode") == 1033:
            return lbl.get("Label", "")
    user_label = label_obj.get("UserLocalizedLabel")
    if user_label:
        return user_label.get("Label", "")
    return ""


def friendly_type(attr: Dict) -> str:
    return ATTRIBUTE_TYPE_MAP.get(attr.get("AttributeType", ""), attr.get("AttributeType", ""))


def required_level(attr: Dict) -> str:
    rl = attr.get("RequiredLevel", {})
    if isinstance(rl, dict):
        return rl.get("Value", "None")
    return str(rl)


def max_len_or_precision(attr: Dict) -> str:
    val = attr.get("MaxLength") or attr.get("Precision") or attr.get("MinValue")
    return str(val) if val is not None else ""


def escape_pipe(text: str) -> str:
    return text.replace("|", "\\|") if text else ""


def attr_notes(attr: Dict) -> str:
    desc = get_display_name(attr.get("Description", {}))
    if attr.get("AttributeType") == "Lookup":
        targets = attr.get("Targets", [])
        if targets:
            target_str = ", ".join(f"`{t}`" for t in targets)
            return f"-> {target_str}{(' - ' + desc) if desc else ''}"
    return desc


def md_row(*cells) -> str:
    return "| " + " | ".join(escape_pipe(str(c)) for c in cells) + " |"


def is_virtual_shadow(a: Dict) -> bool:
    """Return True for virtual/logical label-cache shadow fields (no display name).

    These fields are system-managed and not directly editable:
    - Virtual fields with no display name: option-set *name companion fields
    - Logical attributes with no display name: lookup *idname / *yominame fields
    - Text fields with no display name whose name ends with 'name' or 'yominame':
      lookup name-cache fields that may not have IsLogicalAttribute set
    """
    has_display_name = bool(get_display_name(a.get("DisplayName", {})))
    if not has_display_name:
        attr_type = a.get("AttributeType", "")
        logical_name = a.get("LogicalName", "")
        if attr_type == "Virtual":
            return True
        if a.get("IsLogicalAttribute", False):
            return True
        # Lookup name-cache Text fields (e.g. *idname, *yominame, *accountname)
        # Note: raw Dataverse AttributeType is "String" — "Text" is the display alias
        if a.get("AttributeType") == "String" and (
            logical_name.endswith("yominame")
            or logical_name.endswith("idname")
            or (logical_name.endswith("name") and len(logical_name) > 6)
        ):
            return True
    return False


# ---------------------------------------------------------------------------
# Relationship helpers
# ---------------------------------------------------------------------------


def get_rel_menu_label(rel: Dict) -> str:
    """Return the AssociatedMenuConfiguration label when the relationship is visible."""
    config = rel.get("AssociatedMenuConfiguration") or {}
    if config.get("Behavior") == "DoNotDisplay":
        return ""
    label_obj = config.get("Label")
    return get_display_name(label_obj) if label_obj else ""


def get_rel_cascade_delete(rel: Dict) -> str:
    """Return the delete cascade behaviour from CascadeConfiguration."""
    cascade = rel.get("CascadeConfiguration") or {}
    return cascade.get("Delete", "")


# ---------------------------------------------------------------------------
# FetchXML analysis helpers
# ---------------------------------------------------------------------------


def parse_fetchxml_filters(fetchxml: str) -> List[str]:
    """Return a human-readable list of filter conditions from FetchXML."""
    if not fetchxml:
        return []
    try:
        root = ET.fromstring(fetchxml)
        conditions: List[str] = []
        for cond in root.iter("condition"):
            attr = cond.get("attribute", "")
            op = cond.get("operator", "")
            val = cond.get("value", "")
            if attr:
                conditions.append(f"`{attr}` {op}" + (f" `{val}`" if val else ""))
        return conditions
    except ET.ParseError:
        return []


def parse_fetchxml_orderby(fetchxml: str) -> List[Tuple[str, str]]:
    """Return (attribute, direction) pairs for each order element in FetchXML."""
    if not fetchxml:
        return []
    try:
        root = ET.fromstring(fetchxml)
        orders: List[Tuple[str, str]] = []
        for order in root.iter("order"):
            attr = order.get("attribute", "")
            desc = order.get("descending", "false").lower() == "true"
            if attr:
                orders.append((attr, "desc" if desc else "asc"))
        return orders
    except ET.ParseError:
        return []


# ---------------------------------------------------------------------------
# Manifest (change tracking)
# ---------------------------------------------------------------------------


def load_manifest(entities_dir: Path) -> Dict:
    """Load the first-seen manifest from disk, or return an empty dict."""
    manifest_file = entities_dir / MANIFEST_FILENAME
    if manifest_file.exists():
        try:
            return json.loads(manifest_file.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_manifest(entities_dir: Path, manifest: Dict) -> None:
    """Persist the manifest back to disk."""
    manifest_file = entities_dir / MANIFEST_FILENAME
    manifest_file.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def update_manifest(manifest: Dict, entity: str, data: Dict, today: str) -> None:
    """Record first-seen dates for the entity and each of its attributes.

    Existing dates are never overwritten — only new entries are added.

    Date sourcing priority (best to worst):
      1. solutioncomponent.createdon  — "when it arrived in this environment"
      2. today                        — fallback when component history is unavailable
    """
    entity_record = manifest.setdefault(entity, {})
    if "first_seen" not in entity_record:
        component_date = data.get("entity_component_date")
        entity_record["first_seen"] = component_date or today
        if component_date:
            entity_record["first_seen_source"] = "solution_history"

    attr_dates = entity_record.setdefault("attributes", {})
    attr_component_dates: Dict[str, str] = data.get("attribute_component_dates", {})
    for attr in data["attributes"]:
        name = attr.get("LogicalName", "")
        if name and name not in attr_dates and attr.get("IsCustomAttribute", False):
            created_on = _parse_component_date(attr.get("CreatedOn", ""))
            attr_dates[name] = attr_component_dates.get(name) or created_on or today


# ---------------------------------------------------------------------------
# Solution component date helpers
# ---------------------------------------------------------------------------


def _parse_component_date(createdon_str: str) -> Optional[str]:
    """Parse a solutioncomponent createdon value to YYYY-MM-DD.

    Returns None for placeholder dates (1900-01-01) or anything unparseable.
    Dataverse does not reliably populate metadata CreatedOn; solutioncomponent
    createdon is the best available proxy for "when this arrived in this environment".
    """
    if not createdon_str:
        return None
    if createdon_str.startswith("1900-"):
        return None
    try:
        return createdon_str[:10]
    except Exception:
        return None


def fetch_entity_component_date(client: DataverseClient, metadata_id: str) -> Optional[str]:
    """Return the earliest solutioncomponent createdon for an entity (componenttype=1).

    Queries the solutioncomponents table by the entity's MetadataId and returns the
    earliest non-placeholder createdon as a YYYY-MM-DD string, or None if unavailable.
    """
    if not metadata_id:
        return None
    try:
        base = client.base_uri
        uri = (
            f"{base}solutioncomponents"
            f"?$filter=objectid eq {metadata_id} and componenttype eq 1"
            f"&$select=objectid,createdon"
            f"&$orderby=createdon asc"
            f"&$top=1"
        )
        result = client._invoke_resilient_request("GET", uri)
        components = (result or {}).get("value", [])
        if components:
            return _parse_component_date(components[0].get("createdon", ""))
    except Exception as exc:
        logger.debug("Could not fetch entity component date for %s: %s", metadata_id, exc)
    return None


def fetch_attribute_component_dates(client: DataverseClient, attributes: List[Dict]) -> Dict[str, str]:
    """Return earliest solutioncomponent createdon per custom attribute (componenttype=2).

    Only queries custom attributes (IsCustomAttribute=True) — OOTB fields return
    placeholder dates (1900-01-01) from the platform and are not worth the API cost.

    MetadataIds are batched in groups of 20 to reduce request count.
    Returns dict mapping LogicalName -> YYYY-MM-DD for attributes with a usable date.
    """
    custom_attrs = [
        a for a in attributes
        if a.get("IsCustomAttribute", False) and a.get("MetadataId") and a.get("LogicalName")
    ]
    if not custom_attrs:
        return {}

    base = client.base_uri
    id_to_name: Dict[str, str] = {a["MetadataId"]: a["LogicalName"] for a in custom_attrs}
    result: Dict[str, str] = {}

    ids = list(id_to_name.keys())
    batch_size = 20
    for i in range(0, len(ids), batch_size):
        batch = ids[i : i + batch_size]
        filter_parts = " or ".join(f"objectid eq {mid}" for mid in batch)
        uri = (
            f"{base}solutioncomponents"
            f"?$filter=componenttype eq 2 and ({filter_parts})"
            f"&$select=objectid,createdon"
            f"&$orderby=objectid asc,createdon asc"
        )
        try:
            batch_result = client._invoke_resilient_request("GET", uri)
            components = (batch_result or {}).get("value", [])
            for comp in components:
                oid = comp.get("objectid", "")
                d = _parse_component_date(comp.get("createdon", ""))
                logical_name = id_to_name.get(oid, "")
                if logical_name and d:
                    # Keep the earliest date when multiple solution layers exist
                    if logical_name not in result or d < result[logical_name]:
                        result[logical_name] = d
        except Exception as exc:
            logger.debug("Could not fetch attribute component dates (batch %d): %s", i, exc)

    return result


def fetch_entity_logical_names_for_solution(client: DataverseClient, solution_unique_name: str) -> List[str]:
    """Return the list of entity logical names that belong to a solution."""
    base = client.base_uri

    print(f"  Looking up solution '{solution_unique_name}'...")
    sol_uri = (
        f"{base}solutions?$filter=uniquename eq '{solution_unique_name}'"
        f"&$select=solutionid,uniquename,friendlyname,version"
    )
    sol_result = client._invoke_resilient_request("GET", sol_uri)
    solutions = (sol_result or {}).get("value", [])
    if not solutions:
        raise ValueError(f"Solution '{solution_unique_name}' not found in environment.")
    solution = solutions[0]
    solution_id = solution["solutionid"]
    print(f"  Found solution: {solution.get('friendlyname', solution_unique_name)} v{solution.get('version', '?')}")

    comp_uri = (
        f"{base}solutioncomponents"
        f"?$filter=_solutionid_value eq '{solution_id}' and componenttype eq 1"
        f"&$select=objectid,componenttype"
    )
    comp_result = client._invoke_resilient_request("GET", comp_uri)
    components = (comp_result or {}).get("value", [])
    print(f"  Found {len(components)} entity components in solution.")

    logical_names: List[str] = []
    for comp in components:
        obj_id = comp.get("objectid")
        if not obj_id:
            continue
        meta_uri = f"{base}EntityDefinitions({obj_id})?$select=LogicalName"
        meta = client._invoke_resilient_request("GET", meta_uri)
        if meta and meta.get("LogicalName"):
            logical_names.append(meta["LogicalName"])

    return sorted(logical_names)


def fetch_entity_data(client: DataverseClient, entity: str) -> Dict:
    """Fetch all metadata needed to document an entity."""
    base = client.base_uri

    print(f"    Fetching entity definition...")
    entity_meta = client.get_entity_metadata(entity)

    print(f"    Fetching attributes...")
    attributes = client.get_entity_attributes(entity)

    print(f"    Fetching option sets...")
    pl_uri = (
        f"{base}EntityDefinitions(LogicalName='{entity}')"
        f"/Attributes/Microsoft.Dynamics.CRM.PicklistAttributeMetadata"
        f"?$expand=OptionSet,GlobalOptionSet"
    )
    pl_result = client._invoke_resilient_request("GET", pl_uri)
    picklists = (pl_result or {}).get("value", [])

    ms_uri = (
        f"{base}EntityDefinitions(LogicalName='{entity}')"
        f"/Attributes/Microsoft.Dynamics.CRM.MultiSelectPicklistAttributeMetadata"
        f"?$expand=OptionSet,GlobalOptionSet"
    )
    ms_result = client._invoke_resilient_request("GET", ms_uri)
    multiselects = (ms_result or {}).get("value", [])

    print(f"    Fetching relationships...")
    onetomany = (client._invoke_resilient_request("GET", f"{base}EntityDefinitions(LogicalName='{entity}')/OneToManyRelationships") or {}).get("value", [])
    manytoone = (client._invoke_resilient_request("GET", f"{base}EntityDefinitions(LogicalName='{entity}')/ManyToOneRelationships") or {}).get("value", [])
    manytomany = (client._invoke_resilient_request("GET", f"{base}EntityDefinitions(LogicalName='{entity}')/ManyToManyRelationships") or {}).get("value", [])

    print(f"    Fetching forms...")
    forms_uri = (
        f"{base}systemforms"
        f"?$filter=objecttypecode eq '{entity}' and formactivationstate eq 1"
        f"&$select=name,type,description,isdefault,formjson,formxml,iscustomizable"
        f"&$orderby=type asc,name asc"
    )
    forms_result = client._invoke_resilient_request("GET", forms_uri)
    forms = (forms_result or {}).get("value", [])

    print(f"    Fetching views...")
    views_uri = (
        f"{base}savedqueries"
        f"?$filter=returnedtypecode eq '{entity}'"
        f"&$select=name,querytype,isdefault,iscustomizable,fetchxml,layoutxml,description"
        f"&$orderby=querytype asc,name asc"
    )
    views_result = client._invoke_resilient_request("GET", views_uri)
    views = (views_result or {}).get("value", [])

    print(f"    Fetching solution component dates...")
    entity_metadata_id = entity_meta.get("MetadataId", "")
    entity_component_date = fetch_entity_component_date(client, entity_metadata_id)
    attribute_component_dates = fetch_attribute_component_dates(client, attributes)
    if entity_component_date:
        print(f"      Entity added to environment: {entity_component_date}")
    print(f"      Attribute dates resolved: {len(attribute_component_dates)}/{sum(1 for a in attributes if a.get('IsCustomAttribute'))}")

    return {
        "entity_meta": entity_meta,
        "attributes": attributes,
        "picklists": picklists,
        "multiselects": multiselects,
        "onetomany": onetomany,
        "manytoone": manytoone,
        "manytomany": manytomany,
        "forms": forms,
        "views": views,
        "entity_component_date": entity_component_date,
        "attribute_component_dates": attribute_component_dates,
    }


# ---------------------------------------------------------------------------
# Form XML parsing
# ---------------------------------------------------------------------------


def extract_form_fields(form: Dict) -> List[str]:
    """Extract a flat list of field logical names from a form's formjson or formxml."""
    fields: List[str] = []

    form_json_str = form.get("formjson") or ""
    if form_json_str:
        try:
            fj = json.loads(form_json_str)
            tabs = fj.get("Tabs", {}).get("Tabs", []) or fj.get("tabs", [])
            for tab in tabs:
                cols = tab.get("Columns", {}).get("Columns", []) or tab.get("columns", [])
                for col in cols:
                    sections = col.get("Sections", {}).get("Sections", []) or col.get("sections", [])
                    for sec in sections:
                        rows = sec.get("Rows", {}).get("Rows", []) or sec.get("rows", [])
                        for row in rows:
                            cells = row.get("Cells", {}).get("Cells", []) or row.get("cells", [])
                            for cell in cells:
                                control = cell.get("Control") or cell.get("control") or {}
                                attr = control.get("DataFieldName") or control.get("datafieldname") or ""
                                if attr and attr not in fields:
                                    fields.append(attr)
        except (json.JSONDecodeError, AttributeError):
            pass

    if not fields:
        # Fallback: parse legacy formxml
        structured = _parse_formxml_structured(form.get("formxml") or "")
        fields = [f for _, _, f in structured]

    return fields


def _parse_formxml_structured(formxml_str: str) -> List[Tuple[Optional[str], Optional[str], str]]:
    """Parse formxml and return (tab_label, section_label, field_logical_name) tuples."""
    if not formxml_str:
        return []
    try:
        root = ET.fromstring(formxml_str)
        results: List[Tuple[Optional[str], Optional[str], str]] = []
        seen: set = set()

        tabs_el = root.find("tabs")
        if tabs_el is None:
            # Flat structure — extract all datafieldname values
            for ctrl in root.iter("control"):
                field = ctrl.get("datafieldname", "")
                if field and field not in seen:
                    seen.add(field)
                    results.append((None, None, field))
            return results

        for tab in tabs_el.findall("tab"):
            tab_label: Optional[str] = None
            lbl_el = tab.find("labels/label[@languagecode='1033']")
            if lbl_el is not None:
                tab_label = lbl_el.get("description") or None

            for section in tab.iter("section"):
                sec_label: Optional[str] = None
                sec_lbl_el = section.find("labels/label[@languagecode='1033']")
                if sec_lbl_el is not None:
                    sec_label = sec_lbl_el.get("description") or None

                for ctrl in section.iter("control"):
                    field = ctrl.get("datafieldname", "")
                    if field and field not in seen:
                        seen.add(field)
                        results.append((tab_label, sec_label, field))

        return results
    except ET.ParseError:
        return []


def extract_form_fields_structured(form: Dict) -> Optional[List[Tuple[Optional[str], Optional[str], str]]]:
    """Return (tab_label, section_label, field) tuples when tab/section structure is available.

    Tries formjson first (modern Dataverse), then falls back to formxml.
    Returns None when no structural data is available.
    """
    # Try formjson
    form_json_str = form.get("formjson") or ""
    if form_json_str:
        try:
            fj = json.loads(form_json_str)
            results: List[Tuple[Optional[str], Optional[str], str]] = []
            seen: set = set()
            tabs = fj.get("Tabs", {}).get("Tabs", []) or fj.get("tabs", [])
            for tab in tabs:
                tab_name = tab.get("Name") or tab.get("name") or None
                cols = tab.get("Columns", {}).get("Columns", []) or tab.get("columns", [])
                for col in cols:
                    sections = col.get("Sections", {}).get("Sections", []) or col.get("sections", [])
                    for sec in sections:
                        sec_name = sec.get("Name") or sec.get("name") or None
                        rows = sec.get("Rows", {}).get("Rows", []) or sec.get("rows", [])
                        for row in rows:
                            cells = row.get("Cells", {}).get("Cells", []) or row.get("cells", [])
                            for cell in cells:
                                ctrl = cell.get("Control") or cell.get("control") or {}
                                attr = ctrl.get("DataFieldName") or ctrl.get("datafieldname") or ""
                                if attr and attr not in seen:
                                    seen.add(attr)
                                    results.append((tab_name, sec_name, attr))
            if results:
                return results
        except (json.JSONDecodeError, AttributeError):
            pass

    # Try formxml
    structured = _parse_formxml_structured(form.get("formxml") or "")
    return structured if structured else None


# ---------------------------------------------------------------------------
# FetchXML parsing helpers
# ---------------------------------------------------------------------------


def parse_fetchxml_columns(fetchxml: str) -> List[str]:
    """Extract attribute names from a FetchXML string."""
    if not fetchxml:
        return []
    try:
        root = ET.fromstring(fetchxml)
        return [a.get("name", "") for a in root.iter("attribute") if a.get("name")]
    except ET.ParseError:
        return []


def parse_layout_columns(layoutxml: str) -> List[str]:
    """Extract column names from a layoutxml string."""
    if not layoutxml:
        return []
    try:
        root = ET.fromstring(layoutxml)
        return [c.get("name", "") for c in root.iter("cell") if c.get("name")]
    except ET.ParseError:
        return []


# ---------------------------------------------------------------------------
# Wiki page generation
# ---------------------------------------------------------------------------

ATTR_HEADER = "| Schema Name | Display Name | Type | Required | Max Length | Added | Introduced Version | Notes |"
ATTR_SEP = "|---|---|---|---|---|---|---|---|"

REL_HEADER = "| Schema Name | Direction | Related Entity | Attribute | Menu Label | On Delete |"
REL_SEP = "|---|---|---|---|---|---|"


def _attr_row(a: Dict, added: str = "") -> str:
    return md_row(
        f"`{a.get('LogicalName', '')}`",
        get_display_name(a.get("DisplayName", {})),
        friendly_type(a),
        required_level(a),
        max_len_or_precision(a),
        added,
        a.get("IntroducedVersion", "") or "-",
        attr_notes(a),
    )


def _rel_row(direction: str, r: Dict, entity: str) -> str:
    schema = r.get("SchemaName", "")
    if direction == "1:N":
        related = r.get("ReferencingEntity", "")
        attr = r.get("ReferencingAttribute", "")
    elif direction == "N:1":
        related = r.get("ReferencedEntity", "")
        attr = r.get("ReferencingAttribute", "")
    else:
        e1 = r.get("Entity1LogicalName", "")
        e2 = r.get("Entity2LogicalName", "")
        related = e2 if e1 == entity else e1
        attr = ""
    menu_label = get_rel_menu_label(r)
    on_delete = get_rel_cascade_delete(r) if direction == "1:N" else ""
    return md_row(
        f"`{schema}`",
        direction,
        f"`{related}`",
        f"`{attr}`" if attr else "",
        menu_label,
        on_delete,
    )


def generate_entity_index(data: Dict, entity: str, entity_manifest: Optional[Dict] = None) -> str:
    """Generate the lean entity index page (overview table + sub-page links only).

    The Business Analysis section is intentionally omitted here — it is written
    by the AI merge step using wiki domain context and preserved on re-runs.
    """
    meta = data["entity_meta"]
    attributes = data["attributes"]
    onetomany = data["onetomany"]
    manytoone = data["manytoone"]
    manytomany = data["manytomany"]

    if entity_manifest is None:
        entity_manifest = {}

    display = get_display_name(meta.get("DisplayName", {})) or entity
    lines: List[str] = []

    # Title + overview
    lines += [f"# {display}", ""]
    lines += ["## Overview", ""]
    lines += ["| Property | Value |", "|---|---|"]
    lines.append(md_row("Logical Name", f"`{meta.get('LogicalName', '')}`"))
    lines.append(md_row("Schema Name", meta.get("SchemaName", "")))
    lines.append(md_row("Entity Set Name", meta.get("EntitySetName", "")))
    lines.append(md_row("Object Type Code", meta.get("ObjectTypeCode", "")))
    lines.append(md_row("Primary Key", f"`{meta.get('PrimaryIdAttribute', '')}`"))
    lines.append(md_row("Primary Name Field", f"`{meta.get('PrimaryNameAttribute', '')}`"))
    lines.append(md_row("Ownership", meta.get("OwnershipType", "")))
    lines.append(md_row("Is Custom Entity", "Yes" if meta.get("IsCustomEntity") else "No"))
    desc = get_display_name(meta.get("Description", {}))
    if desc:
        lines.append(md_row("Description", desc))
    first_seen = entity_manifest.get("first_seen", "")
    is_custom_entity = meta.get("IsCustomEntity", False)
    if is_custom_entity and first_seen:
        label = "Added to Environment" if entity_manifest.get("first_seen_source") == "solution_history" else "First Documented"
        lines.append(md_row(label, first_seen))
    elif not is_custom_entity:
        lines.append(md_row("Date Added", "-"))

    # Quick stats
    custom_count = sum(1 for a in attributes if a.get("IsCustomAttribute", False))
    total_count = len(attributes)
    custom_rel_count = sum(
        1 for r in list(onetomany) + list(manytoone) + list(manytomany)
        if r.get("IsCustomRelationship", False)
    )
    lines.append(md_row("Custom Attributes", str(custom_count)))
    lines.append(md_row("Total Attributes", str(total_count)))
    lines.append(md_row("Custom Relationships", str(custom_rel_count)))
    lines.append("")

    # Sub-page links
    base_path = f"/wiki/Technical-Reference/entities/{entity}"
    lines += ["## Pages", ""]
    lines += [
        f"- [Attributes]({base_path}/attributes) — Custom and standard fields, local option sets",
        f"- [Relationships]({base_path}/relationships) — 1:N, N:1, and N:N relationships",
        f"- [Forms]({base_path}/forms) — Form layouts and field mappings",
        f"- [Views]({base_path}/views) — Saved queries and view definitions",
        "",
    ]

    return "\n".join(lines)


def generate_attributes_page(data: Dict, entity: str, entity_manifest: Optional[Dict] = None) -> str:
    """Generate attributes.md — custom fields, standard fields, local option sets, and shadow fields."""
    meta = data["entity_meta"]
    attributes = data["attributes"]
    picklists = data["picklists"]
    multiselects = data["multiselects"]

    if entity_manifest is None:
        entity_manifest = {}
    attr_dates = entity_manifest.get("attributes", {})

    display = get_display_name(meta.get("DisplayName", {})) or entity
    lines: List[str] = [f"# {display} — Attributes", ""]

    all_custom = sorted(
        [a for a in attributes if a.get("IsCustomAttribute", False)],
        key=lambda x: x.get("LogicalName", ""),
    )
    all_ootb = sorted(
        [a for a in attributes if not a.get("IsCustomAttribute", False)],
        key=lambda x: x.get("LogicalName", ""),
    )

    # Split real (editable) fields from virtual/shadow label-cache fields
    custom_real = [a for a in all_custom if not is_virtual_shadow(a)]
    custom_virtual = [a for a in all_custom if is_virtual_shadow(a)]
    ootb_real = [a for a in all_ootb if not is_virtual_shadow(a)]
    ootb_virtual = [a for a in all_ootb if is_virtual_shadow(a)]

    lines += [
        f"This entity has **{len(custom_real)}** editable custom field(s), "
        f"**{len(ootb_real)}** standard (OOTB) field(s), and "
        f"**{len(custom_virtual) + len(ootb_virtual)}** virtual/shadow fields "
        f"(system-managed label-cache fields, listed in the [Virtual / Shadow Fields](#virtual--shadow-fields) section below).",
        "",
    ]

    lines += ["## Custom Fields", ""]
    if custom_real:
        lines += [ATTR_HEADER, ATTR_SEP]
        lines += [_attr_row(a, attr_dates.get(a.get("LogicalName", ""), "")) for a in custom_real]
    else:
        lines.append("*No custom fields.*")
    lines.append("")

    lines += ["## Standard (OOTB) Fields", ""]
    if ootb_real:
        lines += [ATTR_HEADER, ATTR_SEP]
        lines += [_attr_row(a, "-") for a in ootb_real]
    else:
        lines.append("*No standard fields.*")
    lines.append("")

    # Local option sets
    optionset_map: Dict[str, Dict] = {}
    for item in list(picklists) + list(multiselects):
        optionset_map[item.get("LogicalName", "")] = item

    local_sets = [
        (name, item, item["OptionSet"])
        for name, item in optionset_map.items()
        if item.get("OptionSet") and not item.get("GlobalOptionSet")
    ]
    local_sets.sort(key=lambda x: x[0])

    lines += ["## Local Option Sets", ""]
    if local_sets:
        for attr_name, item, os_data in local_sets:
            attr_display = get_display_name(item.get("DisplayName", {}))
            os_desc = get_display_name(os_data.get("Description", {}))
            lines += [f"### `{attr_name}` — {attr_display}", ""]
            if os_desc:
                lines += [os_desc, ""]
            lines += ["| Value | Label |", "|---|---|"]
            for opt in sorted(os_data.get("Options", []), key=lambda o: o.get("Value", 0)):
                label = get_display_name(opt.get("Label", {}))
                lines.append(md_row(str(opt.get("Value", "")), label))
            lines.append("")
    else:
        lines.append("*No local option sets found.*")
        lines.append("")

    # Virtual / shadow fields section
    all_shadow = sorted(custom_virtual + ootb_virtual, key=lambda x: x.get("LogicalName", ""))
    lines += ["## Virtual / Shadow Fields", ""]
    lines += [
        "These fields are system-managed and not directly editable. "
        "Dataverse automatically populates them to cache display labels for lookups and option sets.",
        "",
    ]
    if all_shadow:
        lines += [ATTR_HEADER, ATTR_SEP]
        lines += [_attr_row(a, attr_dates.get(a.get("LogicalName", ""), "") if a.get("IsCustomAttribute", False) else "-") for a in all_shadow]
    else:
        lines.append("*No virtual/shadow fields.*")
    lines.append("")

    return "\n".join(lines)


def generate_relationships_page(data: Dict, entity: str) -> str:
    """Generate relationships.md — all 1:N, N:1, and N:N relationships."""
    meta = data["entity_meta"]
    onetomany = data["onetomany"]
    manytoone = data["manytoone"]
    manytomany = data["manytomany"]

    display = get_display_name(meta.get("DisplayName", {})) or entity
    lines: List[str] = [f"# {display} — Relationships", ""]

    all_rels: List[Tuple[str, Dict]] = (
        [("1:N", r) for r in onetomany]
        + [("N:1", r) for r in manytoone]
        + [("N:N", r) for r in manytomany]
    )
    custom_rels = sorted(
        [(d, r) for d, r in all_rels if r.get("IsCustomRelationship", False)],
        key=lambda x: x[1].get("SchemaName", ""),
    )
    ootb_rels = sorted(
        [(d, r) for d, r in all_rels if not r.get("IsCustomRelationship", False)],
        key=lambda x: x[1].get("SchemaName", ""),
    )

    custom_1n = sum(1 for d, _ in custom_rels if d == "1:N")
    custom_n1 = sum(1 for d, _ in custom_rels if d == "N:1")
    custom_nn = sum(1 for d, _ in custom_rels if d == "N:N")
    lines += [
        f"This entity has **{len(custom_rels)}** custom relationship(s) "
        f"({custom_1n} one-to-many, {custom_n1} many-to-one, {custom_nn} many-to-many) "
        f"and **{len(ootb_rels)}** standard (OOTB) relationship(s). "
        "The **Menu Label** column shows the sub-grid label when the related records are "
        "displayed in the form. **On Delete** shows what happens to child records when "
        "the parent is deleted (1:N only).",
        "",
    ]

    lines += ["## Custom Relationships", ""]
    if custom_rels:
        lines += [REL_HEADER, REL_SEP]
        lines += [_rel_row(d, r, entity) for d, r in custom_rels]
    else:
        lines.append("*No custom relationships.*")
    lines.append("")

    lines += ["## Standard (OOTB) Relationships", ""]
    if ootb_rels:
        lines += [REL_HEADER, REL_SEP]
        lines += [_rel_row(d, r, entity) for d, r in ootb_rels]
    else:
        lines.append("*No standard relationships.*")
    lines.append("")

    return "\n".join(lines)


def generate_forms_page(data: Dict, entity: str) -> str:
    """Generate forms.md wiki page for an entity."""
    forms = data["forms"]
    display = get_display_name(data["entity_meta"].get("DisplayName", {})) or entity
    lines: List[str] = [f"# {display} — Forms", ""]

    if not forms:
        lines.append("*No active forms found for this entity.*")
        return "\n".join(lines)

    # Count forms with field detail available
    forms_with_detail = sum(
        1 for f in forms
        if f.get("formjson") or f.get("formxml")
    )
    lines += [
        f"This entity has **{len(forms)}** active form(s). "
        + (
            f"Field-level detail is available for **{forms_with_detail}** form(s) "
            "(sourced from `formjson` or `formxml`)."
            if forms_with_detail
            else "Field-level detail is not available from the API for any of these forms."
        ),
        "",
    ]

    lines += [
        "| Name | Type | Is Default | Customizable |",
        "|---|---|---|---|",
    ]
    for f in forms:
        form_type = FORM_TYPE_NAMES.get(f.get("type", -1), str(f.get("type", "")))
        lines.append(md_row(
            f.get("name", ""),
            form_type,
            "Yes" if f.get("isdefault") else "No",
            "Yes" if (f.get("iscustomizable") or {}).get("Value", False) else "No",
        ))
    lines.append("")

    for f in forms:
        form_name = f.get("name", "")
        form_type = FORM_TYPE_NAMES.get(f.get("type", -1), str(f.get("type", "")))
        lines += [f"## {form_name} ({form_type})", ""]
        desc = f.get("description", "")
        if desc:
            lines += [desc, ""]

        structured = extract_form_fields_structured(f)
        if structured:
            # Render fields grouped by tab → section
            lines += ["**Fields on this form:**", ""]
            current_tab: Optional[str] = "__unset__"
            current_sec: Optional[str] = "__unset__"
            for tab_label, sec_label, field in structured:
                if tab_label != current_tab:
                    current_tab = tab_label
                    current_sec = "__unset__"
                    if tab_label:
                        lines += [f"**{tab_label}**", ""]
                if sec_label != current_sec:
                    current_sec = sec_label
                    if sec_label:
                        lines += [f"*{sec_label}*", ""]
                lines.append(f"- `{field}`")
            lines.append("")
        else:
            lines.append("*Form field details not available (formjson and formxml not returned by API).*")
            lines.append("")

    return "\n".join(lines)


def generate_views_page(data: Dict, entity: str) -> str:
    """Generate views.md wiki page for an entity."""
    views = data["views"]
    display = get_display_name(data["entity_meta"].get("DisplayName", {})) or entity
    lines: List[str] = [f"# {display} — Views", ""]

    # Build a lookup map: logical_name → display_name for column enrichment
    attr_display_map: Dict[str, str] = {
        a.get("LogicalName", ""): get_display_name(a.get("DisplayName", {}))
        for a in data["attributes"]
        if a.get("LogicalName") and get_display_name(a.get("DisplayName", {}))
    }

    if not views:
        lines.append("*No views found for this entity.*")
        return "\n".join(lines)

    # Count views with column detail
    views_with_cols = sum(1 for v in views if v.get("layoutxml") or v.get("fetchxml"))
    lines += [
        f"This entity has **{len(views)}** saved view(s). "
        f"Column and filter details are derived from `layoutxml` and `fetchxml`.",
        "",
    ]

    lines += [
        "| Name | Type | Is Default | Customizable |",
        "|---|---|---|---|",
    ]
    for v in views:
        query_type = QUERY_TYPE_NAMES.get(v.get("querytype", -1), str(v.get("querytype", "")))
        lines.append(md_row(
            v.get("name", ""),
            query_type,
            "Yes" if v.get("isdefault") else "No",
            "Yes" if (v.get("iscustomizable") or {}).get("Value", False) else "No",
        ))
    lines.append("")

    for v in views:
        view_name = v.get("name", "")
        query_type = QUERY_TYPE_NAMES.get(v.get("querytype", -1), str(v.get("querytype", "")))
        lines += [f"## {view_name} ({query_type})", ""]
        desc = v.get("description", "")
        if desc:
            lines += [desc, ""]

        layout_cols = parse_layout_columns(v.get("layoutxml", ""))
        if layout_cols:
            lines += ["**Columns:**", ""]
            lines += ["| Column | Display Name |", "|---|---|"]
            for col in layout_cols:
                col_display = attr_display_map.get(col, "")
                lines.append(md_row(f"`{col}`", col_display))
            lines.append("")

        filter_conditions = parse_fetchxml_filters(v.get("fetchxml", ""))
        if filter_conditions:
            lines += ["**Filters:**", ""]
            for cond in filter_conditions:
                lines.append(f"- {cond}")
            lines.append("")

        orderby = parse_fetchxml_orderby(v.get("fetchxml", ""))
        if orderby:
            lines += ["**Order by:**", ""]
            for attr, direction in orderby:
                attr_display = attr_display_map.get(attr, "")
                suffix = f" ({attr_display})" if attr_display else ""
                lines.append(f"- `{attr}`{suffix} — {direction}")
            lines.append("")

        fetch_attrs = parse_fetchxml_columns(v.get("fetchxml", ""))
        if fetch_attrs:
            lines += ["**FetchXML Attributes:**", ""]
            lines += ["| Attribute |", "|---|"]
            for attr in fetch_attrs:
                lines.append(md_row(f"`{attr}`"))
            lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# .order file management
# ---------------------------------------------------------------------------


def update_order_file(entities_dir: Path, new_entity: str) -> None:
    """Add entity to .order file if not already present, maintaining alphabetical order."""
    order_file = entities_dir / ".order"
    existing: List[str] = []
    if order_file.exists():
        existing = [line.strip() for line in order_file.read_text(encoding="utf-8").splitlines() if line.strip()]

    if new_entity not in existing:
        existing.append(new_entity)
        existing.sort()
        order_file.write_text("\n".join(existing) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Output writing
# ---------------------------------------------------------------------------


def write_entity_docs(data: Dict, entity: str, entities_dir: Path, manifest: Dict, staging_dir: Path) -> None:
    """Write staging files and update mechanical files (.order, manifest).

    Staging files (fresh Dataverse output) are written to staging_dir/ for AI review.
    The AI merge step (SKILL.md Step 3) is responsible for applying staged changes
    to the final wiki pages without overwriting hand-written content.

    Mechanical files (.order, .manifest.json) are always written directly because
    they are never hand-edited.
    """
    today = date.today().isoformat()
    update_manifest(manifest, entity, data, today)
    entity_manifest = manifest.get(entity, {})

    # --- Staging: fresh Dataverse output for AI consumption ---
    staging_dir.mkdir(parents=True, exist_ok=True)

    # Raw JSON so AI can diff field-by-field without parsing markdown
    (staging_dir / f"{entity}.json").write_text(
        json.dumps(data, indent=2, default=str), encoding="utf-8"
    )

    # Freshly rendered markdown pages
    index_content = generate_entity_index(data, entity, entity_manifest)
    (staging_dir / f"{entity}.md").write_text(index_content, encoding="utf-8")

    staging_entity_dir = staging_dir / entity
    staging_entity_dir.mkdir(parents=True, exist_ok=True)
    (staging_entity_dir / "attributes.md").write_text(generate_attributes_page(data, entity, entity_manifest), encoding="utf-8")
    (staging_entity_dir / "relationships.md").write_text(generate_relationships_page(data, entity), encoding="utf-8")
    (staging_entity_dir / "forms.md").write_text(generate_forms_page(data, entity), encoding="utf-8")
    (staging_entity_dir / "views.md").write_text(generate_views_page(data, entity), encoding="utf-8")

    # --- Mechanical: always overwrite; these are never hand-edited ---
    entity_subdir = entities_dir / entity
    entity_subdir.mkdir(parents=True, exist_ok=True)
    (entity_subdir / ".order").write_text("attributes\nrelationships\nforms\nviews\n", encoding="utf-8")
    update_order_file(entities_dir, entity)

    attr_count = len(data["attributes"])
    form_count = len(data["forms"])
    view_count = len(data["views"])
    existing_index = entities_dir / f"{entity}.md"
    status = "update" if existing_index.exists() else "new"
    print(f"    Staged [{status}]: {attr_count} attrs, {form_count} forms, {view_count} views -> {staging_dir.name}/{entity}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def build_client(args, config: Dict) -> DataverseClient:
    client = DataverseClient(config["environment_url"])
    client.connect(
        app_id=args.app_id or config.get("app_id"),
        client_secret=args.client_secret,
        tenant_id=config["tenant_id"],
    )
    return client


def resolve_output_dir(args, repo_root: Path) -> Path:
    if args.output_dir:
        return Path(args.output_dir)
    return repo_root / "wiki" / "Technical-Reference" / "entities"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch Dataverse entity/solution metadata and generate ADO wiki documentation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python fetch_entity_metadata.py --solution IncomeAssistanceCore
    python fetch_entity_metadata.py --entity mnp_application
    python fetch_entity_metadata.py --entity account --environment dev
    python fetch_entity_metadata.py --solution IncomeAssistance --app-id <id> --client-secret <secret>
        """,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--solution", help="Solution unique name — fetch all entities in this solution")
    group.add_argument("--entity", help="Entity logical name — fetch a single entity")

    parser.add_argument("--environment", default="dev", help="Accepted for backward compatibility; configuration is loaded from .env")
    parser.add_argument("--app-id", help="App ID for service principal auth")
    parser.add_argument("--client-secret", help="Client secret for service principal auth")
    parser.add_argument("--output-dir", help="Override output directory (default: wiki/Technical-Reference/entities)")

    args = parser.parse_args()

    print("Dataverse Entity Documentation Generator")
    print(f"  Mode:        {'Solution: ' + args.solution if args.solution else 'Entity: ' + args.entity}")
    print(f"  Environment: {args.environment}")

    try:
        config = load_dataverse_config(args.environment)
    except ConfigurationError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)

    print(f"  Connecting to {config['environment_url']}...")
    client = build_client(args, config)

    # Script lives at: .github/skills/dv-doc-entity/scripts/
    repo_root = Path(__file__).parent.parent.parent.parent.parent
    entities_dir = resolve_output_dir(args, repo_root)
    entities_dir.mkdir(parents=True, exist_ok=True)

    # Global staging area at repo root — shared across all skills, never committed
    staging_dir = repo_root / ".staging" / "entities"
    staging_dir.mkdir(parents=True, exist_ok=True)

    manifest = load_manifest(entities_dir)

    if args.solution:
        entity_names = fetch_entity_logical_names_for_solution(client, args.solution)
        print(f"\nDocumenting {len(entity_names)} entities...")
        success, errors = 0, []
        for i, entity in enumerate(entity_names, 1):
            print(f"\n  [{i}/{len(entity_names)}] {entity}")
            try:
                data = fetch_entity_data(client, entity)
                write_entity_docs(data, entity, entities_dir, manifest, staging_dir)
                success += 1
            except Exception as exc:
                errors.append((entity, str(exc)))
                print(f"    ERROR: {exc}")

        print(f"\nSummary: {success}/{len(entity_names)} entities documented successfully.")
        if errors:
            print("Errors:")
            for name, msg in errors:
                print(f"  {name}: {msg}")
    else:
        print(f"\nDocumenting entity '{args.entity}'...")
        data = fetch_entity_data(client, args.entity)
        write_entity_docs(data, args.entity, entities_dir, manifest, staging_dir)

    save_manifest(entities_dir, manifest)
    print(f"\nStaging complete: {staging_dir}")
    print("Next step: run the AI merge (see SKILL.md Step 3) to apply staged changes to wiki pages.")


if __name__ == "__main__":
    main()

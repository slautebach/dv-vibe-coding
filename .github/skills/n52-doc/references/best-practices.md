# North52 Best Practices

## 1. Governance, Naming, and Metadata

Consistent naming and metadata are the foundation of a maintainable North52 codebase. Without them, formulas become impossible to map to business domains or search effectively.

**Categorization:** Always populate the Category and Sub Category fields on every Formula definition. Unclassified formulas break architectural mapping and make cross-domain audits impossible.

**Formula Naming:** Name formulas to communicate their purpose, source entity, and execution event without needing to open them. Follow the pattern: `<Process> - <Event> - <Action>` (e.g., `Phone to Case Process - Save - Create Checklist Items`).

**Calculation Identifiers:** Rename all Inline and Global Calculations away from default placeholders (e.g., `Calc1`). Use identifiers that describe the business value being computed (e.g., `Age - Gender Risk`).

**Contextual Comments:** Add a Comment column to any complex logical branch in a Decision Table. Comments should reference the user story, requirement doc, or algorithm being implemented — not restate the logic.

---

## 2. Trigger Architecture and Execution Pipeline

Trigger configuration is one of the highest-impact performance decisions in North52. An over-broad trigger runs your formula on every save, regardless of relevance.

**Trigger Specificity:** On Update formulas, always specify only the fields that should trigger execution in the Source Property. **Never use "All Properties"** — this fires the formula on every field change and is a severe performance anti-pattern that can degrade the entire org.

**Infinite Loop Prevention:** Never configure a Post-Operation formula to write to a field that is also listed in its own Source Property trigger. This creates a recursive execution loop that will continuously re-trigger the formula.

**Execution Mode:** Default to Asynchronous Post-Operation unless there is a specific requirement for real-time UI feedback. Synchronous stages (Pre-Validation, Pre-Operation, Post-Operation Sync) block the user interface for the duration of execution and count against the 120-second plugin timeout.

---

## 3. Decision Table Design

Decision tables evaluate conditions top-to-bottom, left-to-right. Structure them deliberately — the order of rows and columns directly affects both performance and correctness.

**Hit Policy:** Enable "Exit this Decision Table on First Match" whenever the table returns a single discrete outcome. Disable it only when the table aggregates across all rows (e.g., accumulating a risk score). Leaving it enabled on an accumulating table silently truncates results.

**Multi-Sheet Architecture:** Split any sheet that becomes cognitively overloaded into a Multi-Sheet design (e.g., Eligibility Sheet → Calculation Sheet → Output Sheet). As a guide, sheets with more than 100 rows or 15 columns are candidates for decomposition.

**Logical OR Optimization:** Avoid duplicate rows that resolve to the same action. Instead:
- Use inline OptionSet ORs natively in a single cell where possible.
- Use the `Condition-Or` column header syntax for multi-column OR conditions.
- Index distinct OR groups numerically (`Condition-Or-1`, `Condition-Or-2`) to prevent logic cross-contamination.

**Exclusion Flags:** Remove all row, column, and sheet exclusion flags before deploying to production. These are development/testing tools only and must not be present in a live environment.

---

## 4. Data Types and Null Safety

Most runtime faults in North52 formulas trace back to two root causes: comparing values by display name instead of underlying value, and performing operations on fields that are null.

**OptionSet Fields:** Always evaluate OptionSets in Condition columns using the Integer value `{Value}`, never the string name `{Name}`. String-based comparisons break silently when labels change and fail completely in multi-language environments.

**Lookup Fields:** Always evaluate Lookups in Condition columns using the unique identifier (Value), not the display name (Name). Exception: use (Name) when the formula must work consistently across environments where GUIDs differ between dev, test, and prod.

**Action Assignments:** Always use the Value field when writing to a field in an Action column. Never assign by Name — this causes failures when record names change or differ between environments.

**Null Guards:** For every non-mandatory field involved in a mathematical operation or string concatenation, define a default fallback value in Row 3 (Advanced Mode). For example, apply `.0` to a nullable currency field before arithmetic to prevent execution faults.

---

## 5. Modularity, Caching, and Stateless Design

Structure formulas to minimise database calls and keep environment-specific values out of formula logic.

**Global vs. Inline Calculations:**
- **Inline Calculations:** Use for intermediate values scoped to the current sheet only.
- **Global Calculations:** Keep lightweight. Global Calculations run unconditionally at formula startup — every time, on every execution — regardless of whether any branch references them. Never put expensive queries here.
- **Global Actions:** Place heavy or conditionally-needed logic in Global Actions. They execute lazily — only when explicitly called — making them the right home for operations that don't always need to run.

**Power App Integration:** For synchronous Power App integrations, use an unbound Dataverse Custom Action that accepts a serialized JSON payload and passes it directly to the Formula. This eliminates the latency overhead of an intermediary Power Automate flow.

**xCache for Configuration:** Never hardcode environment-specific values (API endpoints, credentials, admin email addresses, configuration constants) directly in a formula. Store them in xCache and retrieve with `xCacheGetGlobal()`. This makes formulas portable across dev, test, and production without modification.

**FindValue Efficiency:**
- Set `NoLock = true` on all `FindValue()` calls that read reference data. This prevents unnecessary read locks and avoids SQL deadlocks under concurrent load.
- Avoid calling `FindValue()` multiple times for the same record within one formula execution. Either consolidate the calls or rely on North52's built-in caching to ensure the database is queried only once.

---

## 6. Scheduled Jobs and Bulk Processing

Scheduled formulas operate outside the normal per-record execution model and require explicit configuration to handle large datasets safely.

**Paging:** Always set the Query Record Limit on Schedules to a value that chunks the dataset into manageable pages (typically 250). Processing all records in a single execution risks hitting the 2-minute Dataverse timeout. Let the scheduler page through records iteratively.

**Targeted FetchXML:** Write FetchXML queries that filter server-side to only the records that need processing. Never retrieve all records and filter in formula logic — push filtering into the query.

**Load Throttling:** For high-volume updates, configure a Query Delay Interval (in milliseconds) between pages. This gives the database transaction log time to flush commits and prevents locking out active users during bulk operations.

---

## 7. Error Handling and Diagnostic Tracing

**Explicit Errors:** Use `ThrowError()` to halt execution for any business rule violation. Provide a message that is specific, user-actionable, and contextual — not a generic system fault. Never rely on an unhandled exception to surface a business logic failure.

**Production Tracing:** Set the Global Tracing Level to errors/exceptions only in production. `Information`-level tracing writes a trace record on every formula execution. Under load, this fills the trace table rapidly, triggers cascading deletion jobs, and can cause database timeouts that affect all users.

---

## 8. Metrics, Thresholds, and Scoring Rubrics

> The numeric thresholds in this section are general engineering heuristics and project guidelines — not documented North52 or Dataverse platform limits. Apply them with judgment based on the specific formula's context and business purpose.

### Complexity Indicators

These are directional signals, not hard pass/fail rules:

| Indicator              | Low Concern        | Worth Monitoring | Consider Refactoring      |
| ---------------------- | ------------------ | ---------------- | ------------------------- |
| **Nesting Depth**      | ≤2 levels          | 3-4 levels       | ≥5 levels                 |
| **Variables Declared** | Few, clearly named | Moderate         | Many with unclear purpose |

### Performance Guidelines

#### Query Performance

> The Dataverse FetchXML hard limit is **5,000 records per page**. The project guidelines below are conservative targets based on engineering best practices (the 1,000 record threshold aligns with the `ExecuteMultiple` batch limit and helps avoid synchronous plugin timeouts).

| Concern                           | Project Guideline                                                            |
| --------------------------------- | ---------------------------------------------------------------------------- |
| **Large Result Sets**             | Flag queries likely to return >1,000 records for pagination review           |
| **Exceed Platform Limit**         | Any unpaginated query that may return >5,000 records must use paging cookies |
| **`FindValue` in loop (dynamic)** | Critical — use FetchXML `link-entity` join before the loop                   |
| **`FindValue` in loop (static)**  | Hoist above loop and cache with `SetVar()`                                   |
| **Repeated identical queries**    | Cache result in `SetVar()`                                                   |

#### Execution Time Guidelines (Server-Side)

> These are rough project guidelines based on engineering judgment, not documented North52 or Dataverse platform limits.

| Formula Type              | Project Target | Review If Slower |
| ------------------------- | -------------- | ---------------- |
| **Validation**            | <100ms         | >200ms           |
| **Calculation**           | <500ms         | >1s              |
| **Perform Action**        | <2s            | >5s              |
| **Schedule (per record)** | <30s           | >60s             |

#### ⚠️ Hard Platform Limit: 2-Minute Plugin Timeout

| Constraint                       | Value                                                                                         | Notes                                                                                        |
| -------------------------------- | --------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| **Synchronous execution window** | **120 seconds (hard limit)**                                                                  | Applies to Validation, Calculate, Save - To Current Record, synchronous Actions              |
| **On breach**                    | Transaction terminated, changes rolled back, user sees `Generic SQL Error` / `Plugin Timeout` | No grace period — Dataverse is unaware of North52                                            |
| **Async operations**             | Not subject to this limit                                                                     | Shift to async formula type, Power Automate, or Background Workflow when processing is heavy |

**Top timeout risks (flag these patterns in synchronous formulas):**

- `FindValue()` / `FindRecordsFD` called inside `ForEachRecord` with a changing key per iteration
- `CallRestAPI()` executed synchronously
- Large `FindRecordsFD` result sets processed record-by-record in a loop

### Decision Table Guidelines

> These thresholds are project guidelines only — larger tables may be perfectly valid depending on business requirements.

| Metric           | Generally Manageable | Worth Reviewing |
| ---------------- | -------------------- | --------------- |
| **Row Count**    | <50                  | >100            |
| **Column Count** | <10                  | >15             |

### Maintainability Scoring

See `prompts/codereview.md` for the full scoring rubrics (Code Readability, Variable Naming, and Overall Formula Rating) used when generating a code review.

### Optimization Patterns

#### Efficient Patterns to Recognize

✅ **Batch Queries**: Using `FindRecordsFD` or `link-entity` FetchXML joins instead of `FindValue` inside loops  
✅ **Variable Caching**: Storing repeated lookup results (`WhoAmI`, repeated `FindValue` calls) in `SetVar()` variables  
✅ **Guard Clauses**: `ContainsData()` checks before dereferencing lookups  
✅ **Early Exit**: Returning immediately when a condition is met, avoiding unnecessary evaluation  
✅ **Decision Tables**: Using tables for complex multi-condition logic instead of nested if-else  
✅ **Inline Default Values**: Using `[entity.fieldname.defaultvalue]` to safely handle null field references  
✅ **SmartFlow**: Grouping related operations for transactional execution  
✅ **Short-Circuit**: Checking if formula should run using `HaveFieldsChanged()` before performing work

### Formula Type-Specific Standards

#### Calculate Formulas

- Must be deterministic (same inputs = same outputs)
- No side effects (`CreateRecord`, `UpdateRecord`)
- Return single calculated value
- Cache intermediate results in variables

#### Validation Formulas

- Return `NoOp` for success (not empty string)
- User-friendly, actionable error messages
- Server-side only (security-critical)
- Early exit on first validation failure

#### Perform Action Formulas

- Use SmartFlow for grouped operations
- Post-operation stage for creating related records
- Consider error handling for external calls
- Idempotent when possible (safe to run multiple times)

#### Schedule Formulas

- Efficient batch processing with `ForEachRecord`
- Paginate large datasets (process in chunks)
- Continue on individual record failures
- Log progress and errors for monitoring

### Client-Side vs Server-Side Decision Matrix

**Use Client-Side when:**

- UI updates needed (hide/show fields, disable controls)
- Form validation with immediate user feedback
- Navigation, alerts, or user interactions
- Calculations not requiring database save
- Performance-critical user experience

**Use Server-Side when:**

- Data validation (security-critical, cannot be bypassed)
- Record creation or updates
- Complex calculations requiring saved data
- Integration with workflows or plugins
- Must work via API calls (not just UI)

**Execution Stage:**

- **Pre-Operation**: Validation (block save), field modifications, access to old+new values
- **Post-Operation**: Create related records, trigger workflows, send notifications (original record saved)

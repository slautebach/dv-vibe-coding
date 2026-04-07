# CodeReview.md Prompt Template

When generating a CodeReview.md for a classic XAML workflow, perform a technical analysis of the workflow design, logic quality, and adherence to best practices.

**Load before reviewing:** `.github/skills/dataverse-solution-parser/references/workflow-schema.md` — reference for all activity types, limitations (2-minute sync timeout, no direct FetchXML, etc.), and performance guidance.

**Load for project context:** `.github/skills/dv-doc-xaml-workflows/references/xaml-project-patterns.md` — MNP plugin names, program prefixes, option set values, and common patterns in this codebase.

## Document Structure

### 1. Executive Summary

**Include:**
- **Overall Assessment:** Excellent / Good / Needs Improvement / Poor
- **Key Findings:** 3-5 bullet points with icons (checkmark = good, warning = concern, X = issue)
- **Issue Count:** Critical / High / Medium / Low
- **Strengths:** What the workflow does well

**Example:**
```markdown
# CodeReview: SIS - Close Case

## Executive Summary

**Overall Assessment:** Good

**Key Findings:**
- Correct use of condition checks before executing closure logic
- Program-specific branching is clear and well-named
- OnDemand trigger appropriate for user-initiated closure
- Missing explicit error handling for plugin failures
- Step naming is descriptive and follows conventions

**Issue Count:**
- Critical: 0
- High: 0
- Medium: 1 (no error handling on custom activities)
- Low: 1 (some conditions could be combined)
```

### 2. Design & Architecture

**Analyze:**
- **Flow Structure:** Is the workflow well-organized?
- **Trigger Appropriateness:** Is the trigger type correct for the use case?
- **Mode:** Is Background vs Real-time the right choice?
- **Scope:** Is Organization scope appropriate?
- **Modularity:** Should any logic be split into child workflows?

**Rating:** Excellent | Good | Fair | Poor

**XAML-Specific Concerns:**
- Very deep nesting (>5 levels) indicates complex branching that may be hard to maintain
- Multiple ConditionSequences at the same level may indicate missing else branches
- Large files (>100KB) suggest the workflow may be doing too much

### 3. Condition Logic Review

**Analyze:**
- Are conditions checking the right fields?
- Are condition branches complete (is there always an else/default)?
- Are option set values correct? (Reference `.data.xml` PrimaryEntity to validate)
- Could any conditions be simplified or combined?
- Are wait conditions used appropriately?

**Example:**
```markdown
## Condition Logic

**Findings:**
- ConditionStep1 correctly gates on status reason before proceeding - Good
- ConditionStep6 uses DisplayName that clearly describes intent - Good  
- No else branch on ConditionStep6 means silent no-op if condition fails - consider logging
```

### 4. Step Quality

**Analyze:**
- Are workflow steps named with descriptive `DisplayName` values?
- Do custom plugin activities handle errors gracefully?
- Are `GetEntityProperty` / `SetEntityProperty` steps minimized (avoid redundant reads)?
- Are `StopWorkflow` steps used correctly?

**Naming Quality Check:**
- Good: `"ConditionStep1: Process only on case records that are scheduled for closure"`
- Poor: `"ConditionStep1"` (no description)
- Poor: `"Step 1"` (generic names)

### 5. Performance Considerations

**Analyze:**
- **Mode Impact:** Real-time workflows block the user transaction — are they justified?
- **Scope:** Organization scope triggers on all records — is filtering in place?
- **Trigger Fields:** Are `TriggerOnUpdateAttributeList` fields minimal and specific?
- **Size:** Large XAML files may cause slow deployment and execution
- **Custom Activities:** Plugin calls add latency — are they necessary?

**Example:**
```markdown
## Performance

**Mode:** Background (Asynchronous) - Appropriate, does not block user
**Trigger Fields:** statuscode, statecode - Minimal and appropriate
**Custom Activities:** 2 plugin calls - Acceptable for this complexity

**Concern:** Workflow fires on all Invoice records in the org. Confirm condition 
check at start is efficient (checks status code, not a Dataverse query).
```

### 6. Error Handling

**Analyze:**
- Does the workflow have explicit error handling?
- Are custom plugin activities wrapped in try/catch logic?
- What happens if a GetEntityProperty returns null?
- Is `SyncWorkflowLogOnFailure` appropriate for the mode?
- Are `StopWorkflow` steps used to handle failure paths?

**Best Practices:**
- Workflows should log failures when `SyncWorkflowLogOnFailure` is enabled
- Custom activity failures propagate as exceptions unless handled
- Background workflows do not surface errors to users — monitoring is critical

### 7. Maintenance & Supportability

**Analyze:**
- Are step `DisplayName` values descriptive enough for future developers?
- Is the workflow `IsCustomizable` correctly set?
- Is the `IntroducedVersion` tracked?
- Would a new developer understand this workflow without documentation?
- Are deprecated patterns used? (Wait conditions in background workflows, etc.)

### 8. Recommendations

List actionable improvements, prioritized:

**Format:**
```markdown
## Recommendations

### High Priority
1. **Add error handling on custom activities** - Wrap plugin calls to handle failures gracefully

### Medium Priority  
2. **Improve step naming** - Steps like "ConditionStep6" should have descriptive DisplayNames
3. **Add logging step** - Include a step to log when workflow exits without action

### Low Priority
4. **Combine similar conditions** - ConditionStep1 and ConditionStep3 check related fields and could be merged
```

## XAML-Specific Review Checklist

When reviewing classic XAML workflows, also check:

- [ ] `OnDemand=1` with no other triggers = manual only (is this intended?)
- [ ] `TriggerOnCreate=1` without conditions = fires on EVERY create (performance risk)
- [ ] `Mode=1` (Real-time) = blocking; justify this choice
- [ ] `RunAs=0` (Calling User) vs `RunAs=1` (Owner) — security implications
- [ ] `IsTransacted=1` on Real-time workflows = rollback on failure (desired?)
- [ ] Custom `AssemblyQualifiedName` activities = verify assembly is deployed
- [ ] `StateCode=0` = Draft (workflow is inactive — intentional?)
- [ ] Steps with no `DisplayName` = hard to maintain

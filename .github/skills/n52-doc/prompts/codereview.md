# CodeReview.md — AI Generation Prompt & Rules

**Purpose**: Generate `CodeReview.md` for a North52 formula — a technical analysis for developers and maintainers.

**Audience**: Developers, technical leads, and system architects.

## AI Review Context

> This prompt references `references/best-practices.md` for evaluation standards, quantitative thresholds, anti-pattern definitions, and formula type guidelines.

**AI Persona**: You are an expert-level enterprise architect and code reviewer evaluating North52 Business Process Activities (Formulas, Decision Tables, and Schedules) deployed in Microsoft Dynamics 365 / Dataverse.

**Review Methodology**: Systematically evaluate configuration metadata against strict performance, stability, and maintainability standards. Detect inefficient data access patterns, redundant logical branching, missing defensive programming (null handling), and risks of pipeline transaction faults (e.g., infinite loops). Apply the evaluation criteria and thresholds defined in `references/best-practices.md`.

---

**Input files to read before generating** (from `.staging/north52/<entity>/<shortcode>/` after fetch, or `wiki/Technical-Reference/North52/<entity>/<shortcode>/` if already merged):

- `*.n52` — the raw formula code
- `*.fetch.xml` — FetchXML queries used in the formula (if present)
- `analysis_metadata.json` — structured metadata (entity, type, event, variables, functions, decision tables, complexity indicators)

---

## Required Sections

### 1. Formula Metadata

- Name, shortcode, entity, and formula type
- Execution order, stage, and mode
- Category and trigger event

### 2. Code Structure

#### Decision Tables
- **Count and purpose**: List all decision tables referenced
- **Optimization assessment**:
  - **Row count**: <50 good, 50-100 acceptable, >100 consider splitting
  - **Column count**: <10 manageable, >10 may be too complex
  - **Column ordering**: Most selective conditions first (left to right)
  - **Default row present**: Always include catch-all row
- Anti-patterns: Too many columns, overlapping rules, no default row

#### Variables Declared
- **Count**: Total variables declared
- Table format showing: Variable name, purpose, data type, scope/usage
- Variables used for caching repeated lookups or expensive operations?
- Naming convention assessment (are names descriptive and consistent?)

#### Functions Called
- Table showing: Function name, call count, purpose
- Flag duplicate calls that could be cached in a `SetVar()` variable

#### FetchXML Queries
- Query name and purpose
- Parameters and filters used
- Result set size estimate (note: Dataverse FetchXML hard limit is 5,000 records per page; flag queries likely to return large result sets)
- Efficiency assessment (indexed fields, necessary columns only?)

### 3. Complexity Analysis

> **Note**: The thresholds below are general software engineering heuristics applied as a guide — they are not documented North52 standards. Use judgment when applying them to North52 formulas, which can legitimately be more complex than typical code.

- **Cyclomatic complexity** (estimated — count distinct decision paths/branches):
  - **Low**: Few branches, straightforward logic
  - **Moderate**: Multiple branches, still manageable
  - **High**: Many branches — consider splitting into sub-formulas or decision tables
- **Nesting depth**:
  - **≤2 levels**: Good readability
  - **3-4 levels**: Acceptable but monitor
  - **≥5 levels**: Consider refactoring to guard clauses or decision tables
- **Conditional branches count** — note overall count and flag if deeply interleaved
- Loop usage and iteration patterns (`ForEachRecord`, `ForEachRecordNested`)
- **Overall complexity rating** (Low / Medium / High) with qualitative justification

### 4. Function Usage

- Complete list of North52 functions used (with call counts)
- Purpose of each function in context
- Parameter patterns and any non-standard usage
- **Optimization patterns**:
  - Check for repeated calls to the same function with the same parameters — cache result in `SetVar()` to avoid redundant evaluation
  - `WhoAmI()` is a Dataverse API call; cache it in a variable if called more than once
  - `FindValue()` is optimized for simple single-attribute lookups and has a built-in caching parameter — use it appropriately (see Section 5)
  - Flag `FindValue()` called inside `ForEachRecord` loops where the lookup value changes per record (genuine N+1 anti-pattern)
  - Flag inefficient function combinations
- Potential alternative functions worth considering (cite North52 documentation)

### 5. Performance Considerations

#### Query Efficiency
- **FetchXML result set size**:
  - The Dataverse FetchXML hard limit is **5,000 records per page**; queries exceeding this must use paging cookies
  - As a project guideline, flag queries likely to return >1,000 records for review — this aligns with the `ExecuteMultiple` batch limit and helps avoid synchronous plugin timeouts
  - Queries on large datasets should use pagination (paging cookies via FetchXML or `FindRecordsFD` with appropriate filters)
- Filter coverage analysis (indexed fields used?)
- **N+1 query detection**: Flag `FindValue()` called inside a `ForEachRecord` loop where the lookup value changes per record
  - **Fix (dynamic lookups)**: Use a FetchXML `link-entity` join in `FindRecordsFD` *before* the loop to pre-fetch related data in a single query
  - **Fix (static lookups)**: Hoist the `FindValue()` call *above* the loop and cache the result in `SetVar()`

#### Execution Performance (Server-Side)

> **Note**: The thresholds below are rough project guidelines based on engineering judgment — they are not documented North52 or Dataverse platform limits. Use them as a directional guide, not hard pass/fail criteria.

- **Validation formulas**: Target <100ms
- **Calculation formulas**: Target <500ms
- **Perform Action formulas**: Target <2s (post-operation)
- **Schedule formulas**: Target <30s per record

#### ⚠️ Hard Platform Constraint: The 2-Minute Dataverse Plugin Timeout

This is the most inflexible and critical execution constraint in the Microsoft ecosystem. Dataverse does not care that you are using North52. Synchronous North52 formulas (Validation, Save - To Current Record, synchronous Actions) are compiled and registered as standard Dataverse C# plugins under the hood — and are subject to the exact same **120-second hard limit**.

If a synchronous formula reaches 120,000ms, Dataverse:
1. Terminates the transaction
2. Rolls back all database changes
3. Returns a `Generic SQL Error` or `Plugin Timeout` exception to the user

**Review these synchronous formula types for timeout risk:**
- Validation formulas
- Calculate formulas
- Save - To Current Record formulas
- Synchronous Action/Process formulas

**Common North52 timeout traps to flag:**

- **N+1 query loops**: `FindValue()` or `FindRecordsFD` inside `ForEachRecord` with a changing key per record — 500 iterations = 500 individual API calls. Almost certain timeout.
- **Synchronous external API calls**: `CallRestAPI()` run synchronously holds the Dataverse transaction open waiting for the external system. If the external API is slow or throttled, the transaction fails.
- **Massive entity collections**: Using `FindRecordsFD` to pull thousands of records and looping through them synchronously for updates or calculations.

**Architectural remedies (flag if applicable):**

- **Shift to async**: If the user doesn't need immediate feedback, change the formula type to **Process - Action** or trigger via an asynchronous Power Automate flow / Background Workflow. Async operations have vastly more generous execution limits.
- **Pre-join data**: Use FetchXML `<link-entity>` tags inside `FindRecordsFD` to fetch related data in a single query rather than per-record.
- **xCache for reference data**: Use `xCacheGetGlobal()` for static configuration values to eliminate repeated database calls during execution.

#### Client-Side vs Server-Side Decision Matrix
- **Use Client-Side for**: UI updates, form validation, immediate feedback, calculations not requiring save
- **Use Server-Side for**: Data validation (security-critical), record creation/updates, cannot be bypassed by API

#### D365 Integration Patterns
- **Execution stage appropriateness** (Pre-operation vs Post-operation)
- **Query patterns**:
  - Use `FindValue()` for simple single-attribute lookups (optimized, with built-in caching parameter for repeated calls within the same formula)
  - Use `FindRecordsFD` for complex multi-record queries requiring FetchXML joins, aggregations, or filtering across related entities
  - Use `FindCountFD` when only a record count is needed
- **Caching strategies**:
  - **Within-formula**: `SetVar()` / `GetVar()` for local variables scoped to the current formula execution
  - **Cross-formula / global**: `xCacheGetGlobal()` / xCache for values shared across formulas or environment-specific configuration (e.g., API endpoints, admin email addresses)
- **Short-circuit optimization**: Check if formula should run before doing work (e.g., use `HaveFieldsChanged()` to skip execution when relevant fields haven't changed)

#### Specific Optimization Suggestions
- Prioritized recommendations (Critical / High / Medium / Low)
- Quantify expected performance improvement where possible
- Provide code examples for suggested optimizations

### 6. Maintainability

#### Code Readability Score: X/10
- **8-10**: Excellent - clear, well-documented, easy to understand
- **5-7**: Good - readable with minor improvements needed
- **3-4**: Fair - requires documentation or refactoring
- **1-2**: Poor - difficult to understand, needs significant refactoring

#### Variable Naming Score: X/10
- **8-10**: Excellent - descriptive, consistent, follows conventions
- **5-7**: Good - mostly clear, minor inconsistencies
- **3-4**: Fair - some unclear names, needs improvement
- **1-2**: Poor - generic names (`temp`, `x`, `data`, `val`), hard to understand

#### Overall Formula Rating
- **⭐⭐⭐⭐⭐** (5/5): Production-ready, excellent quality
- **⭐⭐⭐⭐** (4/5): Good quality, minor improvements recommended
- **⭐⭐⭐** (3/5): Acceptable, needs moderate improvements
- **⭐⭐** (2/5): Needs significant refactoring
- **⭐** (1/5): Critical issues, major rework required

#### Variable Management
- **Variable count**: Note total count; flag if unusually high as a signal to simplify
- **Variable naming**: Are names descriptive and consistent? Avoid generic names like `temp`, `x`, `data`, `val`
- Naming conventions followed consistently within the formula?

#### Documentation Quality
- Header comments present? (purpose, business rules, option set mappings)
- Inline comments for complex logic?
- Magic numbers explained? (hard-coded status codes, option sets)

#### Refactoring Opportunities
- **Priority 1 (High Value)**: Simplify nested conditionals, reduce complexity
- **Priority 2 (Medium Value)**: Extract duplicated code, consolidate queries
- **Priority 3 (Low Value)**: Minor optimizations, style improvements
- Decision table candidates (>3 nested if-else checking same variables)

### 7. Best Practices & Recommendations

#### North52 Best Practices Alignment
✅ Strengths (what the formula does well):
- Examples: Uses SmartFlow, efficient batch queries, appropriate execution stage, good variable usage

⚠️ Gaps (areas for improvement):
- Examples: Missing null checks, deep nesting, magic numbers, no error handling

#### Pattern Analysis
- **Efficient Patterns Found**: Batch queries, variable caching, guard clauses, early exit
- **Anti-Patterns Detected**: 
  - **Critical**: N+1 queries, missing null checks, security bypass
  - **High**: Deep nesting (>5 levels), excessive complexity (>20), large result sets (>1000)
  - **Medium**: Magic numbers, code duplication, poor naming
  - **Low**: Minor optimizations, style inconsistencies

#### Error Handling
- Current approach assessment
- Gaps or improvements needed
- Error message quality (user-friendly, actionable?)

#### Security Considerations
- Server-side vs client-side appropriateness
- Privilege escalation risks (system context execution)
- Data access validation
- Self-approval prevention (segregation of duties)
- Configuration tampering risks (field-level security needed?)

#### Testing Strategies
- **Unit Test Scenarios**: Happy path, null/empty values, boundary conditions, edge cases
- **Integration Test Scenarios**: Configuration errors, concurrent updates, permission variations
- **Performance Test Scenarios**: Individual record, bulk operations (100+ records), large result sets
- Expected test coverage areas

#### Technical Debt & Maintenance Notes
- **Change Impact Areas**: What happens when rules/statuses/config changes?
- **Dependencies**: Entities, FetchXML queries, decision tables, option sets
- **Monitoring Recommendations**: Execution time tracking, error rates, trace logging

### 8. Anti-Patterns Checklist

Flag any of these common North52 anti-patterns found in the formula:

#### 🔴 Critical (Must Fix)
- [ ] **N+1 Queries (Dynamic)**: `FindValue()` called inside `ForEachRecord` loop where the lookup key changes per record — use a FetchXML `link-entity` join in `FindRecordsFD` *before* the loop
- [ ] **N+1 Queries (Static)**: Same `FindValue()` call repeated on every loop iteration — hoist above the loop and cache with `SetVar()`
- [ ] **Synchronous External API Call**: `CallRestAPI()` used synchronously in a formula — external latency or throttling will hold the Dataverse transaction open and risk a plugin timeout
- [ ] **Missing Null Checks**: Dereferencing lookup fields without `ContainsData()` — add guard clause
- [ ] **Infinite Loop Risk**: While loops without proper exit conditions
- [ ] **Client-Side Security**: Security-critical validation only on client-side (can be bypassed)

#### 🟠 High Priority
- [ ] **Deep Nesting**: >5 levels of nested conditionals (hard to read/maintain) — refactor to guard clauses or decision table
- [ ] **High Complexity**: Many branches with no clear decomposition — consider splitting into sub-formulas
- [ ] **Large Result Sets**: FetchXML queries likely to return >1,000 records without pagination (note: Dataverse hard limit is 5,000/page)
- [ ] **Repeated Identical Calls**: `WhoAmI()` or same `FindValue()` called 3+ times with identical parameters — cache in `SetVar()`

#### 🟡 Medium Priority
- [ ] **Magic Numbers**: Hard-coded option set values (e.g., `120310001`) without inline comments explaining their meaning
- [ ] **Code Duplication**: Repeated patterns (3+ occurrences) that could be refactored into a decision table or sub-formula
- [ ] **Poor Variable Naming**: Generic names (`temp`, `x`, `data`, `val`) instead of descriptive names
- [ ] **No Documentation**: Missing header comments explaining purpose and business rules

#### 🟢 Low Priority
- [ ] **Minor Optimizations**: `WhoAmI()` called 2-3 times — consider caching once with `SetVar()`
- [ ] **Readability Issues**: Overly compact code, long function chains
- [ ] **Inconsistent Style**: Mixed naming conventions within the formula

---

## Style Guidelines

- **Audience**: Write for developers and technical leads — assume familiarity with Dynamics 365 and North52
- **Evidence-based**: Support recommendations with specific code examples from the formula
- **Actionable**: Each recommendation should be concrete and implementable
- **References**: Cite North52 documentation or best practices where applicable
- **Prioritisation**: Distinguish between critical issues, improvements, and nice-to-haves
- **Format**: Use markdown headings, code blocks, bullet lists, and tables where appropriate

---

## North52 Reference Links

- Functions: https://support.north52.com/knowledgebase/functions/
- Advanced View: https://support.north52.com/knowledgebase/advanced-view/
- Business Process Activities: https://support.north52.com/knowledgebase/business-process-activities/

**Local references** (in `references/` folder):

- `references/north52-functions.md` — Complete function list
- `references/north52-functions-complete.md` — Detailed function info with parameters
- `references/north52-business-process-activities.md`

---

> **Metrics Reference**: See `references/best-practices.md` for complete quantitative thresholds, optimization patterns, formula type standards, and scoring rubrics.

---

## Output

Save the generated content to:

```
wiki/Technical-Reference/North52/<entity>/<shortcode>/code-review.md
```

After generating, update the metadata timestamp:

```bash
python update_ai_timestamps.py <entity> <shortcode>
```

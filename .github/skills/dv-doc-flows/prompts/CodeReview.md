# CodeReview.md Prompt Template

When generating a CodeReview.md file for a Power Automate cloud flow, perform a comprehensive technical analysis focusing on code quality, performance, security, and best practices. Follow this structure:

## Document Structure

### 1. Executive Summary

**Include:**
- **Overall Assessment:** High-level rating (Excellent, Good, Needs Improvement, Poor)
- **Key Findings:** 3-5 bullet points summarizing the most important observations
- **Critical Issues:** Number of critical, high, medium, and low priority issues
- **Strengths:** Notable positive aspects

**Example:**
```markdown
# CodeReview: AutomatedEmailAudit

## Executive Summary

**Overall Assessment:** Good - Flow is functional and follows most best practices, but has opportunities for performance optimization and error handling improvements.

**Key Findings:**
- ✅ Proper use of try-catch blocks for error handling
- ⚠️ Nested "Apply to each" loops may cause performance issues at scale
- ⚠️ Missing retry policies on Dataverse operations
- ✅ Clean naming conventions and logical flow structure
- ❌ No logging or telemetry for monitoring

**Issue Count:**
- Critical: 0
- High: 1 (Performance - nested loops)
- Medium: 2 (Error handling, logging)
- Low: 1 (Naming consistency)

**Strengths:**
- Good error handling structure
- Clear action naming
- Appropriate use of conditions
```

### 2. Architecture & Design

**Analyze:**
- **Flow Structure:** Is the flow well-organized and logical?
- **Modularity:** Could actions be broken into child flows or reusable components?
- **Complexity:** Is the flow overly complex or could it be simplified?
- **Scalability:** Will the flow handle growth in data volume?
- **Design Patterns:** Are appropriate patterns used (batch processing, pagination, etc.)?

**Rating Scale:** Excellent | Good | Fair | Poor

**Example:**
```markdown
## Architecture & Design

**Rating:** Good

### Structure
The flow follows a logical sequence: retrieve → process → update. The use of try-catch blocks provides good separation of normal flow from error handling.

### Modularity
**Assessment:** The flow would benefit from modularization.

**Recommendations:**
- Extract the email auditing logic into a child flow to enable reuse
- Create a separate flow for configuration loading to improve maintainability

### Complexity
**Assessment:** Moderate complexity. The nested loops add complexity but are necessary for the logic.

**Complexity Indicators:**
- 3 levels of nesting in some areas
- Multiple conditions within loops
- Could be simplified with better query filtering

### Scalability Concerns
**Issue:** The "Apply to each" loop processes emails sequentially, which may not scale well.

**Impact:** Processing 500+ emails could exceed flow timeout limits.

**Recommendation:** Implement batch processing or pagination with continuation tokens.
```

### 3. Performance Analysis

**Analyze:**
- **Loop Performance:** Are loops optimized? Do they process too many items?
- **API Calls:** Are API calls minimized? Is batching used?
- **Concurrency:** Could parallel processing improve performance?
- **Filtering:** Are queries filtered at the source or in the flow?
- **Data Transfer:** Is unnecessary data being retrieved?

**Rating Scale:** Excellent | Good | Fair | Poor

**Example:**
```markdown
## Performance Analysis

**Rating:** Fair - Significant optimization opportunities exist

### API Call Efficiency
**Current State:**
- ❌ API call inside "Apply to each" loop (N+1 problem)
- ⚠️ Configuration data loaded once per run (good)
- ❌ Individual updates instead of batch updates

**Issues Identified:**

#### Issue 1: N+1 Query Problem (HIGH)
**Location:** "Apply_to_each" → "Set_Email_Embedded_Link_to_Yes"

**Problem:** Each email record triggers a separate API call for update.

**Impact:** 
- Processing 100 emails = 100+ API calls
- High API throttling risk
- Slow execution time

**Recommendation:**
```json
// Current: Individual updates in loop
Apply to each: @outputs('Get_Emails')?['body/value']
  → Update Record (1 API call per email)

// Recommended: Batch update
Compose: Build array of updates
→ Batch Update Records (1 API call for multiple emails)
```

#### Issue 2: Nested Loops (HIGH)
**Location:** "Apply_to_each" → "Apply_to_each_2"

**Problem:** Inner loop checks every configured link for every email.

**Impact:**
- 100 emails × 10 links = 1,000 iterations
- Exponential growth with data volume

**Recommendation:**
- Use Dataverse query with filter on email description
- Use contains() check with OR conditions instead of nested loop

### Query Optimization
**Current Query:**
```javascript
// Gets all unaudited emails (no limit)
entityName: 'emails'
filter: 'mnp_automatedaudit eq null'
```

**Issues:**
- ❌ No $top or pagination
- ❌ No $select to limit fields
- ❌ Retrieves full email body unnecessarily

**Recommended Query:**
```javascript
// Optimized query
entityName: 'emails'
filter: 'mnp_automatedaudit eq null'
top: 100  // Limit per run
select: 'activityid,description,mnp_automatedaudit,mnp_embeddedlinksfound'
```

### Concurrency Settings
**Current:** Default concurrency (sequential)

**Recommendation:** Enable concurrency with degree of 10-20 for "Apply to each" loops to parallelize processing.

### Expected Performance
| Scenario | Current | Optimized |
|----------|---------|-----------|
| 10 emails | ~30 sec | ~5 sec |
| 100 emails | ~5 min | ~30 sec |
| 500 emails | Timeout risk | ~2 min |
```

### 4. Error Handling

**Analyze:**
- **Try-Catch Usage:** Are errors caught appropriately?
- **Error Logging:** Are errors logged with sufficient detail?
- **Retry Policies:** Are retry policies configured for transient failures?
- **Fallback Logic:** Is there graceful degradation or fallback behavior?
- **User Notification:** Are failures communicated to users/admins?

**Rating Scale:** Excellent | Good | Fair | Poor

**Example:**
```markdown
## Error Handling

**Rating:** Fair - Basic error handling present but incomplete

### Try-Catch Implementation
**Current State:**
- ✅ Outer try-catch block wraps main logic
- ✅ Inner try-catch for individual email processing
- ❌ No error details captured or logged

**Positive Aspects:**
```json
{
  "Try": {
    "actions": { /* main logic */ },
    "runAfter": {},
    "type": "Scope"
  },
  "Catch": {
    "actions": { /* error handling */ },
    "runAfter": { "Try": ["Failed", "Skipped", "TimedOut"] },
    "type": "Scope"
  }
}
```

**Issues:**

#### Issue 1: No Error Logging (MEDIUM)
**Problem:** Catch blocks exist but don't log error details.

**Impact:** 
- Difficult to troubleshoot failures
- No visibility into partial failures
- No audit trail

**Recommendation:**
```markdown
Add action in Catch scope:
- Compose error payload: @result('Try')
- Create record in error log table
- Send notification to admin team
```

#### Issue 2: Missing Retry Policies (MEDIUM)
**Problem:** No retry configuration on Dataverse operations.

**Impact:** Transient errors (network issues, throttling) cause immediate failure.

**Recommendation:**
```json
// Add to each Dataverse action
"retryPolicy": {
  "type": "exponential",
  "count": 3,
  "interval": "PT10S",
  "maximumInterval": "PT1M"
}
```

#### Issue 3: No Partial Success Handling (LOW)
**Problem:** If one email fails, entire batch processing stops.

**Impact:** All emails remain unaudited if any single email causes error.

**Recommendation:**
- Move try-catch inside "Apply to each" loop
- Continue processing remaining emails even if one fails
- Track failed emails for retry

### Error Scenarios Not Handled
| Scenario | Current Behavior | Recommended |
|----------|------------------|-------------|
| Dataverse throttling | Flow fails | Retry with exponential backoff |
| Invalid email format | Flow fails | Skip email, log warning |
| Configuration missing | Flow fails | Use default configuration or notify admin |
| Timeout | Partial processing | Save checkpoint, resume next run |
```

### 5. Security Review

**Analyze:**
- **Authentication:** Are connections properly secured?
- **Authorization:** Does flow have appropriate permissions?
- **Data Exposure:** Is sensitive data logged or exposed?
- **Input Validation:** Are inputs validated before use?
- **Secrets Management:** Are secrets/keys properly secured?

**Rating Scale:** Excellent | Good | Fair | Poor

**Example:**
```markdown
## Security Review

**Rating:** Good - No critical security issues, minor improvements needed

### Authentication & Authorization
**Current State:**
- ✅ Uses connection reference (not hardcoded credentials)
- ✅ Proper use of $authentication parameter
- ✅ Service account with least-privilege access (assumed)

**Recommendation:**
- Document the required security roles for the service account
- Implement periodic access review

### Data Handling
**Assessment:** Low risk - handles business email data, no PII.

**Observations:**
- ✅ No sensitive data written to flow run history
- ✅ No external data transmission
- ⚠️ Email body content checked but not logged

**Minor Concern:**
Email descriptions may contain sensitive information. Ensure flow run history is secured and retention policies are appropriate.

### Input Validation
**Issue:** No validation of configuration data (MEDIUM)

**Problem:** Flow assumes configuration records are well-formed.

**Risk:** Malformed links in configuration could cause unexpected behavior.

**Recommendation:**
```markdown
Before "Apply_to_each_2":
- Add condition to validate configuration link format
- Skip invalid entries
- Log validation warnings
```

### Secrets & Credentials
**Assessment:** Properly managed.

- ✅ Connection references used (not embedded credentials)
- ✅ Environment-specific configuration
- ✅ No hardcoded secrets in flow

### Security Best Practices Compliance
| Practice | Status | Notes |
|----------|--------|-------|
| Principle of least privilege | ✅ Pass | Connection has minimal required permissions |
| Secure credential storage | ✅ Pass | Uses connection references |
| Input validation | ⚠️ Partial | Configuration data not validated |
| Output sanitization | ✅ Pass | No dynamic output to external systems |
| Audit logging | ❌ Fail | No audit trail of flow actions |
```

### 6. Code Quality & Maintainability

**Analyze:**
- **Naming Conventions:** Are actions and variables well-named?
- **Code Readability:** Is the flow logic easy to understand?
- **Comments/Documentation:** Are complex sections documented?
- **Magic Numbers:** Are constants hardcoded or configurable?
- **Code Duplication:** Is logic repeated unnecessarily?

**Rating Scale:** Excellent | Good | Fair | Poor

**Example:**
```markdown
## Code Quality & Maintainability

**Rating:** Good - Generally well-structured with minor improvements needed

### Naming Conventions
**Assessment:** Mostly good, some inconsistencies.

**Well-Named Actions:**
- ✅ "Set_Email_Embedded_Link_to_Yes" - clear, descriptive
- ✅ "Get_Emails" - simple and clear
- ✅ "Parse_JSON_Embedded_Links_Config" - descriptive

**Needs Improvement:**
- ⚠️ "Try_2" - generic, should be "Try_Process_Individual_Email"
- ⚠️ "Apply_to_each_2" - default name, should be "Apply_to_each_ConfiguredLink"

**Recommendation:** Rename all default action names to describe their purpose.

### Code Readability
**Positive Aspects:**
- Logical flow sequence
- Proper use of scopes for organization
- Reasonable nesting levels (mostly)

**Areas for Improvement:**
- Some nested conditions are difficult to follow
- Complex expressions should be broken into Compose actions with descriptive names

**Example - Complex Expression:**
```javascript
// Current: Hard to read
"@contains(items('Apply_to_each')?['description'],items('Apply_to_each_2')['Link'])"

// Recommended: Break into steps
Compose: emailDescription = @items('Apply_to_each')?['description']
Compose: configuredLink = @items('Apply_to_each_2')['Link']
Condition: @contains(variables('emailDescription'), variables('configuredLink'))
```

### Configuration & Constants
**Issue:** Hardcoded option set values (LOW)

**Problem:**
```json
"item/mnp_automatedaudit": 120310002,  // What does this value mean?
"item/mnp_embeddedlinksfound": 120310001
```

**Impact:** Code is unclear; changes require finding magic numbers.

**Recommendation:**
- Use Compose actions at top of flow to define constants:
  ```javascript
  Compose: AUDIT_STATUS_COMPLETE = 120310002
  Compose: EMBEDDED_LINKS_YES = 120310001
  Compose: EMBEDDED_LINKS_NO = 120310000
  ```
- Reference variables instead of magic numbers

### Code Duplication
**Assessment:** Minimal duplication detected.

**One Instance Found:**
- Update email action appears twice (Yes path and No path)
- Consider consolidating with a Compose action to build update payload

### Comments & Documentation
**Current State:**
- ❌ No inline comments or descriptions on actions
- ❌ No flow description in properties

**Recommendation:**
- Add description to flow properties explaining purpose
- Add notes on complex actions (available in action settings)
- Consider adding Compose actions as "comment placeholders" for major sections
```

### 7. Best Practices Compliance

**Analyze against Power Automate best practices:**
- **Error Handling:** Try-catch, retry policies
- **Performance:** Pagination, batching, concurrency
- **Monitoring:** Logging, telemetry
- **Governance:** Naming, documentation
- **Security:** Authentication, authorization

**Example:**
```markdown
## Best Practices Compliance

### Power Automate Best Practices Checklist

| Practice | Status | Notes |
|----------|--------|-------|
| **Error Handling** |
| Use try-catch scopes | ✅ Pass | Implemented at multiple levels |
| Configure retry policies | ❌ Fail | No retry policies configured |
| Log errors appropriately | ⚠️ Partial | Catch blocks exist but don't log |
| Handle partial failures | ❌ Fail | Fails entire run on single error |
| **Performance** |
| Use pagination/limits | ❌ Fail | No $top limit on query |
| Batch API operations | ❌ Fail | Individual updates in loop |
| Enable concurrency | ❌ Fail | Sequential processing |
| Filter at source | ⚠️ Partial | Basic filter but no field selection |
| **Monitoring** |
| Implement logging | ❌ Fail | No logging actions |
| Track telemetry | ❌ Fail | No telemetry |
| Set appropriate run history | ⚠️ Unknown | Needs verification |
| **Governance** |
| Descriptive action names | ⚠️ Partial | Some defaults not renamed |
| Flow description | ❌ Fail | No description |
| Solution awareness | ✅ Pass | Deployed in solution |
| Connection references | ✅ Pass | Properly used |
| **Security** |
| Secure authentication | ✅ Pass | Connection references used |
| Validate inputs | ⚠️ Partial | No configuration validation |
| Principle of least privilege | ✅ Pass | Appropriate permissions |

**Overall Compliance:** 7/19 Pass, 6/19 Partial, 6/19 Fail

**Priority Improvements:**
1. Add retry policies (HIGH - prevents transient failures)
2. Implement pagination and batching (HIGH - prevents scale issues)
3. Add comprehensive logging (MEDIUM - enables troubleshooting)
```

### 8. Recommendations

**Provide prioritized, actionable recommendations:**

**Example:**
```markdown
## Recommendations

### Priority 1: Critical (Fix Immediately)
None identified.

### Priority 2: High (Address Soon)

#### 1. Implement Batch Updates
**Current Issue:** Individual API calls in loop create N+1 problem.

**Action Items:**
1. Replace "Update Record" actions with array composition
2. Use Dataverse batch update API (requires custom connector or HTTP action)
3. Test with 100+ emails to verify performance improvement

**Expected Impact:** 80% reduction in API calls, 60% faster execution

#### 2. Add Pagination
**Current Issue:** Query retrieves all unaudited emails (no limit).

**Action Items:**
1. Add `$top: 100` to initial query
2. Track processed record count
3. Consider implementing continuation token for large backlogs

**Expected Impact:** Prevents timeout, enables reliable processing

### Priority 3: Medium (Address When Possible)

#### 3. Enhance Error Logging
**Action Items:**
1. Add "Create record" action in Catch scope to write to error log table
2. Include: timestamp, flow run ID, error message, email ID
3. Set up email notification to admins for critical errors

**Expected Impact:** Faster troubleshooting, better visibility

#### 4. Configure Retry Policies
**Action Items:**
1. Add exponential retry policy to all Dataverse actions
2. Set retry count to 3, initial interval to 10 seconds
3. Test retry behavior with simulated throttling

**Expected Impact:** Improved resilience to transient failures

#### 5. Validate Configuration Data
**Action Items:**
1. Add Condition to check if configuration results are empty
2. Add Compose action to validate link format (URL pattern)
3. Skip invalid configuration entries, log warnings

**Expected Impact:** Prevents flow failure from bad configuration

### Priority 4: Low (Nice to Have)

#### 6. Improve Action Naming
**Action Items:**
- Rename "Try_2" → "Try_Process_Individual_Email"
- Rename "Apply_to_each_2" → "Apply_to_each_ConfiguredLink"
- Rename "Condition" → "Condition_Link_Found_In_Email"

**Expected Impact:** Improved code readability

#### 7. Extract Magic Numbers
**Action Items:**
1. Add Compose actions at flow start for option set values
2. Replace hardcoded integers with variable references

**Expected Impact:** Improved maintainability

### Implementation Roadmap

**Week 1:**
- Add pagination ($top: 100)
- Configure retry policies
- Add error logging

**Week 2:**
- Implement batch updates
- Validate configuration data
- Test performance improvements

**Week 3:**
- Improve naming conventions
- Add flow documentation
- Deploy to production
```

### 9. Technical Metrics

**Provide quantitative analysis:**

**Example:**
```markdown
## Technical Metrics

### Complexity Metrics
- **Total Actions:** 24
- **Conditions:** 5
- **Loops:** 2 (nested)
- **Try-Catch Blocks:** 3
- **API Calls per Run:** ~100+ (variable)
- **Maximum Nesting Depth:** 4 levels
- **Cyclomatic Complexity:** Moderate-High

### Performance Metrics (Estimated)
| Metric | Current | Target | Optimized |
|--------|---------|--------|-----------|
| Avg Runtime (100 emails) | 5 min | 2 min | 30 sec |
| API Calls (100 emails) | 150+ | 50 | 10 |
| Success Rate | 95% | 99% | 99.5% |
| Throttling Risk | High | Low | Very Low |

### Maintainability Score
**Rating:** 6.5/10

**Breakdown:**
- Code Readability: 7/10 (good structure, some complex expressions)
- Naming Conventions: 6/10 (mixed, some defaults)
- Documentation: 3/10 (minimal)
- Error Handling: 7/10 (present but incomplete)
- Reusability: 5/10 (monolithic, not modular)

### Code Coverage (Error Handling)
- Covered Scenarios: 3 (API failure, individual email failure, timeout)
- Uncovered Scenarios: 5 (configuration missing, invalid data, throttling, partial failure, network errors)
- Coverage: 37.5%
```

### 10. Conclusion

**Summarize key points:**

**Example:**
```markdown
## Conclusion

The AutomatedEmailAudit flow is functionally sound and achieves its business objective of auditing emails for embedded links. The implementation demonstrates good foundational practices with proper error handling structure and logical flow organization.

**Key Strengths:**
- Clear business purpose and well-defined scope
- Appropriate use of try-catch error handling
- Proper authentication via connection references

**Critical Areas for Improvement:**
- Performance optimization (batch updates, pagination) is essential for scale
- Error logging and monitoring need enhancement for production reliability
- Retry policies should be added to handle transient failures

**Overall Recommendation:**
With the Priority 2 (High) improvements implemented, this flow will be production-ready and scalable. The current version is functional for low-to-moderate email volumes but will encounter performance and reliability issues at scale.

**Estimated Effort:**
- Priority 2 (High) fixes: 8-12 hours
- Priority 3 (Medium) enhancements: 4-6 hours
- Priority 4 (Low) improvements: 2-3 hours
- **Total: 14-21 hours** for comprehensive improvement

**Risk Assessment:**
- **Current Risk Level:** Medium (performance and scalability concerns)
- **Post-Improvement Risk Level:** Low (production-ready with proper error handling and performance)
```

## Tone & Style Guidelines

- **Audience:** Technical audience (developers, architects, DevOps engineers)
- **Depth:** Technical and detailed
- **Balance:** Be critical but constructive
- **Actionable:** Every issue should have a clear recommendation
- **Evidence-Based:** Support observations with code examples or metrics

## What to Include

- ✅ Specific code examples showing issues
- ✅ Quantitative metrics where possible
- ✅ Prioritized, actionable recommendations
- ✅ Expected impact of changes
- ✅ Implementation guidance

## What NOT to Include

- ❌ Business context or purpose (that's in README.md)
- ❌ Vague criticism without solutions
- ❌ Personal opinions without technical basis
- ❌ Recommendations without priority or impact

## Rating Guidelines

Use consistent rating scale across all sections:

- **Excellent:** Exceeds best practices, no improvements needed
- **Good:** Follows best practices, minor improvements possible
- **Fair:** Functional but significant improvements needed
- **Poor:** Major issues requiring immediate attention

## Handling Edge Cases

- **Simple Flows:** For very simple flows (< 10 actions), focus on architecture and potential enhancements rather than complexity
- **Complex Flows:** For highly complex flows, consider suggesting decomposition into child flows
- **Legacy Flows:** Acknowledge technical debt but prioritize critical issues

---

**Remember:** CodeReview.md is for understanding HOW the flow works technically and HOW to improve it. README.md is for understanding WHAT it does and WHY.

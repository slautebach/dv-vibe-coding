# North52 Functions Reference

> **📘 About this reference**: This document provides practical examples, usage patterns, and performance tips for common North52 functions.  
> **📚 For a complete list** of all 539 North52 functions with official documentation links, see [north52-functions-complete.md](north52-functions-complete.md).  
> **🔧 For business process activities**, see [north52-business-process-activities.md](north52-business-process-activities.md).

This document provides a quick reference for common North52 Decision Suite functions, their usage patterns, performance considerations, and recommended alternatives.

## Table of Contents

1. [Data Query Functions](#data-query-functions)
2. [Conditional Logic Functions](#conditional-logic-functions)
3. [Data Manipulation Functions](#data-manipulation-functions)
4. [Client-Side Functions](#client-side-functions)
5. [Advanced Flow Control](#advanced-flow-control)
6. [Performance Best Practices](#performance-best-practices)
7. [Common Patterns](#common-patterns)

---

## Data Query Functions

### FindRecordsFD()

**Purpose**: Query Dataverse records using FetchXML with parameter substitution.

**Syntax**:
```
FindRecordsFD('FetchName', 'attribute', setparams(param1, param2, ...))
```

**Parameters**:
- `FetchName`: Name of the FetchXML query defined in the formula
- `attribute`: Field name to return (use 'true' to return entire record)
- `setparams()`: Values to substitute for {0}, {1}, etc. in FetchXML

**Performance Considerations**:
- ✓ Returns multiple records - suitable for iteration with ForEachRecord
- ✓ Uses FetchXML optimization
- ⚠ Large result sets impact performance
- ⚠ Always use filters to limit results

**Best Practices**:
```
// Good: Filtered query with date range
FindRecordsFD('RateConfiguration', 'true', 
  setparams([startdate], [enddate], [ratetable]))

// Bad: No filters, retrieves all records
FindRecordsFD('RateConfiguration', 'true', setparams())
```

**Common Use Cases**:
- Loading configuration data
- Retrieving related records for calculations
- Bulk data operations within ForEachRecord

**Alternative**: Use `FindRecords()` if FetchXML is not needed, or `GetRecords()` for simple lookups.

### FindValueFD()

**Purpose**: Query a single value from Dataverse using FetchXML.

**Syntax**:
```
FindValueFD('FetchName', 'attribute', 'defaultValue', returnFirstOnly, setparams(...))
```

**Parameters**:
- `FetchName`: Name of FetchXML query
- `attribute`: Field name to return
- `defaultValue`: Return value if no records found (e.g., '0', '')
- `returnFirstOnly`: true/false - return only first match
- `setparams()`: Parameter values

**Performance Considerations**:
- ✓ Optimized for single value retrieval
- ✓ Specify `top="1"` in FetchXML for best performance
- ✓ Use default value to avoid null handling

**Best Practices**:
```
// Good: Single value with default
FindValueFD('BenefitConfig', 'mnp_configurationvalue', '0', true,
  setparams([startdate], [enddate], 'THRESHOLDCODE'))

// Better: Add top="1" in FetchXML definition
```

**Common Use Cases**:
- Loading threshold values from configuration
- Retrieving single lookup values
- Configuration-driven calculations

**Alternative**: Use `GetRecordValue()` if you already have a record reference.

### GetRecords()

**Purpose**: Simplified record retrieval without FetchXML.

**Syntax**:
```
GetRecords('EntityName', 'filter', 'attribute1,attribute2,attribute3')
```

**Performance Considerations**:
- ✓ Simpler than FetchXML for basic queries
- ⚠ Limited filtering capabilities
- ⚠ Not suitable for complex joins

**Best Practice**: Use for simple single-entity queries; prefer FindRecordsFD for complex scenarios.

---

## Conditional Logic Functions

### If()

**Purpose**: Simple if-then-else conditional.

**Syntax**:
```
If(condition, valueIfTrue, valueIfFalse)
```

**Performance**: Lightweight, suitable for simple conditions.

**Best Practices**:
```
// Good: Simple condition
If([age] >= 65, 100, 0)

// Bad: Nested If statements (use IfTrue or Switch instead)
If([age] >= 65, If([income] < 1000, 100, 50), 0)
```

**Alternative**: Use `IfTrue()` for actions, `Switch()` for multiple conditions.

### IfTrue()

**Purpose**: Execute actions when condition is true (no else branch).

**Syntax**:
```
IfTrue(condition, actionWhenTrue)
```

**Performance**: More efficient than If() when else branch is not needed.

**Best Practices**:
```
// Good: Action only when condition met
IfTrue([age] >= 65, SetVar('eligible', 'Yes'))

// Good: Returns value when true, null otherwise
IfTrue([age] >= 65, [income] / 12)
```

**Common Use Cases**:
- Conditional variable assignments
- Eligibility checks
- Optional calculations

### Switch()

**Purpose**: Multi-way conditional logic (like SELECT CASE).

**Syntax**:
```
Switch(value,
  case1, result1,
  case2, result2,
  defaultResult)
```

**Performance**: More efficient than nested If() statements.

**Best Practices**:
```
// Good: Multiple conditions
Switch([ratetable],
  '1', 'Single',
  '2', 'Couple',
  '3', 'Single with Dependent',
  'Unknown')

// Better than nested If statements for 3+ conditions
```

**Alternative**: Use DecisionTable for complex multi-condition logic.

---

## Data Manipulation Functions

### SetVar() / GetVar()

**Purpose**: Create and retrieve formula variables for reusable calculations.

**Syntax**:
```
SetVar('variableName', value)
GetVar('variableName')
```

**Performance Considerations**:
- ✓ Excellent for caching calculated values
- ✓ Reduces redundant calculations
- ✓ Improves formula readability

**Best Practices**:
```
// Good: Calculate once, use multiple times
SetVar('monthlyIncome', [annualIncome] / 12),
SetVar('eligibleAmount', If(GetVar('monthlyIncome') < 1000, 100, 0))

// Naming convention: Use camelCase or descriptive names
SetVar('totalAnnualNetIncome', ...) // Good
SetVar('tANI', ...)                  // Less clear
```

**Common Use Cases**:
- Breaking complex calculations into steps
- Storing query results for reuse
- Clarifying formula logic with named intermediates

### SetAttribute() / GetAttribute()

**Purpose**: Set or retrieve record attribute values.

**Syntax**:
```
SetAttribute('attributename', value)
GetAttribute('entityname.attributename')
```

**Performance**: Direct Dataverse field access, efficient.

**Best Practices**:
```
// Server-side formula
UpdateRecord('mnp_assessment', [recordid],
  SetAttribute('mnp_calculatedamount', [amount]),
  SetAttribute('mnp_processingdate', Now())
)

// Use with UpdateRecord for bulk updates
```

**Alternative**: Use `SetClientSideField()` for client-side formulas.

### SetClientSideField()

**Purpose**: Update form fields in client-side formulas (browser).

**Syntax**:
```
SetClientSideField('fieldname', value)
```

**Performance**: Immediate UI update, no server round-trip.

**Best Practices**:
```
// Good: Update visible fields for immediate feedback
MultipleClientSide(
  SetClientSideField('mnp_pchbamount', [calculatedAmount]),
  SetClientSideField('mnp_status', 'Calculated'),
  FormSave()
)

// Note: Only works in Client-Side formulas
```

**Alternative**: Use `SetAttribute()` in server-side formulas.

---

## Client-Side Functions

### FormSave()

**Purpose**: Trigger form save from client-side formula.

**Syntax**:
```
FormSave()
```

**Performance**: Triggers save event, executes server-side logic.

**Best Practices**:
```
// Good: Save after updating fields
MultipleClientSide(
  SetClientSideField('mnp_amount', [value]),
  FormSave()
)

// Caution: Avoid in infinite loop scenarios
// (e.g., Update trigger that runs on save)
```

**Common Use Cases**:
- Persisting calculated values
- Triggering server-side validation
- Cascade updates to related records

### ShowMessage()

**Purpose**: Display notification to user.

**Syntax**:
```
ShowMessage('message text', 'title', messageLevel)
```

**Message Levels**:
- `0`: Information
- `1`: Warning  
- `2`: Error

**Best Practices**:
```
// Good: Inform user of validation errors
IfTrue([age] < 18,
  ShowMessage('Applicant must be 18 or older', 'Validation Error', 2))

// Use for business rule violations or important notifications
```

### GetCurrentUserAttribute()

**Purpose**: Retrieve information about current user.

**Syntax**:
```
GetCurrentUserAttribute('attributename')
```

**Common Attributes**:
- `systemuserid`: User's GUID
- `fullname`: User's full name
- `businessunitid`: User's business unit
- `territoryid`: User's territory

**Best Practices**:
```
// Good: Default field to current user
IfTrue(IsNull([owner]), 
  SetAttribute('ownerid', GetCurrentUserAttribute('systemuserid')))

// Security: Filter records by user territory
```

---

## Advanced Flow Control

### SmartFlow()

**Purpose**: Execute multiple operations in sequence, passing context between steps.

**Syntax**:
```
SmartFlow(
  operation1,
  operation2,
  operation3,
  ...
)
```

**Performance**: Efficient for multi-step operations within single transaction.

**Best Practices**:
```
// Good: Initialize variables, query data, calculate, update
SmartFlow(
  SetVar('threshold', FindValueFD('Config', 'value', '0', true, setparams())),
  SetVar('income', [annualIncome] / 12),
  SetVar('eligible', If(GetVar('income') < GetVar('threshold'), true, false)),
  IfTrue(GetVar('eligible'), 
    UpdateRecord('mnp_assessment', [id], 
      SetAttribute('mnp_approved', true)))
)

// Structure: Initialize -> Query -> Calculate -> Act
```

**Common Use Cases**:
- Complex multi-step calculations
- Conditional data updates
- Orchestrating multiple operations

### ForEachRecord()

**Purpose**: Iterate over query results and execute actions.

**Syntax**:
```
ForEachRecord(
  FindRecordsFD('FetchName', 'true', setparams(...)),
  SetVar('value', CurrentRecord('attributename')),
  // ... actions on current record
)
```

**Performance Considerations**:
- ⚠ Iterates all matching records - ensure queries are filtered
- ⚠ Avoid nested ForEachRecord (N² performance)
- ⚠ Consider batch operations for large datasets

**Best Practices**:
```
// Good: Process filtered results
ForEachRecord(
  FindRecordsFD('Payments', 'true', setparams([startdate], [enddate])),
  SetVar('total', GetVar('total') + CurrentRecord('amount'))
)

// Bad: Unfiltered query with nested loop
ForEachRecord(
  FindRecordsFD('AllRecords', 'true', setparams()),
  ForEachRecord(...) // Avoid this!
)
```

**Alternative**: Use aggregation functions if only calculating totals (more efficient).

### MultipleSide() / MultipleClientSide()

**Purpose**: Execute multiple operations (server or client context).

**Syntax**:
```
MultipleClientSide(
  operation1,
  operation2,
  operation3
)
```

**Best Practices**:
```
// Client-side: Update multiple fields
MultipleClientSide(
  SetClientSideField('field1', value1),
  SetClientSideField('field2', value2),
  FormSave()
)

// Server-side: Update multiple records
MultipleSide(
  UpdateRecord('entity1', [id1], SetAttribute('field', value)),
  UpdateRecord('entity2', [id2], SetAttribute('field', value))
)
```

---

## Performance Best Practices

### 1. Cache Repeated Calculations

**Bad**:
```
SetAttribute('field1', [annualIncome] / 12 * 0.05),
SetAttribute('field2', [annualIncome] / 12 * 0.10),
SetAttribute('field3', [annualIncome] / 12 - 500)
```

**Good**:
```
SetVar('monthlyIncome', [annualIncome] / 12),
SetAttribute('field1', GetVar('monthlyIncome') * 0.05),
SetAttribute('field2', GetVar('monthlyIncome') * 0.10),
SetAttribute('field3', GetVar('monthlyIncome') - 500)
```

### 2. Optimize FetchXML Queries

**Bad FetchXML**:
```xml
<fetch>
  <entity name="mnp_rateconfiguration">
    <all-attributes />  <!-- Retrieves all fields -->
    <!-- No filters -->
  </entity>
</fetch>
```

**Good FetchXML**:
```xml
<fetch top="1">
  <entity name="mnp_rateconfiguration">
    <attribute name="mnp_rate" />
    <attribute name="mnp_threshold" />
    <filter>
      <condition attribute="mnp_startdate" operator="le" value="{0}" />
      <condition attribute="mnp_enddate" operator="ge" value="{0}" />
    </filter>
    <order attribute="mnp_startdate" descending="true" />
  </entity>
</fetch>
```

**Guidelines**:
- Specify only needed attributes
- Always include filters
- Use `top="n"` when possible
- Add ordering for deterministic results
- Index filter fields in Dataverse

### 3. Choose Appropriate Execution Mode

**Client-Side Formulas**:
- ✓ Immediate user feedback
- ✓ No server round-trip for calculations
- ✗ Limited to client-side functions
- ✗ Bypassed by API/integration calls

**Server-Side Formulas**:
- ✓ Full function access
- ✓ Executes on all create/update paths
- ✓ Can trigger workflows and plugins
- ✗ Slower due to server round-trip

**Scheduled Formulas**:
- ✓ Bulk operations
- ✓ Background processing
- ✗ Not real-time
- ✗ Requires careful error handling

**Recommendation**: Use client-side for UI-focused calculations, server-side for business-critical logic.

### 4. Minimize Record Updates

**Bad**:
```
UpdateRecord(...),
UpdateRecord(...),
UpdateRecord(...) // Three separate update transactions
```

**Good**:
```
UpdateRecord('entity', [id],
  SetAttribute('field1', value1),
  SetAttribute('field2', value2),
  SetAttribute('field3', value3)
) // Single update transaction
```

### 5. Use Global Calculations for Reusability

Instead of duplicating formula logic across multiple formulas:

**Bad**: Same calculation repeated in multiple formulas

**Good**: Create Global Calculation "CalculateMonthlyRate" and reference it
```
{Global.CalculateMonthlyRate}
```

**Benefits**:
- Single source of truth
- Easier maintenance
- Consistent results across formulas

---

## Common Patterns

### Pattern 1: Configuration-Driven Thresholds

```
SetVar('threshold', 
  FindValueFD('Configuration', 'value', '0', true,
    setparams([effectivedate], 'THRESHOLDCODE'))),
    
IfTrue([income] < GetVar('threshold'),
  SetAttribute('eligible', true))
```

### Pattern 2: Age-Based Eligibility

```
Switch([age],
  '<65', 'Not Eligible',
  '65-74', 'Standard Rate',
  '>=75', 'Enhanced Rate')
  
// Or with IfTrue:
IfTrue([age] >= 65 and [age] < 75,
  SetVar('rate', 'standard')),
IfTrue([age] >= 75,
  SetVar('rate', 'enhanced'))
```

### Pattern 3: Rate Table Lookup

```
SmartFlow(
  SetVar('rateTable', GetOptionSetName('entity.ratetable', [ratetable])),
  
  ForEachRecord(
    FindRecordsFD('RateConfig', 'true',
      setparams([date], GetVar('rateTable'), [income])),
    SetVar('selectedRate', CurrentRecord('rate'))
  ),
  
  SetAttribute('calculatedamount', [income] * GetVar('selectedRate'))
)
```

### Pattern 4: Conditional Form Save

```
MultipleClientSide(
  SetClientSideField('mnp_amount', [calculated]),
  
  // Only save if amount changed
  IfTrue([calculated] != [mnp_amount],
    FormSave())
)
```

### Pattern 5: Error Handling with Defaults

```
// Provide default values for missing data
SetVar('income', IfNull([mnp_income], 0)),
SetVar('threshold', 
  FindValueFD('Config', 'value', '1000', true, setparams())), // Default 1000

// Validate before calculation
IfTrue(GetVar('income') >= 0 and GetVar('threshold') > 0,
  SetVar('eligible', GetVar('income') < GetVar('threshold')))
```

---

## Function Categories Quick Reference

### Data Retrieval
- `FindRecordsFD()` - Multiple records via FetchXML
- `FindValueFD()` - Single value via FetchXML
- `GetRecords()` - Simple record query
- `GetRecordValue()` - Value from existing record

### Conditional Logic
- `If()` - If-then-else
- `IfTrue()` - If-then (no else)
- `Switch()` - Multi-way conditional
- `IsNull()` - Check for null values

### Variables
- `SetVar()` / `GetVar()` - Formula variables
- `SetGlobal()` / `GetGlobal()` - Global variables

### Data Updates (Server)
- `UpdateRecord()` - Update Dataverse record
- `SetAttribute()` - Set field value
- `CreateRecord()` - Create new record
- `DeleteRecord()` - Delete record

### Client-Side Operations
- `SetClientSideField()` - Update form field
- `FormSave()` - Trigger form save
- `ShowMessage()` - Display notification
- `RefreshForm()` - Reload form data

### Flow Control
- `SmartFlow()` - Sequential operations
- `ForEachRecord()` - Iterate records
- `MultipleSide()` - Multiple server operations
- `MultipleClientSide()` - Multiple client operations

### Utility
- `GetOptionSetName()` - Option set label from value
- `GetCurrentUserAttribute()` - Current user info
- `Now()` - Current date/time
- `AddDays() / AddYears()` - Date manipulation

---

## Deprecated or Discouraged Functions

### Avoid: ExecuteFetchXML()

**Reason**: Deprecated in favor of FindRecordsFD()

**Migration**:
```
// Old
ExecuteFetchXML('query', 'entity')

// New
FindRecordsFD('FetchName', 'true', setparams(...))
```

### Avoid: SetValue()

**Reason**: Ambiguous - use specific functions

**Alternatives**:
- `SetAttribute()` for server-side
- `SetClientSideField()` for client-side
- `SetVar()` for variables

### Avoid: Excessive Nesting

**Bad**:
```
If(condition1,
  If(condition2,
    If(condition3,
      If(condition4, value1, value2),
      value3),
    value4),
  value5)
```

**Good**: Use DecisionTable or Switch instead

---

## Additional Resources

- **North52 Support**: https://support.north52.com/
- **Function Reference**: https://support.north52.com/knowledgebase/functions/
- **Advanced Patterns**: https://support.north52.com/knowledgebase/advanced-view/
- **Community Forum**: North52 Community on Microsoft Dynamics Forums

---

## Recommended Reading Order

1. Start with **Data Query Functions** - Most formulas need to retrieve data
2. Learn **Conditional Logic** - Essential for business rules
3. Master **Variables** - Key to readable, maintainable formulas
4. Understand **SmartFlow** - Orchestrates complex operations
5. Apply **Performance Best Practices** - Optimize from the start

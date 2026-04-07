# Workflow Schema Reference

## Overview

**Location**: `Workflows/{guid}.xaml`  
**Format**: Windows Workflow Foundation (WF) XAML  
**Purpose**: Business process automation using declarative workflow definitions.

Dataverse workflows use Windows Workflow Foundation XAML with Dataverse-specific activities. Workflows can be synchronous (real-time) or asynchronous (background).

## File Structure

```xml
<Activity 
  x:Class="Microsoft.Crm.Workflow.Activities.WorkflowActivity"
  xmlns="http://schemas.microsoft.com/netfx/2009/xaml/activities"
  xmlns:mxswa="http://schemas.microsoft.com/crm/2006/webservices"
  xmlns:mxs="http://schemas.microsoft.com/xrm/2011/Contracts"
  xmlns:x="http://www.w3.org/2001/XMLSchema-instance">
  
  <mxswa:Workflow>
    <!-- Workflow metadata and steps -->
  </mxswa:Workflow>
</Activity>
```

## Workflow Element

The `<mxswa:Workflow>` element contains all workflow metadata and execution logic.

### Key Attributes

```xml
<mxswa:Workflow 
  DisplayName="Calculate Total Amount"
  Description="Calculates sum of line items"
  IsCustomizable="True"
  IsAsync="False"
  Mode="0"
  Scope="4"
  OnDemand="False"
  TriggerOnCreate="True"
  TriggerOnDelete="False"
  TriggerOnStatusChange="False"
  TriggerOnUndelete="False"
  TriggerOnUpdateAttributeList="mnp_amount,mnp_quantity"
  FilteringAttributes="mnp_amount,mnp_quantity"
  PrimaryEntity="mnp_orderitem"
  TargetTypeCode="10001">
```

**Attributes**:
- **Mode**: 0=Background, 1=Real-time
- **Scope**: 1=User, 2=BusinessUnit, 3=ParentChildBusinessUnit, 4=Organization
- **IsAsync**: True for background workflows, False for synchronous
- **TriggerOnCreate/Update/Delete**: When workflow executes
- **FilteringAttributes**: Comma-separated list of fields that trigger on update
- **PrimaryEntity**: Logical name of target table
- **TargetTypeCode**: Entity type code

## Common Workflow Activities

### GetEntityProperty

Retrieves a field value from an entity.

```xml
<mxswa:GetEntityProperty 
  Attribute="mnp_amount" 
  Entity="[InputEntities(&quot;primaryEntity&quot;)]" 
  EntityName="mnp_orderitem" 
  Value="[mnp_amount]">
  <mxswa:GetEntityProperty.TargetType>
    <InArgument x:TypeArguments="s:Type">
      <mxs:EntityReference x:TypeArguments="mxs:EntityReference" />
    </InArgument>
  </mxswa:GetEntityProperty.TargetType>
</mxswa:GetEntityProperty>
```

**Attributes**:
- **Attribute**: Logical name of field to retrieve
- **Entity**: Source entity (often uses InputEntities function)
- **EntityName**: Logical name of table
- **Value**: Variable to store result

### SetEntityProperty

Sets a field value on an entity.

```xml
<mxswa:SetEntityProperty 
  Attribute="mnp_totalamount" 
  Entity="[CreatedEntities(&quot;CreateStep1_localParameter#Temp&quot;)]" 
  EntityName="mnp_order" 
  Value="[CalculatedTotal]">
  <mxswa:SetEntityProperty.TargetType>
    <InArgument x:TypeArguments="s:Type">
      <mxs:EntityReference x:TypeArguments="mxs:Money" />
    </InArgument>
  </mxswa:SetEntityProperty.TargetType>
</mxswa:SetEntityProperty>
```

**Attributes**:
- **Attribute**: Logical name of field to set
- **Entity**: Target entity reference
- **EntityName**: Logical name of table
- **Value**: Value to assign (can be variable or literal)

### CreateEntity

Creates a new record.

```xml
<mxswa:CreateEntity 
  DisplayName="Create Task" 
  EntityName="task" 
  Entity="[CreateStep1_localParameter]">
  <mxswa:CreateEntity.TargetType>
    <InArgument x:TypeArguments="s:Type">
      <mxs:EntityReference x:TypeArguments="mxs:Entity" />
    </InArgument>
  </mxswa:CreateEntity.TargetType>
</mxswa:CreateEntity>
```

Often preceded by multiple `SetEntityProperty` calls to populate fields.

### UpdateEntity

Updates an existing record.

```xml
<mxswa:UpdateEntity 
  DisplayName="Update Status" 
  Entity="[InputEntities(&quot;primaryEntity&quot;)]" 
  EntityName="mnp_application">
</mxswa:UpdateEntity>
```

Typically follows `SetEntityProperty` calls that modify field values.

### AssignEntity

Changes record ownership.

```xml
<mxswa:AssignEntity 
  DisplayName="Assign to Queue" 
  Entity="[InputEntities(&quot;primaryEntity&quot;)]" 
  EntityName="mnp_case"
  Assignee="[QueueReference]">
</mxswa:AssignEntity>
```

### SetState

Changes status or status reason of a record.

```xml
<mxswa:SetState 
  DisplayName="Deactivate Record" 
  Entity="[InputEntities(&quot;primaryEntity&quot;)]" 
  EntityName="mnp_application"
  State="Inactive"
  Status="2">
</mxswa:SetState>
```

**Attributes**:
- **State**: Active or Inactive
- **Status**: Integer status reason code

### SendEmail

Sends an email message.

```xml
<mxswa:SendEmail 
  DisplayName="Send Notification" 
  Email="[EmailEntity]" 
  From="[SystemUser]"
  To="[ContactReference]"
  BCC="[BCCRecipients]"
  Subject="Application Approved"
  Body="Your application has been approved.">
</mxswa:SendEmail>
```

## Control Flow Activities

### ActivityReference

References a child workflow step or custom action.

```xml
<mxswa:ActivityReference 
  AssemblyQualifiedName="Microsoft.Crm.Workflow.Activities.ConditionSequence"
  DisplayName="Check Condition">
  <Sequence>
    <!-- Nested activities -->
  </Sequence>
</mxswa:ActivityReference>
```

### ConditionSequence

Implements if-then-else logic.

```xml
<mxswa:ActivityReference AssemblyQualifiedName="Microsoft.Crm.Workflow.Activities.ConditionSequence">
  <Sequence>
    <mxswa:EvaluateCondition 
      Condition="[mnp_amount] &gt; 1000" 
      Result="[ConditionResult]">
    </mxswa:EvaluateCondition>
    
    <If Condition="[ConditionResult]">
      <If.Then>
        <!-- Activities when true -->
      </If.Then>
      <If.Else>
        <!-- Activities when false -->
      </If.Else>
    </If>
  </Sequence>
</mxswa:ActivityReference>
```

### Composite

Groups multiple activities together.

```xml
<mxswa:Composite DisplayName="Process Line Items">
  <Sequence>
    <mxswa:GetEntityProperty ... />
    <mxswa:SetEntityProperty ... />
    <mxswa:UpdateEntity ... />
  </Sequence>
</mxswa:Composite>
```

## Expressions and Variables

### Variable Declaration

```xml
<Variable x:TypeArguments="x:String" Name="EmailBody" />
<Variable x:TypeArguments="mxs:Money" Name="TotalAmount" />
<Variable x:TypeArguments="x:Boolean" Name="IsApproved" />
```

**Common Types**:
- `x:String` - Text
- `x:Int32` - Integer
- `x:Decimal` - Decimal number
- `mxs:Money` - Currency
- `x:Boolean` - True/false
- `x:DateTime` - Date/time
- `mxs:EntityReference` - Lookup to another record

### Functions

**InputEntities**: Gets the triggering entity

```xml
[InputEntities("primaryEntity")]
```

**CreatedEntities**: Gets an entity created in a previous step

```xml
[CreatedEntities("CreateStep1_localParameter")]
```

**LookupValue**: Extracts value from lookup field

```xml
[LookupValue("mnp_customer", "accountid")]
```

### Operators

Workflows use Visual Basic expression syntax:

- **Comparison**: `=`, `<>`, `>`, `<`, `>=`, `<=`
- **Logical**: `And`, `Or`, `Not`
- **Arithmetic**: `+`, `-`, `*`, `/`, `Mod`
- **String**: `&` (concatenation), `.Contains()`, `.StartsWith()`

Example:
```xml
[mnp_amount] > 1000 And [mnp_status] = "Pending"
```

## Wait Conditions

Workflows can wait for conditions before continuing.

```xml
<mxswa:Wait 
  DisplayName="Wait for Approval"
  TimeoutDuration="7.00:00:00"
  Condition="[mnp_status] = 120310002">
  <!-- Activities after wait -->
</mxswa:Wait>
```

**Attributes**:
- **TimeoutDuration**: Format: `days.hours:minutes:seconds`
- **Condition**: Expression to evaluate

## Custom Workflow Activities

Custom activities (from plugins or third-party tools) appear as:

```xml
<mxswa:ActivityReference 
  AssemblyQualifiedName="MyNamespace.MyActivity, MyAssembly"
  DisplayName="Custom Action">
  <InArgument x:TypeArguments="x:String" x:Key="InputParameter">
    [ParameterValue]
  </InArgument>
  <OutArgument x:TypeArguments="x:String" x:Key="OutputParameter">
    [OutputVariable]
  </OutArgument>
</mxswa:ActivityReference>
```

## Parsing Strategy

### 1. Extract Workflow Metadata

From `<mxswa:Workflow>` attributes:
- Trigger conditions (Create, Update, Delete)
- Execution mode (Synchronous vs. Asynchronous)
- Target entity
- Filtered attributes (what triggers updates)

### 2. Identify Steps

Walk through `<mxswa:ActivityReference>` and activity elements:
- Create/Update/Delete operations
- Conditional branches
- Data retrieval and assignment
- Email notifications

### 3. Map Data Flow

Track variables:
- Where values are retrieved (GetEntityProperty)
- How they're transformed (expressions, calculations)
- Where they're used (SetEntityProperty, conditions)

### 4. Document Logic

Translate XAML to human-readable logic:
1. When application is created
2. If amount > $1000, assign to manager
3. Otherwise, assign to team queue
4. Send notification email to applicant

## Common Patterns

### Create Related Record

```xml
<!-- Create entity variable -->
<mxswa:CreateEntity EntityName="task" Entity="[TaskEntity]" />

<!-- Set lookup to parent -->
<mxswa:SetEntityProperty 
  Entity="[TaskEntity]" 
  Attribute="regardingobjectid" 
  Value="[InputEntities(&quot;primaryEntity&quot;)]" />

<!-- Set other fields -->
<mxswa:SetEntityProperty 
  Entity="[TaskEntity]" 
  Attribute="subject" 
  Value="Follow up required" />

<!-- Save record -->
<mxswa:CreateEntity Entity="[TaskEntity]" />
```

### Update Parent from Child

```xml
<!-- Get parent reference -->
<mxswa:GetEntityProperty 
  Entity="[InputEntities(&quot;primaryEntity&quot;)]"
  Attribute="mnp_parentid"
  Value="[ParentRef]" />

<!-- Retrieve parent record -->
<mxswa:GetEntityProperty 
  Entity="[ParentRef]"
  Attribute="mnp_totalamount"
  Value="[ParentTotal]" />

<!-- Update parent -->
<mxswa:SetEntityProperty 
  Entity="[ParentRef]"
  Attribute="mnp_totalamount"
  Value="[ParentTotal + CurrentAmount]" />

<mxswa:UpdateEntity Entity="[ParentRef]" />
```

### Conditional Email Notification

```xml
<!-- Check condition -->
<mxswa:EvaluateCondition 
  Condition="[mnp_amount] &gt; 5000"
  Result="[RequiresApproval]" />

<If Condition="[RequiresApproval]">
  <If.Then>
    <!-- Get manager -->
    <mxswa:GetEntityProperty 
      Attribute="mnp_manager"
      Value="[ManagerRef]" />
    
    <!-- Send email -->
    <mxswa:SendEmail 
      To="[ManagerRef]"
      Subject="Approval Required"
      Body="High-value application needs review" />
  </If.Then>
</If>
```

## Workflow Metadata (savedquery Table)

Workflows are stored in the `workflow` table. When exported, they include metadata:

```xml
<Workflow 
  WorkflowId="{guid}"
  Name="Calculate Totals"
  Category="Process"
  PrimaryEntity="mnp_application"
  Mode="0"
  LanguageCode="1033">
  <!-- XAML content -->
</Workflow>
```

## Important Notes

### Encoding

HTML entities used for XML special characters:
- `&gt;` for `>`
- `&lt;` for `<`
- `&quot;` for `"`
- `&amp;` for `&`

### Case Sensitivity

- Logical names are lowercase: `mnp_application`
- Display names preserve casing
- Visual Basic expressions are case-insensitive

### Performance

- Synchronous workflows block user operations
- Avoid long-running operations in real-time workflows
- FilteringAttributes limits when update workflows trigger

### Limitations

- Cannot use FetchXML directly (must use custom activities)
- Limited string manipulation functions
- No direct access to related entities (must use steps)
- 2-minute timeout for synchronous workflows

## See Also

- **Entity Schema**: For understanding field types and relationships
- **FetchXML Reference**: For data queries (used in custom activities)
- **Microsoft Documentation**: [Workflow processes overview](https://learn.microsoft.com/power-automate/workflow-processes)

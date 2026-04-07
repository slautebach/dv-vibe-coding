# Power Automate Flow Analysis Guide

This reference provides detailed guidance for analyzing Power Automate cloud flows and identifying common issues, anti-patterns, and optimization opportunities.

## Common Issues & Anti-Patterns

### 1. Performance Issues

#### N+1 Query Problem
**Description:** Executing API calls inside loops, resulting in one query per item.

**Detection:**
```json
"Apply_to_each": {
  "foreach": "@outputs('GetRecords')?['body/value']",
  "actions": {
    "UpdateRecord": {
      "type": "OpenApiConnection",
      "inputs": {
        "host": {
          "operationId": "UpdateRecord"  // ❌ API call per item
        }
      }
    }
  }
}
```

**Impact:**
- High API consumption
- Throttling risk
- Slow execution
- Poor scalability

**Solution:**
- Use batch operations
- Compose array of updates, make single batch call
- Use Dataverse batch API or custom connector

---

#### Missing Pagination
**Description:** Queries that retrieve unlimited records.

**Detection:**
```json
"ListRecords": {
  "parameters": {
    "entityName": "contacts",
    "$filter": "statecode eq 0"
    // ❌ No $top limit
  }
}
```

**Impact:**
- Timeout risk with large datasets
- Memory issues
- Unpredictable runtime

**Solution:**
```json
"parameters": {
  "entityName": "contacts",
  "$filter": "statecode eq 0",
  "$top": 100,  // ✅ Limit results
  "$select": "contactid,fullname,emailaddress1"  // ✅ Limit fields
}
```

---

#### Nested Loops
**Description:** Loops within loops causing exponential complexity.

**Detection:**
```json
"Apply_to_each": {
  "foreach": "@outputs('GetEmails')?['body/value']",
  "actions": {
    "Apply_to_each_2": {  // ❌ Nested loop
      "foreach": "@outputs('GetLinks')?['body/value']"
    }
  }
}
```

**Impact:**
- Exponential time complexity (O(n²) or worse)
- Timeout risk
- High API consumption

**Solution:**
- Optimize with better queries (filter at source)
- Use hash tables/dictionaries for lookups
- Consider child flows for inner loop logic

---

#### Unbounded Concurrency
**Description:** Processing items sequentially when parallel processing would be faster.

**Detection:**
```json
"Apply_to_each": {
  "foreach": "@outputs('GetRecords')?['body/value']",
  // ❌ No concurrency settings (sequential by default)
  "actions": { /* ... */ }
}
```

**Solution:**
```json
"Apply_to_each": {
  "foreach": "@outputs('GetRecords')?['body/value']",
  "runtimeConfiguration": {
    "concurrency": {
      "repetitions": 20  // ✅ Process 20 items in parallel
    }
  },
  "actions": { /* ... */ }
}
```

---

### 2. Error Handling Issues

#### Missing Try-Catch
**Description:** No error handling, allowing failures to stop flow execution.

**Detection:**
```json
{
  "actions": {
    "GetRecord": { /* ... */ },
    "UpdateRecord": { /* ... */ },
    // ❌ No Scope with error handling
  }
}
```

**Solution:**
```json
{
  "Try": {
    "type": "Scope",
    "actions": {
      "GetRecord": { /* ... */ },
      "UpdateRecord": { /* ... */ }
    }
  },
  "Catch": {
    "type": "Scope",
    "runAfter": {
      "Try": ["Failed", "Skipped", "TimedOut"]
    },
    "actions": {
      "LogError": { /* ... */ }
    }
  }
}
```

---

#### No Retry Policies
**Description:** Transient failures cause immediate flow failure.

**Detection:**
```json
"UpdateRecord": {
  "type": "OpenApiConnection",
  // ❌ No retryPolicy configured
  "inputs": { /* ... */ }
}
```

**Solution:**
```json
"UpdateRecord": {
  "type": "OpenApiConnection",
  "inputs": { /* ... */ },
  "retryPolicy": {  // ✅ Retry on transient failures
    "type": "exponential",
    "count": 3,
    "interval": "PT10S",
    "maximumInterval": "PT1M"
  }
}
```

---

#### No Error Logging
**Description:** Errors caught but not logged, making troubleshooting difficult.

**Detection:**
```json
"Catch": {
  "type": "Scope",
  "runAfter": {
    "Try": ["Failed", "Skipped", "TimedOut"]
  },
  "actions": {}  // ❌ Empty catch block
}
```

**Solution:**
```json
"Catch": {
  "type": "Scope",
  "actions": {
    "Compose_Error_Details": {
      "type": "Compose",
      "inputs": {
        "flowRunId": "@workflow().run.id",
        "error": "@result('Try')",
        "timestamp": "@utcNow()"
      }
    },
    "Log_To_Table": {
      "type": "OpenApiConnection",
      "inputs": {
        "host": { "operationId": "CreateRecord" },
        "parameters": {
          "entityName": "mnp_errorlogs",
          "item/mnp_errordetails": "@{outputs('Compose_Error_Details')}"
        }
      }
    }
  }
}
```

---

### 3. Security Issues

#### Hardcoded Credentials
**Description:** Credentials or secrets embedded in flow definition.

**Detection:**
```json
"inputs": {
  "uri": "https://api.example.com",
  "headers": {
    "Authorization": "Bearer abc123xyz"  // ❌ Hardcoded token
  }
}
```

**Solution:**
- Use connection references
- Store secrets in Azure Key Vault
- Reference via environment variables

---

#### Missing Input Validation
**Description:** External inputs used without validation.

**Detection:**
```json
"UpdateRecord": {
  "inputs": {
    "parameters": {
      "item/email": "@triggerBody()?['email']"  // ❌ No validation
    }
  }
}
```

**Solution:**
```json
"Validate_Email": {
  "type": "Compose",
  "inputs": "@if(contains(triggerBody()?['email'], '@'), triggerBody()?['email'], null)"
},
"Condition_Valid_Email": {
  "type": "If",
  "expression": {
    "not": {
      "equals": ["@outputs('Validate_Email')", null]
    }
  },
  "actions": {
    "UpdateRecord": { /* ... */ }
  }
}
```

---

### 4. Code Quality Issues

#### Default Action Names
**Description:** Actions with default names like "Apply_to_each" or "Condition".

**Detection:**
```json
"Apply_to_each": {  // ❌ Default name
  "foreach": "@outputs('GetEmails')?['body/value']"
}
```

**Solution:**
```json
"Apply_to_each_Email": {  // ✅ Descriptive name
  "foreach": "@outputs('GetEmails')?['body/value']"
}
```

---

#### Magic Numbers
**Description:** Hardcoded option set values or constants without context.

**Detection:**
```json
"parameters": {
  "item/statuscode": 120310002  // ❌ What does this mean?
}
```

**Solution:**
```json
// At start of flow
"Compose_STATUS_APPROVED": {
  "type": "Compose",
  "inputs": 120310002
},
// Later in flow
"parameters": {
  "item/statuscode": "@outputs('Compose_STATUS_APPROVED')"  // ✅ Self-documenting
}
```

---

#### Complex Expressions
**Description:** Long, nested expressions that are hard to read.

**Detection:**
```json
"expression": {
  "and": [
    { "equals": ["@items('Apply_to_each')?['properties']?['status']", "Active"] },
    { "greater": ["@int(items('Apply_to_each')?['properties']?['count'])", 10] },
    { "contains": ["@items('Apply_to_each')?['properties']?['tags']", "Important"] }
  ]
}  // ❌ Hard to read
```

**Solution:**
```json
// Break into Compose actions
"Compose_IsActive": {
  "inputs": "@equals(items('Apply_to_each')?['properties']?['status'], 'Active')"
},
"Compose_HasHighCount": {
  "inputs": "@greater(int(items('Apply_to_each')?['properties']?['count']), 10)"
},
"Compose_IsImportant": {
  "inputs": "@contains(items('Apply_to_each')?['properties']?['tags'], 'Important')"
},
"Condition": {
  "expression": {
    "and": [
      { "equals": ["@outputs('Compose_IsActive')", true] },
      { "equals": ["@outputs('Compose_HasHighCount')", true] },
      { "equals": ["@outputs('Compose_IsImportant')", true] }
    ]
  }
}  // ✅ Readable and debuggable
```

---

## Best Practices Checklist

### Performance
- [ ] Use `$top` to limit query results
- [ ] Use `$select` to retrieve only needed fields
- [ ] Avoid API calls inside loops (use batching)
- [ ] Enable concurrency on loops when appropriate
- [ ] Use pagination for large datasets
- [ ] Filter data at the source (Dataverse query) not in the flow

### Error Handling
- [ ] Wrap main logic in Try-Catch (Scope actions)
- [ ] Configure retry policies on API actions
- [ ] Log errors with sufficient detail for troubleshooting
- [ ] Handle partial failures in loops
- [ ] Set appropriate timeout values
- [ ] Notify admins of critical failures

### Security
- [ ] Use connection references (no embedded credentials)
- [ ] Validate all external inputs
- [ ] Apply principle of least privilege to service accounts
- [ ] Avoid logging sensitive data in run history
- [ ] Use Azure Key Vault for secrets
- [ ] Implement appropriate authorization checks

### Code Quality
- [ ] Use descriptive names for all actions
- [ ] Add flow description in properties
- [ ] Break complex expressions into Compose actions
- [ ] Define constants at flow start (avoid magic numbers)
- [ ] Organize logic into Scopes for readability
- [ ] Minimize nesting depth (max 3-4 levels)

### Monitoring & Governance
- [ ] Implement logging for important operations
- [ ] Track flow run metrics (success rate, duration)
- [ ] Set appropriate run history retention
- [ ] Deploy via solutions (not as standalone flows)
- [ ] Use environment variables for configuration
- [ ] Document flow purpose and dependencies

---

## Analysis Metrics

### Complexity Metrics
- **Action Count**: Total number of actions
- **Condition Count**: Number of conditional branches
- **Loop Count**: Number of loops (Apply to each)
- **Nesting Depth**: Maximum nesting level
- **API Call Count**: Number of connector operations per run

**Guidelines:**
- Simple: < 10 actions, 1-2 conditions
- Moderate: 10-30 actions, 3-5 conditions
- Complex: 30-50 actions, 6+ conditions
- Very Complex: > 50 actions (consider decomposition)

### Performance Metrics
- **Average Runtime**: Expected time to complete
- **API Calls per Run**: Number of connector operations
- **Throttling Risk**: High if > 100 API calls or nested loops
- **Timeout Risk**: High if runtime > 5 minutes for scheduled flows

### Quality Metrics
- **Error Handling Coverage**: % of actions protected by try-catch
- **Naming Quality**: % of actions with descriptive names
- **Documentation**: Presence of flow description and action notes
- **Retry Coverage**: % of API actions with retry policies

---

## Common Flow Patterns

### Pattern 1: Batch Processing
**Use Case:** Process multiple records efficiently

```json
{
  "Get_Records": {
    "inputs": {
      "parameters": {
        "$top": 100,
        "$select": "id,status"
      }
    }
  },
  "Apply_to_each_Record": {
    "foreach": "@outputs('Get_Records')?['body/value']",
    "runtimeConfiguration": {
      "concurrency": { "repetitions": 20 }
    },
    "actions": {
      "Process_Record": { /* ... */ }
    }
  }
}
```

### Pattern 2: Child Flow Decomposition
**Use Case:** Break complex logic into reusable child flows

```json
{
  "Main_Flow": {
    "actions": {
      "Call_Child_Flow_Validation": {
        "type": "Workflow",
        "inputs": {
          "host": {
            "workflowId": "child-validation-flow-id"
          },
          "body": { "data": "@triggerBody()" }
        }
      },
      "Call_Child_Flow_Processing": {
        "runAfter": { "Call_Child_Flow_Validation": ["Succeeded"] }
      }
    }
  }
}
```

### Pattern 3: Configuration-Driven Logic
**Use Case:** Externalize business rules to configuration tables

```json
{
  "Get_Configuration": {
    "inputs": {
      "parameters": {
        "entityName": "mnp_flowconfigurations",
        "$filter": "mnp_flowname eq 'MyFlow' and statecode eq 0"
      }
    }
  },
  "Apply_Configuration": {
    "foreach": "@outputs('Get_Configuration')?['body/value']",
    "actions": {
      "Process_Based_On_Config": { /* ... */ }
    }
  }
}
```

### Pattern 4: Idempotent Operations
**Use Case:** Ensure flow can be safely rerun without duplicates

```json
{
  "Check_If_Already_Processed": {
    "inputs": {
      "parameters": {
        "$filter": "mnp_externalid eq '@{triggerBody()?['id']}'"
      }
    }
  },
  "Condition_Already_Exists": {
    "expression": {
      "greater": ["@length(outputs('Check_If_Already_Processed')?['body/value'])", 0]
    },
    "actions": {
      "Terminate_Already_Processed": {
        "type": "Terminate",
        "inputs": {
          "runStatus": "Succeeded",
          "runError": { "message": "Record already processed" }
        }
      }
    },
    "else": {
      "actions": {
        "Process_New_Record": { /* ... */ }
      }
    }
  }
}
```

---

## Optimization Strategies

### Query Optimization
```json
// ❌ Before: Inefficient query
{
  "parameters": {
    "entityName": "accounts",
    "$filter": "statecode eq 0"
  }
}

// ✅ After: Optimized query
{
  "parameters": {
    "entityName": "accounts",
    "$filter": "statecode eq 0 and createdon gt @{addDays(utcNow(), -7)}",
    "$top": 100,
    "$select": "accountid,name,emailaddress1",
    "$orderby": "createdon desc"
  }
}
```

### Batch Update Optimization
```json
// ❌ Before: Individual updates in loop (N API calls)
"Apply_to_each": {
  "actions": {
    "Update_Record": {
      "inputs": {
        "host": { "operationId": "UpdateRecord" }
      }
    }
  }
}

// ✅ After: Batch update (1 API call)
"Compose_Batch_Payload": {
  "inputs": {
    "requests": "@body('Build_Update_Array')"
  }
},
"HTTP_Batch_Update": {
  "type": "Http",
  "inputs": {
    "method": "POST",
    "uri": "@{parameters('DataverseUrl')}/$batch",
    "body": "@outputs('Compose_Batch_Payload')"
  }
}
```

---

## Troubleshooting Tips

### High API Consumption
1. Check for loops with API calls inside
2. Review query result limits ($top)
3. Enable concurrency carefully (increases parallel API calls)
4. Consider caching frequently accessed data

### Timeout Issues
1. Add pagination to limit records per run
2. Increase concurrency to parallelize
3. Move long-running operations to child flows
4. Consider breaking into multiple flows with triggers

### Throttling Errors
1. Implement retry policies with exponential backoff
2. Reduce API calls (batching, caching)
3. Spread load across time (stagger scheduled flows)
4. Review API limits for connectors used

---

## Related Documentation

- [Power Automate Best Practices](https://learn.microsoft.com/en-us/power-automate/guidance/planning/best-practices)
- [Power Automate Limits](https://learn.microsoft.com/en-us/power-automate/limits-and-config)
- [Dataverse API Limits](https://learn.microsoft.com/en-us/power-apps/developer/data-platform/api-limits)

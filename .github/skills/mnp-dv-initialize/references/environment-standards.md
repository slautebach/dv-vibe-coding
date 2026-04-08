# Environment Standards

Source: wiki/Welcome/Platform-Delivery-Playbook/Implementation-Standards/Environment-Standards.md

## Naming Convention

### Power Platform Environments

All environments in the MNP Digital tenant follow this naming standard:

```
DC-{Solution}-{Environment}
```

- **DC** = Digital Customer
- **{Solution}** = Solution name/acronym (e.g., QUARTS, ROCS, OHAS, PATH, GRANTS)
- **{Environment}** = Environment tier

### Environment Tiers

| Environment | Used By | Purpose |
|---|---|---|
| **DEV** | Dev Team | Implement and unit test the solution |
| **SANDBOX** | Dev Team | POC / out-of-stream development |
| **SIT** | QA Team | System integration testing |
| **UAT** | Client Team | Client validation and acceptance testing |
| **PROD** | Client | Live production environment |

**Examples:**
- `DC-QUARTS-DEV`, `DC-QUARTS-SIT`, `DC-QUARTS-UAT`, `DC-QUARTS-PROD`
- `DC-GRANTS-DEV`, `DC-GRANTS-SIT`, `DC-GRANTS-UAT`, `DC-GRANTS-PROD`

## Dataverse Configuration

- **Publisher**: MNP Digital (unless client requests their own publisher)
- **Dataverse Search**: Enable
- **Auditing**: Enable; retain logs forever

## Power Pages

- Create using the **Blank Template**
- When out of Preview, enable **Enhanced Data Model**

## SharePoint Online

Site naming: `CRMDocuments{Environment}`

Examples:
- `qqq.sharepoint.com/sites/CRMDocumentsDEV`
- `qqq.sharepoint.com/sites/CRMDocumentsSIT`

## DLP Policies

1. Create a policy spanning all environments that blocks all unsupported non-Microsoft connectors and classifies all Microsoft connectors as 'Business Data'
2. Create a policy for the default environment (and other training environments) that further restricts which Microsoft connectors are classified as 'Business Data'
3. Create additional policies or exclude environments from policies 1 and 2 that permit certain connectors or connector combinations for specific environments

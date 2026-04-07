# PlantUML Templates

Ready-to-use PlantUML templates for common diagram scenarios. Copy, customize, and use these templates as starting points for your documentation.

## Available Templates

### 1. ERD Database Template
**File**: `erd-database-template.puml`  
**Use for**: Database schema design, entity-relationship modeling  
**Features**:
- Primary and foreign key notation
- Relationship cardinality (one-to-many, many-to-many)
- Attribute types and constraints
- Junction tables for many-to-many relationships
- Comprehensive annotations and notes
- Legend with key symbols

**Best for**: Relational database design, data modeling documentation

---

### 2. Microservices Architecture Template
**File**: `microservices-architecture-template.puml`  
**Use for**: Distributed systems, service-oriented architecture  
**Features**:
- Multiple service layers (API Gateway, Services, Data)
- Message queue integration (event-driven architecture)
- External service integrations
- Caching strategy
- Color-coded components by type
- Communication patterns (sync/async)

**Best for**: Modern cloud-native application architecture

---

### 3. API Sequence Diagram Template
**File**: `sequence-api-template.puml`  
**Use for**: REST API flows, request/response documentation  
**Features**:
- Authentication and authorization flows
- Business logic execution
- Database transactions (BEGIN/COMMIT/ROLLBACK)
- Error handling scenarios
- Async operations (message queues)
- External API integration
- Comprehensive HTTP status codes
- Rate limiting notes

**Best for**: API documentation, integration guides, debugging workflows

---

### 4. Domain Model Class Diagram Template
**File**: `class-domain-template.puml`  
**Use for**: Domain-driven design, object-oriented modeling  
**Features**:
- Entity and Value Object patterns
- Aggregate Root boundaries
- Repository interfaces
- Domain events
- Rich domain model with business logic
- Comprehensive visibility indicators
- DDD patterns (Entity, Value Object, Aggregate, Repository, Service)

**Best for**: Domain-driven design, complex business logic modeling

---

### 5. AWS Architecture Template
**File**: `aws-architecture-template.puml`  
**Use for**: AWS cloud infrastructure diagrams  
**Features**:
- Official AWS icons via stdlib
- VPC with multi-AZ subnets
- Auto Scaling groups
- Serverless components (Lambda)
- Database services (RDS, DynamoDB, ElastiCache)
- Monitoring and security services
- External service integrations
- Detailed annotations and configurations

**Best for**: AWS solution architecture, infrastructure documentation

---

### 6. State Machine Template
**File**: `state-machine-template.puml`  
**Use for**: Workflow states, application lifecycle, process flows  
**Features**:
- Hierarchical (nested) states
- Entry/exit/do actions
- State transitions with guards and actions
- Parallel processing (fork/join)
- Choice and history pseudo-states
- Comprehensive state documentation
- Transition rules and conditions

**Best for**: Workflow modeling, business process states, application lifecycle

---

### 7. Gantt Project Template
**File**: `gantt-project-template.puml`  
**Use for**: Project planning, timeline visualization  
**Features**:
- Multi-phase project structure
- Task dependencies
- Milestones
- Progress tracking (% complete)
- Resource allocation
- Color-coded by phase
- Weekend/holiday handling
- Critical path identification

**Best for**: Project schedules, sprint planning, delivery timelines

---

### 8. Component Architecture Template
**File**: `component-architecture-template.puml`  
**Use for**: System architecture, component interactions  
**Features**:
- Layered architecture (Presentation, Application, Data)
- Component ports (input/output interfaces)
- Shared libraries
- Message bus integration
- Infrastructure components (monitoring, logging, tracing)
- Service discovery
- Detailed component descriptions
- Technology stack documentation

**Best for**: System architecture, microservices documentation, technical design

---

## How to Use Templates

### 1. Copy the Template

```bash
cp template-name.puml my-diagram.puml
```

### 2. Customize Placeholders

Replace bracketed placeholders with your specific information:
- `[Your Name]` → Your actual name
- `[Date]` → Current date
- `[Project Name]` → Your project name
- `[System Name]` → Your system name
- etc.

### 3. Modify Content

- Add/remove entities, components, or services as needed
- Update relationships and connections
- Adjust colors and styling to match your standards
- Modify notes and documentation

### 4. Generate Diagram

```bash
# PNG (default)
java -jar plantuml.jar my-diagram.puml

# SVG (recommended for web)
java -jar plantuml.jar -tsvg my-diagram.puml

# PDF
java -jar plantuml.jar -tpdf my-diagram.puml
```

### 5. Integrate into Documentation

- Commit `.puml` files to version control
- Generate diagrams in CI/CD pipeline
- Embed in markdown with relative paths
- Link from technical documentation

## Template Conventions

### Color Schemes

Templates use semantic colors:
- **Blue** (`#4A90E2`, `LightBlue`) - Services, components
- **Green** (`#50C878`, `LightGreen`) - Databases, data stores
- **Orange** (`#FFA500`, `Coral`) - External services, third-party
- **Purple** (`#9B59B6`) - Gateway, routing
- **Yellow** (`#FFD93D`, `LightYellow`) - Shared libraries, utilities

Feel free to adjust colors to match your organization's standards.

### Naming Conventions

- **PascalCase**: For class and entity names
- **camelCase**: For fields and methods
- **UPPER_CASE**: For enums and constants
- **kebab-case**: For file names

### Comments

All templates include:
- **Header comments**: Author, date, description
- **Inline notes**: Explain complex relationships
- **Legends**: Define symbols and colors
- **Footers**: Version and last updated date

## Customization Tips

### 1. Apply Themes

```plantuml
!theme cerulean
' Other themes: aws-orange, vibrant, spacelab, materia
```

### 2. Include Reusable Components

```plantuml
!include ../common/styles.puml
!include ../common/icons.puml
```

### 3. Use Standard Library Icons

```plantuml
!include <awslib/AWSCommon>
!include <font-awesome-5/users>
```

### 4. Adjust Layout

```plantuml
left to right direction
skinparam linetype ortho
scale 1.5
```

### 5. Add Hyperlinks

```plantuml
class MyClass [[https://docs.example.com/myclass]]
```

## Rendering Best Practices

1. **Start simple**: Add complexity incrementally
2. **Test frequently**: Generate output after each major change
3. **Use SVG for web**: Better scalability and clickable links
4. **Optimize for readability**: Limit elements per diagram (aim for 10-15 main components)
5. **Split large diagrams**: Create separate diagrams for different perspectives
6. **Version control**: Commit both `.puml` and generated images

## Common Modifications

### Change Component Colors

```plantuml
component [My Service] #CustomColor
database "My DB" as db #LightGreen
```

### Adjust Font Sizes

```plantuml
skinparam defaultFontSize 14
skinparam titleFontSize 20
```

### Hide Shadows

```plantuml
skinparam shadowing false
```

### Modify Line Type

```plantuml
skinparam linetype ortho  ' Orthogonal lines
skinparam linetype polyline  ' Angled lines
```

## Integration Examples

### Markdown

```markdown
# System Architecture

![Architecture Diagram](./diagrams/architecture.svg)

See [source](./diagrams/architecture.puml) for details.
```

### CI/CD (GitHub Actions)

```yaml
- name: Generate PlantUML diagrams
  run: |
    find . -name "*.puml" -exec java -jar plantuml.jar -tsvg {} \;
```

### Documentation Sites

PlantUML is supported by:
- **Sphinx**: `sphinxcontrib-plantuml`
- **MkDocs**: `mkdocs-plantuml`
- **Jekyll**: `jekyll-plantuml`
- **Hugo**: Shortcodes

## Getting Help

- Review the main SKILL.md for comprehensive PlantUML syntax
- Check references/ folder for quick guides
- Visit https://plantuml.com/ for official documentation
- Use online editor: http://www.plantuml.com/plantuml/

## Contributing

Have a useful template to share?
1. Ensure it follows the template conventions
2. Include comprehensive comments and notes
3. Test with multiple output formats
4. Add documentation to this README

---

**Template Library Version**: 1.0  
**Last Updated**: February 2026  
**Maintained by**: [Your Organization]

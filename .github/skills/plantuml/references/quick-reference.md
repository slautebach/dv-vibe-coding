# PlantUML Quick Reference

A concise reference guide for PlantUML syntax and common patterns.

## Common Diagram Tags

| Diagram Type | Start Tag | End Tag |
|-------------|-----------|---------|
| Most diagrams | `@startuml` | `@enduml` |
| Gantt | `@startgantt` | `@endgantt` |
| Mind Map | `@startmindmap` | `@endmindmap` |
| WBS | `@startwbs` | `@endwbs` |
| JSON | `@startjson` | `@endjson` |
| YAML | `@startyaml` | `@endyaml` |
| EBNF | `@startebnf` | `@endebnf` |
| Salt (UI) | `salt { }` | N/A |

## Comments

```plantuml
' Single line comment
/' Multi-line
   comment '/
```

## Sequence Diagrams

### Participants
```plantuml
actor Actor
participant Participant
boundary Boundary
control Control
entity Entity
database Database
collections Collections
queue Queue
```

### Arrows
```plantuml
->   ' Solid line
-->  ' Dashed line
->>  ' Thin arrow
-\   ' Lost message
/--  ' Return message
```

### Activation
```plantuml
activate ParticipantName
deactivate ParticipantName
' Or inline:
A -> B++ : Message (activate)
B --> A-- : Response (deactivate)
```

### Grouping
```plantuml
alt condition
  ' true path
else
  ' false path
end

opt condition
  ' optional
end

loop n times
  ' repeated
end

par
  ' parallel
and
  ' also parallel
end

group Label
  ' grouped
end
```

### Autonumbering
```plantuml
autonumber
autonumber 10
autonumber 10 5 "Message #"
```

## Class Diagrams

### Visibility
```plantuml
+ public
- private
# protected
~ package
{static} static member
{abstract} abstract member
```

### Relationships
```plantuml
<|--   ' Inheritance
<|..   ' Interface implementation
*--    ' Composition
o--    ' Aggregation
-->    ' Association
..>    ' Dependency
--     ' Link
```

### Example
```plantuml
class MyClass {
  - privateField: String
  + publicMethod(): void
  # protectedMethod(): int
  {static} staticMethod(): void
}
```

## Entity-Relationship Diagrams

### Entity Definition
```plantuml
entity "EntityName" as alias {
  * primary_key : type <<PK>>
  * foreign_key : type <<FK>>
  --
  field1 : type
  field2 : type <<unique>>
}
```

### Relationships
```plantuml
||--||  ' One to one
||--o{  ' One to many
}o--o{  ' Many to many
|o--o|  ' Zero or one to zero or one
||--o|  ' One to zero or one
```

## Activity Diagrams

### Basic Elements
```plantuml
start
:Activity;
stop
end
```

### Conditionals
```plantuml
if (condition?) then (yes)
  :action1;
else (no)
  :action2;
endif

switch (value?)
case (1)
  :action1;
case (2)
  :action2;
endswitch
```

### Loops
```plantuml
while (condition?) is (true)
  :activity;
endwhile (false)

repeat
  :activity;
repeat while (condition?)
```

### Fork/Join
```plantuml
fork
  :parallel1;
fork again
  :parallel2;
end fork
```

### Partitions
```plantuml
partition "Partition Name" {
  :activity;
}
```

## Component Diagrams

### Components
```plantuml
[Component Name]
component [Another Component]
package "Package" {
  [Component Inside]
}
```

### Interfaces
```plantuml
() "Interface" as I1
[Component] - I1
I1 - [Another Component]
```

### Ports
```plantuml
component [Component] {
  portin "Input"
  portout "Output"
}
```

## State Diagrams

### States
```plantuml
[*] --> State1
State1 --> State2 : event
State2 --> [*]

state State1 {
  [*] --> SubState
  SubState --> [*]
}
```

### State Actions
```plantuml
state State1 {
  State1 : entry / entryAction()
  State1 : do / doActivity()
  State1 : exit / exitAction()
}
```

### Choice and Fork
```plantuml
state choice <<choice>>
state fork <<fork>>
state join <<join>>
```

## Styling

### Colors
```plantuml
#Color ' Inline color
class MyClass #LightBlue
participant A #Red/White ' Background/Text
```

### Themes
```plantuml
!theme cerulean
!theme aws-orange
!theme black-knight
!theme bluegray
!theme vibrant
```

### Skinparam
```plantuml
skinparam backgroundColor #EEEBDC
skinparam monochrome true
skinparam shadowing false
skinparam defaultFontName Arial
skinparam defaultFontSize 12
skinparam classBorderColor black
skinparam classBackgroundColor lightblue
```

## Creole Text Formatting

### Basic Formatting
```plantuml
**bold**
//italic//
__underlined__
--strikethrough--
""monospace""
~~wave underline~~
```

### HTML-style
```plantuml
<b>bold</b>
<i>italic</i>
<u>underline</u>
<s>strike</s>
<color:red>colored</color>
<back:yellow>background</back>
<size:18>sized text</size>
```

### Lists
```plantuml
* Bullet item
** Sub-item
# Numbered item
## Sub-numbered
```

### Tables
```plantuml
|= Header 1 |= Header 2 |
| Cell 1 | Cell 2 |
| Cell 3 | Cell 4 |
```

## Layout Control

### Direction
```plantuml
left to right direction
top to bottom direction
```

### Hidden Links
```plantuml
A -[hidden]-> B
A -[hidden]down-> C
```

### Together
```plantuml
together {
  class A
  class B
}
```

## Notes

### Placement
```plantuml
note left: Text
note right: Text
note top: Text
note bottom: Text

note left of ClassName
  Multi-line
  text
end note
```

### On Links
```plantuml
A -> B : Label
note on link
  Note text
end note
```

## Standard Library

### Import Syntax
```plantuml
!include <library/path/Icon>
```

### Common Libraries
```plantuml
' AWS
!include <awslib/AWSCommon>
!include <awslib/Compute/EC2>

' Azure
!define AzurePuml https://raw.githubusercontent.com/plantuml-stdlib/Azure-PlantUML/release/2-2/dist
!include AzurePuml/AzureCommon.puml

' Kubernetes
!include <kubernetes/k8s-sprites-unlabeled-25pct>

' Font Awesome
!include <font-awesome-5/users>

' Material Icons
!include <material/computer>
```

## Preprocessor

### Variables
```plantuml
!$var = "value"
!define CONSTANT value
```

### Conditionals
```plantuml
!if %variable_exists("VAR")
  ' code
!else
  ' alternative
!endif
```

### Procedures
```plantuml
!procedure $myProc($param)
  ' code using $param
!endprocedure

$myProc("argument")
```

### Include Files
```plantuml
!include path/to/file.puml
!include https://url/to/file.puml
```

## Legend and Title

### Title
```plantuml
title Simple Title
title Multi-line\nTitle
```

### Legend
```plantuml
legend
  Simple legend
endlegend

legend left
  Left-aligned legend
endlegend

legend right
  |= Header |
  | Content |
endlegend
```

### Footer/Header
```plantuml
header Page Header
footer Page Footer
```

## Common Patterns

### Zoom In/Out
```plantuml
scale 1.5
scale 200 width
scale 150 height
scale 200x100
```

### Split Diagrams
```plantuml
page 2x1
' Creates 2 columns, 1 row
```

### External Links
```plantuml
class MyClass [[https://example.com]]
class Another [[https://example.com{Tooltip}]]
```

## Output Formats

### Command Line
```bash
# PNG (default)
plantuml diagram.puml

# SVG
plantuml -tsvg diagram.puml

# PDF
plantuml -tpdf diagram.puml

# ASCII
plantuml -ttxt diagram.puml

# LaTeX
plantuml -tlatex diagram.puml
```

## Tips & Tricks

1. **Use aliases** for long names: `class "Very Long Name" as VLN`
2. **Combine directions** with links: `A -down-> B`
3. **Group related items** with `together`
4. **Use themes** for consistent styling
5. **Add metadata** in comments at file start
6. **Version your diagrams** in the footer
7. **Use !include** for reusable components
8. **Test incrementally** - build diagrams step by step
9. **Use skinparam** for global styling
10. **Check syntax** with `plantuml -syntax file.puml`

## Common Issues

| Issue | Solution |
|-------|----------|
| Diagram too wide | Use `left to right direction` or split into multiple diagrams |
| Text too small | Use `skinparam defaultFontSize 14` |
| Elements misaligned | Use hidden links for positioning |
| Slow generation | Reduce complexity, use simpler themes, disable shadows |
| Java not found | Install JRE 8+, set JAVA_HOME |
| Graphviz error | Install Graphviz or use text-based output |

## Resources

- **Official Site**: https://plantuml.com/
- **Online Editor**: http://www.plantuml.com/plantuml/
- **GitHub**: https://github.com/plantuml/plantuml
- **Standard Library**: https://github.com/plantuml/plantuml-stdlib
- **Real World PlantUML**: https://real-world-plantuml.com/

---

**Last Updated**: February 2026  
**PlantUML Version**: Latest

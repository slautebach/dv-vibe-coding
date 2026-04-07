# Best Practices for Skill Development

This guide provides proven patterns for creating effective skills that bridge the gap between non-deterministic LLMs and deterministic codebases.

## Table of Contents

- [Naming and Style Conventions](#naming-and-style-conventions)
- [Implementation Patterns](#implementation-patterns)
- [Planner-Worker Architecture](#planner-worker-architecture)
- [Common Pitfalls](#common-pitfalls)

## Naming and Style Conventions

### Skill Names

Use gerund form (verbs ending in `-ing`) for skill names to clearly signal an action:

- `optimizing-performance` (good)
- `performance-optimizer` (avoid)
- `managing-dependencies` (good)
- `dependency-manager` (avoid)

### Descriptions

Write descriptions as routing logic, not marketing copy:

**Include "Use when" and "Don't use when" logic:**

```markdown
description: Parse and analyze Dynamics 365 Dataverse solution XML files including 
Entity.xml (table metadata), FormXml (form layouts), and FetchXML queries. Use when 
working with D365 solutions, analyzing entity definitions, or reviewing FetchXML 
queries. Do NOT use for exporting solutions (use export-solution skill instead) or 
for general XML parsing.
```

**Always use third person:**

- "Processes logs and generates reports" (good)
- "I can help you process logs" (avoid)
- "Analyzes code quality metrics" (good)
- "You can use this to analyze code" (avoid)

### Instruction Writing

Use imperative/infinitive form in SKILL.md body:

- "Run the validation script" (good)
- "You should run the validation script" (avoid)
- "Extract field values from the response" (good)
- "The agent can extract field values" (avoid)

## Implementation Patterns

Follow these patterns to balance flexibility with reliability:

| Feature | Best Practice | Rationale |
|---------|--------------|-----------|
| **Logic** | **Deterministic over Generative** - If a task can be done with a Bash/Python script (like checking linting status), use a script. Don't ask the LLM to "check if the code is clean." | Scripts are token-efficient, deterministic, and less error-prone than LLM-generated approaches |
| **Examples** | **Include Negative Examples** - Show cases where the skill should *not* be used to prevent misfires and routing errors | Helps the agent understand boundaries and avoid inappropriate triggering |
| **Size** | **Keep it Lean** - Aim for SKILL.md under 500 lines. If it grows too large, split into sub-skills or domain-specific reference files | Preserves context window space and improves load times |
| **Feedback** | **Validation Loops** - Always include a step where the agent must verify its own work (e.g., "Run `npm test` after modification") | Catches errors early and ensures quality without manual verification |

### When to Use Scripts vs. Instructions

**Use scripts (`scripts/` directory) when:**
- The same code is rewritten repeatedly
- Deterministic reliability is critical
- The task is error-prone without exact steps
- The logic is complex but unchanging

**Use text instructions when:**
- Multiple approaches are valid
- Context affects the decision
- The agent needs to adapt to variations
- Heuristics guide the approach better than rigid rules

### Validation Loop Pattern

Every skill that modifies code or produces artifacts should include explicit verification:

```markdown
## Workflow

1. Analyze the requirements
2. Generate the implementation  
3. **Verify the output:**
   - Run `npm test` to ensure tests pass
   - Run `npm run lint` to check code quality
   - Execute the script with sample input to verify behavior
4. Report results and any issues found
```

## Planner-Worker Architecture

For complex multi-step tasks, avoid creating a single "Super Agent" skill. Instead, decompose into specialized roles:

### The Three-Role Pattern

1. **Architect/Planner:** Analyzes the codebase, understands requirements, and creates a structured plan (e.g., `todo.md` or step-by-step breakdown)

2. **Implementer/Worker:** Executes specific coding tasks based on the plan, focusing on one concrete step at a time

3. **Verifier/Validator:** Runs tests and linters, providing pass/fail signals back to the planner

### When to Use This Pattern

- Tasks requiring 5+ distinct steps
- Work involving multiple files or subsystems
- Projects where failure in one step affects downstream work
- Complex refactoring or feature implementations

### Example Structure

```markdown
## Workflow

This skill follows a planner-worker pattern:

**Phase 1: Planning**
1. Analyze the codebase structure
2. Identify affected components
3. Create implementation plan with validation checkpoints

**Phase 2: Implementation**
4. Execute plan step-by-step
5. After each step, verify the change compiles/runs
6. Proceed only after validation passes

**Phase 3: Verification**
7. Run full test suite
8. Check linting and type checking
9. Generate summary of changes and test results
```

### Benefits

- **Reduced context thrashing:** Each phase has clear focus
- **Better error recovery:** Failures are caught at checkpoints, not at the end
- **Improved quality:** Explicit verification prevents cascading errors
- **Easier debugging:** Clear separation makes it obvious where issues occurred

## Common Pitfalls

Avoid these anti-patterns when creating skills:

### 1. Over-explaining

**Problem:** Explaining things the model already knows wastes precious context space.

**Avoid:**
```markdown
## Working with JSON

JSON is a data format that uses key-value pairs. It supports strings, 
numbers, booleans, arrays, and objects. Here's how JSON syntax works...
```

**Instead:**
```markdown
## Working with JSON

Use the company schema defined in references/schema.json. All timestamps 
must be ISO 8601 format. Nested objects should not exceed 3 levels deep.
```

**Rule:** Only provide "tribal knowledge" or project-specific conventions that the model can't infer.

### 2. Hardcoded Values

**Problem:** Hardcoded paths break when environments differ.

**Avoid:**
```markdown
Run the script located at `/home/user/projects/app/scripts/deploy.sh`
```

**Instead:**
```markdown
1. Locate the deployment script in the project's `scripts/` directory
2. Run `scripts/deploy.sh` from the project root

Or use an environment variable:
```bash
${PROJECT_ROOT}/scripts/deploy.sh
```
```

**Rule:** Use relative paths, environment variables, or instruct the agent to discover paths dynamically.

### 3. Ambiguous Instructions

**Problem:** Vague guidance like "be helpful" or "do your best" provides no actionable direction.

**Avoid:**
```markdown
Try to write good commit messages that are helpful.
```

**Instead:**
```markdown
Ensure all commit messages follow conventional commits format:
- Use present tense ("add feature" not "added feature")
- Limit first line to 72 characters
- Include ticket number in footer: "Refs: #123"
```

**Rule:** Replace subjective guidance with specific, measurable criteria.

### 4. Missing Negative Examples

**Problem:** Without counterexamples, agents may trigger inappropriately.

**Always include:**
```markdown
## When NOT to use this skill

- **For general Python questions** - Use standard LLM knowledge
- **For non-Dataverse XML files** - This skill is specific to D365 solutions
- **For exporting solutions** - Use the export-solution skill instead
```

### 5. Deeply Nested References

**Problem:** References that reference other references create navigation complexity.

**Avoid:**
```
SKILL.md → references/guide.md → references/advanced/details.md
```

**Instead:**
```
SKILL.md → references/guide.md
SKILL.md → references/advanced-guide.md
```

**Rule:** Keep all references one level deep from SKILL.md.

### 6. Duplicate Information

**Problem:** Having the same information in SKILL.md and reference files wastes tokens.

**Choose one location:**
- **SKILL.md:** Essential workflow, when to use, high-level structure
- **References:** Detailed examples, comprehensive lists, domain knowledge

If information appears in references/, don't repeat it in SKILL.md—just link to it.

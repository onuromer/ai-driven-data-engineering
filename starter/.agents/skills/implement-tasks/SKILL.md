---
name: implement-tasks
description: Guidelines for code structure, testing requirements, task completion protocol, and AI behavior when contributing to the project. Use when implementing tasks from the task list.
---

# Implementation Workflow

Follow this step-by-step workflow for all tasks:

1. **Setup Development Environment**
   Create an isolated worktree for the feature:
   ```
   Use skill: git-worktree
   ```

2. **Search for Past Solutions**
   Before implementing, check `docs/learnings/` for relevant past solutions:
   - Extract keywords from the task description
   - Search for matching files in `docs/learnings/`
   - Read relevant learnings to avoid repeated mistakes

3. **Read the Task List**
   - Open the relevant task file in `docs/tasks/`
   - Identify the next uncompleted sub-task
   - Read the PRD in `docs/prds/` for full context

4. **Implementation & Testing**
   Follow the coding standards, testing requirements, and task completion protocol below.

5. **Document Learnings**
   After completing the task, capture any new learnings:
   ```
   Use skill: document-learnings
   ```

## Coding Standards

- Maximum 500 lines per file — split into modules if approaching limit
- Organize code into clearly separated modules grouped by feature or responsibility
- Use clear, consistent imports following Python best practices
- Use `uv` for package management and running scripts
- Use appropriate logging for observability

## Testing Requirements

- Create end-to-end tests using actual data and real connections
- Prefer integration tests over mocked tests
- Isolate test context to enable parallel execution
- Minimum test coverage per component:
  - 1 test for expected use
  - 1 edge case test
  - 1 failure case test

### Test Quality

- NO docstrings on test functions — names should be self-explanatory
- NO comments explaining test steps — code should be clear
- Use descriptive assertion messages with context:
  - BAD: `assert x == y, "Should be equal"`
  - GOOD: `assert x == y, f"Expected {y} but got {x}"`
- ALWAYS test the end result — verify what the user would see

## Task Completion Protocol

### Validation
- Run all tests before marking tasks complete
- Use: `uv run pytest tests/ -v`

### Tracking
- Mark completed tasks in `docs/tasks/` immediately after finishing
- Mark each finished sub-task with `[x]`
- Mark parent task `[x]` only once ALL sub-tasks are `[x]`
- Add discovered sub-tasks under "Discovered During Work" section
- Maintain the "Relevant Files" section — list every file created or modified

### Workflow
- Before starting work, check which sub-task is next
- After implementing a sub-task, update the task file and pause for user approval

## AI Behavior Rules

- Never assume missing context — ask questions if uncertain
- Never hallucinate libraries or functions — only use known, verified packages
- Always confirm file paths and module names exist before referencing
- Never delete or overwrite existing code unless explicitly instructed
- Always plan features vertically (code + tests + observability + docs)

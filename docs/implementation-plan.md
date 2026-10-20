# Implementation plan — IDEA-001

| Order | Task | Work and verification | Acceptance criteria | Dependency |
| --- | --- | --- | --- | --- |
| 1 | TASK-001 | Implement pure word count and CLI; run sample unit tests; review error paths. | AC-001, AC-002, AC-003 | None |
| 2 | TASK-002 | Keep implementation standard-library-only; run both CI test commands and compile check. | AC-004 | TASK-001 |

Create one GitHub issue per task with `.github/ISSUE_TEMPLATE/task.md`. Each issue must link this approved plan, its `TASK-###`, the parent `IDEA-001`, and the listed acceptance criteria. Create dependent tasks only after prerequisite issues are complete. This repository does not create issues automatically.

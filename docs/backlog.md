# Prioritized backlog — IDEA-001

| Priority | Task | Scope / completion criteria | Acceptance criteria | Dependencies |
| --- | --- | --- | --- | --- |
| P1 | TASK-001: Implement and test the word-count CLI | Count words from one UTF-8 file; handle empty, Unicode, and read/decoding errors; focused unit tests pass. | AC-001, AC-002, AC-003 | None |
| P2 | TASK-002: Verify portability and dependency boundary | Document Python requirement, run through standard-library CI, and confirm no network/runtime dependency. | AC-004 | TASK-001 |

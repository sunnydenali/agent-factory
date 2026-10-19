# Acceptance criteria — IDEA-001

- **AC-001 — Basic count:** Given `Hello, factory!`, when the file is counted, the CLI prints `2` and exits successfully.
- **AC-002 — Empty and Unicode input:** Given an empty or whitespace-only UTF-8 file, the count is `0`; Unicode word sequences are counted.
- **AC-003 — Invalid input:** Given a missing, unreadable, or invalid UTF-8 file, the CLI reports an actionable error on stderr and exits non-zero.
- **AC-004 — Offline, dependency-free execution:** The sample runs using Python 3.11+ standard library only and makes no network requests.

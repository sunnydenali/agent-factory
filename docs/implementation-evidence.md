# Implementation evidence — IDEA-001

- Task: TASK-001
- Acceptance criteria: AC-001, AC-002, AC-003
- Implementation: `examples/sample-app/wordcount.py`
- Tests: `examples/sample-app/test_wordcount.py`
- Executed: `python3 -m unittest discover -s examples/sample-app -v` — PASS (5 tests)
- Executed: `python3 -m unittest discover -s tests -v` — PASS (7 tests)
- Executed: `python3 -m compileall -q scripts tests examples` — PASS
- Dependency boundary: standard library only; no package manifest or external runtime dependency.

The CI workflow repeats compilation and both test suites on pull requests and pushes to `main`. Use the recorded CI run, not this text alone, as merge evidence for a future pull request.

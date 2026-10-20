# ADR-0001: Use Python standard library for the factory MVP

- Status: Accepted
- Context: The factory needs portable artifact validation and workflow gates without requiring a provider API, deployment, or package installation.
- Decision: Implement orchestration and tests in Python using only the standard library. Keep sample application code separate under `examples/sample-app/`.
- Consequences: The factory runs with Python 3.11+ and uses `unittest`; downstream application languages remain configurable and do not inherit the sample's runtime choice. Advanced schema validation and GitHub API automation are deferred.
- Alternatives: A framework-based agent runtime or hosted service would add setup and credentials without improving the required manual handoff MVP.

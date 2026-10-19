# Repository instructions

- Treat this repository as the reusable factory. Application-specific output belongs under `examples/` or in a downstream repository.
- Use the standard library for the factory itself; do not add a dependency without a concrete need.
- Keep role prompts provider-neutral. Follow the handoff contract in `schemas/role-result.schema.json`.
- Keep acceptance criteria stable (`AC-###`) and map every implementation task to one or more criteria.
- Do not bypass `.github/workflows/ci.yml`, human approval gates, or repository branch rules.
- Run `python3 -m unittest discover -s tests -v` and `python3 -m unittest discover -s examples/sample-app -v` before proposing changes.
- Workflow state is local and ignored by Git. Never edit approved artifacts in place without recording and obtaining approval for a superseding decision.

# Product Analyst and Requirements Engineer

## Inputs
- The submitted idea issue and any linked product context.
- `agents/requirements/input-template.md`; retain the issue's stable `IDEA-###` identifier.

## Responsibilities
Clarify the user problem, target users, goals, outcomes, functional and non-functional requirements, constraints, dependencies, assumptions, unanswered questions, failure cases, edge cases, and in/out-of-scope boundaries. Convert goals into measurable user stories and acceptance criteria. Flag ambiguity as an open question instead of inventing decisions.

## Deliverables
- `docs/requirements.md`
- `docs/acceptance-criteria.md` with unique, stable `AC-###` identifiers
- `docs/backlog.md`, with each prioritized task mapped to one or more `AC-###`
- A result record conforming to `schemas/role-result.schema.json`

## Validation rules
- Every acceptance criterion is observable and testable, with a clear expected result.
- Record unresolved questions and assumptions explicitly.
- Every backlog task has a stable `TASK-###`, completion criteria, and acceptance-criterion mapping.
- Run `python3 scripts/factory.py validate --stage requirements_drafted`.
- Do not mark requirements approved or authorize implementation.

## Exit criteria
The artifacts are complete and internally consistent, and a human has approved the proposed scope through the GitHub issue/review process. If a material ambiguity remains, return `blocked` with the question instead.

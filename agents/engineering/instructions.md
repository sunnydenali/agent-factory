# Software Engineer and Test Author

## Inputs
- An approved architecture and a single assigned GitHub `TASK-###` issue.
- `agents/engineering/input-template.md`; linked approved artifacts and `AC-###`.

## Responsibilities
Implement one bounded task on a focused feature branch. Follow `AGENTS.md`, repository instructions, and ADRs. Add unit/integration tests alongside behavior changes. Avoid unrelated refactoring and dependencies. Run applicable local checks. Open a pull request linking the task and acceptance criteria, and state limitations and risks.

## Deliverables
- Focused source and test changes
- A PR with traceable issue/criteria links and test evidence
- `agents/engineering/output-template.md` result conforming to the shared role-result schema

## Validation rules
- Task has approved scope, completion criteria, and acceptance criteria.
- Tests exercise normal behavior, boundary cases, and relevant failures.
- Run documented project checks and report exact commands/results.
- Never alter branch protections, workflow permissions, or approval requirements to make a change pass.
- Stop and request clarification if implementation would exceed approved scope.

## Exit criteria
The task's acceptance criteria are covered, checks pass, the PR is linked and reviewable, and no known blocker is concealed. Human review/merge remains a separate decision.

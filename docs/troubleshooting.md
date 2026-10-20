# Troubleshooting

## Artifact validation fails

- Run `python3 scripts/factory.py validate --stage <stage>` and address each reported missing or empty artifact.
- Acceptance criteria must use stable `AC-###` IDs, and every criterion must appear in the backlog.
- Remove unresolved `TODO`, `TBD`, `FIXME`, or `{{...}}` markers from stage artifacts.
- Implementation evidence must map a `TASK-###` to an `AC-###`.

## Workflow refuses to advance

- Run `python3 scripts/factory.py status` to inspect the current stage.
- Advance one stage at a time; the command intentionally rejects skipped/backward transitions.
- Approval stages require `--approved-by`, and the corresponding artifacts are revalidated before the state advances.
- `init` refuses to replace existing state. Preserve `.factory/state.json`; do not remove it to bypass an approval.
- If a command fails, no stage transition is written. Fix the issue and retry; validation itself never edits artifacts.

## Tests or CI fail

- Re-run `python3 -m unittest discover -s tests -v`, `python3 -m unittest discover -s examples/sample-app -v`, and `python3 -m compileall -q scripts tests examples`.
- For formatter/linter errors, run `ruff check .` and `ruff format .`, then inspect the diff.
- In GitHub, inspect the failing `factory-ci` or `dependency-review` job log. Do not advance review/release based on a failed required check.
- A deliberately failing test should make `factory-ci` fail; revert the test-only change after verifying the check.

## Dependency or secret control unavailable

Dependency review is a PR workflow. Enable it in Actions and require the check in branch rules. Secret scanning/push protection availability varies by GitHub plan; configure it where offered. If unavailable, document the limitation and require an approved local scanning and human review process before merge. Never paste secrets into an issue, PR, log, or AI prompt.

## Handoff blocked or ambiguous

Mark the role result `blocked`, list the unanswered question and required decision, and return it to the issue owner. Do not silently infer product requirements or relax checks.

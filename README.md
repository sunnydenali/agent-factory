# Agentic AI Software Factory

A small, GitHub-native repository template for turning a submitted idea into approved requirements, an architecture, traceable implementation tasks, reviewed code, and release-ready documentation. It starts with human-operated, provider-neutral role handoffs and deterministic Python checks; it does not require API keys, hosted agents, or deployed services.

The factory tooling lives in `scripts/`, its own tests in `tests/`, and the illustrative downstream word-count application in `examples/sample-app/`. The example artifacts for `IDEA-001` are in `docs/`.

## Quick start

Requirements: Python 3.11+. The factory CLI and sample app use only the standard library. Optional development checks are pinned in `requirements-dev.txt`.

```sh
python3 -m pip install -r requirements-dev.txt
python3 -m unittest discover -s tests -v
python3 -m unittest discover -s examples/sample-app -v
python3 -m compileall -q scripts tests examples
ruff check .
ruff format --check .
```

Try the sample:

```sh
python3 examples/sample-app/wordcount.py path/to/file.txt
```

## Workflow

Use an issue from `.github/ISSUE_TEMPLATE/idea.md` to submit an idea. Preserve its stable `IDEA-###` ID in artifact names, task issues, branches, PRs, test evidence, and release notes. Roles are manual or AI-assisted handoffs, not autonomous services. Every role has its own instructions plus input/output templates under `agents/<role>/`.

Lifecycle and gates:

| State | Entry condition / exit |
| --- | --- |
| `idea_submitted` | Idea issue exists; initialize the local record. |
| `requirements_drafted` | Requirements, acceptance criteria (`AC-###`), and mapped backlog (`TASK-###`) validate. |
| `requirements_approved` | A human explicitly approves the drafted requirements. |
| `architecture_drafted` | Architecture, implementation plan, and ADR validate against approved requirements. |
| `architecture_approved` | A human approves architecture and task plan. |
| `implementation_started` | Implementation and evidence link tasks to criteria; CI checks apply to the PR. |
| `review_complete` | Review report explicitly says Approved and a human records the gate approval. Findings or failed checks block. |
| `release_prepared` | Changelog, release notes, and checklist validate. |
| `released` | Human explicitly approves publication after required checks. |

Initialize and advance exactly one state at a time:

```sh
python3 scripts/factory.py init --id IDEA-001
python3 scripts/factory.py validate --stage requirements_drafted
python3 scripts/factory.py advance --to requirements_drafted
python3 scripts/factory.py advance --to requirements_approved --approved-by "Human reviewer"
python3 scripts/factory.py validate --stage architecture_drafted
python3 scripts/factory.py advance --to architecture_drafted
python3 scripts/factory.py advance --to architecture_approved --approved-by "Human reviewer"
python3 scripts/factory.py validate --stage implementation_started
python3 scripts/factory.py advance --to implementation_started
python3 scripts/factory.py advance --to review_complete --approved-by "Independent reviewer"
python3 scripts/factory.py validate --stage release_prepared
python3 scripts/factory.py advance --to release_prepared
python3 scripts/factory.py advance --to released --approved-by "Release approver"
python3 scripts/factory.py status
```

`--approved-by` is an explicit local acknowledgment, not GitHub identity verification. Obtain approvals in the linked GitHub issue/PR and configure branch rules; retain the references in the artifacts. State is local under ignored `.factory/state.json`, is never initialized over an existing record, and must not be committed. Validation is read-only. A failed stage leaves the current stage unchanged; repair or retry that stage before advancing. Preserve approved artifacts and record superseding decisions rather than silently editing them.

The validator checks required artifacts, unresolved template markers, `AC-###` IDs, task mapping, review decision, and implementation traceability. It does not create GitHub issues, authenticate approvers, or verify claimed CI results. Create each task issue from the implementation plan and link issues/PRs manually. GitHub Actions, branch rules, and human review remain the enforcement points for remote work.

## GitHub setup

1. Create a repository from this template and set the default branch. Configure GitHub Actions permissions to read-only by default.
2. Add a ruleset requiring pull requests, at least one human approval, resolved conversations, and successful `factory-ci` and `dependency-review` checks. Prevent force pushes and branch deletion on the default branch.
3. Create the [suggested issue labels](docs/github-labels.md). Enable secret scanning and push protection where available; see [SECURITY.md](SECURITY.md) for limitations and alternatives.
4. Submit an idea using the issue template. Review and approve scope before architecture; approve architecture before implementation. Create task issues manually from `docs/backlog.md`.
5. Use a feature branch per bounded task. Open a PR with `.github/PULL_REQUEST_TEMPLATE.md`, link its issue and `AC-###`, and attach actual test/check evidence. Obtain independent review and human approval before merge.
6. Prepare release docs only after review. A human approves merge and publication; this repository does not publish releases automatically.

## Quality gates

`.github/workflows/ci.yml` compiles Python, runs factory and sample unit tests, checks formatting/linting, and emits a coverage report. It runs for pull requests and pushes to `main`. Deliberately breaking a test on a disposable branch makes the required `factory-ci` check fail; do not merge the failure. `.github/workflows/dependency-review.yml` checks PR dependency changes. No dedicated vulnerability or secret scan is run by the sample workflows; configure GitHub secret scanning/push protection where supported and disclose any unavailable control. Never represent an AI review as deterministic scanning.

## Provider-neutral role interface

Each `agents/<role>/instructions.md` declares inputs, responsibilities, outputs, validation, and exit criteria. Manual execution requires no key. Record role, stable artifact ID, execution status, output paths, validation, and errors in the format described by `schemas/role-result.schema.json`. An optional API adapter belongs on the roadmap; credentials must stay in an approved secret manager and the adapter must not change approval gates.

## Docs

- [Architecture](docs/architecture.md), [implementation plan](docs/implementation-plan.md), and [ADR](docs/adr/0001-minimal-stack.md)
- [Security and permissions](SECURITY.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Suggested GitHub labels](docs/github-labels.md)
- [Roadmap](docs/roadmap.md)
- [Contributing](CONTRIBUTING.md)

The sample review, implementation evidence, and release checklist are examples. They do not claim a GitHub PR, CI run, security scan, tag, or published release occurred.

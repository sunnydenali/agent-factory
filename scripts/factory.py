#!/usr/bin/env python3
"""Deterministic artifact and workflow-state checks for the Agent Factory."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

STAGES = (
    "idea_submitted",
    "requirements_drafted",
    "requirements_approved",
    "architecture_drafted",
    "architecture_approved",
    "implementation_started",
    "review_complete",
    "release_prepared",
    "released",
)

REQUIRED_ARTIFACTS = {
    "requirements_drafted": (
        "docs/requirements.md",
        "docs/acceptance-criteria.md",
        "docs/backlog.md",
    ),
    "architecture_drafted": (
        "docs/architecture.md",
        "docs/implementation-plan.md",
        "docs/adr/0001-minimal-stack.md",
    ),
    "implementation_started": (
        "docs/implementation-evidence.md",
        "examples/sample-app/wordcount.py",
        "examples/sample-app/test_wordcount.py",
    ),
    "review_complete": ("docs/reviews/sample-review.md",),
    "release_prepared": (
        "CHANGELOG.md",
        "docs/release-notes.md",
        "docs/release-checklist.md",
    ),
}

STATE_PATH = ".factory/state.json"


class FactoryError(Exception):
    """An expected workflow or artifact validation error."""


def validate(root: Path, stage: str) -> list[str]:
    """Return validation errors for the artifacts required at ``stage``."""
    errors = []
    contents = {}
    for relative_path in REQUIRED_ARTIFACTS.get(stage, ()):
        path = root / relative_path
        if not path.is_file():
            errors.append(f"Missing required artifact: {relative_path}")
            continue
        try:
            content = path.read_text(encoding="utf-8").strip()
        except (OSError, UnicodeError) as exc:
            errors.append(f"Cannot read required artifact {relative_path}: {exc}")
            continue
        contents[relative_path] = content
        if not content:
            errors.append(f"Required artifact is empty: {relative_path}")
        if re.search(r"\b(?:TODO|TBD|FIXME)\b|\{\{", content, re.IGNORECASE):
            errors.append(f"Unresolved template marker in: {relative_path}")

    if stage == "requirements_drafted":
        criteria = contents.get("docs/acceptance-criteria.md", "")
        backlog = contents.get("docs/backlog.md", "")
        criteria_ids = set(re.findall(r"\bAC-\d+\b", criteria))
        backlog_ids = set(re.findall(r"\bAC-\d+\b", backlog))
        if not criteria_ids:
            errors.append("Acceptance criteria must include stable AC-### identifiers")
        if criteria_ids - backlog_ids:
            errors.append(
                "Backlog does not map every acceptance criterion: "
                + ", ".join(sorted(criteria_ids - backlog_ids))
            )

    if stage == "implementation_started":
        evidence = contents.get("docs/implementation-evidence.md", "")
        if not re.search(r"\bTASK-\d+\b", evidence) or not re.search(r"\bAC-\d+\b", evidence):
            errors.append("Implementation evidence must link a TASK-### to an AC-###")

    if stage == "review_complete":
        review = contents.get("docs/reviews/sample-review.md", "")
        if review and not re.search(r"Decision:\s*Approved\b", review, re.IGNORECASE):
            errors.append("Review report must explicitly state 'Decision: Approved'")
    return errors


def load_state(root: Path) -> dict:
    path = root / STATE_PATH
    if not path.is_file():
        raise FactoryError(
            "Workflow state is not initialized; run: factory.py init --id <stable-id>"
        )
    try:
        state = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise FactoryError(f"Cannot read workflow state at {STATE_PATH}: {exc}") from exc
    except UnicodeError as exc:
        raise FactoryError(f"Workflow state at {STATE_PATH} is not valid UTF-8: {exc}") from exc
    if (
        not isinstance(state, dict)
        or state.get("stage") not in STAGES
        or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{2,63}", str(state.get("id", "")))
        or not isinstance(state.get("approvals"), list)
    ):
        raise FactoryError(f"Invalid workflow state in {STATE_PATH}")
    return state


def write_state(root: Path, state: dict) -> None:
    path = root / STATE_PATH
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(".tmp")
        temporary.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")
        temporary.replace(path)
    except OSError as exc:
        raise FactoryError(f"Cannot write workflow state at {STATE_PATH}: {exc}") from exc


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Factory repository root (default: current directory)",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    init_parser = commands.add_parser(
        "init", help="Initialize workflow state without overwriting existing state"
    )
    init_parser.add_argument("--id", required=True, help="Stable idea identifier")
    validate_parser = commands.add_parser(
        "validate", help="Validate artifacts for a workflow stage"
    )
    validate_parser.add_argument("--stage", choices=STAGES, required=True)
    commands.add_parser("status", help="Show the current workflow state")
    advance_parser = commands.add_parser(
        "advance", help="Advance exactly one stage after validating its prerequisites"
    )
    advance_parser.add_argument("--to", choices=STAGES, required=True)
    advance_parser.add_argument(
        "--approved-by", help="Human approver for approval and release gates"
    )

    args = parser.parse_args(argv)
    root = args.root.resolve()
    try:
        if args.command == "init":
            if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]{2,63}", args.id):
                raise FactoryError(
                    "ID must be 3-64 characters: letters, numbers, dot, underscore, or hyphen"
                )
            if (root / STATE_PATH).exists():
                raise FactoryError(
                    f"Workflow state already exists at {STATE_PATH}; refusing to overwrite it"
                )
            write_state(root, {"id": args.id, "stage": STAGES[0], "approvals": []})
            print(f"Initialized {args.id} at {STAGES[0]}")
        elif args.command == "validate":
            errors = validate(root, args.stage)
            if errors:
                print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
                return 1
            print(f"Artifacts valid for {args.stage}")
        elif args.command == "status":
            print(json.dumps(load_state(root), indent=2))
        else:
            state = load_state(root)
            target_index = STAGES.index(args.to)
            current_index = STAGES.index(state["stage"])
            if target_index <= current_index:
                if target_index == current_index:
                    print(f"Already at {args.to}")
                    return 0
                raise FactoryError(
                    f"Cannot move workflow backward from {state['stage']} to {args.to}"
                )
            if target_index != current_index + 1:
                raise FactoryError(
                    f"Cannot skip stages; next required stage is {STAGES[current_index + 1]}"
                )
            if args.to in {
                "requirements_approved",
                "architecture_approved",
                "review_complete",
                "released",
            }:
                if not args.approved_by or not args.approved_by.strip():
                    raise FactoryError(
                        f"Human approval required; provide --approved-by for {args.to}"
                    )
                state["approvals"].append(
                    {"stage": args.to, "approved_by": args.approved_by.strip()}
                )
            artifact_stage = {
                "requirements_approved": "requirements_drafted",
                "architecture_approved": "architecture_drafted",
                "released": "release_prepared",
            }.get(args.to, args.to)
            errors = validate(root, artifact_stage)
            if errors:
                raise FactoryError("; ".join(errors))
            state["stage"] = args.to
            write_state(root, state)
            print(f"Advanced {state['id']} to {args.to}")
    except FactoryError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

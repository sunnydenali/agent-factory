import json
import tempfile
import unittest
from pathlib import Path

from scripts.factory import STAGES, STATE_PATH, main, validate


class FactoryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def test_missing_requirements_are_reported(self):
        errors = validate(self.root, "requirements_drafted")
        missing = [error for error in errors if error.startswith("Missing required artifact:")]
        self.assertEqual(len(missing), 3)

    def test_backlog_must_map_all_acceptance_criteria(self):
        self.write("docs/requirements.md", "Users can count words.")
        self.write("docs/acceptance-criteria.md", "AC-001: count words\nAC-002: handle empty input")
        self.write("docs/backlog.md", "TASK-001 implements AC-001")
        self.assertIn("AC-002", " ".join(validate(self.root, "requirements_drafted")))

    def test_cannot_skip_approval_gate_or_overwrite_state(self):
        self.assertEqual(main(["--root", str(self.root), "init", "--id", "IDEA-1"]), 0)
        self.assertNotEqual(
            main(["--root", str(self.root), "advance", "--to", "architecture_drafted"]), 0
        )
        state = json.loads((self.root / STATE_PATH).read_text())
        self.assertEqual(state["stage"], STAGES[0])
        self.assertNotEqual(main(["--root", str(self.root), "init", "--id", "IDEA-2"]), 0)
        self.assertEqual(json.loads((self.root / STATE_PATH).read_text())["id"], "IDEA-1")

    def test_approval_requires_human_identity(self):
        self.write("docs/requirements.md", "Requirements")
        self.write("docs/acceptance-criteria.md", "AC-001: count")
        self.write("docs/backlog.md", "TASK-001: AC-001")
        self.assertEqual(main(["--root", str(self.root), "init", "--id", "IDEA-1"]), 0)
        self.assertEqual(
            main(["--root", str(self.root), "advance", "--to", "requirements_drafted"]), 0
        )
        self.assertNotEqual(
            main(["--root", str(self.root), "advance", "--to", "requirements_approved"]), 0
        )
        self.assertEqual(
            main(
                [
                    "--root",
                    str(self.root),
                    "advance",
                    "--to",
                    "requirements_approved",
                    "--approved-by",
                    "Human",
                ]
            ),
            0,
        )
        state = json.loads((self.root / STATE_PATH).read_text())
        self.assertEqual(state["approvals"][0]["approved_by"], "Human")

    def test_review_blocks_unapproved_decision(self):
        self.write("docs/reviews/sample-review.md", "Decision: Changes Required")
        self.assertTrue(
            any("Approved" in error for error in validate(self.root, "review_complete"))
        )

    def test_approval_revalidates_requirements_before_advancing(self):
        self.write("docs/requirements.md", "Requirements")
        self.write("docs/acceptance-criteria.md", "AC-001: count")
        self.write("docs/backlog.md", "TASK-001: AC-001")
        self.assertEqual(main(["--root", str(self.root), "init", "--id", "IDEA-1"]), 0)
        self.assertEqual(
            main(["--root", str(self.root), "advance", "--to", "requirements_drafted"]), 0
        )
        self.write("docs/acceptance-criteria.md", "TODO")
        self.assertNotEqual(
            main(
                [
                    "--root",
                    str(self.root),
                    "advance",
                    "--to",
                    "requirements_approved",
                    "--approved-by",
                    "Human",
                ]
            ),
            0,
        )
        state = json.loads((self.root / STATE_PATH).read_text())
        self.assertEqual(state["stage"], "requirements_drafted")

    def test_invalid_state_shape_is_reported(self):
        state_path = self.root / STATE_PATH
        state_path.parent.mkdir(parents=True)
        state_path.write_text("[]", encoding="utf-8")
        self.assertNotEqual(main(["--root", str(self.root), "status"]), 0)


if __name__ == "__main__":
    unittest.main()

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from wordcount import count_words

CLI = Path(__file__).with_name("wordcount.py")


class WordCountTests(unittest.TestCase):
    def test_cli_prints_word_count(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "words.txt"
            path.write_text("Hello, factory!", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(CLI), str(path)],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "2")

    def test_counts_words_and_ignores_punctuation(self):
        self.assertEqual(count_words("Hello, factory! It's ready."), 4)

    def test_empty_and_whitespace_input(self):
        self.assertEqual(count_words(" \n\t "), 0)

    def test_counts_unicode_words(self):
        self.assertEqual(count_words("café 東京"), 2)

    def test_missing_file_returns_actionable_error(self):
        result = subprocess.run(
            [sys.executable, str(CLI), "missing-input.txt"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cannot read input file", result.stderr)

    def test_invalid_utf8_returns_actionable_error(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.txt"
            path.write_bytes(b"\xff")
            result = subprocess.run(
                [sys.executable, str(CLI), str(path)],
                capture_output=True,
                text=True,
                check=False,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cannot read input file", result.stderr)


if __name__ == "__main__":
    unittest.main()

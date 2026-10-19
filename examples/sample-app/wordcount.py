"""Small standard-library word counter used to demonstrate the factory lifecycle."""

import re


def count_words(text: str) -> int:
    """Count Unicode word sequences; punctuation and whitespace are separators."""
    return len(re.findall(r"\b[\w']+\b", text, flags=re.UNICODE))


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Count words in a UTF-8 text file.")
    parser.add_argument("file", help="Path to the input text file")
    args = parser.parse_args()
    try:
        with open(args.file, encoding="utf-8") as source:
            print(count_words(source.read()))
    except (OSError, UnicodeError) as exc:
        parser.error(f"cannot read input file: {exc}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

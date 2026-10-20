# Architecture — IDEA-001

## Decision summary
Use a small Python 3.11+ command-line application with a pure `count_words(text)` function and a thin argument/file-I/O boundary. Python's standard `re`, `argparse`, and file APIs meet the sample's requirements without a runtime dependency or service.

## Components and contract
- `examples/sample-app/wordcount.py`: `count_words(str) -> int`; CLI accepts a single path, reads UTF-8, prints a count, and reports I/O/decoding errors through argparse.
- `examples/sample-app/test_wordcount.py`: unit coverage for punctuation, empty input, and Unicode. CLI failure behavior is exercised by the CLI's explicit exception path and can be extended in a downstream task.
- No persistent data model, network endpoint, credentials, or external API.

## Security, reliability, and operation
Input remains local and is never logged or transmitted. File and decoding errors are converted to concise non-zero CLI errors. The process uses the invoking user's filesystem permissions. No secrets or environment configuration are needed. CI executes in a least-privilege runner.

## Testing and quality strategy
Unit-test the pure counting contract and boundary cases. CI compiles Python, runs factory orchestration tests, runs sample tests, and reviews dependency changes. A downstream repository should add integration tests for its chosen CLI/deployment environment.

## Risks and trade-offs
Unicode regular-expression word boundaries provide a compact baseline, not linguistically precise segmentation for every language. Apostrophes are included; hyphens and punctuation split words. This is sufficient for the approved sample scope. A future language-specific tokenizer requires a new acceptance criterion and dependency review.

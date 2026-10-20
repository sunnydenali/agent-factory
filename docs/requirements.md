# Requirements — IDEA-001

## Problem and users
People working with local text files need a small offline command-line word counter. Users include writers, reviewers, and developers who need a quick count without uploading text to a service.

## Goals and outcomes
- Count words from a supplied UTF-8 file and print one integer.
- Handle empty input, punctuation, Unicode text, and read/decoding errors predictably.
- Run with the Python standard library and no network access.

## Functional requirements
- Accept one file path as a command-line argument.
- Treat Unicode word sequences as words; punctuation and whitespace separate words.
- Print zero for an empty or whitespace-only file.
- Report an actionable error and non-zero exit status when the file cannot be read or decoded.

## Non-functional requirements
- Python 3.11 or newer; standard-library-only runtime.
- Local processing only; do not transmit input contents or store credentials.
- Unit tests cover normal, boundary, Unicode, and failure behavior.

## Assumptions and constraints
- Input is a local UTF-8 text file.
- Apostrophes within a word are counted as part of that word.
- No locale-specific tokenization or language-specific stemming is required.

## Open questions
- No unresolved questions for the initial sample scope. Language-specific tokenization is explicitly deferred.

## Scope
In scope: one-file CLI word counting and clear input errors.

Out of scope: recursive directory scans, graphical UI, cloud upload, language detection, document formats other than plain text, and word-frequency reports.

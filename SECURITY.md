# Security and permissions

## Controls

- The CI workflows use `contents: read`; add permissions only when a reviewed workflow needs them.
- Keep the factory free of credentials. Optional provider integrations are intentionally not part of this MVP.
- Enable GitHub secret scanning and push protection in repository **Settings → Code security and analysis** when available. For plans without these features, require a documented human secret review before merge and use a local secret scanner approved by the repository owner.
- The dependency-review workflow checks dependency changes in pull requests. The factory currently has no third-party runtime dependencies.
- Require CI and human PR review through branch protection/rulesets. Require linear, traceable PRs and prohibit force pushes to the default branch.
- Treat issue text and generated artifacts as untrusted input. Review generated code and never execute commands copied from an issue or agent output without inspection.

## Repository setup

Set the default branch ruleset to require pull requests, at least one human approval, resolved conversations, and the `factory-ci` and `dependency-review` checks. Enable secret scanning/push protection where supported. Restrict workflow permissions to read-only by default and review any request for write tokens.

AI-assisted reviews do not replace tests, dependency checks, human review, or security scanning. Record scans only when actually run; report unavailable checks explicitly.

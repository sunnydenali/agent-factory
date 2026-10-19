# Roadmap

## Current MVP

Manual/provider-neutral role handoffs, Markdown artifacts and templates, read-only artifact validation, local sequential approval-gated state, sample app, and GitHub CI/dependency review.

## Optional next steps

- Add an API-backed role adapter behind a provider-neutral interface; keep manual mode functional, make credentials optional, and store them only in GitHub Secrets or another approved secret manager.
- Add authenticated GitHub issue/PR automation only after defining idempotency keys, minimum token permissions, rate-limit handling, and audit behavior.
- Add artifact schema validation and stronger cross-artifact task/criteria checks.
- Add a release workflow after documenting trusted tag provenance, required check verification, human approval, and rollback procedures.
- Add project-specific language toolchains and coverage thresholds only when downstream application needs justify them.

No roadmap item is currently implemented. Automation must preserve human approval, required CI, and protected workflow rules.

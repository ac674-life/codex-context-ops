---
name: context-release-check
description: Use when explicitly invoked for release readiness, pre-merge checks, final verification, known bug audit, or risk signoff.
---

# Context Release Check

Respond in the user's current language unless they explicitly request another language.

1. Inspect current changes or requested release scope.
2. Check `docs/bugs.md` for unresolved high-risk issues.
3. Use CodeGraph for high-risk impact questions.
4. Run the project's documented test, lint, or build commands when feasible.
5. Separate release blockers from non-blocking risks.

Final response must include blockers, non-blocking risks, tests/checks run, skipped checks and why, and release recommendation.

## Feature Index Check

Before release, check whether the feature index reflects the current changed modules. Flag stale `docs/feature-index.md` or `docs/modules/*.md` entries as release risks when they would mislead future Codex threads.

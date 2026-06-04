---
name: context-release-check
description: Use when explicitly invoked for release readiness, pre-merge checks, final verification, known bug audit, or risk signoff.
---

# Context Release Check

1. Inspect current changes or requested release scope.
2. Check `docs/bugs.md` for unresolved high-risk issues.
3. Use CodeGraph for high-risk impact questions.
4. Run the project's documented test, lint, or build commands when feasible.
5. Separate release blockers from non-blocking risks.

Final response must include blockers, non-blocking risks, tests/checks run, skipped checks and why, and release recommendation.

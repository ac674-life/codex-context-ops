---
name: context-safe-bugfix
description: Use when explicitly invoked for bug fixes, failing tests, regressions, runtime errors, flaky behavior, or recurring defects.
---

# Context-Safe Bugfix

Respond in the user's current language unless they explicitly request another language.

1. Reproduce the bug or identify the failing test.
2. Use CodeGraph for relevant symbols, call chains, and impact.
3. Read only files on the suspected path.
4. Add or update a regression test when feasible.
5. Make the smallest scoped fix.
6. Run targeted tests first; broaden tests when risk is high.
7. Update `docs/bugs.md` if the bug is recurring, subtle, or high-risk.

Final response must include symptom, root cause, fix summary, files changed, tests run, and residual risk.

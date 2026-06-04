---
name: context-safe-review
description: Use when explicitly invoked for code review, branch review, PR review, risk analysis, security review, maintainability review, or test gap analysis.
---

# Context-Safe Review

1. Inspect the changed files or requested scope.
2. Use CodeGraph for impact and call-chain questions.
3. Prioritize correctness, regressions, security, data loss, and missing tests.
4. Avoid broad unrelated refactors.
5. Report findings first, ordered by severity.

For each finding include severity, file and line, issue, why it matters, and suggested fix.

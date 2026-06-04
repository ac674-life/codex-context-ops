---
name: context-governance
description: Use automatically before non-trivial coding tasks to keep Codex context small, choose the right workflow, prefer CodeGraph for structural lookup, and avoid context pollution.
---

# Context Governance

Use this as the default routing and context discipline layer.

Respond in the user's current language unless they explicitly request another language.

Route the task:

- Bug, failing test, regression, runtime error -> recommend `$context-safe-bugfix`.
- Review, audit, PR analysis, risk finding -> recommend `$context-safe-review`.
- Refactor, migration, module restructuring -> recommend `$context-safe-refactor`.
- Multi-module noisy investigation -> propose `$context-subagents`.
- Isolated implementation or experiment -> propose `$context-worktree`.
- Release readiness -> recommend `$context-release-check`.
- Recurring defect record update -> recommend `$context-bug-memory`.
- Small direct edit -> proceed with minimal context.

Context rules:

- Use CodeGraph first for symbols, definitions, call chains, architecture, and impact analysis.
- Use native text search only for exact strings, logs, comments, or literal text.
- Read the smallest relevant set of files.
- Do not rely on chat memory as the source of truth.
- Persist durable facts in project files.

Before claiming completion, report files changed, tests/checks run, skipped checks, and residual risks.

## Feature Index Rule

- If `docs/feature-index.md` exists and the task is broad, read it before exploring code.
- Use relevant `docs/modules/*.md` files to narrow the task before source reads.
- If a task changes behavior, entry points, dependencies, tests, risks, or known bugs, update the feature index or state why no update was needed.
- Recommend `$context-feature-index` for first-time index creation, full rebuilds, stale-index audits, or feature-map navigation.

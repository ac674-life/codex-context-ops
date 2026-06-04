---
name: context-bug-memory
description: Use when explicitly invoked to record, update, audit, or summarize recurring bugs and regression notes in docs/bugs.md.
---

# Context Bug Memory

Respond in the user's current language unless they explicitly request another language.

Use `docs/bugs.md` as durable project memory for recurring, subtle, or high-risk bugs.

Each entry should include:

- Symptom
- Root cause
- Affected files
- Regression test
- Fix
- Status
- Notes

Rules:

- Do not store secrets.
- Prefer concrete file paths and test names over vague prose.
- Mark status clearly: open, fixed, mitigated, deferred, or needs reproduction.
- If the same issue recurs, update the existing entry instead of creating duplicates.

Summarize entries created or updated, and list unresolved follow-up actions.

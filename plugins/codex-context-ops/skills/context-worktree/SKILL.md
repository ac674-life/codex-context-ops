---
name: context-worktree
description: Use when explicitly invoked to isolate implementation, experiments, risky fixes, or parallel tasks in a Codex or Git worktree.
---

# Context Worktree

Use worktrees when implementation should not disturb the current local checkout.

Before work, confirm target branch or starting point, whether the task is experimental or intended for merge, and expected verification commands.

During work:

- Keep the worktree scoped to one task.
- Avoid unrelated edits.
- Track generated or ignored files that may not move during handoff.

Final response must include worktree or branch used, files changed, tests/checks run, diff summary, merge or handoff recommendation, and rollback notes.

---
name: context-init
description: Use only when explicitly invoked to initialize a project with Codex context governance files, bug memory docs, and repo-local context-safe skills.
---

# Context Init

Initialize the current project with the context-safe Codex workflow.

Choose the initialization language from the user's request:

- Chinese request or explicit Chinese preference -> `zh-CN`
- English request or explicit English preference -> `en`
- If unclear, ask which language to use.

Run the bundled script from the plugin root:

```bash
python scripts/init_context_ops.py --target . --lang zh-CN
```

Supported language values are `en`, `zh-CN`, and `auto`. Use `auto` only when the environment locale is reliable.

If the current directory is not the intended project root, ask the user for the target path first.

Creates or updates:

- `AGENTS.md`
- `docs/bugs.md`
- `docs/architecture.md`
- `.agents/skills/context-governance/SKILL.md`
- `.agents/skills/context-safe-bugfix/SKILL.md`
- `.agents/skills/context-safe-review/SKILL.md`
- `.agents/skills/context-safe-refactor/SKILL.md`
- `.agents/skills/context-subagents/SKILL.md`
- `.agents/skills/context-worktree/SKILL.md`
- `.agents/skills/context-release-check/SKILL.md`
- `.agents/skills/context-bug-memory/SKILL.md`

Do not overwrite existing files unless the user explicitly asks for `--force`.

After init, tell the user which skills are automatic candidates and which must be explicitly invoked.

Respond in the user's chosen language.

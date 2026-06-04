# Codex Context Ops

[English](README.md) | [简体中文](README.zh-CN.md)

Codex Context Ops is a bilingual Codex plugin marketplace for context-safe AI coding workflows.

It helps large projects reduce context pollution, repeated bugs, and noisy long-running conversations through reusable Codex skills.

## Skills

| Skill | Purpose | Trigger |
|---|---|---|
| `$context-init` | Initialize project governance files and local skills | Explicit |
| `$context-governance` | Route non-trivial tasks and keep context small | Automatic candidate |
| `$context-safe-bugfix` | Reproduce, fix, test, and record bugs | Explicit |
| `$context-safe-review` | Review correctness, regressions, security, and tests | Explicit |
| `$context-safe-refactor` | Plan bounded refactors and migrations | Explicit |
| `$context-subagents` | Isolate noisy multi-module investigations | Explicit |
| `$context-worktree` | Guide isolated implementation | Explicit |
| `$context-release-check` | Perform release-readiness checks | Explicit |
| `$context-bug-memory` | Maintain durable bug records | Explicit |

## Install

Recommended remote install:

```powershell
codex plugin marketplace add ac674-life/codex-context-ops
codex plugin add codex-context-ops@context-tools
```

This installs from GitHub and does not depend on a local project folder.

Local development install:

```powershell
git clone https://github.com/ac674-life/codex-context-ops.git
cd codex-context-ops
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

If the Codex CLI cannot run, open Codex app, go to Plugins, add the cloned repository as a marketplace, then install `codex-context-ops`.

Restart Codex or open a new thread after installation.

## Initialize A Project

English:

```text
Use $context-init to initialize this project in English.
```

Simplified Chinese:

```text
使用 $context-init，以简体中文初始化这个项目。
```

The initializer supports:

```powershell
python scripts/init_context_ops.py --target . --lang en
python scripts/init_context_ops.py --target . --lang zh-CN
python scripts/init_context_ops.py --target . --lang auto
```

It creates or updates:

```text
AGENTS.md
docs/bugs.md
docs/architecture.md
.agents/skills/context-governance
.agents/skills/context-safe-bugfix
.agents/skills/context-safe-review
.agents/skills/context-safe-refactor
.agents/skills/context-subagents
.agents/skills/context-worktree
.agents/skills/context-release-check
.agents/skills/context-bug-memory
```

Existing files are not overwritten unless `--force` is explicitly requested.

## Examples

```text
Use $context-safe-bugfix to fix this bug.
Use $context-safe-review to review the current changes.
Use $context-safe-refactor to plan this migration.
Use $context-subagents to investigate this multi-module issue.
Use $context-worktree for isolated implementation.
Use $context-release-check before release.
Use $context-bug-memory to update recurring bug records.
```

## Design Principles

- Keep the main Codex context small.
- Use CodeGraph for structural questions.
- Use text search only for literal strings.
- Store durable rules in `AGENTS.md`.
- Store recurring bug history in `docs/bugs.md`.
- Use subagents and worktrees only when needed.
- Verify before claiming completion.

## Repository Layout

```text
marketplace.json
install.ps1
plugins/
  codex-context-ops/
    .codex-plugin/plugin.json
    scripts/init_context_ops.py
    skills/
```

## License

MIT

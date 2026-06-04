# Codex Context Ops

Codex Context Ops is a local Codex plugin marketplace for context-safe AI coding workflows.

It helps large projects avoid context pollution, repeated bugs, and noisy long-running conversations by installing a small set of reusable Codex skills:

- `$context-init` initializes project-level context governance.
- `$context-governance` routes non-trivial tasks and keeps context small.
- `$context-safe-bugfix` handles bug fixes with reproduction, CodeGraph analysis, regression tests, and bug records.
- `$context-safe-review` reviews changes for correctness, regressions, security, and test gaps.
- `$context-safe-refactor` plans and executes refactors with bounded scope and impact analysis.
- `$context-subagents` delegates noisy multi-module investigations to isolated subagents.
- `$context-worktree` guides isolated worktree-based implementation.
- `$context-release-check` performs pre-release or pre-merge risk checks.
- `$context-bug-memory` maintains durable recurring bug notes in `docs/bugs.md`.

## Repository Layout

```text
marketplace.json
install.ps1
plugins/
  codex-context-ops/
    .codex-plugin/plugin.json
    scripts/
      init_context_ops.py
    skills/
      context-init/
      context-governance/
      context-safe-bugfix/
      context-safe-review/
      context-safe-refactor/
      context-subagents/
      context-worktree/
      context-release-check/
      context-bug-memory/
```

## Install

Clone this repository:

```powershell
git clone https://github.com/YOUR_NAME/codex-context-ops.git
cd codex-context-ops
```

Run the installer:

```powershell
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

The installer registers this folder as a local Codex marketplace and installs the plugin:

```powershell
codex plugin marketplace add <repo-folder>
codex plugin add codex-context-ops@context-tools
```

If the Codex CLI cannot run on the machine, open Codex app, go to Plugins, add this repository folder as a marketplace, then install `codex-context-ops`.

After installation, restart Codex or open a new thread.

## Publish This Repository

Create an empty GitHub repository named `codex-context-ops`, then run:

```powershell
git init
git add .
git commit -m "Initial release"
git branch -M main
git remote add origin https://github.com/YOUR_NAME/codex-context-ops.git
git push -u origin main
```

## First Use In A Project

Ask Codex:

```text
使用 $context-init 初始化这个项目。
```

This creates or updates:

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

Existing files are not overwritten unless you explicitly ask Codex to use `--force`.

## Daily Usage

Bug fix:

```text
使用 $context-safe-bugfix 修复这个 Bug。先复现或定位失败测试，再做最小修复。
```

Code review:

```text
使用 $context-safe-review review 当前改动，重点检查正确性、回归风险和测试缺口。
```

Refactor or migration:

```text
使用 $context-safe-refactor 准备这个重构。先用 CodeGraph 分析影响范围，不要直接改代码。
```

Large multi-module investigation:

```text
使用 $context-subagents 隔离分析这个复杂问题。
```

Isolated implementation:

```text
使用 $context-worktree 在隔离环境实现这个修复。
```

Release check:

```text
使用 $context-release-check 做发布前检查。
```

Bug memory update:

```text
使用 $context-bug-memory 更新历史 Bug 记录。
```

## Design Principles

- Keep the main Codex context small.
- Use CodeGraph for structural questions.
- Use text search only for literal strings.
- Store durable project rules in `AGENTS.md`.
- Store recurring bug history in `docs/bugs.md`.
- Use subagents and worktrees only when explicitly needed.
- Verify before claiming work is complete.

## Updating The Plugin

After editing the plugin, update the version in:

```text
plugins/codex-context-ops/.codex-plugin/plugin.json
```

Then reinstall:

```powershell
codex plugin add codex-context-ops@context-tools
```

Open a new Codex thread after reinstalling so the new skills are loaded.

## License

MIT

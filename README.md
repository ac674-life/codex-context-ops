# Codex Context Ops

[English](README.md) | [简体中文](README.zh-CN.md)

Codex Context Ops is a bilingual Codex plugin marketplace for context-safe AI coding workflows.

It helps large projects reduce context pollution, repeated bugs, and noisy long-running conversations through reusable Codex skills.

Agency agent installation is powered by [jnMetaCode/agency-agents-zh](https://github.com/jnMetaCode/agency-agents-zh).

## Skills

| Skill | Purpose | Trigger |
|---|---|---|
| `$context-init` | Initialize project governance files and local skills | Explicit |
| `$context-governance` | Route non-trivial tasks and keep context small | Automatic candidate |
| `$context-agency-agents-install` | Install a focused agency-agents-zh subset into `.codex/agents` | Explicit |
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
.agents/skills/context-agency-agents-install
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
Use $context-agency-agents-install to install suitable agency agents for this project.
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

## Feature Index Workflow

`codex-context-ops` now includes `$context-feature-index` for projects that are too large to rediscover from scratch in every thread.

What `$context-init` creates:

- `docs/feature-index.md`: the project navigation entry.
- `docs/modules/README.md`: the template and home for module-level maps.
- `.agents/skills/context-feature-index`: the manual skill for creating, rebuilding, auditing, or navigating the feature map.

How to use it:

```text
Use $codex-context-ops:context-feature-index to build a feature index for this project.
Group the project by user-facing features or domain modules, then create docs/modules/*.md files.
Do not modify business code while building the index.
```

During later coding tasks, Codex should read `docs/feature-index.md` first when the task is broad, select the relevant `docs/modules/*.md`, and then use CodeGraph for focused structural analysis. After code changes, Codex should update the feature index when behavior, entry points, dependencies, tests, risks, or known bugs change.

## Agency Agents Install Flow

`$context-agency-agents-install` installs selected agents from [jnMetaCode/agency-agents-zh](https://github.com/jnMetaCode/agency-agents-zh) into the current project:

```text
.codex/agents/*.toml
```

Recommended prompts:

```text
Use $context-agency-agents-install to install suitable agents for this project.
Use $context-agency-agents-install with the web profile.
Use $context-agency-agents-install with the unity profile.
```

Profiles:

| Profile | Best for |
|---|---|
| `auto` | Let Codex infer a conservative project profile |
| `core` | Unknown or general coding projects |
| `web` | React, Vue, Next.js, Vite, frontend, full-stack |
| `backend` | APIs, services, databases, DevOps |
| `ai-data` | AI, ML, data pipelines, analytics |
| `unity` | Unity, games, XR, shaders, technical art |
| `product-design` | Product planning, UX, UI |
| `marketing-cn` | Xiaohongshu, Douyin, WeChat, Bilibili, China ecommerce |
| `review` | Code review, testing, security, release quality |

The skill intentionally installs a small project-specific subset instead of all agency agents. Restart Codex or open a new thread after installing project agents.

## Update Local Plugin

After this repository publishes a new version, update the local Codex plugin cache with:

```powershell
codex plugin marketplace upgrade context-tools
codex plugin add codex-context-ops@context-tools
```

Verify the installed version:

```powershell
codex plugin list
```

You should see `codex-context-ops@context-tools` as `installed, enabled` with the latest version.

If `codex.exe` from WindowsApps fails with `Access is denied`, use the Codex App bundled CLI instead. First locate it:

```powershell
Get-ChildItem -Path "$env:LOCALAPPDATA\OpenAI\Codex\bin" -Recurse -Filter codex.exe |
  Select-Object -First 1 -ExpandProperty FullName
```

Then run the same commands with the full path:

```powershell
C:\Users\<you>\AppData\Local\OpenAI\Codex\bin\<version>\codex.exe plugin marketplace upgrade context-tools
C:\Users\<you>\AppData\Local\OpenAI\Codex\bin\<version>\codex.exe plugin add codex-context-ops@context-tools
C:\Users\<you>\AppData\Local\OpenAI\Codex\bin\<version>\codex.exe plugin list
```

After updating, restart Codex App or open a new thread in the target project. Existing threads may keep the old skill list in their context snapshot.

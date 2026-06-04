# Codex Context Ops

[English](README.md) | [简体中文](README.zh-CN.md)

Codex Context Ops 是一个支持中英文的 Codex 插件市场，用于建立上下文安全的 AI 编程工作流。

它通过一组可复用的 Codex 技能，帮助大型项目减少上下文污染、重复 Bug 和长会话噪声。

## 技能列表

| 技能 | 用途 | 触发方式 |
|---|---|---|
| `$context-init` | 初始化项目治理文件和本地技能 | 主动调用 |
| `$context-governance` | 路由非简单任务并控制上下文 | 自动候选 |
| `$context-safe-bugfix` | 复现、修复、测试并记录 Bug | 主动调用 |
| `$context-safe-review` | 审查正确性、回归、安全和测试问题 | 主动调用 |
| `$context-safe-refactor` | 规划范围明确的重构和迁移 | 主动调用 |
| `$context-subagents` | 隔离复杂的跨模块调查 | 主动调用 |
| `$context-worktree` | 指导隔离实现 | 主动调用 |
| `$context-release-check` | 执行发布准备检查 | 主动调用 |
| `$context-bug-memory` | 维护持久 Bug 记录 | 主动调用 |

## 安装

```powershell
git clone https://github.com/ac674-life/codex-context-ops.git
cd codex-context-ops
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

如果 Codex CLI 无法运行，请打开 Codex app，进入 Plugins，将克隆后的仓库目录添加为 marketplace，然后安装 `codex-context-ops`。

安装后请重启 Codex 或开启新线程。

## 初始化项目

使用中文初始化：

```text
使用 $context-init，以简体中文初始化这个项目。
```

使用英文初始化：

```text
Use $context-init to initialize this project in English.
```

初始化脚本支持：

```powershell
python scripts/init_context_ops.py --target . --lang zh-CN
python scripts/init_context_ops.py --target . --lang en
python scripts/init_context_ops.py --target . --lang auto
```

初始化后会创建或更新：

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

除非明确使用 `--force`，否则不会覆盖已有文件。

## 使用示例

```text
使用 $context-safe-bugfix 修复这个 Bug。
使用 $context-safe-review 审查当前改动。
使用 $context-safe-refactor 规划这个迁移。
使用 $context-subagents 调查这个跨模块问题。
使用 $context-worktree 进行隔离实现。
使用 $context-release-check 做发布前检查。
使用 $context-bug-memory 更新重复 Bug 记录。
```

## 设计原则

- 保持 Codex 主上下文精简。
- 结构问题优先使用 CodeGraph。
- 只有文本问题才使用文本搜索。
- 持久规则写入 `AGENTS.md`。
- 重复 Bug 历史写入 `docs/bugs.md`。
- 仅在需要时使用 subagents 和 worktree。
- 在声称完成前进行验证。

## 仓库结构

```text
marketplace.json
install.ps1
plugins/
  codex-context-ops/
    .codex-plugin/plugin.json
    scripts/init_context_ops.py
    skills/
```

## 许可证

MIT

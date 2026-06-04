#!/usr/bin/env python3
"""Initialize Codex Context Ops files in a project."""

from __future__ import annotations

import argparse
import locale
import shutil
from pathlib import Path


START = "<!-- CODEX_CONTEXT_OPS_START -->"
END = "<!-- CODEX_CONTEXT_OPS_END -->"


AGENTS_BLOCK = f"""{START}
## Codex Context Ops

Before any non-trivial coding task, Codex should use `$context-governance`.

Goals:
- Keep context small and task-focused.
- Avoid context pollution and context rot.
- Prefer structural lookup over broad file reading.
- Persist durable project facts in files, not chat memory.
- Maintain a feature index so future threads can locate relevant modules quickly.

Default rules:
- Use CodeGraph first for symbols, definitions, call chains, architecture, and impact analysis.
- Use native text search only for exact strings, logs, comments, or literal text.
- Do not read the whole repository unless explicitly requested.
- Read `docs/feature-index.md` before broad exploration when it exists.
- Use `docs/modules/*.md` to select the smallest relevant code area before reading source files.
- Record recurring, subtle, or high-risk bugs in `docs/bugs.md`.
- Keep architecture notes in `docs/architecture.md` when they become durable project facts.
- Update `docs/feature-index.md` and related module docs after behavior, entry point, dependency, test, risk, or known-bug changes.
- Before claiming completion, report changed files, tests/checks run, skipped checks, residual risks, and whether feature-index docs were updated.

Automatic candidate:
- `$context-governance` for non-trivial tasks and workflow routing.

Manual skills:
- `$context-feature-index` for creating, rebuilding, auditing, or navigating feature/module maps.
- `$context-safe-bugfix` for bugs, failing tests, regressions, runtime errors, and recurring defects.
- `$context-safe-review` for code review, PR review, risk analysis, and test gap analysis.
- `$context-safe-refactor` for refactors, migrations, large edits, and module restructuring.
- `$context-subagents` for broad, noisy, multi-module investigation.
- `$context-worktree` for isolated implementation or experimental work.
- `$context-release-check` for release readiness, final verification, and pre-merge risk checks.
- `$context-bug-memory` for recording or auditing recurring bugs in `docs/bugs.md`.

Manual capabilities:
- Use `$context-feature-index` explicitly for first-time index creation, full rebuilds, or stale-index audits.
- Use subagents only when explicitly requested or after proposing them for broad multi-module work.
- Use worktrees only when explicitly requested or after proposing them for isolated implementation.
{END}
"""


BUGS_MD = """# Known Bugs And Regression Notes

Use this file for recurring, subtle, or high-risk defects. Do not store secrets.

## Template

### BUG-001: Short title

- Symptom:
- Root cause:
- Affected files:
- Regression test:
- Fix:
- Status:
- Notes:
"""


ARCHITECTURE_MD = """# Architecture Notes

Use this file for durable architecture facts that Codex should recover across threads.

## System Overview

- TBD

## Important Boundaries

- TBD

## Durable Decisions

- TBD

## Risky Areas

- TBD
"""


FEATURE_INDEX_MD = """# Feature Index

Use this file as the project navigation map. Keep it concise so a new Codex thread can find the right module without reading the whole repository.

## How To Use

1. Start here before broad code exploration.
2. Pick the relevant module document under `docs/modules/`.
3. Use CodeGraph to inspect symbols, call chains, and impact inside that focused area.
4. Read source files only after the likely module is identified.

## Feature Map

| Feature / Area | Module Doc | Main Files | Entry Points | Tests | Notes |
|---|---|---|---|---|---|
| TBD | `docs/modules/README.md` | TBD | TBD | TBD | Fill this during the first feature-index pass. |

## Maintenance Rules

Update this file and the relevant module document when any of these change:

- user-facing behavior
- feature/module ownership
- entry points
- main files
- data flow
- dependencies
- tests
- known risks
- known bugs

If a new feature or module appears, create a new `docs/modules/<module>.md`.
"""


MODULES_README_MD = """# Module Maps

Create one file per major feature or domain module. Prefer names that users and future Codex threads can understand, such as `authentication.md`, `checkout.md`, or `training-flow.md`.

## Module Document Template

### Purpose

- TBD

### User-Facing Features

- TBD

### Main Files

- TBD

### Entry Points

- TBD

### Data Flow

- TBD

### Dependencies

- TBD

### Tests

- TBD

### Known Risks

- TBD

### Related Known Bugs

- TBD

### Maintenance Rules

- Update this document when behavior, entry points, dependencies, tests, risks, or known bugs change.
"""


AGENTS_BLOCK_ZH = f"""{START}
## Codex 上下文治理

在执行任何非简单编码任务前，Codex 应先使用 `$context-governance`。

目标：
- 保持上下文精简并聚焦当前任务。
- 避免上下文污染和上下文退化。
- 优先使用结构化检索，不要大范围读取文件。
- 将持久项目事实保存到文件中，不要只依赖聊天记忆。
- 维护功能索引，让新线程能快速定位相关模块。

默认规则：
- 符号、定义、调用链、架构和影响分析优先使用 CodeGraph。
- 只有搜索精确字符串、日志、注释或文本时才使用原生文本搜索。
- 除非用户明确要求，否则不要读取整个代码库。
- 如果存在 `docs/feature-index.md`，在大范围探索前先读取它。
- 使用 `docs/modules/*.md` 先缩小相关代码区域，再读取源码。
- 将重复、隐蔽或高风险 Bug 记录到 `docs/bugs.md`。
- 将持久架构信息记录到 `docs/architecture.md`。
- 当行为、入口点、依赖、测试、风险或已知 Bug 发生变化时，更新 `docs/feature-index.md` 和相关模块文档。
- 在声明完成前，报告修改文件、测试或检查结果、跳过的检查、剩余风险，以及是否更新了功能索引文档。

自动候选技能：
- `$context-governance`：用于非简单任务和工作流路由。

需要主动调用的技能：
- `$context-feature-index`：创建、重建、审计或导航功能/模块地图。
- `$context-safe-bugfix`：Bug、测试失败、回归问题、运行时错误和重复缺陷。
- `$context-safe-review`：代码审查、PR 审查、风险分析和测试缺口分析。
- `$context-safe-refactor`：重构、迁移、大范围修改和模块调整。
- `$context-subagents`：复杂、嘈杂、跨模块的调查任务。
- `$context-worktree`：隔离实现或实验性工作。
- `$context-release-check`：发布准备、最终验证和合并前风险检查。
- `$context-bug-memory`：记录或审计 `docs/bugs.md` 中的重复 Bug。

需要主动调用的能力：
- 首次建立索引、完整重建索引或审计过期索引时，显式使用 `$context-feature-index`。
- 仅在用户明确要求，或 Codex 对跨模块任务提出建议并获得同意后，使用 subagents。
- 仅在用户明确要求，或 Codex 对隔离实现提出建议并获得同意后，使用 worktree。
{END}
"""


BUGS_MD_ZH = """# 已知 Bug 与回归记录

本文件用于记录重复、隐蔽或高风险缺陷。不要记录密钥或其他敏感信息。

## 模板

### BUG-001：简短标题

- 现象：
- 根因：
- 影响文件：
- 回归测试：
- 修复方案：
- 状态：
- 备注：
"""


ARCHITECTURE_MD_ZH = """# 架构记录

本文件用于记录需要跨线程恢复的持久架构信息。

## 系统概览

- 待补充

## 重要边界

- 待补充

## 持久决策

- 待补充

## 高风险区域

- 待补充
"""


FEATURE_INDEX_MD_ZH = """# 功能索引

本文件是项目导航地图。保持简洁，让新的 Codex 线程不用读取整个仓库，也能快速找到相关模块。

## 使用方式

1. 大范围探索代码前先从这里开始。
2. 选择 `docs/modules/` 下相关的模块文档。
3. 在缩小后的范围内使用 CodeGraph 查看符号、调用链和影响面。
4. 确认可能模块后，再读取源码文件。

## 功能地图

| 功能 / 区域 | 模块文档 | 主要文件 | 入口点 | 测试 | 备注 |
|---|---|---|---|---|---|
| 待补充 | `docs/modules/README.md` | 待补充 | 待补充 | 待补充 | 首次执行功能索引时填写。 |

## 维护规则

以下内容变化时，更新本文件和相关模块文档：

- 用户可见行为
- 功能/模块归属
- 入口点
- 主要文件
- 数据流
- 依赖
- 测试
- 已知风险
- 已知 Bug

如果出现新功能或新模块，创建新的 `docs/modules/<module>.md`。
"""


MODULES_README_MD_ZH = """# 模块地图

每个主要功能或领域模块创建一个文件。文件名优先使用用户和未来 Codex 线程都能理解的名称，例如 `authentication.md`、`checkout.md` 或 `training-flow.md`。

## 模块文档模板

### 目的

- 待补充

### 用户可见功能

- 待补充

### 主要文件

- 待补充

### 入口点

- 待补充

### 数据流

- 待补充

### 依赖

- 待补充

### 测试

- 待补充

### 已知风险

- 待补充

### 相关已知 Bug

- 待补充

### 维护规则

- 当行为、入口点、依赖、测试、风险或已知 Bug 变化时，更新本文档。
"""


PROJECT_SKILLS = [
    "context-governance",
    "context-feature-index",
    "context-safe-bugfix",
    "context-safe-review",
    "context-safe-refactor",
    "context-subagents",
    "context-worktree",
    "context-release-check",
    "context-bug-memory",
]


def write_file(path: Path, text: str, force: bool, actions: list[str]) -> None:
    existed = path.exists()
    if existed and not force:
        actions.append(f"skipped existing {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    actions.append(("updated " if existed else "created ") + str(path))


def update_agents(path: Path, block: str, force: bool, actions: list[str]) -> None:
    if not path.exists():
        write_file(path, "# AGENTS.md\n\n" + block, force=True, actions=actions)
        return

    current = path.read_text(encoding="utf-8")
    if START in current and END in current:
        if not force:
            actions.append(f"skipped existing context ops block in {path}")
            return
        before = current.split(START, 1)[0].rstrip()
        after = current.split(END, 1)[1].lstrip()
        path.write_text(f"{before}\n\n{block}\n{after}".rstrip() + "\n", encoding="utf-8")
        actions.append(f"updated context ops block in {path}")
        return

    path.write_text(current.rstrip() + "\n\n" + block + "\n", encoding="utf-8")
    actions.append(f"appended context ops block to {path}")


def copy_skill(plugin_root: Path, target: Path, skill_name: str, force: bool, actions: list[str]) -> None:
    src = plugin_root / "skills" / skill_name
    dst = target / ".agents" / "skills" / skill_name
    if dst.exists() and not force:
        actions.append(f"skipped existing {dst}")
        return
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    actions.append(("updated " if force else "created ") + str(dst))


def resolve_language(value: str) -> str:
    if value != "auto":
        return value
    locale_name = (locale.getlocale()[0] or "").lower()
    return "zh-CN" if locale_name.startswith("zh") else "en"


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize Codex Context Ops in a project.")
    parser.add_argument("--target", default=".", help="Project directory to initialize.")
    parser.add_argument(
        "--lang",
        choices=["auto", "en", "zh-CN"],
        default="auto",
        help="Language for generated AGENTS.md and docs.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite generated docs, skills, and managed AGENTS block.")
    args = parser.parse_args()

    plugin_root = Path(__file__).resolve().parents[1]
    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)

    language = resolve_language(args.lang)
    agents_block = AGENTS_BLOCK_ZH if language == "zh-CN" else AGENTS_BLOCK
    bugs_md = BUGS_MD_ZH if language == "zh-CN" else BUGS_MD
    architecture_md = ARCHITECTURE_MD_ZH if language == "zh-CN" else ARCHITECTURE_MD
    feature_index_md = FEATURE_INDEX_MD_ZH if language == "zh-CN" else FEATURE_INDEX_MD
    modules_readme_md = MODULES_README_MD_ZH if language == "zh-CN" else MODULES_README_MD

    actions: list[str] = []
    update_agents(target / "AGENTS.md", agents_block, args.force, actions)
    write_file(target / "docs" / "bugs.md", bugs_md, args.force, actions)
    write_file(target / "docs" / "architecture.md", architecture_md, args.force, actions)
    write_file(target / "docs" / "feature-index.md", feature_index_md, args.force, actions)
    write_file(target / "docs" / "modules" / "README.md", modules_readme_md, args.force, actions)

    for skill_name in PROJECT_SKILLS:
        copy_skill(plugin_root, target, skill_name, args.force, actions)

    print(f"Codex Context Ops initialization complete. Language: {language}")
    for action in actions:
        print(f"- {action}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

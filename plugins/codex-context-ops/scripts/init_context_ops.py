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

Default rules:
- Use CodeGraph first for symbols, definitions, call chains, architecture, and impact analysis.
- Use native text search only for exact strings, logs, comments, or literal text.
- Do not read the whole repository unless explicitly requested.
- Record recurring, subtle, or high-risk bugs in `docs/bugs.md`.
- Keep architecture notes in `docs/architecture.md` when they become durable project facts.
- Before claiming completion, report changed files, tests/checks run, skipped checks, and residual risks.

Automatic candidate:
- `$context-governance` for non-trivial tasks and workflow routing.

Manual skills:
- `$context-safe-bugfix` for bugs, failing tests, regressions, runtime errors, and recurring defects.
- `$context-safe-review` for code review, PR review, risk analysis, and test gap analysis.
- `$context-safe-refactor` for refactors, migrations, large edits, and module restructuring.
- `$context-subagents` for broad, noisy, multi-module investigation.
- `$context-worktree` for isolated implementation or experimental work.
- `$context-release-check` for release readiness, final verification, and pre-merge risk checks.
- `$context-bug-memory` for recording or auditing recurring bugs in `docs/bugs.md`.

Manual capabilities:
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


AGENTS_BLOCK_ZH = f"""{START}
## Codex 上下文治理

在执行任何非简单编码任务前，Codex 应先使用 `$context-governance`。

目标：
- 保持上下文精简并聚焦当前任务。
- 避免上下文污染和上下文退化。
- 优先使用结构化检索，不要大范围读取文件。
- 将持久项目事实保存到文件中，不要只依赖聊天记忆。

默认规则：
- 符号、定义、调用链、架构和影响分析优先使用 CodeGraph。
- 只有搜索精确字符串、日志、注释或文本时才使用原生文本搜索。
- 除非用户明确要求，否则不要读取整个代码库。
- 将重复、隐蔽或高风险 Bug 记录到 `docs/bugs.md`。
- 将持久架构信息记录到 `docs/architecture.md`。
- 在声称完成前，报告修改文件、测试或检查结果、跳过的检查以及剩余风险。

自动候选技能：
- `$context-governance`：用于非简单任务和工作流路由。

需要主动调用的技能：
- `$context-safe-bugfix`：Bug、测试失败、回归问题、运行时错误和重复缺陷。
- `$context-safe-review`：代码审查、PR 审查、风险分析和测试缺口分析。
- `$context-safe-refactor`：重构、迁移、大范围修改和模块调整。
- `$context-subagents`：复杂、嘈杂、跨模块的调查任务。
- `$context-worktree`：隔离实现或实验性工作。
- `$context-release-check`：发布准备、最终验证和合并前风险检查。
- `$context-bug-memory`：记录或审计 `docs/bugs.md` 中的重复 Bug。

需要主动调用的能力：
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


PROJECT_SKILLS = [
    "context-governance",
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

    actions: list[str] = []
    update_agents(target / "AGENTS.md", agents_block, args.force, actions)
    write_file(target / "docs" / "bugs.md", bugs_md, args.force, actions)
    write_file(target / "docs" / "architecture.md", architecture_md, args.force, actions)

    for skill_name in PROJECT_SKILLS:
        copy_skill(plugin_root, target, skill_name, args.force, actions)

    print(f"Codex Context Ops initialization complete. Language: {language}")
    for action in actions:
        print(f"- {action}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

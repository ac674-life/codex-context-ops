#!/usr/bin/env python3
"""Initialize Codex Context Ops files in a project."""

from __future__ import annotations

import argparse
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


def update_agents(path: Path, force: bool, actions: list[str]) -> None:
    if not path.exists():
        write_file(path, "# AGENTS.md\n\n" + AGENTS_BLOCK, force=True, actions=actions)
        return

    current = path.read_text(encoding="utf-8")
    if START in current and END in current:
        if not force:
            actions.append(f"skipped existing context ops block in {path}")
            return
        before = current.split(START, 1)[0].rstrip()
        after = current.split(END, 1)[1].lstrip()
        path.write_text(f"{before}\n\n{AGENTS_BLOCK}\n{after}".rstrip() + "\n", encoding="utf-8")
        actions.append(f"updated context ops block in {path}")
        return

    path.write_text(current.rstrip() + "\n\n" + AGENTS_BLOCK + "\n", encoding="utf-8")
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize Codex Context Ops in a project.")
    parser.add_argument("--target", default=".", help="Project directory to initialize.")
    parser.add_argument("--force", action="store_true", help="Overwrite generated docs, skills, and managed AGENTS block.")
    args = parser.parse_args()

    plugin_root = Path(__file__).resolve().parents[1]
    target = Path(args.target).resolve()
    target.mkdir(parents=True, exist_ok=True)

    actions: list[str] = []
    update_agents(target / "AGENTS.md", args.force, actions)
    write_file(target / "docs" / "bugs.md", BUGS_MD, args.force, actions)
    write_file(target / "docs" / "architecture.md", ARCHITECTURE_MD, args.force, actions)

    for skill_name in PROJECT_SKILLS:
        copy_skill(plugin_root, target, skill_name, args.force, actions)

    print("Codex Context Ops initialization complete.")
    for action in actions:
        print(f"- {action}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

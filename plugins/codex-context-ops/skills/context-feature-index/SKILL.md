---
name: context-feature-index
description: Use when explicitly invoked to create, update, audit, or navigate feature index docs that map user-facing features to modules, files, entry points, dependencies, tests, risks, and known bugs.
---

# Context Feature Index

Respond in the user's current language unless they explicitly request another language.

## Purpose

Maintain a human-readable feature map so Codex can locate relevant code without scanning the whole repository.

## Create Index

1. Use CodeGraph first to identify major modules, entry points, callers, and dependencies.
2. Group by user-facing features or domain concepts, not mechanically by folders.
3. Create or update `docs/feature-index.md` as the navigation entry.
4. Create or update one document per major module under `docs/modules/<module>.md`.
5. Keep docs concise, concrete, and understandable for both the user and Codex.
6. Do not modify business code while creating or auditing the index unless explicitly asked.

## Module Document Shape

Each `docs/modules/<module>.md` should include:

- Purpose
- User-facing features
- Main files
- Entry points
- Data flow
- Dependencies
- Tests
- Known risks
- Related known bugs
- Maintenance rules

## Update Index

After code changes, update `docs/feature-index.md` and related module docs when any of these change:

- user-facing behavior
- feature/module ownership
- entry points
- main files
- data flow
- dependencies
- tests
- known risks
- known bugs

If a new feature or module is introduced, create a new module doc.

## Navigate With Index

When starting a task:

1. Read `docs/feature-index.md` if it exists.
2. Select the relevant module docs.
3. Use CodeGraph for focused structural analysis.
4. Read only the related code first.

## Audit Mode

When asked to audit the index:

1. Compare the index against current code structure using CodeGraph.
2. Report stale entries, missing modules, wrong entry points, and outdated tests.
3. Ask before rewriting large portions of the index.

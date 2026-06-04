---
name: context-safe-refactor
description: Use when explicitly invoked for refactors, migrations, architecture changes, large edits, module restructuring, or behavior-preserving cleanup.
---

# Context-Safe Refactor

Respond in the user's current language unless they explicitly request another language.

1. Define the intended behavior-preserving boundary.
2. Use CodeGraph to identify callers, callees, and impact.
3. Split work into small phases.
4. Avoid unrelated cleanup.
5. Preserve public interfaces unless explicitly asked.
6. Run targeted tests after each meaningful phase.

Before editing, state intended scope, files likely affected, compatibility risks, and verification plan.

## Feature Index Maintenance

For refactors, migrations, or module restructuring, treat `docs/feature-index.md` and related `docs/modules/*.md` files as part of the change. Update ownership, main files, entry points, data flow, dependencies, tests, and risks before completion.

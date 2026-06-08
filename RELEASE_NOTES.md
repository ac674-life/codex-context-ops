# Release Notes

## 0.2.0

- Adds English and Simplified Chinese initialization.
- Adds `--lang en`, `--lang zh-CN`, and `--lang auto`.
- Adds English and Chinese README navigation.
- Makes the default governance workflow respond in the user's language.
- Documents remote GitHub marketplace installation.

## 0.1.0

- Initial local Codex marketplace.
- Adds `codex-context-ops` plugin.
- Adds project initializer and context-safe workflow skills.
- Adds one-click PowerShell installer.

## 0.3.0

- Added `$context-feature-index` for creating, rebuilding, auditing, and navigating feature/module maps.
- `$context-init` now creates `docs/feature-index.md` and `docs/modules/README.md`.
- Context governance, bugfix, review, refactor, and release-check workflows now maintain feature-index docs when code changes affect behavior, entry points, dependencies, tests, risks, or known bugs.
- Updated bilingual documentation for large-project feature indexing.

## 0.4.0

- Added `$context-agency-agents-install` for installing focused `jnMetaCode/agency-agents-zh` Codex agents into project-level `.codex/agents`.
- Added a PowerShell installer script with project profiles: `auto`, `core`, `web`, `backend`, `ai-data`, `unity`, `product-design`, `marketing-cn`, and `review`.
- Updated project initialization so the agency-agent installer skill is copied into `.agents/skills`.

## Documentation

- Added README instructions for updating the local Codex plugin cache from the GitHub marketplace, including the Windows bundled CLI fallback when WindowsApps `codex.exe` is not executable.

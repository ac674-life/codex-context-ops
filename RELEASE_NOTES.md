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

## Documentation

- Added README instructions for updating the local Codex plugin cache from the GitHub marketplace, including the Windows bundled CLI fallback when WindowsApps `codex.exe` is not executable.

---
name: context-agency-agents-install
description: Use when the user wants to install, select, update, or plan jnMetaCode/agency-agents-zh agents for a Codex project, especially choosing a small project-specific subset of Codex .toml agents instead of installing every role.
---

# Context Agency Agents Install

Respond in the user's current language unless they explicitly request another language.

## Purpose

Install a focused subset of `jnMetaCode/agency-agents-zh` into the current Codex project as `.codex/agents/*.toml`.

Do not install all agents by default. Choose a small set that fits the project so Codex stays easy to steer.

## Default Flow

1. Identify the target project root.
2. If the user names specific agents, install only those agents by passing `-Agents`.
3. Otherwise, pick one profile:
   - `core`: general coding projects.
   - `web`: frontend or full-stack web projects.
   - `backend`: API, database, service, or infrastructure projects.
   - `ai-data`: AI, ML, data pipeline, analytics, or data quality projects.
   - `unity`: Unity, game, XR, shader, or technical art projects.
   - `product-design`: product, UX, UI, and planning projects.
   - `marketing-cn`: Chinese market content, ecommerce, social media, or growth projects.
   - `review`: code review, testing, security, and release quality.
   - `auto`: infer a conservative profile from project files.
4. Use the bundled installer script when available:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File <skill-dir>\scripts\install_agency_agents.ps1 -Target <project-root> -Profile <profile>
```

5. The script prints the agents selected for installation and asks for confirmation before copying files. Proceed only when the user confirms.
6. Report installed agents and the target `.codex/agents` path.
7. Tell the user to restart Codex or open a new thread in that project.

## Select Agents by Name

Use `-ListAgents` to show the available agent names from `jnMetaCode/agency-agents-zh` after conversion:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File <skill-dir>\scripts\install_agency_agents.ps1 -ListAgents
```

Install a hand-picked set by name with `-Agents`:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File <skill-dir>\scripts\install_agency_agents.ps1 -Target <project-root> -Agents engineering-code-reviewer,testing-api-tester
```

If both `-Agents` and `-Profile` are provided, `-Agents` wins and the profile is ignored.

Use `-Yes` only when the user has already approved the exact list or when running in automation:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File <skill-dir>\scripts\install_agency_agents.ps1 -Target <project-root> -Profile web -Yes
```

## Profile Guidance

Use `core` for unknown projects:

- `engineering-codebase-onboarding-engineer`
- `engineering-software-architect`
- `engineering-code-reviewer`
- `engineering-minimal-change-engineer`
- `testing-test-results-analyzer`
- `engineering-technical-writer`

Use `web` for React, Vue, Next.js, Vite, frontend, full-stack, CMS:

- core agents
- `engineering-frontend-developer`
- `engineering-backend-architect`
- `engineering-database-optimizer`
- `testing-api-tester`
- `testing-accessibility-auditor`
- `design-ui-designer`

Use `backend` for services, APIs, databases, DevOps:

- core agents
- `engineering-backend-architect`
- `engineering-database-optimizer`
- `engineering-devops-automator`
- `engineering-sre`
- `testing-api-tester`
- `engineering-security-engineer`

Use `ai-data` for AI, ML, data processing:

- core agents
- `engineering-ai-engineer`
- `engineering-data-engineer`
- `engineering-ai-data-remediation-engineer`
- `specialized-model-qa`
- `testing-evidence-collector`

Use `unity` for Unity/game/XR:

- core agents
- `unity-architect`
- `unity-editor-tool-developer`
- `unity-shader-graph-artist`
- `game-designer`
- `technical-artist`
- `testing-reality-checker`

Use `product-design` for product planning and design:

- `product-manager`
- `product-feedback-synthesizer`
- `product-sprint-prioritizer`
- `design-ux-researcher`
- `design-ux-architect`
- `design-ui-designer`
- `project-management-project-shepherd`

Use `marketing-cn` for Chinese market operations:

- `marketing-xiaohongshu-operator`
- `marketing-douyin-strategist`
- `marketing-wechat-official-account`
- `marketing-weixin-channels-strategist`
- `marketing-bilibili-strategist`
- `marketing-china-ecommerce-operator`
- `marketing-private-domain-operator`

Use `review` for quality gates:

- `engineering-code-reviewer`
- `engineering-security-engineer`
- `testing-api-tester`
- `testing-performance-benchmarker`
- `testing-accessibility-auditor`
- `testing-test-results-analyzer`
- `compliance-auditor`

## Safety Rules

- Install into the target project only: `<project-root>/.codex/agents`.
- Show the exact install list and ask for confirmation before installing unless the user explicitly requested non-interactive mode.
- Do not overwrite existing agent files unless the user asks for force/refresh.
- Do not modify business code.
- Keep the installed set small; usually 6 to 12 agents is enough.
- If the user asks for all agents, warn that it may make selection noisy, then proceed only if they confirm.

## Useful User Prompts

```text
Use $context-agency-agents-install to install suitable agents for this project.
```

```text
Use $context-agency-agents-install with the unity profile for this project.
```

```text
Use $context-agency-agents-install to refresh the web profile agents in this project.
```

```text
Use $context-agency-agents-install to list available agents, then install engineering-code-reviewer and testing-api-tester.
```

---
name: context-subagents
description: Use when explicitly invoked for large, noisy, multi-module, or parallel investigation tasks that should isolate exploration context into subagents.
---

# Context Subagents

Respond in the user's current language unless they explicitly request another language.

Use subagents to keep noisy exploration out of the main thread.

Dispatch by independent concern, for example:

- Agent A: call chains, architecture boundaries, and CodeGraph exploration.
- Agent B: tests, reproduction paths, and historical bug records.
- Agent C: implementation risks, compatibility risks, and rollout concerns.

Each subagent should return only concise summary, evidence, file paths, risks, and recommended next step.

Do not return raw logs, broad notes, or unrelated exploration.

Wait for subagents to complete, then synthesize one plan with conflicts, open questions, and recommended execution order.

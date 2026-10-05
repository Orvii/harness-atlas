# Codex CLI

- **repo:** openai/codex
- **version pin:** `rust-v0.160.0` — gh api repos/openai/codex/releases/latest → https://github.com/openai/codex/releases/tag/rust-v0.160.0 (published 2026-10-01)
- **docs home:** https://developers.openai.com/codex (redirects to https://learn.chatgpt.com/docs; per-page markdown at <url>.md)

## What it promises

Codex CLI is a coding agent from OpenAI that runs locally on your computer (repo README). It promises to let you inspect code, make changes, run commands, and automate repeatable work without leaving your terminal, staying in control of model, reasoning effort, and permissions.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | Enabled by default in current Codex releases; /agent inspects and switches between running threads; custom agents definable with own model and instructions. | [src](https://learn.chatgpt.com/docs/agent-configuration/subagents.md) |
| workflow_orchestration | ✅ yes | config-reference lists primitives spawn_agent, send_input, resume_agent, wait_agent, close_agent (features.multi_agent, stable, on by default); concurrent-thread caps configurable. | [src](https://learn.chatgpt.com/docs/agent-configuration/subagents.md) |
| mcp | ✅ yes | Client only: STDIO + Streamable HTTP, OAuth login, tool allow/deny lists via codex mcp add/list/login; the codex mcp-server binary was removed (https://learn.chatgpt.com/docs/mcp-server.md). | [src](https://learn.chatgpt.com/docs/extend/mcp.md) |
| hooks_lifecycle | ✅ yes | Events: PreToolUse, PermissionRequest, PostToolUse, PreCompact, PostCompact, UserPromptSubmit, SubagentStart/Stop, Stop, SessionStart/SessionEnd, Interrupt; command hooks can run async in background. | [src](https://learn.chatgpt.com/docs/hooks.md) |
| skills | ✅ yes | Progressive disclosure; invoked as $skill-name or /skills; read from repository (.agents/skills), user, admin, and system locations; skills can ship inside plugins. | [src](https://learn.chatgpt.com/docs/build-skills.md) |
| memory_persistence | ✅ yes | Local Codex memories are off by default; local memory store under Codex home; enable via [features] memories = true. | [src](https://learn.chatgpt.com/docs/customization/memories.md) |
| sandboxing | ✅ yes | Sandbox modes read-only \| workspace-write \| danger-full-access plus approval policies; hooks expose current permission_mode (default, acceptEdits, plan, dontAsk, bypassPermissions). | [src](https://learn.chatgpt.com/docs/permission-modes.md) |
| plan_mode | ✅ yes | /plan switches to plan mode and optionally sends a prompt; plan_mode_reasoning_effort config; plan is also a permission_mode value in hooks. | [src](https://learn.chatgpt.com/docs/developer-commands.md) |
| background_tasks | ✅ yes | /ps and /stop manage background terminals; background_terminal_max_timeout config (default 300000 ms) controls background terminal polling; async hook handlers run in background. | [src](https://learn.chatgpt.com/docs/developer-commands.md) |
| ide_integration | ✅ yes | Also Cursor, Windsurf, VS Code Insiders; the IDE extension does not support plugins. | [src](https://learn.chatgpt.com/docs/codex/ide.md) |
| model_agnostic | ✅ yes | Custom model_providers.<id> with base_url; --oss flag with oss_provider for local models; docs cover Amazon Bedrock and LLM gateways. | [src](https://learn.chatgpt.com/docs/config-file/config-reference.md) |
| plugins | ✅ yes | Codex CLI has a /plugins browser to install from a configured marketplace; IDE extension doesn't support plugins. | [src](https://learn.chatgpt.com/docs/plugins.md) |
| session_resume | ✅ yes | Via `codex resume`; hooks SessionStart matcher includes resume. | [src](https://learn.chatgpt.com/docs/codex/cli.md) |
| cost_controls | ✅ yes | /status shows session token usage and remaining context; /usage shows account token activity and rate-limit resets; rollout_budget token-limit feature exists but is experimental and off by default. | [src](https://learn.chatgpt.com/docs/developer-commands.md) |

## Notable

Far beyond the "local coding agent" pitch: current releases ship subagents on by default, lifecycle hooks, skills, a plugin browser, local memories, and plan/goal modes — yet OpenAI removed the codex mcp-server binary, so Codex consumes MCP but no longer acts as an MCP server.

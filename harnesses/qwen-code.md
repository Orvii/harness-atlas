# Qwen Code

- **repo:** https://github.com/QwenLM/qwen-code
- **version pin:** `v0.24.7` — GitHub releases list via gh api repos/QwenLM/qwen-code/releases shows latest stable tag v0.24.7 (2026-09-29) — https://github.com/QwenLM/qwen-code/releases/tag/v0.24.7 (note: releases/latest returns SDK sub-package tag sdk-typescript-v0.1.17); npm @qwen-code/qwen-code latest = 0.24.7 via https://registry.npmjs.org/@qwen-code/qwen-code/latest
- **docs home:** https://qwenlm.github.io/qwen-code-docs/

## What it promises

"The open-source AI coding agent for your terminal, editor, desktop, browser, and chat." It promises an agentic coding tool that lives in your terminal and turns ideas into code faster, spanning CLI, IDE, desktop, browser, and chat surfaces.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | Named subagents defined in Markdown+YAML; forking via subagent_type: "fork"; /agents manage; can continue finished agents with send_message. | [src](https://raw.githubusercontent.com/QwenLM/qwen-code/v0.24.7/docs/users/features/sub-agents.md) |
| workflow_orchestration | ✅ yes | Experimental Agent Team runtime via /coordinate (shared task list, teammate messaging); also workflow scripts gated by tools.workflowsEnabled (/workflows lists runs), Agent Board cross-agent tasks, Arena multi-model competition, Herdr. | [src](https://raw.githubusercontent.com/QwenLM/qwen-code/v0.24.7/docs/users/features/multi-agent-coordination.md) |
| mcp | ✅ yes | Client role; stdio, SSE, HTTP transports; servers manageable via /mcp and extensions. No MCP server mode found in docs. | [src](https://raw.githubusercontent.com/QwenLM/qwen-code/v0.24.7/docs/users/features/mcp.md) |
| hooks_lifecycle | ✅ yes | Events include PreToolUse, PostToolUse, SessionStart, SessionEnd; configured in settings.json under hooks with matcher + executor; /hooks command manages them. | [src](https://raw.githubusercontent.com/QwenLM/qwen-code/v0.24.7/docs/users/features/hooks.md) |
| skills | ✅ yes | Model-invoked; personal ~/.qwen/skills/, project .qwen/skills/, bundled, extension-provided; auto-skill generation plus /curator maintenance; Agent Skills spec compatible. | [src](https://raw.githubusercontent.com/QwenLM/qwen-code/v0.24.7/docs/users/features/skills.md) |
| memory_persistence | ✅ yes | QWEN.md/AGENTS.md instruction files plus auto-memory written by Qwen under ~/.qwen/projects/<project>/memory/ (Markdown files, managed with /dream, /forget). | [src](https://raw.githubusercontent.com/QwenLM/qwen-code/v0.24.7/docs/users/features/memory.md) |
| sandboxing | ✅ yes | tools.executionSandbox backends bwrap/Landlock plus Docker/Podman/Seatbelt whole-CLI modes; filesystem workspace-write/read-only and network closed/open policies; five approval modes incl. classifier-based Auto. | [src](https://raw.githubusercontent.com/QwenLM/qwen-code/v0.24.7/docs/users/features/sandbox.md) |
| plan_mode | ✅ yes | Distinct 'plan' approval mode (Shift+Tab cycle or /plan enter/exit), read-only, no edits or shell commands; proposes plan then user approves by switching modes. | [src](https://raw.githubusercontent.com/QwenLM/qwen-code/v0.24.7/docs/users/features/approval-mode.md) |
| background_tasks | ✅ yes | Also /tasks lists background tasks; /loop cron scheduled prompts (session-scoped); DashScope /batch-api async batch jobs; headless mode with --continue/--resume. | [src](https://raw.githubusercontent.com/QwenLM/qwen-code/v0.24.7/docs/users/features/sub-agents.md) |
| ide_integration | ✅ yes | VS Code extension (Beta), JetBrains via Agent Client Protocol, Zed integration; ACP session support with conversation history and context usage in-IDE. | [src](https://raw.githubusercontent.com/QwenLM/qwen-code/v0.24.7/docs/users/integration-vscode.md) |
| model_agnostic | ✅ yes | Built-in auth types openai, anthropic, gemini, vertex-ai plus custom provider ids via providerProtocol; /model picker; Alibaba ModelStudio; OAuth models hard-coded. | [src](https://raw.githubusercontent.com/QwenLM/qwen-code/v0.24.7/docs/users/configuration/model-providers.md) |
| plugins | ✅ yes | qwen extensions CLI + /extensions manager with marketplace Discover tab; installs Gemini CLI Extensions Gallery, Claude Code Marketplace, and portable Agent Plugins v1 packages. | [src](https://raw.githubusercontent.com/QwenLM/qwen-code/v0.24.7/docs/users/extension/introduction.md) |
| session_resume | ✅ yes | Interactive /resume (alias /continue); CLI --continue and --resume <sessionId>; restored sessions re-add compatible background agents via list_agents. | [src](https://raw.githubusercontent.com/QwenLM/qwen-code/v0.24.7/docs/users/features/headless.md) |
| cost_controls | ✅ yes | /stats shows cached token % and savings; /context detail breaks down resident prefix cost (tools, MCP, context files, skills); token caching automatic for API-key users. No hard spend limits documented. | [src](https://raw.githubusercontent.com/QwenLM/qwen-code/v0.24.7/docs/users/features/token-caching.md) |

## Notable

Ships built-in `claude-code` and `codex` subagent executors that delegate tasks to separately installed Claude Code (ACP) and Codex CLIs using their own models/auth, and it installs extensions directly from the Claude Code and Gemini CLI marketplaces.

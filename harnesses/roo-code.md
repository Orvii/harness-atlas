# Roo Code

- **repo:** RooCodeInc/Roo-Code
- **version pin:** `v3.54.0` — gh api repos/RooCodeInc/Roo-Code/releases/latest → https://github.com/RooCodeInc/Roo-Code/releases/tag/v3.54.0 (published 2026-05-15)
- **docs home:** https://roocodeinc.github.io/Roo-Code/

## What it promises

Roo Code promises "Your AI-Powered Dev Team, Right in Your Editor" — a whole team of AI agents inside VS Code that generate code from natural language, adapt with Code/Architect/Ask/Debug and custom modes, refactor and debug existing code, write documentation, answer codebase questions, automate repetitive tasks, and plug into external tools via MCP.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | Built-in Orchestrator mode delegates via new_task tool; child task runs in isolated context, parent pauses and resumes with the child's summary. Subtask creation/completion auto-approvable. | [src](https://roocodeinc.github.io/Roo-Code/features/boomerang-tasks) |
| workflow_orchestration | ◐ partial | Parent→child subtask chains with summary handoff only (sequential, no scripts/DAGs/swarms/YAML workflows). Worktrees allow parallel tasks in separate windows; message queueing sequences input. | [src](https://roocodeinc.github.io/Roo-Code/basic-usage/using-modes) |
| mcp | ✅ yes | MCP client with stdio/SSE/streamable-HTTP transports, global mcp_settings.json + project .roo/mcp.json, per-tool auto-approve, marketplace install. No evidence Roo itself acts as an MCP server. | [src](https://roocodeinc.github.io/Roo-Code/features/mcp/using-mcp-in-roo) |
| hooks_lifecycle | ? unknown | No lifecycle-hook feature (pre/post tool, session start/stop) found in any docs page or in the repo source (no hook files/config keys). Nearest extension points are MCP tools, custom modes, and experimental custom tools; nothing documented either way. | [src](https://roocodeinc.github.io/Roo-Code/) |
| skills | ✅ yes | SKILL.md with progressive disclosure; ~/.roo/skills and .roo/skills (also cross-agent ~/.agents/skills), mode targeting, bundled scripts/templates, project overrides global. | [src](https://roocodeinc.github.io/Roo-Code/features/skills) |
| memory_persistence | ◐ partial | No memory-bank/long-term memory feature. Persistence comes from shadow-git checkpoints, resumable task history (conversations stored and reopened), and file-based rules (.roorules / AGENTS.md loaded each session). | [src](https://roocodeinc.github.io/Roo-Code/features/checkpoints) |
| sandboxing | ◐ partial | Permission modes exist: per-action auto-approve tiles (read/edit/commands/MCP/browser/mode-switch), command whitelisting, CLI --require-approval. No OS-level sandbox — rooignore docs state '.rooignore ... does not create a system-level sandbox.' | [src](https://roocodeinc.github.io/Roo-Code/features/auto-approving-actions) |
| plan_mode | ◐ partial | Architect mode is a dedicated planning persona restricted to markdown-only edits. No formal plan-then-approve gate; the user approves implicitly by switching to Code/Debug mode. | [src](https://roocodeinc.github.io/Roo-Code/basic-usage/using-modes) |
| background_tasks | ◐ partial | Long-running terminal commands keep running, later checked via read_command_output; message queueing and the headless CLI (--print/--oneshot) are async-ish. No managed background-task queue for agent tasks. | [src](https://roocodeinc.github.io/Roo-Code/advanced-usage/available-tools/execute-command) |
| ide_integration | ✅ yes | VS Code Marketplace + Open VSX; works in Cursor, VSCodium, Windsurf. No JetBrains plugin. CLI also ships (apps/cli, npm-free shell installer) for terminal use. | [src](https://roocodeinc.github.io/Roo-Code/getting-started/installing) |
| model_agnostic | ✅ yes | Docs list ~28 providers (Anthropic, OpenAI, Gemini, Bedrock, Vertex, OpenRouter, xAI, Mistral, DeepSeek, Z.ai, Ollama, LM Studio, OpenAI-compatible, etc.); per-mode sticky model selection; API configuration profiles. | [src](https://roocodeinc.github.io/Roo-Code/providers/) |
| plugins | ◐ partial | Third-party distribution via marketplace (MCP servers + custom modes) and experimental defineCustomTool TS/JS tool API. No formal plugin/extension API with lifecycle or packaging spec beyond this. | [src](https://roocodeinc.github.io/Roo-Code/features/marketplace) |
| session_resume | ✅ yes | Task history persists conversations and tasks can be reopened/resumed (resumeTask+isTaskInHistory also in the extension API); CLI supports session/task IDs (--create-with-session-id, taskId in stdin stream mode). | [src](https://roocodeinc.github.io/Roo-Code/features/api-configuration-profiles) |
| cost_controls | ✅ yes | Per-request input/output token counts and estimated cost shown in chat (incl. reasoning tokens); 'Max Requests' cap for auto-approved actions forces re-approval; per-profile rate limits; supports free local models. | [src](https://roocodeinc.github.io/Roo-Code/advanced-usage/rate-limits-costs) |

## Notable

The project is discontinued: the README states the extension "was shut down on May 15th" (2026) — the same date as the final v3.54.0 release — and redirects users to the community fork ZooCode or to Cline.

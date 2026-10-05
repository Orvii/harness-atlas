# Gemini CLI

- **repo:** google-gemini/gemini-cli
- **version pin:** `v0.62.0` — gh api repos/google-gemini/gemini-cli/releases/latest -> tag v0.62.0, https://github.com/google-gemini/gemini-cli/releases/tag/v0.62.0 (published 2026-09-29); cross-checked npm @google/gemini-cli@0.62.0 via https://registry.npmjs.org/@google/gemini-cli/latest
- **docs home:** https://geminicli.com/docs/

## What it promises

An open-source AI agent that brings Gemini models directly into your terminal - "giving you the most direct path from your prompt to our model" - with built-in tools (Google Search grounding, file ops, shell, web fetch) and MCP extensibility. Promises a free tier of 60 requests/min and 1,000 requests/day with a personal Google account, plus Gemini 3 models with a 1M-token context window.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | Built-in codebase_investigator plus custom, extension-bundled, and remote (A2A) agents; automatic delegation, @name forcing, /agents list\|enable\|disable; each runs in its own context loop to save main-context tokens. | [src](https://geminicli.com/docs/core/subagents) |
| workflow_orchestration | ◐ partial | Multi-agent delegation primitives exist (local subagents, A2A remote agents, extension-bundled agents, headless scripting + an experimental a2a-server package), but no DAG/team/swarm orchestration layer. | [src](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/core/remote-agents.md) |
| mcp | ✅ yes | MCP client over Stdio, SSE, and Streamable HTTP with tool and resource discovery; extensions can bundle MCP servers. No documented MCP-server mode for Gemini CLI itself. | [src](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/tools/mcp-server.md) |
| hooks_lifecycle | ✅ yes | 11 events including SessionStart, SessionEnd, BeforeAgent/AfterAgent, BeforeTool/AfterTool, BeforeModel/AfterModel; hooks can block tools, rewrite args, and inject context. | [src](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/hooks/index.md) |
| skills | ✅ yes | Implements the agentskills.io open standard; SKILL.md directories discovered from built-in, extension, user, and workspace tiers; activate_skill tool with user consent, plus /skills command. | [src](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/skills.md) |
| memory_persistence | ✅ yes | Hierarchical GEMINI.md (global, workspace/parent, just-in-time) with @file.md imports (memport); experimental Auto Memory mines past session transcripts into reviewable memory patches and skill drafts. | [src](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/gemini-md.md) |
| sandboxing | ✅ yes | Docker/Podman/macOS seatbelt containers via -s flag, GEMINI_SANDBOX env, or settings.json; backed by approval modes (default/auto-edit/plan/YOLO) and a policy engine for tool permissions. | [src](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/sandbox.md) |
| plan_mode | ✅ yes | Enter via --approval-mode=plan, /plan [goal], Shift+Tab cycle, or natural language; agent researches read-only, agrees strategy with ask_user, writes a Markdown plan for approval before executing. | [src](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/plan-mode.md) |
| background_tasks | ✅ yes | run_shell_command can background processes and returns Background PIDs, with a BackgroundTaskDisplay UI (confirmed by repo paths packages/cli/src/ui/components/BackgroundTaskDisplay.tsx and evals/background_processes.eval.ts); no generic async agent-task queue documented. | [src](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/tools/shell.md) |
| ide_integration | ✅ yes | VS Code companion (open files, cursor, selection context, native diffing, command palette) plus ACP mode (--acp / --experimental-acp) used for JetBrains and Zed via the ACP Agent Registry. | [src](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/ide-integration/index.md) |
| model_agnostic | ✗ no | Generation is Gemini-only: /model lists just gemini-3-pro/flash-preview and gemini-2.5-pro/flash across Google account, Gemini API key, or Vertex AI auth. The one local-model feature (Gemma) is Google's own and used only for routing decisions; no OpenAI/Anthropic/other providers documented. | [src](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/core/gemma-setup.md) |
| plugins | ✅ yes | Install from GitHub URLs or local paths; manage via /extensions and gemini extensions commands; official extension gallery (geminicli.com/extensions/browse) with publishing docs for third parties. | [src](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/extensions/index.md) |
| session_resume | ✅ yes | gemini --resume/-r [latest\|index] and interactive session browser; sessions auto-saved per project under ~/.gemini/tmp. Also /rewind (chat and/or code revert) and optional checkpointing with /restore. | [src](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/cli/session-management.md) |
| cost_controls | ✅ yes | /stats session\|model\|tools reports tokens, duration, and quota; OpenTelemetry telemetry exports usage metrics; documented per-auth-method quota tiers (1,000-2,000 requests/day etc.). No hard spend-cap/limit setting documented. | [src](https://raw.githubusercontent.com/google-gemini/gemini-cli/main/docs/reference/commands.md) |

## Notable

The official docs banner and Google Developers Blog announce that Gemini CLI was replaced by Antigravity CLI on June 18, 2026 for free, Pro, and Ultra users, yet the repo keeps shipping weekly releases (v0.62.0, Sep 29, 2026) for enterprise and API-key users - a live-but-transitioning project.

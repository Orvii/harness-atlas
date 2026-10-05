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

## Architecture

Qwen Code is a TypeScript monorepo on Node.js >=22, published as a bundled CLI plus a standalone core package (https://raw.githubusercontent.com/QwenLM/qwen-code/main/package.json, https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/developers/development/npm.md). packages/cli owns the qwen executable, Ink TUI, and runtime-mode selection; packages/core owns the UI-independent agent loop, model-provider integration, tool registration and execution, permissions, and sessions (https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/developers/architecture.md). Two execution models: direct execution, where TUI/headless construct the runtime in-process, and ACP execution, where qwen --acp hosts the agent behind the Agent Client Protocol; qwen serve wraps ACP in an HTTP+SSE control plane for long-lived, workspace-scoped, multi-client runtimes. Tools execute in core: schemas are declared to the model, requests validated, permission-checked, executed in the workspace sandbox, results returned (https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/developers/tools/introduction.md).

## Context management

Every session starts with a fresh context window; durable knowledge lives in user-written QWEN.md files (~/.qwen/QWEN.md, project QWEN.md, .qwen/QWEN.local.md) and Auto-memory, markdown notes Qwen writes into ~/.qwen/projects/<project>/memory/, maintained by background Dream consolidation and /memory, /remember, /forget, /dream commands (https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/users/features/memory.md). Auto-compaction replaces chat history with a summary via /compress (alias /summarize) or AI-free /compress-fast (https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/users/features/commands.md); context.autoCompactThreshold defaults to 0.85 with a warn/auto/hard ladder, compactionModel picks the summarizer, and recent files/images are restored post-compaction (https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/users/configuration/settings.md). Resident prefix cost is itemized by /context detail and reduced by tools.eager deferral and context.clearContextOnIdle clearing (https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/users/features/context-cost.md).

## Ecosystem

Extensions bundle prompts, MCP servers, subagents, skills, and custom commands and install from the Gemini CLI Extensions Gallery, Claude Code Marketplace (manifests auto-converted), Qoder plugins, portable Agent Plugins v1, scoped npm registries, git URLs, local paths, and archives (https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/users/extension/introduction.md). /extensions opens an interactive Discover/Installed/Sources manager with hot-reloading; /extensions explore opens the Gemini or ClaudeCode marketplace. No extension or marketplace counts are documented; the docs instead emphasize cross-ecosystem compatibility. Broader ecosystem: TypeScript, Python, and Java SDKs; a desktop app for macOS/Windows/Linux; VS Code, Zed, and JetBrains plugins; Telegram/DingTalk/WeChat/Feishu channels via qwen channel start (https://raw.githubusercontent.com/QwenLM/qwen-code/main/README.md).

## Governance

Licensed under the Apache License 2.0 (https://raw.githubusercontent.com/QwenLM/qwen-code/main/LICENSE); owned and maintained by the QwenLM organization at github.com/QwenLM/qwen-code, described as "Qwen's agentic coding tool" (https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/users/overview.md). Contribution model: every submission requires review via GitHub pull requests; PRs must link an existing, maintainer-approved issue, stay small (split beyond ~1,200 changed lines), pass npm run preflight, and update docs for user-facing changes (https://raw.githubusercontent.com/QwenLM/qwen-code/main/CONTRIBUTING.md). Documented release cadence: nightly builds daily at 21:00 UTC, preview builds weekly on Tuesdays at 17:00 UTC, stable releases triggered manually by maintainers through the release.yml workflow, all gated on preflight checks and integration tests (https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/developers/development/npm.md).

## Limitations

qwen serve first shipped as v0.16-alpha: text-only chat/coding with local-only deployment; image/file attachments, streaming uploads, containerized deployment (Docker/k8s/nginx), multi-daemon coordination, and Prometheus metrics are explicitly deferred (https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/users/qwen-serve.md). README labels the Web UI (qwen serve --open) and daemon mode experimental (https://raw.githubusercontent.com/QwenLM/qwen-code/main/README.md). Agent Plugins v1 installs do not activate commands, agents, hooks, client namespaces, or legacy SSE MCP (https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/users/extension/introduction.md). Git-based extension installs needing submodules/LFS require Git >=2.37, and Windows symlink installation may need Developer Mode. Commands /workflows, /lsp (--experimental-lsp), and /trust register only when features are enabled; the roadmap lists hooks and cross-platform compatibility as in-progress (https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/users/features/commands.md, https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/developers/roadmap.md).

## In its own words

> Qwen Code is actively iterating on itself — using its own agent and models to file issues, submit PRs, review code, and run tests. Powered by the community, driven by AI.  
> — [https://raw.githubusercontent.com/QwenLM/qwen-code/main/README.md](https://raw.githubusercontent.com/QwenLM/qwen-code/main/README.md)

> The core package does not decide how results are displayed or how a remote client transports them.  
> — [https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/developers/architecture.md](https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/developers/architecture.md)

> Stage 1 is sized for developers prototyping clients against the protocol surface and for local single-user / small-team collaboration.  
> — [https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/users/qwen-serve.md](https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/users/qwen-serve.md)

> Every Qwen Code session starts with a fresh context window.  
> — [https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/users/features/memory.md](https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/users/features/memory.md)


## Notable

Ships built-in `claude-code` and `codex` subagent executors that delegate tasks to separately installed Claude Code (ACP) and Codex CLIs using their own models/auth, and it installs extensions directly from the Claude Code and Gemini CLI marketplaces.

## Sources fetched

- https://raw.githubusercontent.com/QwenLM/qwen-code/main/README.md
- https://raw.githubusercontent.com/QwenLM/qwen-code/main/LICENSE
- https://raw.githubusercontent.com/QwenLM/qwen-code/main/CONTRIBUTING.md
- https://raw.githubusercontent.com/QwenLM/qwen-code/main/package.json
- https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/index.md
- https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/users/overview.md
- https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/users/configuration/settings.md
- https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/users/features/memory.md
- https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/users/features/commands.md
- https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/users/features/token-caching.md
- https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/users/features/context-cost.md
- https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/users/extension/introduction.md
- https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/users/extension/getting-started-extensions.md
- https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/users/qwen-serve.md
- https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/developers/architecture.md
- https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/developers/roadmap.md
- https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/developers/tools/introduction.md
- https://raw.githubusercontent.com/QwenLM/qwen-code/main/docs/developers/development/npm.md

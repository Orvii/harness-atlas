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

## Architecture

TypeScript monorepo with npm workspaces: package @google/gemini-cli handles the React-based terminal UI and command parsing and is bundled into one self-contained executable, while @google/gemini-cli-core handles Gemini API requests, authentication, and local cache and is published standalone (https://github.com/google-gemini/gemini-cli/blob/main/docs/npm.md); a third package, an A2A server, appears in the release package table (docs/releases.md). Runtime is Node.js 20+ (CONTRIBUTING.md, docs/get-started/installation.mdx). Tools execute through the core package's tool registry: the model requests a tool, the CLI evaluates it against security policies, mutators such as write_file and run_shell_command require manual confirmation (docs/reference/tools.md), and shell commands run via node-pty with a child_process fallback (docs/tools/shell.md). ACP mode turns the CLI into a JSON-RPC 2.0 server over stdio for IDE clients (docs/cli/acp-mode.md).

## Context management

Context comes from hierarchical GEMINI.md files: a global ~/.gemini/GEMINI.md, workspace and parent-directory files, and just-in-time scans of directories touched by tools, all concatenated into every prompt (https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md). Automatic compression triggers at model.compressionThreshold, default 0.5 of context usage (docs/reference/configuration.md); /compress replaces the chat context with a summary (docs/reference/commands.md) and a PreCompress hook fires first (docs/hooks/index.md). Sessions and tool I/O auto-save to ~/.gemini/tmp/<project_hash>/chats (docs/cli/session-management.md); checkpointing snapshots files into a shadow git repo for /restore (docs/cli/checkpointing.md); /rewind reverts conversation and/or code, working across compression points (docs/cli/rewind.md). Token caching is API-key/Vertex only (docs/cli/token-caching.md), and experimental Auto Memory mines past transcripts into reviewable memory patches and skills (docs/cli/auto-memory.md).

## Ecosystem

Extensions package prompts, MCP servers, custom commands, themes, hooks, subagents, and Agent Skills into installable units; installs come from GitHub repository URLs (gemini extensions install) or the official gallery (https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/index.md). The gallery page fetched during research advertises "Search all 2132 extensions" (https://geminicli.com/extensions), and a publishing flow to that gallery is documented (docs/extensions/releasing.md). Beyond extensions: SKILL.md agent skills (docs/cli/skills.md), .toml custom commands, hooks, MCP servers over Stdio/SSE/Streamable HTTP (docs/tools/mcp-server.md), subagents, an ACP Agent Registry listing for Zed/JetBrains, and a VS Code Companion extension (docs/ide-integration/index.md). Official sample repositories live under the gemini-cli-extensions GitHub organization.

## Governance

Apache License 2.0 (https://github.com/google-gemini/gemini-cli/blob/main/LICENSE), owned by Google under the google-gemini GitHub organization. Contributions require the Google CLA and follow Google's Open Source Community Guidelines; maintainer-reserved issues carry a "🔒Maintainers only" label (CONTRIBUTING.md). Cadence: nightly daily UTC 00:00, preview weekly Tuesday UTC 23:59, stable weekly Tuesday UTC 20:00, semver-based with patch hotfixes, coordinated by a release manager; npm publishing runs through Google's Wombat Dressing Room (docs/releases.md, README.md). A May 19, 2026 Google Developers Blog post announced unification into Antigravity CLI, stopping consumer requests June 18, 2026 while enterprise licenses and paid API keys continue; latest stable, v0.61.0, shipped September 23, 2026 (docs/changelogs/latest.md).

## Limitations

Token caching is unavailable to OAuth users because the Code Assist API cannot create cached content (https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/token-caching.md). The FAQ forbids third-party clients piggybacking OAuth authentication, warning of suspension (docs/resources/faq.md). Requires macOS 15+, Windows 11 24H2+, or Ubuntu 20.04+, Node.js 20+, internet access, and a Code Assist supported location (docs/get-started/installation.mdx). /copy needs xclip/xsel on Linux, and interactive shell requires node-pty or it falls back to non-interactive child_process (docs/reference/commands.md, docs/tools/shell.md). Sandboxing is platform-bound: Seatbelt macOS-only, runsc Linux-only, Windows native via icacls, LXC/LXD experimental (docs/cli/sandbox.md). Plan mode, Subagents, and Remote subagents are marked 🔬 in the docs index; Auto Memory is experimental (docs/index.md, docs/cli/auto-memory.md). Consumer service ended June 18, 2026.

## In its own words

> Gemini CLI is an open-source AI agent that brings the power of Gemini directly into your terminal. It provides lightweight access to Gemini, giving you the most direct path from your prompt to our model.  
> — [https://github.com/google-gemini/gemini-cli/blob/main/README.md](https://github.com/google-gemini/gemini-cli/blob/main/README.md)

> ACP (Agent Client Protocol) mode is a special operational mode of Gemini CLI designed for programmatic control, primarily for IDE and other developer tool integrations. It uses a JSON-RPC protocol over stdio to communicate between Gemini CLI agent and a client.  
> — [https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/acp-mode.md](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/acp-mode.md)

> The CLI uses a hierarchical system to source context. It loads various context files from several locations, concatenates the contents of all found files, and sends them to the model with every prompt.  
> — [https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md)

> Gemini CLI extensions package prompts, MCP servers, custom commands, themes, hooks, sub-agents, and agent skills into a familiar and user-friendly format. With extensions, you can expand the capabilities of Gemini CLI and share those capabilities with others.  
> — [https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/index.md](https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/index.md)


## Notable

The official docs banner and Google Developers Blog announce that Gemini CLI was replaced by Antigravity CLI on June 18, 2026 for free, Pro, and Ultra users, yet the repo keeps shipping weekly releases (v0.62.0, Sep 29, 2026) for enterprise and API-key users - a live-but-transitioning project.

## Sources fetched

- https://github.com/google-gemini/gemini-cli
- https://github.com/google-gemini/gemini-cli/blob/main/README.md
- https://github.com/google-gemini/gemini-cli/blob/main/CONTRIBUTING.md
- https://github.com/google-gemini/gemini-cli/blob/main/LICENSE
- https://github.com/google-gemini/gemini-cli/blob/main/docs/index.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/npm.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/releases.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/changelogs/latest.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/acp-mode.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/sandbox.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/session-management.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/checkpointing.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/token-caching.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/headless.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/rewind.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/plan-mode.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/auto-memory.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/settings.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/custom-commands.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/trusted-folders.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/model.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/model-routing.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/telemetry.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/system-prompt.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/enterprise.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/git-worktrees.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/cli-reference.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/tutorials/memory-management.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/core/index.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/core/subagents.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/core/remote-agents.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/file-system.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/shell.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/memory.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/tools.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/commands.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/configuration.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/policy-engine.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/memport.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/hooks/index.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/ide-integration/index.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/index.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/reference.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/writing-extensions.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/get-started/index.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/get-started/installation.mdx
- https://github.com/google-gemini/gemini-cli/blob/main/docs/get-started/authentication.mdx
- https://github.com/google-gemini/gemini-cli/blob/main/docs/get-started/gemini-3.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/resources/faq.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/resources/troubleshooting.md
- https://github.com/google-gemini/gemini-cli/blob/main/docs/resources/quota-and-pricing.md
- https://geminicli.com/extensions
- https://developers.googleblog.com/en/an-important-update-transitioning-gemini-cli-to-antigravity-cli

# OpenCode

- **repo:** anomalyco/opencode (formerly sst/opencode; default branch dev)
- **version pin:** `v1.18.34` — gh api repos/anomalyco/opencode/releases/latest → https://github.com/anomalyco/opencode/releases/tag/v1.18.34 (published 2026-09-30); cross-checked npm opencode-ai@1.18.34 via registry.npmjs.org
- **docs home:** https://opencode.ai/docs

## What it promises

An open source AI coding agent ("The open source AI coding agent") available as a terminal TUI, desktop app, or IDE extension, usable with any of 75+ LLM providers including local models. It promises a plan-first workflow (read-only Plan agent) with full-access Build agent, undo/redo, shareable sessions, and Claude Code-compatible AGENTS.md/CLAUDE.md conventions.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | Built-in General/Explore/Scout subagents; custom via JSON or markdown; @ mention or Task tool; task permission gates which subagents each agent may invoke. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/agents.mdx) |
| workflow_orchestration | ◐ partial | No DAG/team/swarm framework in docs; orchestration is fan-out via the task tool plus programmatic control through the SDK/server (sdk.mdx: control opencode programmatically) and a GitHub Actions bot. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/agents.mdx) |
| mcp | ✅ yes | MCP client only (local + remote, headers, OAuth/DCR, per-agent enable/disable); no MCP server mode documented. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/mcp-servers.mdx) |
| hooks_lifecycle | ✅ yes | Via plugin API: tool.execute.before/after, session.created/idle/deleted/error, file.edited, permission.asked, experimental.session.compacting; no hooks declared in plain config. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/plugins.mdx) |
| skills | ✅ yes | SKILL.md folders in .opencode/skills, ~/.config/opencode/skills, and Claude-compatible .claude/skills and .agents/skills; loaded on demand via native skill tool with per-pattern permissions. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/skills.mdx) |
| memory_persistence | ✅ yes | File-based memory: AGENTS.md (project + global) and CLAUDE.md fallback, plus extra instruction files/URLs; sessions persist and resume. No automatic memory extraction/retrieval system. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/rules.mdx) |
| sandboxing | ✅ yes | Permission modes allow/ask/deny global and per-tool with glob rules (e.g. bash command patterns), external_directory guard, doom_loop guard, and --auto mode. No OS-level filesystem/process sandbox found in docs. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/permissions.mdx) |
| plan_mode | ✅ yes | Built-in Plan primary agent, Tab to switch; edits and bash default to ask; README also documents build/plan agent cycle. | [src](https://opencode.ai/docs/) |
| background_tasks | ◐ partial | Behind OPENCODE_EXPERIMENTAL_BACKGROUND_SUBAGENTS flag; server also exposes POST /session/:id/prompt_async ('Send a message asynchronously (no wait)'). Not a general background-job system. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/cli.mdx) |
| ide_integration | ✅ yes | Auto-installing VS Code/Cursor/Windsurf/VSCodium extension with keybinds; JetBrains, Zed and Neovim via ACP (opencode acp) per acp.mdx. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/ide.mdx) |
| model_agnostic | ✅ yes | Any provider via /connect or config; custom baseURL for proxies; optional OpenCode Zen curated gateway; per-agent model overrides. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/providers.mdx) |
| plugins | ✅ yes | TS/JS plugin modules loaded from .opencode/plugins, ~/.config/opencode/plugins, or npm packages listed in config; can add custom tools; community ecosystem page. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/plugins.mdx) |
| session_resume | ✅ yes | --continue/-c resumes last session, --session/-s a specific ID, --fork branches while continuing; TUI session list; sessions deletable/exportable. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/cli.mdx) |
| cost_controls | ✅ yes | opencode stats with --days/--models breakdown; --verbose shows cost metadata; per-agent 'steps' cap limits agentic iterations to control cost; Zen pay-as-you-go pricing. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/cli.mdx) |

## Architecture

OpenCode is client/server: when run, "it starts a TUI and a server", and the TUI is "the client that talks to the server"; the server exposes an OpenAPI 3.1 spec that also generates the SDK (https://opencode.ai/docs/server). Other clients: `opencode web`, an Electron desktop app wrapping the web UI, a VS Code/Cursor/Windsurf extension, and `opencode acp` (JSON-RPC over stdio) for Zed/JetBrains (https://opencode.ai/docs/web, /docs/ide, /docs/acp, raw CONTRIBUTING.md). Development requires Bun 1.3+ — a TypeScript codebase where `bun dev` runs server plus TUI (the contributing guide notes the server may run in a worker thread) (https://raw.githubusercontent.com/anomalyco/opencode/dev/CONTRIBUTING.md). Tools execute as LLM tool calls — built-in bash/edit/write/read/grep/glob/apply_patch/skill/webfetch/websearch, ripgrep-backed — extended by MCP servers and plugin hooks like `tool.execute.before/after` (https://opencode.ai/docs/tools, /docs/plugins).

## Context management

Compaction is controlled by the `compaction` option: `auto` (default true) "Automatically compact the session when context is full", `prune` removes old tool outputs, `reserved` keeps a token buffer; `OPENCODE_DISABLE_AUTOCOMPACT` disables it (https://opencode.ai/docs/config, /docs/cli). A hidden system agent named compaction "compacts long context into a smaller summary" and "runs automatically when needed and is not selectable in the UI" (https://opencode.ai/docs/agents). Users can compact manually via `/compact` (alias `/summarize`) or `POST /session/:id/summarize` (https://opencode.ai/docs/tui, /docs/server). Persistent instructions live in AGENTS.md (project root and `~/.config/opencode/AGENTS.md`), with Claude Code fallbacks CLAUDE.md and `~/.claude/skills/` (https://opencode.ai/docs/rules). Plugins can inject context into, or fully replace, the compaction prompt via the `experimental.session.compacting` hook (https://opencode.ai/docs/plugins).

## Ecosystem

The ecosystem page lists 38 community plugins, 11 projects, and 2 agent collections, and points to aggregators awesome-opencode and opencode.cafe (https://opencode.ai/docs/ecosystem). Plugins are distributed two ways: local JavaScript/TypeScript files in `.opencode/plugins/` or `~/.config/opencode/plugins/`, or (scoped) npm packages listed in the `plugin` config array — "npm plugins are installed automatically using Bun at startup" and cached in `~/.cache/opencode/node_modules/` (https://opencode.ai/docs/plugins). Model coverage comes from the AI SDK plus Models.dev, "supporting 75+ LLM providers" (https://opencode.ai/docs/models). MCP servers (local or remote, with OAuth) add external tools (https://opencode.ai/docs/mcp-servers); a published `@opencode-ai/sdk` enables programmatic integrations (https://opencode.ai/docs/sdk); Zed installs OpenCode through its ACP registry (https://opencode.ai/docs/acp).

## Governance

OpenCode is MIT-licensed — the LICENSE file reads "MIT License Copyright (c) 2025 opencode" (https://raw.githubusercontent.com/anomalyco/opencode/dev/LICENSE). It is owned by Anomaly: repo github.com/anomalyco/opencode, docs footer "© Anomaly" linking anoma.ly, and the recommended Homebrew tap anomalyco/tap (https://opencode.ai/docs/, https://github.com/anomalyco/opencode). CONTRIBUTING.md defines the contribution model: commonly merged changes are bug fixes, LSP/formatter additions, provider support, performance, and docs; "any UI or core product feature must go through a design review with the core team before implementation"; new providers are added via PRs to anomalyco/models.dev. No release-cadence statement appears in fetched docs; the repo shows 15,837 commits on dev, 28k forks, and commits dated Oct 2026 (https://github.com/anomalyco/opencode).

## Limitations

Documented gaps: v2 docs state "Windows package managers are not supported" (https://opencode.ai/v2/docs); v1 recommends WSL for Windows, Desktop requires Microsoft Edge WebView2, and blank Wayland windows need OC_ALLOW_WAYLAND=1 (https://opencode.ai/docs/windows-wsl, /docs/troubleshooting). `/undo` and file-change rollback require the project to be a git repository (https://opencode.ai/docs/tui). Several features are experimental: an OPENCODE_EXPERIMENTAL umbrella plus _LSP_TOOL, _EXA, and _EVENT_SYSTEM flags (https://opencode.ai/docs/cli); policies are "experimental" and "currently supports one policy action" (https://opencode.ai/docs/policies); LSP and formatters ship disabled by default (https://opencode.ai/docs/lsp, /docs/formatters). The official SDK is JS/TS-only (https://opencode.ai/docs/sdk).

## In its own words

> OpenCode is an open source AI coding agent. It's available as a terminal-based interface, desktop app, or IDE extension.  
> — [https://opencode.ai/docs/](https://opencode.ai/docs/)

> When you run `opencode` it starts a TUI and a server. Where the TUI is the client that talks to the server. The server exposes an OpenAPI 3.1 spec endpoint. This endpoint is also used to generate an SDK.  
> — [https://opencode.ai/docs/server](https://opencode.ai/docs/server)

> However, any UI or core product feature must go through a design review with the core team before implementation.  
> — [https://raw.githubusercontent.com/anomalyco/opencode/dev/CONTRIBUTING.md](https://raw.githubusercontent.com/anomalyco/opencode/dev/CONTRIBUTING.md)

> Have no lock-in by allowing you to use it with any other coding agent. And always let you use any other provider with OpenCode as well.  
> — [https://opencode.ai/docs/zen](https://opencode.ai/docs/zen)


## Notable

Deep Claude Code compatibility is a first-class fallback path (reads CLAUDE.md and .claude/skills unless disabled), plus a /oc GitHub bot that runs entire tasks inside your repo's GitHub Actions runners.

## Sources fetched

- https://opencode.ai/docs/
- https://opencode.ai/docs/cli
- https://opencode.ai/docs/config
- https://opencode.ai/docs/tui
- https://opencode.ai/docs/rules
- https://opencode.ai/docs/server
- https://opencode.ai/docs/plugins
- https://opencode.ai/docs/mcp-servers
- https://opencode.ai/docs/agents
- https://opencode.ai/docs/skills
- https://opencode.ai/docs/tools
- https://opencode.ai/docs/models
- https://opencode.ai/docs/providers
- https://opencode.ai/docs/go
- https://opencode.ai/docs/zen
- https://opencode.ai/docs/share
- https://opencode.ai/docs/enterprise
- https://opencode.ai/docs/troubleshooting
- https://opencode.ai/docs/lsp
- https://opencode.ai/docs/formatters
- https://opencode.ai/docs/permissions
- https://opencode.ai/docs/commands
- https://opencode.ai/docs/references
- https://opencode.ai/docs/policies
- https://opencode.ai/docs/ecosystem
- https://opencode.ai/docs/sdk
- https://opencode.ai/docs/acp
- https://opencode.ai/docs/web
- https://opencode.ai/docs/ide
- https://opencode.ai/docs/network
- https://opencode.ai/docs/github
- https://opencode.ai/docs/windows-wsl
- https://opencode.ai/v2/docs
- https://github.com/anomalyco/opencode
- https://raw.githubusercontent.com/anomalyco/opencode/dev/README.md
- https://raw.githubusercontent.com/anomalyco/opencode/dev/CONTRIBUTING.md
- https://raw.githubusercontent.com/anomalyco/opencode/dev/LICENSE

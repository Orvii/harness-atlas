# Kilo Code

- **repo:** https://github.com/Kilo-Org/kilocode
- **version pin:** `v7.8.3` — gh api repos/Kilo-Org/kilocode/releases/latest -> tag v7.8.3, published 2026-10-01; confirmation via releases list (v7.8.2 same day, separate jetbrains/v7.1.9-rc.1 train)
- **docs home:** https://kilocode.ai/docs

## What it promises

Landing page: "One open agent for every developer workflow — 500+ models, zero markup" with "No black boxes. Inspect everything... Fork, modify, self-host" under MIT-licensed source. README: "The open source coding agent for building with AI in VS Code, JetBrains, or the CLI."

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | Primary agents (Code, Plan, Debug) invoke subagents via the task tool; users invoke them with @agent-name. Built-in general and explore subagents; custom ones defined in kilo.jsonc or markdown files. UI-based config not yet available. | [src](https://kilocode.ai/docs/customize/custom-subagents) |
| workflow_orchestration | ✅ yes | Task subagents for in-session children; Agent Manager for top-level parallel worktree sessions (multi-version mode runs up to 4 parallel implementations), Kilo Swarm shared board for cross-agent findings, markdown workflows/slash commands. Dedicated Orchestrator mode is deprecated in favor of built-in delegation. No DAG primitives documented. | [src](https://kilocode.ai/docs/automate/agent-manager) |
| mcp | ✅ yes | Curated MCP servers installable from the Kilo Marketplace; local STDIO and remote SSE transports; MCP tool permissions use the same allow/ask/deny system as built-in tools. | [src](https://kilocode.ai/docs/automate/mcp/overview) |
| hooks_lifecycle | ✅ yes | Plugin hook events include tool.execute.before/after (mutate args/output), chat.message/params/headers, permission.ask (auto-allow/deny), command.execute.before, and session.created/updated/idle/error/deleted/compacted plus message/file events. Hooks ship through the TypeScript plugin API rather than a standalone hooks config file. | [src](https://raw.githubusercontent.com/Kilo-Org/kilocode/main/packages/kilo-docs/pages/automate/extending/plugins.md) |
| skills | ✅ yes | Implements the open Agent Skills spec (agentskills.io); skills are discoverable, load into context on demand, and are installable per project or globally via the Kilo Marketplace. | [src](https://kilocode.ai/docs/customize/skills) |
| memory_persistence | ✅ yes | Stores project.md, environment.md, corrections.md plus saved session digests under ~/.local/share/kilo/memory/<project-slug>-<sha1-12>/; linked git worktrees share memory. Personal/user-level memory is explicitly not supported; replaced the deprecated memory bank. | [src](https://kilocode.ai/docs/customize/context/memory) |
| sandboxing | ◐ partial | Permission system with allow/ask/deny rules gates shell commands, file paths, sensitive files, and MCP tools; Agent Manager offers a /sandbox toggle for new worktree sessions (only when sandbox controls are enabled); Cloud Agent gets policy-selected sandbox allocation. No general OS-level jail documented for the local CLI; auto-approved commands can run without prompts. | [src](https://kilocode.ai/docs/automate/agent-manager) |
| plan_mode | ✅ yes | The Plan agent (successor to legacy Architect mode) is read-only apart from writing plans; in VS Code the saved plan opens in the editor when ready for review. Approval is a review flow rather than a hard execution gate. | [src](https://kilocode.ai/docs/code-with-ai/agents/using-agents) |
| background_tasks | ✅ yes | Contrast with foreground tasks that block the parent; Agent Manager runs independent top-level sessions in parallel git worktrees, and the goal tool keeps long-running objectives (/goal pause, agent-started goals). Cloud Agent runs hosted sessions. | [src](https://kilocode.ai/docs/customize/custom-subagents) |
| ide_integration | ✅ yes | Distributed via VS Code Marketplace and Open VSX; a separate JetBrains plugin (Kotlin, jb/ release train) exists; sessions sync across IDE, CLI, cloud, and mobile. Sessions can be inspected from VS Code history views. | [src](https://kilocode.ai/docs/getting-started) |
| model_agnostic | ✅ yes | Cloud providers (Anthropic, OpenAI, Gemini, Bedrock, Vertex, DeepSeek, Mistral...), local models (Ollama, LM Studio, Atomic Chat, Anaconda Desktop), and gateways (OpenRouter, Vercel AI Gateway). Landing page claims 500+ models via the zero-markup Kilo Gateway; BYOK supported. | [src](https://kilocode.ai/docs/ai-providers) |
| plugins | ✅ yes | Public plugin API: TypeScript/JavaScript modules adding tools, hooks, auth/model providers, and workspace adaptors (experimental); loaded from config, plugin directories, or npm packages; KILO_PURE=1 disables external plugins. Kilo Marketplace distributes plugins, agents, skills, and MCP servers as config/files, not VS Code extensions. | [src](https://kilocode.ai/docs/customize/marketplace) |
| session_resume | ✅ yes | Local sessions live in SQLite (kilo db / sqlite3); resume and title search in VS Code, JetBrains, and CLI (kilo session list --search, --all); agent-assisted recall of chat content; scope includes worktree and Cloud sessions. History/CLI list searches cover titles, not message bodies. | [src](https://raw.githubusercontent.com/Kilo-Org/kilocode/main/packages/kilo-docs/pages/code-with-ai/agents/session-history.md) |
| cost_controls | ✅ yes | Per-request token/cost tracking incl. cache tokens; balance checks before proxying; no inference markup (5% payment fee); BYOK billed at $0 on Kilo's side. Safeguards: doom_loop permission (default ask) pauses repeated failures, auto-model tiers, compaction/pruning to cut tokens, org-level spend governance. | [src](https://kilocode.ai/docs/gateway/usage-and-billing) |

## Architecture

Kilo Code is an editor-and-terminal stack: a VS Code extension, a Kotlin-based JetBrains plugin, a CLI/TUI, cloud agents, and Slack/mobile clients. Locally, editor clients talk to a `kilo serve` HTTP/SSE server (WebSocket on some paths); the TUI attaches to a detached `kilo daemon` when available or starts a Bun worker speaking RPC. The monorepo splits into `Kilo-Org/kilocode` (CLI runtime, daemon, extensions, JS SDK, gateway client, docs) and `Kilo-Org/cloud` (control plane, gateway routes, Cloud Agent runtime). Tools run locally through the CLI runtime's permission system, with an LSP client providing diagnostics.

## Context management

Kilo auto-compacts: when provider-reported usage or estimated outgoing tokens reach `compaction.threshold_percent` or the safety buffer (20,000 tokens, or the model's output cap up to 32,000), an anchored summary replaces older history while recent turns stay verbatim; an incremental prune pass clears tool outputs outside a 40,000-token recency window. Custom models without a declared context window are not tracked. Opt-in, project-scoped memory stores `project.md`, `environment.md`, `corrections.md` and session digests under `~/.local/share/kilo/memory/`, with AGENTS.md rules and checkpoints for file state.

## Ecosystem

Distribution spans the VS Code Marketplace, Open VSX, a JetBrains plugin, npm (`@kilocode/cli`), iOS/Android apps, Slack, and web (coming soon). The Kilo Marketplace installs agents, skills, MCP servers, and plugins as configuration files — project-scoped under `.kilo/` or globally — not VS Code extensions; MCP servers are curated there, and community contributions land in `Kilo-Org/kilo-marketplace`. Kilo advertises 500+ models through its zero-markup Gateway. No extension counts are documented; the landing page claims 5M+ "Kilo Coders" and 10T+ tokens processed monthly.

## Governance

MIT-licensed and owned by Kilo-Org (Kilo Code), which Anaconda acquired — the docs footer links the announcement. The monorepo carries a contributor architecture section covering CLI runtime, VS Code extension, JetBrains plugin, cloud platform, and development patterns, and public issues/PRs on GitHub. Release cadence is rapid: v7.8.3 shipped 2026-10-01 hours after v7.8.2, alongside a separate JetBrains train (jetbrains/v7.1.9-rc.1) and ~27.5k stars. Ecosystem repos (kilocode, cloud, kilo-marketplace) sit under the same org, and docs sources live in `packages/kilo-docs/`.

## Limitations

Orchestrator mode and Kilo Console are deprecated; subagents are configured only through `kilo.jsonc` or Markdown agent files — "UI-based configuration is not yet available." Memory is opt-in and project-scoped, with personal or user-level memory explicitly unsupported, and auto-compaction skips custom models lacking a declared context window. Browser access is "coming soon." Agent Manager's `/sandbox` toggle only appears when sandbox controls are enabled, and sandboxing is documented mainly as worktree and Cloud Agent allocation plus per-command permissions rather than an OS-level jail. Legacy docs live in the separate `kilocode-legacy` repo.

## In its own words

> Kilo Code is an open-source AI coding assistant that works wherever you do—in your IDE, terminal, browser, or on the go.  
> — [https://kilocode.ai/docs/getting-started](https://kilocode.ai/docs/getting-started)

> Kilo Code's CLI supports custom subagents — specialized AI assistants that can be invoked by primary agents or manually via @ mentions.  
> — [https://kilocode.ai/docs/customize/custom-subagents](https://kilocode.ai/docs/customize/custom-subagents)

> Plugins extend Kilo by hooking into events, adding custom tools, registering auth or model providers, and customizing runtime behavior.  
> — [https://raw.githubusercontent.com/Kilo-Org/kilocode/main/packages/kilo-docs/pages/automate/extending/plugins.md](https://raw.githubusercontent.com/Kilo-Org/kilocode/main/packages/kilo-docs/pages/automate/extending/plugins.md)

> The open source coding agent for building with AI in VS Code, JetBrains, or the CLI.  
> — [https://raw.githubusercontent.com/Kilo-Org/kilocode/main/README.md](https://raw.githubusercontent.com/Kilo-Org/kilocode/main/README.md)


## Notable

Kilo Code's CLI is a descendant of opencode — it still reads and deep-merges `opencode.json` configs and uses an opencode-style plugin system — and the project was acquired by Anaconda, while its once-signature Orchestrator mode has been deprecated in favor of every full-tool agent delegating to subagents natively.

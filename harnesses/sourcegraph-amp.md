# Sourcegraph Amp

- **repo:** sourcegraph/amp (not public — github.com/sourcegraph/amp returns 404; the product is closed source and now operates as Amp / Amp Frontier Corporation, docs at ampcode.com)
- **version pin:** `0.0.1791187719-g319a37` — Closed-source product; no public source repo (github.com/sourcegraph/amp 404, checked during research). Version pinned from the published CLI package's npm dist-tag latest: https://registry.npmjs.org/-/package/@sourcegraph/amp/dist-tags reports latest = 0.0.1791187719-g319a37 (fetched during research; package https://registry.npmjs.org/@sourcegraph/amp, license field "SEE LICENSE"). the legacy docs URL https://sourcegraph.com/docs/amp returns 404; the current docs home is https://ampcode.com/docs.
- **docs home:** https://ampcode.com/docs (legacy https://sourcegraph.com/docs/amp returns HTTP 404)

## What it promises

Amp is a coding agent and development environment built for the frontier: multi-model (Amp uses the best model for each task), orbs that keep working after you close your laptop, and the same agent and threads everywhere — web, terminal, Mac, and iPhone. It is deliberately opinionated: you get fewer knobs, because "you're always using the good parts of Amp."

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | Specialist subagents: Search, Oracle (hard reasoning/planning), Librarian (external code/docs research), Read Thread (reads other threads). Worker subagents are spawned via a Task tool; plugins can define custom subagents exposed as tools (https://ampcode.com/docs/plugin-api). | [src](https://ampcode.com/docs/models-and-subagents) |
| workflow_orchestration | ✅ yes | Fan-out across projects/orbs/runners; plugin API exposes coordination tools create_thread, list_agent_modes, get_thread_status, send_thread_message, wait_for_threads (https://ampcode.com/docs/plugin-api); Puck launches and coordinates agents (https://ampcode.com/docs/puck); scheduled automations and webhook triggers (https://ampcode.com/docs/orbs/automations, https://ampcode.com/docs/orbs/event-driven); TS/Python SDK for programmatic runs (https://ampcode.com/docs/sdk). No declarative DAG DSL documented. | [src](https://ampcode.com/docs/orbs/agent-to-agent) |
| mcp | ✅ yes | Local (amp.mcpServers) and remote (ampcode.com-managed) servers; servers bundleable inside skills via mcp.json and hidden until the skill loads; workspace MCP servers require explicit approval; enterprise MCP registry allowlist (https://ampcode.com/docs/enterprise/mcp-registry-allowlist); browser OAuth unavailable in orbs. | [src](https://ampcode.com/docs/customize/mcp) |
| hooks_lifecycle | ✅ yes | Plugin API event hooks: session.start, tool.call (with allow / reject-and-continue actions), tool.result, agent.start, agent.end, configuration observers, onDispose; plugins described as adding 'tools, commands, and event-driven behavior' (https://ampcode.com/docs/customize/plugins). Configured via TypeScript/JavaScript plugins, not plain config files. | [src](https://ampcode.com/docs/plugin-api) |
| skills | ✅ yes | SKILL.md-based skill system; search paths include Claude Code directories (.claude/skills, ~/.claude/skills) which can be disabled via amp.skills.disableClaudeCodeSkills; personal/workspace skills live in hosted Git repos (https://ampcode.com/docs/customize/global-plugins-and-skills). | [src](https://ampcode.com/docs/customize/skills) |
| memory_persistence | ✗ no | Complete docs index (llms.txt) contains no memory feature. Durability is file-based: AGENTS.md guidance files (system-wide, home, workspace, repo, subtree; https://ampcode.com/docs/customize/agents-md) plus persistent resumable threads. No agent-authored cross-session memory store documented. | [src](https://ampcode.com/llms.txt) |
| sandboxing | ◐ partial | No built-in interactive permission modes; orbs are sandboxed cloud VMs (https://ampcode.com/security: 'An orb is a sandboxed cloud machine'), MCP allow/deny rules via amp.mcpPermissions (https://ampcode.com/docs/cli/settings), and custom policy plugins can gate tool calls (permissions example in https://ampcode.com/docs/customize/plugins). Local tool execution is unsandboxed and unapproved by default. | [src](https://ampcode.com/docs/tools) |
| plan_mode | ✗ no | No dedicated plan-then-approve mode documented; planning is a prompt convention, with the Oracle subagent handling hard reasoning/planning questions. Modes are only low/medium/high/ultra (https://ampcode.com/modes, https://ampcode.com/docs/the-dial). | [src](https://ampcode.com/docs/prompting) |
| background_tasks | ✅ yes | Orbs run remotely and pause when idle (waking with conversation/files/services intact); automations run threads on schedules (https://ampcode.com/docs/orbs/automations); event-driven orbs trigger on webhooks (https://ampcode.com/docs/orbs/event-driven); amp --no-tui runners serve remotely started threads (https://ampcode.com/docs/cli/runners). | [src](https://ampcode.com/docs/orbs) |
| ide_integration | ✅ yes | Integration lets Amp see the open file/selection and edit files through the IDE with undo; Neovim needs the ampcode/amp.nvim plugin; JetBrains diagnostics supported for JVM languages (https://ampcode.com/news/jetbrains-diagnostics); VS Code extension listed on the marketplace (https://ampcode.com/news/cli-vscode-neovim). In-editor Amp Tab completion was discontinued (https://ampcode.com/chronicle — 'Tab, Tab, Dead'). | [src](https://ampcode.com/docs/cli) |
| model_agnostic | ✅ yes | Amp routes per task across foundation models (GPT/Claude/Gemini families) and supports BYOK API keys, provider subscriptions (ChatGPT, X Premium+/SuperGrok), custom HTTPS/Vertex gateways, and per-subagent model pins. Docs frame it as opinionated: Amp picks models, you pick modes (https://ampcode.com/docs). | [src](https://ampcode.com/docs/customize/model-routing) |
| plugins | ✅ yes | Full plugin API (@ampcode/plugin types) for tools, commands, hooks, custom mode/agent definitions, webhooks, UI dialogs; distribution via hosted personal/workspace Git repos and global plugins (https://ampcode.com/docs/customize/global-plugins-and-skills). Plugins run code in your environment. | [src](https://ampcode.com/docs/customize/plugins) |
| session_resume | ✅ yes | Threads are durable and shareable across clients; cross-client access continues a running CLI thread from ampcode.com (https://ampcode.com/docs/cli/remote-control); SDK supports continue: true / continue by thread ID (https://ampcode.com/docs/sdk). | [src](https://ampcode.com/docs/threads) |
| cost_controls | ✅ yes | Threads display cost so far (https://ampcode.com/docs/threads); CLI setting amp.showCosts (https://ampcode.com/docs/cli/settings); credits model with included usage then paid credits at provider API prices; Enterprise adds per-user cost controls, pooled credits, spend limits/reporting, and workspace entitlements with per-user quotas (https://ampcode.com/docs/pricing, https://ampcode.com/docs/enterprise/workspace-entitlements). | [src](https://ampcode.com/docs/pricing) |

## Architecture

Amp is a closed-source coding agent built around persistent threads. A thread runs in one of three places: a local CLI process (terminal TUI); an orb — a fresh sandboxed cloud VM created per thread with the repo, tools, and plugins, snapshotted (reused at most 72 hours) and paused when idle; or a runner, your own machine serving remotely started threads via amp --no-tui (the macOS app can be a runner). Tools execute as shell commands in a shared tmux session; plugins are TypeScript/JavaScript modules running in the host environment. The SDK drives the installed CLI. Web, Mac, and iOS clients steer the same running threads. (https://ampcode.com/docs/orbs, https://ampcode.com/docs/cli/runners, https://ampcode.com/docs/plugin-api, https://ampcode.com/docs/sdk)

## Context management

Context enters via @-mentioned files, which Amp truncates to 500 lines and 2KB per line (the agent reads more if needed), and leaves via message edits or restoring the window to an earlier point. Handoff distills one context window into a fresh thread; threads can reference other threads so the agent pulls what it needs. Long threads get automatic context summarization. Specialist subagents run their own context windows and return only results — an explicit strategy to keep the main window clean. Orbs keep conversation, files, and services across pauses. (https://ampcode.com/guides/context-management, https://ampcode.com/docs/models-and-subagents, https://ampcode.com/modes, https://ampcode.com/docs/orbs)

## Ecosystem

Extensions are Git repositories. Amp hosts personal and workspace plugins/skills repos; amp clone user-plugins / workspace-skills fetches them, and publishing is a git push (owners can require signed commits). Global repos load everywhere the user works; project-local .amp/plugins and skills also load, and Amp reads Claude Code skill directories. Plugins are typed via the @ampcode/plugin API; skills can bundle MCP servers through mcp.json. TypeScript and Python SDKs embed Amp in programs. Enterprises can enforce an MCP registry allowlist. A VS Code extension and Neovim plugin exist, though the Amp Tab completion engine was discontinued. (https://ampcode.com/docs/customize/global-plugins-and-skills, https://ampcode.com/docs/plugin-api, https://ampcode.com/docs/sdk, https://ampcode.com/docs/customize/mcp, https://ampcode.com/docs/cli)

## Governance

Closed source and commercial. There is no public repository — github.com/sourcegraph/amp returns 404 (checked during research) — and the CLI ships as npm @sourcegraph/amp under license "SEE LICENSE". Amp spun out of Sourcegraph into Amp Frontier Corporation, an independent agent research lab, with an explicit "no backward compatibility" posture; unloved features are deleted (Amp Tab, custom commands replaced by skills). Cadence is fast, with news/chronicle posts several times a month. Tiers: Hobby, Megawatt, Gigawatt, Teams, Enterprise (SSO/SCIM, audit, spend limits). the legacy sourcegraph.com/docs/amp 404s; current docs are ampcode.com. (https://ampcode.com/news/amp-frontier-corporation, https://ampcode.com/about, https://registry.npmjs.org/@sourcegraph/amp, https://ampcode.com/docs/pricing)

## Limitations

Locally, Amp asks no approval before running tools; permissions come only from custom plugins or MCP allow/deny rules. No plan-then-approve mode exists — planning is a prompt convention. No dedicated cross-session memory; guidance is file-based AGENTS.md. Browser OAuth is unavailable in orbs, so MCP auth must use headers or remote MCP definitions. Workspace MCP servers require explicit approval, and an unreachable enterprise MCP registry blocks all MCP servers. Windows is supported only via WSL. Orbs reuse snapshots for at most 72 hours; archiving a thread pauses its orb. (https://ampcode.com/docs/tools, https://ampcode.com/docs/prompting, https://ampcode.com/docs/customize/agents-md, https://ampcode.com/docs/customize/mcp, https://ampcode.com/docs/cli, https://ampcode.com/docs/orbs)

## In its own words

> Amp is a coding agent and development environment built for the frontier.  
> — [https://ampcode.com/docs](https://ampcode.com/docs)

> Amp can delegate focused work to specialist subagents. Each subagent has its own context window and access to tools like file editing and terminal commands.  
> — [https://ampcode.com/docs/models-and-subagents](https://ampcode.com/docs/models-and-subagents)

> By default, Amp does not ask for approval before running tools.  
> — [https://ampcode.com/docs/tools](https://ampcode.com/docs/tools)

> Amp agents can start other agents, send them instructions, exchange files, and bring their results back into the current thread.  
> — [https://ampcode.com/docs/orbs/agent-to-agent](https://ampcode.com/docs/orbs/agent-to-agent)


## Notable

Amp's default unit of work is a per-thread cloud machine it manages for you (the orb) rather than your laptop, agent-to-agent delegation and steering running agents from a phone are core UX, and the company openly kills features it stops loving ("If we don't use and love a feature, we kill it") with an explicit no-backward-compatibility stance.

## Sources fetched

- https://ampcode.com/docs
- https://ampcode.com/llms.txt
- https://ampcode.com/docs/models-and-subagents
- https://ampcode.com/docs/the-dial
- https://ampcode.com/docs/prompting
- https://ampcode.com/docs/tools
- https://ampcode.com/docs/threads
- https://ampcode.com/docs/pricing
- https://ampcode.com/docs/orbs
- https://ampcode.com/docs/orbs/getting-started
- https://ampcode.com/docs/orbs/agent-to-agent
- https://ampcode.com/docs/orbs/automations
- https://ampcode.com/docs/orbs/event-driven
- https://ampcode.com/docs/cli
- https://ampcode.com/docs/cli/settings
- https://ampcode.com/docs/cli/execute-mode
- https://ampcode.com/docs/cli/remote-control
- https://ampcode.com/docs/cli/runners
- https://ampcode.com/docs/puck
- https://ampcode.com/docs/sdk
- https://ampcode.com/docs/customize/plugins
- https://ampcode.com/docs/customize/global-plugins-and-skills
- https://ampcode.com/docs/customize/skills
- https://ampcode.com/docs/customize/mcp
- https://ampcode.com/docs/customize/agents-md
- https://ampcode.com/docs/customize/model-routing
- https://ampcode.com/docs/plugin-api
- https://ampcode.com/docs/enterprise/mcp-registry-allowlist
- https://ampcode.com/modes
- https://ampcode.com/guides/context-management
- https://ampcode.com/security
- https://ampcode.com/about
- https://ampcode.com/chronicle
- https://ampcode.com/news/amp-frontier-corporation
- https://ampcode.com/news/cli-vscode-neovim
- https://ampcode.com/news/jetbrains-diagnostics
- https://ampcode.com/news/amp-tab-for-all
- https://ampcode.com/sitemap.xml
- https://registry.npmjs.org/@sourcegraph/amp
- https://registry.npmjs.org/-/package/@sourcegraph/amp/dist-tags
- https://sourcegraph.com/docs/amp (404 — legacy docs URL, verified dead during research)
- https://api.github.com/repos/sourcegraph/amp (404 — no public repo)

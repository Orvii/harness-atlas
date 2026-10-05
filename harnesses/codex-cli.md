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

## Architecture

Codex CLI is a local coding agent built as a Rust Cargo workspace (codex-rs) driving a terminal UI; OpenAI's README says it "runs locally on your computer" (raw.githubusercontent.com/openai/codex/main/README.md, docs/install.md). Rich clients connect through codex app-server, a JSON-RPC 2.0 service — stdio JSONL default, WebSocket and Unix-socket transports — powering the VS Code extension and letting `codex --remote ws://` attach a TUI to a remote server (learn.chatgpt.com/docs/app-server.md). Headless automation uses `codex exec`, streaming progress to stderr and printing only the final message to stdout (learn.chatgpt.com/docs/non-interactive-mode.md). Tools execute as spawned commands inheriting sandbox boundaries: git, package managers, and test runners share the same platform-native enforcement (learn.chatgpt.com/docs/sandboxing.md).

## Context management

Three layers. Per-session instruction chain: global ~/.codex/AGENTS.md (or AGENTS.override.md), then per-directory files walked from project root downward, concatenated so closer files override earlier ones, capped at 32 KiB via project_doc_max_bytes (learn.chatgpt.com/docs/agent-configuration/agents-md.md). Cross-session recall: a separate local memory store, toggled per chat with /memories, which docs call "a helpful recall layer, not... the only source for rules" (learn.chatgpt.com/docs/customization/memories.md). Window pressure: /compact "replaces earlier turns with a concise summary, freeing context while keeping critical details" (developers.openai.com/codex/cli/slash-commands.md); config keys compact_prompt and experimental_compact_prompt_file override the compaction prompt, and sqlite_home stores SQLite-backed resumable runtime state (developers.openai.com/codex/config-file/config-reference.md).

## Ecosystem

Codex ships through npm (@openai/codex), a Homebrew cask, standalone curl/PowerShell installers, and GitHub Releases with a DotSlash pinned-tool file (raw README, docs/install.md). Extensions are plugins: "Plugins bundle capabilities into reusable workflows in ChatGPT and Codex. They can include skills and MCP servers. Both products use one universal plugin directory" (developers.openai.com/codex/plugins.md). Codex CLI browses marketplaces via /plugins — its docs page shows a browser reading "Installed 17 of 1751 available plugins" — while the IDE extension does not support plugins (developers.openai.com/codex/cli/, plugins.md). Also documented: a $1M Codex open source fund awarding up to $25,000 in API credits on a rolling basis (raw docs/open-source-fund.md), and a Codex for OSS program (learn.chatgpt.com/docs/open-source.md). No other registry counts are documented.

## Governance

Owned by OpenAI; openai/codex is the primary open-source home for CLI, SDK (sdk/), and app-server (codex-rs/app-server), with Codex Security split into a separate openai/codex-security repo (learn.chatgpt.com/docs/open-source.md). License: Apache-2.0 (raw LICENSE, README). Contribution model is deliberately closed to code: "We do not accept external code contributions or pull requests"; issues, root-cause analyses, and feature requests are the accepted channels (raw docs/contributing.md), although an Apache-style CLA document remains for contributors (docs/CLA.md). Security reports go through OpenAI's Bugcrowd program (SECURITY.md). Release cadence is rapid: tags prefixed rust-v, stable rust-v0.158.0 alongside alphas reaching rust-v0.162.0-alpha.14, with six prerelease tags published between 2026-10-03 and 2026-10-05 (github.com/openai/codex/releases, api.github.com/repos/openai/codex/releases).

## Limitations

Documented gaps: "WSL1 was supported through Codex 0.114; starting in 0.115, the Linux sandbox moved to bwrap, so WSL1 is no longer supported" (learn.chatgpt.com/docs/agent-approvals-security.md). Linux/WSL2 requires installing bubblewrap; without it Codex falls back to a helper needing unprivileged user namespaces and warns at startup on AppArmor-restricted distros (learn.chatgpt.com/docs/sandboxing.md). App-server is not production-ready: "The app-server command and WebSocket transport are experimental and aren't supported for production workloads," and non-loopback listeners "allow unauthenticated connections by default during rollout" (learn.chatgpt.com/docs/app-server.md). Maturity labels rate Experimental as "Unstable and OpenAI may remove or change it" (learn.chatgpt.com/docs/feature-maturity.md). The IDE extension does not support plugins (developers.openai.com/codex/plugins.md), and documented OS support is macOS 12+, Ubuntu 20.04+/Debian 10+, or Windows 11 via WSL2 (raw docs/install.md).

## In its own words

> Codex CLI is a coding agent from OpenAI that runs locally on your computer.  
> — [https://raw.githubusercontent.com/openai/codex/main/README.md](https://raw.githubusercontent.com/openai/codex/main/README.md)

> The sandbox applies to spawned commands, not just to built-in file operations. If the agent runs tools like git, package managers, or test runners, those commands inherit the same sandbox boundaries.  
> — [https://learn.chatgpt.com/docs/sandboxing.md](https://learn.chatgpt.com/docs/sandboxing.md)

> We do not accept external code contributions or pull requests.  
> — [https://raw.githubusercontent.com/openai/codex/main/docs/contributing.md](https://raw.githubusercontent.com/openai/codex/main/docs/contributing.md)

> Plugins bundle capabilities into reusable workflows in ChatGPT and Codex. They can include skills and MCP servers. Both products use one universal plugin directory, so the same public plugins are discoverable from their supported surfaces.  
> — [https://developers.openai.com/codex/plugins.md](https://developers.openai.com/codex/plugins.md)


## Notable

Far beyond the "local coding agent" pitch: current releases ship subagents on by default, lifecycle hooks, skills, a plugin browser, local memories, and plan/goal modes — yet OpenAI removed the codex mcp-server binary, so Codex consumes MCP but no longer acts as an MCP server.

## Sources fetched

- https://github.com/openai/codex
- https://raw.githubusercontent.com/openai/codex/main/README.md
- https://raw.githubusercontent.com/openai/codex/main/docs/install.md
- https://raw.githubusercontent.com/openai/codex/main/docs/contributing.md
- https://raw.githubusercontent.com/openai/codex/main/docs/CLA.md
- https://raw.githubusercontent.com/openai/codex/main/docs/license.md
- https://raw.githubusercontent.com/openai/codex/main/LICENSE
- https://raw.githubusercontent.com/openai/codex/main/SECURITY.md
- https://raw.githubusercontent.com/openai/codex/main/docs/open-source-fund.md
- https://raw.githubusercontent.com/openai/codex/main/docs/config.md
- https://raw.githubusercontent.com/openai/codex/main/docs/slash_commands.md
- https://raw.githubusercontent.com/openai/codex/main/docs/getting-started.md
- https://github.com/openai/codex/releases
- https://api.github.com/repos/openai/codex/contents/docs
- https://api.github.com/repos/openai/codex/releases?per_page=6
- https://developers.openai.com/llms.txt
- https://developers.openai.com/codex/llms.txt
- https://developers.openai.com/codex/cli/
- https://developers.openai.com/codex/cli.md
- https://developers.openai.com/codex/cli/features.md
- https://developers.openai.com/codex/cli/slash-commands.md
- https://developers.openai.com/codex/cli/reference.md
- https://developers.openai.com/codex/agent-approvals-security.md
- https://developers.openai.com/codex/sandboxing.md
- https://developers.openai.com/codex/config-file/config-reference.md
- https://developers.openai.com/codex/plugins.md
- https://developers.openai.com/codex/skills-and-plugins.md
- https://learn.chatgpt.com/docs/app-server.md
- https://learn.chatgpt.com/docs/agent-configuration/agents-md.md
- https://learn.chatgpt.com/docs/agent-configuration/subagents.md
- https://learn.chatgpt.com/docs/customization/memories.md
- https://learn.chatgpt.com/docs/non-interactive-mode.md
- https://learn.chatgpt.com/docs/feature-maturity.md
- https://learn.chatgpt.com/docs/open-source.md
- https://learn.chatgpt.com/docs/sandboxing.md

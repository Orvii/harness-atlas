# Vibe

- **repo:** mistralai/mistral-vibe (the task-referenced github.com/mistralai/vibe returns 404; canonical repo is mistralai/mistral-vibe, description "Minimal CLI coding agent by Mistral")
- **version pin:** `v2.25.8` — GitHub latest release tag via gh api repos/mistralai/mistral-vibe/releases/latest (tag v2.25.8, published 2026-09-23T15:10:39Z); cross-checked against PyPI registry mistral-vibe 2.25.8 (https://pypi.org/pypi/mistral-vibe/json)
- **docs home:** https://github.com/mistralai/mistral-vibe#readme (docs/README.md states: "For basic setup, see the main README"; in-repo docs live under /docs plus 17 ADRs under /docs/adr — there is no standalone docs website)

## What it promises

In its own framing: "Mistral Vibe is a command-line coding assistant powered by Mistral's models. It provides a conversational interface to your codebase, allowing you to use natural language to explore, modify, and interact with your projects through a powerful set of tools." It markets itself as "Highly Configurable: Customize models, providers, tool permissions, and UI preferences through a simple `config.toml` file" while promising safety through tool-execution approval.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | `task` tool delegates to child sessions; built-in `explore` agent plus user-defined agents with agent_type "subagent"; interactive mode shows live subagent status and read-only transcripts. Depth limit of 1 — subagents cannot spawn further subagents. | [src](https://raw.githubusercontent.com/mistralai/mistral-vibe/main/README.md) |
| workflow_orchestration | ◐ partial | Primitives: subagent delegation, run_typescript code mode that calls tools with deterministic replay (recorded time/randomness), and scheduled /loop prompts persisted in session metadata. No teams/DAG/swarm workflow DSL found in docs or code. | [src](https://raw.githubusercontent.com/mistralai/mistral-vibe/main/harness/core/src/core/features/programmatic_tool_calling/tools.rs) |
| mcp | ✅ yes | stdio, http and streamable-http transports; OAuth or static auth; per-tool permissions (ask/always/never) and enabled/disabled globs; /mcp add/remove shell commands, /mcp browser; plugins can ship MCP servers; connectors panel alongside. | [src](https://raw.githubusercontent.com/mistralai/mistral-vibe/main/README.md) |
| hooks_lifecycle | ◐ partial | Exactly three events — pre_tool, post_tool, post_agent (HookType enum in vibe/core/hooks/models.py); no session start/stop hooks. Project (.vibe/hooks.toml, trusted-only) and user (~/.vibe/hooks.toml) scopes; subagents inherit parent hook config; plugins can ship hooks. | [src](https://raw.githubusercontent.com/mistralai/mistral-vibe/main/README.md) |
| skills | ✅ yes | SKILL.md + YAML frontmatter; discovered in .agents/skills, .vibe/skills, ~/.vibe/skills, tool search paths and plugins; slash-command or model-invoked; skills can be toggled in /skills browser and marked explicit-only; ships a builtin `vibe` skill that documents the app's own internals. | [src](https://raw.githubusercontent.com/mistralai/mistral-vibe/main/README.md) |
| memory_persistence | ◐ partial | No learned cross-session memory store or memory tool found in docs or builtin toolset. Continuity comes from session resume, AGENTS.md project instructions, plugin knowledge folders (KNOWLEDGE.md), and the per-session scratchpad that survives compaction within one session. | [src](https://raw.githubusercontent.com/mistralai/mistral-vibe/main/CHANGELOG.md) |
| sandboxing | ◐ partial | Permission machinery: per-tool ask/always/never, agent presets (ask/plan/accept-edits/auto-approve), --yolo bypass, shell-command analysis, protected-path escalation. No OS-level sandbox — the repo's own _protected_paths.py says the check is "a heuristic, not a boundary ... only an OS sandbox can make that a guarantee"; code-mode TypeScript sandbox has no filesystem/network access. | [src](https://raw.githubusercontent.com/mistralai/mistral-vibe/main/README.md) |
| plan_mode | ✅ yes | Built-in read-only `plan` agent (write/edit allowed only under plans dir); `exit_plan_mode` tool is enabled only for that agent and surfaces the plan for review/approval; live-editable plan display with Ctrl+G; default_agent configurable to "plan". | [src](https://raw.githubusercontent.com/mistralai/mistral-vibe/main/CHANGELOG.md) |
| background_tasks | ✅ yes | Managed shell sessions with background=true + polling/stdin; dedicated background_processes feature in the Rust harness core; subagents run independently while the parent continues; /loop schedules recurring prompts that fire when the agent is idle. | [src](https://raw.githubusercontent.com/mistralai/mistral-vibe/main/README.md) |
| ide_integration | ✅ yes | Documented setups for Zed, JetBrains AI Assistant (2025.3+ registry or acp.json), and Neovim via avante.nvim; official VS Code extension shipped as `mistralai.mistral-vibe-code` (changelog: scheduled loops and a session status panel in the extension). No standalone JetBrains plugin beyond the AI Assistant integration. | [src](https://raw.githubusercontent.com/mistralai/mistral-vibe/main/docs/acp-setup.md) |
| model_agnostic | ✅ yes | Defaults: Mistral API (mistral-medium-3.5 / mistral-vibe-cli-latest) plus local llama.cpp Devstral. [[providers]] config with api_base/api_style/extra_headers; adapter registry covers openai, openai-responses, anthropic and vertex-anthropic (vibe/core/llm/backend/generic.py); README covers Mistral-compatible custom domains. | [src](https://raw.githubusercontent.com/mistralai/mistral-vibe/main/CHANGELOG.md) |
| plugins | ✅ yes | Agent Plugins 1.0 schema (plugin.json); project (.vibe/plugins, trusted-only) and user (~/.vibe/plugins) scopes; /plugins + /reload-plugins; adapters import Claude Code, Codex, Kimi and OpenCode plugin packages (skills + MCP only, executable code refused); ADR 0007 calls filesystem plugin support an optional backend capability. | [src](https://raw.githubusercontent.com/mistralai/mistral-vibe/main/vibe/plugins/builtins/vibe/skills/vibe/SKILL.md) |
| session_resume | ✅ yes | --resume opens an interactive session picker or resumes by ID (partial matching); /resume and /continue inside the TUI; sessions deletable; scoped per directory; unified harness lists legacy sessions with provenance tags for cross-harness resume; resumed sessions keep their pinned model and permission mode. | [src](https://raw.githubusercontent.com/mistralai/mistral-vibe/main/README.md) |
| cost_controls | ✅ yes | Also --max-tokens (cumulative prompt+completion budget) and --max-turns; per-model input/output/cached token pricing in config and allowed_models filters; /status shows cache-hit usage and session cost with cached-token discounts; VS Code status panel shows steps, tokens, tokens/sec, context and cost. | [src](https://raw.githubusercontent.com/mistralai/mistral-vibe/main/README.md) |

## Architecture

One Python app server (`vibe-app-server`) owns runtime, sessions and tools; every front end is a client speaking newline-delimited JSON-RPC 2.0 on stdio (ADR 0009/0002). Surfaces: Textual TUI (`vibe`), programmatic `-p` mode, `vibe-acp` for ACP editors, a Rust `vibe-rs` thin-client TUI, the `mistralai.mistral-vibe-code` VS Code extension, and Vibe Desktop. The agent loop is an event-driven async generator emitting typed events for output, tool calls, approvals, compaction, plan review and hooks (ADR 0003); tools are typed and permissioned. Two backends coexist: legacy Python `AgentLoop` and the Rust "Unified Harness" core with a Python runtime (`harness/core`, `harness/runtimes/python`); harness-core execution is replay-deterministic (checkpoints, recorded time/randomness), chosen at session creation with `--legacy-harness` as escape hatch.

## Context management

Compaction is the core mechanism: each model carries `auto_compact_threshold` (200,000 for the default Mistral Medium 3.5 config); `/compact` accepts extra instructions and a custom `compaction_prompt_id` (built-in prompt `prompts/compact.md`); after compaction, requests use the compacted context followed by newer messages. Oversized tool output is absorbed by the harness `large_output` feature with paged reads. Subagents encapsulate exploration in child sessions that return only results, "preventing the context from being overloaded". Unified-harness sessions pin a live todo plan and keep a per-session scratchpad whose notes are re-stated after summarization; `/status` and the VS Code panel expose context/token/cache usage.

## Ecosystem

Install via uv/pip (`mistral-vibe` on PyPI), Homebrew, or `curl -LsSf https://mistral.ai/vibe/install.sh | bash`. Editor reach: VS Code marketplace extension `mistralai.mistral-vibe-code`, JetBrains AI Assistant agent registry (2025.3+), Zed's ACP agent directory, avante.nvim. Extensions follow ADR 0007's explicit families: skills (Agent Skills specification, agentskills.io), MCP servers, lifecycle hooks, connectors (Mistral Studio-managed), custom tools (deprecated in favor of skills), and plugins — filesystem packages in the Agent Plugins 1.0 format under `.vibe/plugins/` and `~/.vibe/plugins/`, with adapters importing Claude Code, Codex, Kimi and OpenCode plugin packages (skills + MCP only). A builtin `vibe` skill documents the app's own internals for the agent.

## Governance

Owned by Mistral AI (GitHub org `mistralai`), Apache-2.0 license, repo created 2025-12-08. Actively maintained: last push 2026-10-03; 12 releases between 2026-08-18 and 2026-09-23 (latest v2.25.8, 2026-09-23) — roughly 2-3 per week; PyPI version matches the GitHub tag. 5,046 stars, 356 open issues. CONTRIBUTING.md and SECURITY.md present; changelog credits outside contributors and merged community plugin-format work. Governance is single-vendor: decisions land as numbered in-repo ADRs (17 as of this release), written for agents as much as humans; no foundation or multi-vendor steering is documented.

## Limitations

README warns Vibe "works on Windows, but we officially support and target UNIX environments." No OS-level sandbox: protected-path interception is "a heuristic, not a boundary ... only an OS sandbox can make that a guarantee"; enforcement is permission prompts, trust folders and shell-command analysis. Subagents cannot spawn subagents (depth limit 1). Foreign plugin packages are capped at skills and MCP — hooks/knowledge/agents/libraries/connectors are native-only, executable plugin code is refused, and plugin support is an optional backend capability (ADR 0007). Custom tools will be deprecated in favor of skills. Docs are in-repo only (README + docs/ + ADRs); the task-referenced github.com/mistralai/vibe 404s — canonical repo is mistralai/mistral-vibe. Telemetry is on by default (opt-out via enable_telemetry); voice mode and several harness features sit behind experimental flags.

## In its own words

> Vibe supports subagents for delegating tasks. Subagents run independently and can perform specialized work without user interaction, preventing the context from being overloaded.  
> — [https://raw.githubusercontent.com/mistralai/mistral-vibe/main/README.md](https://raw.githubusercontent.com/mistralai/mistral-vibe/main/README.md)

> Hooks wire arbitrary shell commands into Vibe's lifecycle to gate, audit, or rewrite agent behavior. No flag is required — declaring a hook is enough.  
> — [https://raw.githubusercontent.com/mistralai/mistral-vibe/main/README.md](https://raw.githubusercontent.com/mistralai/mistral-vibe/main/README.md)

> Vibe extends through explicit mechanisms: agents, subagents, skills, hooks, MCP servers, connectors, custom tools, and config layers.  
> — [https://raw.githubusercontent.com/mistralai/mistral-vibe/main/docs/adr/0007-extension-mechanisms.md](https://raw.githubusercontent.com/mistralai/mistral-vibe/main/docs/adr/0007-extension-mechanisms.md)

> It is a heuristic, not a boundary. It reads the argument text, never a resolved target, so a symlink or a ``git config core.hooksPath /tmp/hooks`` write goes unseen. What it buys is that the ordinary route to a hooks file reaches a human; only an OS sandbox can make that a guarantee.  
> — [https://raw.githubusercontent.com/mistralai/mistral-vibe/main/harness/runtimes/python/python/mistralai_vibe_local_harness/vibe/_protected_paths.py](https://raw.githubusercontent.com/mistralai/mistral-vibe/main/harness/runtimes/python/python/mistralai_vibe_local_harness/vibe/_protected_paths.py)


## Notable

Despite being a Mistral-branded CLI, Vibe ships OpenAI, OpenAI-responses, Anthropic and Vertex-Anthropic API adapters, imports Claude Code / Codex / Kimi / OpenCode plugin packages, and is migrating to a replay-deterministic Rust "Unified Harness" whose TypeScript sandbox runs orchestration code with recorded time and randomness — and the repo the task pointed at (github.com/mistralai/vibe) does not exist; the real one is mistralai/mistral-vibe.

## Sources fetched

- https://raw.githubusercontent.com/mistralai/mistral-vibe/main/README.md
- https://raw.githubusercontent.com/mistralai/mistral-vibe/main/docs/README.md
- https://raw.githubusercontent.com/mistralai/mistral-vibe/main/docs/acp-setup.md
- https://raw.githubusercontent.com/mistralai/mistral-vibe/main/CHANGELOG.md
- https://raw.githubusercontent.com/mistralai/mistral-vibe/main/docs/adr/0002-core-engine-and-delivery-surfaces.md
- https://raw.githubusercontent.com/mistralai/mistral-vibe/main/docs/adr/0003-event-driven-agent-loop.md
- https://raw.githubusercontent.com/mistralai/mistral-vibe/main/docs/adr/0007-extension-mechanisms.md
- https://raw.githubusercontent.com/mistralai/mistral-vibe/main/docs/adr/0011-unified-harness-backend.md
- https://raw.githubusercontent.com/mistralai/mistral-vibe/main/vibe/plugins/builtins/vibe/skills/vibe/SKILL.md
- https://raw.githubusercontent.com/mistralai/mistral-vibe/main/vibe/plugins/builtins/vibe/skills/create-plugin/SKILL.md
- https://raw.githubusercontent.com/mistralai/mistral-vibe/main/harness/core/src/core/features/programmatic_tool_calling/tools.rs
- https://raw.githubusercontent.com/mistralai/mistral-vibe/main/harness/runtimes/python/python/mistralai_vibe_local_harness/vibe/_protected_paths.py
- https://raw.githubusercontent.com/mistralai/mistral-vibe/main/vibe/core/config/models.py
- https://api.github.com/repos/mistralai/mistral-vibe
- https://api.github.com/repos/mistralai/mistral-vibe/releases/latest
- https://pypi.org/pypi/mistral-vibe/json

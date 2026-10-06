# Zed

- **repo:** zed-industries/zed
- **version pin:** `v1.22.0` — GitHub latest-release API: gh api repos/zed-industries/zed/releases/latest returned tag v1.22.0, prerelease=false, published 2026-09-30 (https://github.com/zed-industries/zed/releases/tag/v1.22.0)
- **docs home:** https://zed.dev/docs/ai/overview

## What it promises

"Describe the task, the agent does the rest: discovering context, editing files, and staying on track until it's done." — https://zed.dev/ai. The README frames the product: "Zed is a high-performance, multiplayer code editor from the creators of Atom and Tree-sitter." — https://github.com/zed-industries/zed

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | Built-in spawn_agent tool; each subagent gets the parent's tools and 'the parent agent continues its work' while it runs. agent.subagent_model can override the model (agent-settings page). No user-defined subagent catalog/file format documented on fetched pages. | [src](https://zed.dev/docs/ai/tools) |
| workflow_orchestration | ◐ partial | Threads Sidebar runs multiple threads/agents/projects concurrently with optional Git-worktree isolation and a Threads History; spawn_agent adds delegation. No DAG, script, team, or swarm primitives documented. | [src](https://zed.dev/docs/ai/parallel-agents) |
| mcp | ✅ yes | Handles notifications/tools/list_changed; MCP servers install as extensions, local or remote servers; can be forwarded to External Agents over ACP. Discovery, Sampling, Elicitation not implemented ('We welcome contributions'). | [src](https://zed.dev/docs/ai/mcp) |
| hooks_lifecycle | ✗ no | Only a Git-worktree task hook exists. No pre/post-tool, session start/stop, or prompt hooks documented anywhere on fetched pages. | [src](https://zed.dev/docs/tasks.html#hooks) |
| skills | ✅ yes | Agent sees a catalog and calls the `skill` tool on demand; slash-command/@-mention invocation; built-in /create-skill; skills.sh community registry; self-contained zed://skill sharing links; permission prompts for non-built-in skills. | [src](https://zed.dev/docs/ai/skills) |
| memory_persistence | ◐ partial | Persistent personal ~/.config/zed/AGENTS.md plus project instruction files (AGENTS.md, .rules, CLAUDE.md, .cursorrules, GEMINI.md...), and Thread History restores past threads. No agent-written long-term memory subsystem documented. | [src](https://zed.dev/docs/ai/instructions) |
| sandboxing | ✅ yes | Covers the Zed Agent terminal and fetch tools only (not LSPs, extensions, tasks, External Agents). macOS Mach-service allowlist + proxy network control; Linux non-setuid Bubblewrap; sandbox approval prompts and persistent agent.sandbox_permissions. Native Windows unsandboxed (WSL Bubblewrap used instead). | [src](https://zed.dev/docs/ai/sandboxing) |
| plan_mode | ✗ no | Ask is a read-only profile, but no explicit plan-then-approve workflow or Plan profile is documented; profiles select tools/model, tool permissions gate execution. | [src](https://zed.dev/docs/ai/agent-profiles) |
| background_tasks | ✅ yes | Threads and Terminal Threads run independently while you work (parallel-agents page); spawned subagents continue while the parent works; settings agent.notify_when_agent_waiting / agent.play_sound_when_agent_done; keep-system-awake option. | [src](https://zed.dev/docs/ai/agent-panel) |
| ide_integration | ✗ no | Zed is itself the IDE; no first-party VS Code or JetBrains extension for Zed's agent exists on fetched pages. ACP is the reverse direction: JetBrains/VS Code run third-party ACP clients hosting other ACP agents, not the Zed Agent. | [src](https://agentclientprotocol.com/get-started/clients) |
| model_agnostic | ✅ yes | LLM Providers page details Zed-hosted billing, API access (Anthropic, OpenAI, Google...), existing subscriptions (ChatGPT/Claude/Copilot), gateways (OpenRouter, Bedrock, Vercel), and local/self-hosted models; External Agents own their own model config. | [src](https://zed.dev/docs/ai/overview) |
| plugins | ✅ yes | Extension types: languages, themes, icon themes, snippets, debuggers, MCP-server extensions; published at zed.dev/extensions; procedural parts compiled to WebAssembly (wasm32-wasip2) and governed by a capability system. | [src](https://zed.dev/docs/extensions) |
| session_resume | ✅ yes | Thread search (fuzzy on titles), archived threads restorable, plus importing existing external-agent threads (Cursor and Gemini CLI import not supported). | [src](https://zed.dev/docs/ai/agent-panel) |
| cost_controls | ◐ partial | Pricing page: Pro $10/mo with $5 of tokens included then usage-based billing; Business $30/seat adds org-wide AI policies and unified spend visibility; Personal $0 (2,000 accepted edit predictions). No per-thread token limits or hard spend caps documented. | [src](https://zed.dev/docs/ai/agent-panel#token-usage) |

## Architecture

Zed is a native desktop app written from scratch in Rust; the homepage stresses it is "Written from scratch in Rust to efficiently leverage multiple CPU cores and your GPU" (https://zed.dev). The repo is a Cargo workspace whose crates — gpui, agent, agent_skills, acp_thread, context_server, extension_host — mirror the AI stack (https://raw.githubusercontent.com/zed-industries/zed/main/Cargo.toml). The native Zed Agent runs in-process; External Agents "run as separate processes that communicate with Zed over ACP" (https://zed.dev/docs/ai/external-agents); the terminal tool "creating a new shell process for each invocation" (https://zed.dev/docs/ai/tools); MCP servers are configured local/remote processes; extensions compile to WebAssembly wasm32-wasip2 (https://zed.dev/docs/extensions/developing-extensions).

## Context management

Each thread has its own context window and a visible token counter near the profile selector. Zed auto-compacts at 90% of the model window by default (agent.auto_compact; percentage, absolute, or remaining-token thresholds), summarizing earlier messages into an expandable "Context Compacted" entry; /compact triggers it manually and agent.compaction_model can offload summarization. "New From Summary" seeds a fresh thread from a summary, and past threads can be @-mentioned as context. Persistent guidance lives in AGENTS.md (personal and project) with .rules/.cursorrules/CLAUDE.md compatibility. Models with windows under 80,000 tokens get a banner suggesting a new thread instead (https://zed.dev/docs/ai/agent-panel, https://zed.dev/docs/ai/agent-settings, https://zed.dev/docs/ai/instructions).

## Ecosystem

Capability distributes via extensions: languages, themes, snippets, debuggers, icon themes, and MCP-server extensions hosted at zed.dev/extensions and gated by a capability system (https://zed.dev/docs/extensions, https://zed.dev/docs/extensions/capabilities). Skills are a second ecosystem — built-in create-skill flow, the community skills.sh registry, and self-contained zed://skill sharing links (https://zed.dev/docs/ai/skills). External agents install from an in-editor ACP Registry (https://zed.dev/docs/ai/external-agents), and Zed's ACP page lists roughly 40 agents plus editors including JetBrains IDEs, VS Code, and Neovim (https://zed.dev/acp). No numeric extension count appears on any fetched page.

## Governance

Owned by Zed Industries, Inc.; source is "licensed primarily under GPL-3.0-or-later, with Apache-2.0 components where marked" (https://github.com/zed-industries/zed). Contributors sign a CLA, keep at most three open PRs, discuss features with staff first, and — notably — "we don't accept contributions from autonomous agents", with rules for disclosing LLM-written contributor communication (https://github.com/zed-industries/zed/blob/main/CONTRIBUTING.md, https://zed.dev/cla). Stable and preview channels ship on a "weekly releases" cadence per https://zed.dev/pricing; the latest stable tag fetched via the GitHub API was v1.22.0, published 2026-09-30.

## Limitations

Sandboxing applies only to Zed Agent's terminal and fetch tools — not Zed itself, language servers, extensions, tasks, normal terminals, External Agents, or Terminal Threads; native Windows processes cannot be OS-sandboxed, so WSL's Bubblewrap is used and NTFS paths may weaken write confinement (https://zed.dev/docs/ai/sandboxing). MCP supports only Tools and Prompts — Discovery, Sampling, and Elicitation are unimplemented (https://zed.dev/docs/ai/mcp). Agent Panel features like thread restore, checkpoints, and token display "depend on the agent integration" for External Agents (https://zed.dev/docs/ai/agent-panel); thread import excludes Cursor and Gemini CLI; web builds are unavailable (README); there is no plan mode — just Write/Ask/Minimal profiles.

## In its own words

> Zed is a minimal code editor crafted for speed and collaboration with humans and AI.  
> — [https://zed.dev](https://zed.dev)

> Zed is a high-performance, multiplayer code editor from the creators of Atom and Tree-sitter.  
> — [https://github.com/zed-industries/zed](https://github.com/zed-industries/zed)

> The Agent Client Protocol (ACP) is an open standard that enables any agent to integrate seamlessly with any editing environment.  
> — [https://zed.dev/acp](https://zed.dev/acp)

> This does not rely on an agent following a particular set of instructions. If the agent attempts to access a resource that is restricted by the sandbox, the OS will block it.  
> — [https://zed.dev/docs/ai/sandboxing](https://zed.dev/docs/ai/sandboxing)


## Notable

A product built around agentic coding explicitly "don't accept contributions from autonomous agents" (CONTRIBUTING.md) and bans undisclosed LLM-written PR discussion — a governance stance stricter than most AI-first editors ship.

## Sources fetched

- https://zed.dev/docs/ai/overview
- https://zed.dev/docs/ai/agent-panel
- https://zed.dev/docs/ai/tools
- https://zed.dev/docs/ai/tool-permissions
- https://zed.dev/docs/ai/sandboxing
- https://zed.dev/docs/ai/instructions
- https://zed.dev/docs/ai/skills
- https://zed.dev/docs/ai/agent-profiles
- https://zed.dev/docs/ai/agent-settings
- https://zed.dev/docs/ai/mcp
- https://zed.dev/docs/ai/parallel-agents
- https://zed.dev/docs/ai/external-agents
- https://zed.dev/docs/ai/llm-providers
- https://zed.dev/docs/ai/terminal-threads
- https://zed.dev/docs/tasks
- https://zed.dev/docs/extensions
- https://zed.dev/docs/extensions/developing-extensions
- https://zed.dev/docs/extensions/capabilities
- https://zed.dev/docs/windows
- https://zed.dev
- https://zed.dev/ai
- https://zed.dev/pricing
- https://zed.dev/cla
- https://zed.dev/acp
- https://agentclientprotocol.com/get-started/clients
- https://agentclientprotocol.com/llms.txt
- https://github.com/zed-industries/zed (README, CONTRIBUTING.md, Cargo.toml raw)
- https://github.com/zed-industries/zed/releases/tag/v1.22.0

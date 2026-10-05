# Amazon Kiro

- **repo:** AWS — kiro.dev (closed-source IDE/CLI; official GitHub org: kirodotdev, home of open-source Kiro Crew)
- **version pin:** `Kiro CLI 2.27.0 (Oct 1, 2026); Kiro IDE 1.2.4 (Sep 30, 2026); Kiro Crew 0.7.2 (Sep 28, 2026); latest changelog entry Oct 2, 2026 (Claude Sonnet 5.5 rollout). KiroCrew insider release: v0.8.0-insider.12 (Oct 4, 2026)` — Kiro's IDE and CLI are closed source with no public release tags, so vendor documentation is the source: the official changelog at https://kiro.dev/changelog/ pins Kiro CLI 2.27.0 (Oct 1, 2026), Kiro IDE 1.2.4 (Sep 30, 2026), and Kiro Crew 0.7.2 (Sep 28, 2026). The only public release stream, the Apache-2.0 repo kirodotdev/KiroCrew (https://github.com/kirodotdev/KiroCrew/releases), runs ahead on its insider channel at v0.8.0-insider.12 (Oct 4, 2026).
- **docs home:** https://kiro.dev/docs/

## What it promises

Kiro's pitch is structure for AI coding: spec-driven development turns an idea into requirements, design, and tracked tasks, carried out by one agent that follows the developer across IDE, terminal, web, and phone. Its documentation now frames that as sustainable autonomy — workflows that coordinate reviewer agents in the background, cloud sandbox sessions that keep working after the laptop closes, steering files that hold every surface to team standards, and memory that lets the agent learn from feedback instead of being retaught.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | Automatic and explicit invocation on IDE, CLI, Web, and Mobile; built-in context-gathering and general-purpose sub-agents; any custom agent can be invoked as a sub-agent; parallel execution plus upfront-planned DAG task dependencies; shares steering, MCP servers, workspace access and permissions while isolating conversation history. Crew adds kirocrew spawn run --async background subagents with an Activity panel. | [src](https://kiro.dev/docs/custom-agents/subagents/) |
| workflow_orchestration | ✅ yes | Declarative JSON/YAML recipes stored in .kiro/workflows/, with handoffs, loops, waits, and completion conditions; agent-authored from a single prompt; per-step custom agents, model, and thinking effort; each step runs in its own session with fresh context; runs in background with pause/resume/steer; bundled investigate, feature-pipeline, and publish-pr recipes; opt-in in every client. Crew layers Python-script workflows (fan-out, pipeline, judge-and-verify patterns) plus a Task Runner that decomposes a markdown spec into retried, git-committed, independently reviewed steps. | [src](https://kiro.dev/docs/workflows/) |
| mcp | ✅ yes | Local stdio and remote HTTP/SSE servers, JSON config, server-provided prompts and resources via # mentions on IDE/CLI/Web; server elicitation requests supported; enterprise MCP registry allow-lists with organization/account-level override; Powers bundle MCP servers with on-demand loading; Crew exposes its own MCP tools (cron_add, task_run, spawn). | [src](https://kiro.dev/docs/mcp/) |
| hooks_lifecycle | ✅ yes | Triggers include Prompt Submit, Agent Stop, Session Start, Session End (CLI V3), Agent Spawn, Pre Tool Use, Post Tool Use, File Create/Save/Delete, Pre/Post Task Execution, and Manual; shell-command or agent-prompt actions with exit-code semantics (exit 0 output can be injected into context); JSON files under .kiro/hooks/; Crew mirrors the trigger set with context injection. | [src](https://kiro.dev/docs/hooks/) |
| skills | ✅ yes | Workspace skills in .kiro/skills/ and global skills in ~/.kiro/skills/ (workspace-only on Web/Mobile); progressive disclosure loads only name/description at startup, full instructions on match; importable from the community or other compatible AI tools; saved prompts invokable as slash commands; Crew ships built-in skills with always-on, on-demand, or trigger modes and imports whole skill sets from public GitHub repositories. | [src](https://kiro.dev/docs/skills/) |
| memory_persistence | ✅ yes | Web memory is maintained automatically from user feedback, visible in Settings, and deletable; steering files provide persistent project context on every surface, with global and workspace scope; CLI auto-saves sessions per directory; Crew implements six memory layers (preferences, projects, recent history with 3-tier decay, confidence-gated semantic key-values, FAISS-backed episodic vectors, and lessons where user-explicit corrections always win). | [src](https://kiro.dev/docs/web/memory/) |
| sandboxing | ✅ yes | Two complementary models: capability-based permissions on IDE/CLI (fs_read, fs_write, shell, mcp, subagent, skill, power match rules with deny/ask/allow effects, deny always winning, global plus workspace scopes, YAML config) and a per-task cloud sandbox for Web/Mobile/cloud sessions with configurable internet domain access. CLI 3.0 replaces 2.x trust flags with permissions.yaml and defaults to prompting when no policy exists; sandbox includes headless Chrome with Playwright MCP, agent-browser, and Chrome DevTools MCP. | [src](https://kiro.dev/docs/web/sandbox/) |
| plan_mode | ✅ yes | Specs run a three-phase workflow producing requirements.md/bugfix.md, design.md, and tasks.md in .kiro/specs/, with approval gates in the standard variants (Quick Spec explicitly skips approval gates); a task execution interface tracks per-task status and supports interactive stepping; Autopilot is the autonomous default while Supervised mode yields for per-hunk approval after each turn that edits files; Crew's Task Runner decomposes a markdown spec into test-verified, retried, independently reviewed steps. | [src](https://kiro.dev/docs/specs/) |
| background_tasks | ✅ yes | Cloud sessions detach and reattach across IDE, CLI, Web, and Mobile (up to 10 concurrent) and the loop runs server-side; workflows run in the background while the parent conversation continues; CLI headless mode runs non-interactive prompts in CI/CD with KIRO_API_KEY; the experimental delegate tool launches background chat sessions (deprecated in favor of subagents); Crew runs cron jobs, heartbeats, 10+ hour Task Runner loops, and a gateway installable as a systemd/launchd service or Docker container; Web automations execute on a schedule. | [src](https://kiro.dev/docs/cloud-sessions/) |
| ide_integration | ✅ yes | Kiro ships its own VS Code-fork desktop IDE rather than a plugin for someone else's editor: VS Code profile, extension, theme, and keybinding migration works out of the box, and the IDE uses the Open VSX extension marketplace. The CLI doubles as a client that connects third-party editors — JetBrains IDEs and Zed — and custom integrations through ACP; an iOS app in early access steers cloud sessions from a phone. | [src](https://kiro.dev/docs/ide/) |
| model_agnostic | ✅ yes | Anthropic Claude Opus 5.5/5/4.8/4.7/4.6/4.5, Sonnet 5.5/5/4.6/4.5/4.0, Haiku 4.5; OpenAI GPT-5.6 Sol/Terra/Luna; open-weight DeepSeek 3.2, MiniMax M2.5/M2.1, GLM-5, Qwen3 Coder Next; Auto routing picks a model per task; per-model credit multipliers from 0.05x (Qwen3 Coder Next) to 6x (Claude Fable 5.1 preview); inference geographies US and EU, with some models US East only; model selection is available for chat experiences (interactive and non-interactive). | [src](https://kiro.dev/docs/models/) |
| plugins | ✅ yes | Powers follow the open Agent Plugins specification (plugin.json plus skills and MCP server definitions) and install from the kiro.dev/powers marketplace one-click, from GitHub repositories, or local builds, with create-and-share support; the IDE inherits VS Code's Open VSX extension marketplace and supports custom or private registries via OS policy (ExtensionGalleryServiceUrl); enterprise MCP registry governs which servers may be added; Crew imports skills from public GitHub repositories. | [src](https://kiro.dev/docs/powers/) |
| session_resume | ✅ yes | Resume via kiro-cli chat --resume, --resume-picker, --resume-id, or --list-sessions, with per-directory storage in a local database under ~/.kiro/; V3 --resume picks the newest matching local or cloud session; rewind forks the conversation at an earlier turn into a new session without touching files; checkpoints restore files and context together (IDE, experimental on CLI v2); cloud sessions resume from any surface, including the phone. | [src](https://kiro.dev/docs/cli/chat/session-management/) |
| cost_controls | ✅ yes | Credits are consumed fractionally per request: Free 50, Pro 1,000, Pro+ 2,000, Pro Max 5,000, Power 10,000, with purchasable add-on credits on paid tiers; per-model credit multipliers are documented (0.05x to 6x baseline); proactive notifications fire at 80% of monthly usage and usage pauses when credits run out; enterprise billing and subscription management are separate; cloud compute for cloud sessions is included at no extra charge. | [src](https://kiro.dev/docs/billing/) |

## Architecture

One unified agent harness sits behind every Kiro surface: the VS Code-based desktop IDE, the terminal CLI, the web app, and the iOS app are all ACP clients of the same agent, which orchestrates conversations, executes tools, manages context, evaluates permissions, and talks to the LLM providers. IDE and CLI runs execute locally on the developer's machine; Kiro Web, Mobile, and opt-in cloud sessions run that harness server-side in an AWS-managed sandbox — the loop keeps running after you disconnect — where repositories are cloned and a headless Chrome with Playwright and Chrome DevTools MCP is available. Accounts can run up to 10 concurrent cloud sessions (https://kiro.dev/docs/how-kiro-works/, https://kiro.dev/docs/cloud-sessions/, https://kiro.dev/docs/web/sandbox/).

## Context management

Kiro pairs large windows — 1M tokens on most current models — with automated compaction: when a session nears its limit, older history is replaced by a structured summary of goals, decisions, and progress while recent messages stay verbatim, surfaced through a context usage meter and a manual /compact command in the CLI. Sub-agents and workflow steps each run with fresh, isolated context, inheriting steering, MCP servers, and permissions but not conversation history. Skills and Powers load progressively; steering files apply globally or by match; checkpoints and rewind roll context back or fork it; Crew injects six memory layers into a roughly 55K-token window (https://kiro.dev/docs/compaction/, https://kiro.dev/docs/custom-agents/subagents/, https://kiro.dev/docs/skills/, https://kiro.dev/docs/crew/features/memory/).

## Ecosystem

Extensions distribute through several channels. Powers follow the Agent Plugins specification, bundling context, skills, and MCP servers; they install in one click from the kiro.dev/powers marketplace, from GitHub repositories, or from code you write. Skills follow the open agentskills.io standard, so packages port between compatible agents; steering markdown and AGENTS.md carry project rules; MCP servers come from the wider MCP ecosystem with an enterprise registry for allow-lists. The IDE inherits VS Code's Open VSX marketplace, with custom registries configurable by OS policy. ACP lets JetBrains IDEs, Zed, and custom clients attach to the same harness. Kiro Crew is open source under Apache-2.0, with GitHub releases and skill imports from repositories (https://kiro.dev/docs/powers/, https://kiro.dev/docs/skills/, https://kiro.dev/docs/mcp/registry/, https://kiro.dev/docs/ide/editor/extension-registry/, https://kiro.dev/docs/acp/, https://github.com/kirodotdev/KiroCrew).

## Governance

Kiro is an AWS-owned, closed-source product: the IDE and CLI ship as proprietary binaries, vendor documentation is the authoritative source, and no public source repository exists for them; the verified kirodotdev GitHub organization hosts the open-source Kiro Crew component under Apache-2.0. Kiro is the declared continuation of Amazon Q Developer CLI — Q CLI auto-updated to Kiro CLI from November 2025 with subscriptions intact — while Q Developer IDE extension users get migration guides. Enterprise governance spans model allow-lists, an MCP server registry, API key enablement, web-tool disablement, sign-in controls through IAM Identity Center, Okta, or Microsoft Entra ID, managed-settings.json policies, OpenTelemetry monitoring, and prompt logging (https://kiro.dev/docs/privacy-and-security/, https://kiro.dev/docs/upgrade-guides/migrating-from-q/, https://kiro.dev/docs/enterprise/governance/, https://github.com/kirodotdev/KiroCrew).

## Limitations

Surface-coverage tables show real gaps: Mobile supports only built-in sub-agents — no custom agents, no hooks, and no MCP — and cloud sessions cap at 10 concurrent, with IDE attach requiring version 1.0.293+ and CLI attach 2.17+. Workflows are opt-in in every client and consume more tokens than a single session; sub-agent task graphs are planned upfront and cannot be modified during a run. The Free tier offers 50 credits with only some models; API keys and web automations require paid plans, and organizations must enable API keys. Some models are region-restricted, such as the Fable 5.1 enterprise preview in US East only. Third-party ACP editors receive only the standard capabilities their clients implement, and the iOS app is TestFlight early access with detailed documentation still "coming soon" (https://kiro.dev/docs/custom-agents/subagents/, https://kiro.dev/docs/cloud-sessions/, https://kiro.dev/docs/workflows/, https://kiro.dev/docs/mcp/, https://kiro.dev/docs/billing/, https://kiro.dev/docs/mobile/).

## In its own words

> At the center is the unified agent harness, which handles everything an agent run involves: orchestrating the conversation, executing tools, managing context, evaluating permissions, and talking to the LLM providers.  
> — [https://kiro.dev/docs/how-kiro-works/](https://kiro.dev/docs/how-kiro-works/)

> Workflows are graphs of agent steps, sequences, loops, and parallel branches, in a format that people and agents can both read and create.  
> — [https://kiro.dev/docs/workflows/](https://kiro.dev/docs/workflows/)

> A cloud session runs the Kiro agent harness in a managed cloud sandbox instead of on your machine.  
> — [https://kiro.dev/docs/cloud-sessions/](https://kiro.dev/docs/cloud-sessions/)

> Kiro is an AWS application that works as a standalone agentic IDE.  
> — [https://kiro.dev/docs/privacy-and-security/](https://kiro.dev/docs/privacy-and-security/)


## Notable

From a spec-driven VS Code-fork IDE launched in 2025, Kiro has grown into a CLI that absorbed Amazon Q Developer CLI, scheduled cloud-sandbox automations that open pull requests on GitHub or GitLab, open-weight models billed at a twentieth of the baseline rate — and Kiro Crew, an Apache-2.0 self-hosted persistent agent with six memory layers that chats over Slack, Discord, Telegram, and WeChat.

## Sources fetched

- https://kiro.dev/docs/
- https://kiro.dev/llms.txt
- https://kiro.dev/changelog/
- https://kiro.dev/docs/how-kiro-works/
- https://kiro.dev/docs/acp/
- https://kiro.dev/docs/ide/
- https://kiro.dev/docs/ide/chat/autopilot/
- https://kiro.dev/docs/ide/editor/extension-registry/
- https://kiro.dev/docs/cli/
- https://kiro.dev/docs/cli/chat/session-management/
- https://kiro.dev/docs/cli/headless/
- https://kiro.dev/docs/cli/v3/permissions/
- https://kiro.dev/docs/cli/experimental/delegate/
- https://kiro.dev/docs/custom-agents/
- https://kiro.dev/docs/custom-agents/subagents/
- https://kiro.dev/docs/workflows/
- https://kiro.dev/docs/skills/
- https://kiro.dev/docs/hooks/
- https://kiro.dev/docs/hooks/types/
- https://kiro.dev/docs/permissions/
- https://kiro.dev/docs/specs/
- https://kiro.dev/docs/steering/
- https://kiro.dev/docs/mcp/
- https://kiro.dev/docs/mcp/registry/
- https://kiro.dev/docs/powers/
- https://kiro.dev/docs/models/
- https://kiro.dev/docs/models/available-models/
- https://kiro.dev/docs/billing/
- https://kiro.dev/docs/billing/proactive-usage-notifications/
- https://kiro.dev/docs/checkpoints/
- https://kiro.dev/docs/compaction/
- https://kiro.dev/docs/cloud-sessions/
- https://kiro.dev/docs/web/sandbox/
- https://kiro.dev/docs/web/memory/
- https://kiro.dev/docs/web/autonomous-mode/
- https://kiro.dev/docs/web/automations/
- https://kiro.dev/docs/web/setup/
- https://kiro.dev/docs/crew/
- https://kiro.dev/docs/crew/installation/
- https://kiro.dev/docs/crew/features/subagents/
- https://kiro.dev/docs/crew/features/workflows/
- https://kiro.dev/docs/crew/features/memory/
- https://kiro.dev/docs/crew/features/task-runner/
- https://kiro.dev/docs/crew/features/cron/
- https://kiro.dev/docs/crew/capabilities/skills/
- https://kiro.dev/docs/crew/capabilities/hooks/
- https://kiro.dev/docs/crew/capabilities/agents/
- https://kiro.dev/docs/crew/running-24-7/
- https://kiro.dev/docs/enterprise/governance/
- https://kiro.dev/docs/privacy-and-security/
- https://kiro.dev/docs/upgrade-guides/migrating-from-q/
- https://kiro.dev/docs/upgrade-guides/migrating-from-q-developer/
- https://kiro.dev/docs/upgrade-guides/migrating-from-vscode/
- https://kiro.dev/docs/cli/v3/migration-guide/
- https://kiro.dev/docs/mobile/
- https://github.com/kirodotdev/KiroCrew

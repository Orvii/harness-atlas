# Warp

- **repo:** warpdotdev/warp (AGPL-3.0, client source public; issue tracker at warpdotdev/warp)
- **version pin:** `v0.2026.09.30.08.29` — https://docs.warp.dev/changelog/2026/ — fetched live this run; the page's newest release heading is '2026.09.30 (v0.2026.09.30.08.29)', and the changelog index states updates ship weekly, typically on Thursdays.
- **docs home:** https://docs.warp.dev/

## What it promises

Warp presents itself as an agentic development environment born out of the terminal: a real terminal with a built-in coding agent that runs commands, reads their output, and decides what to do next (https://docs.warp.dev/agents/). The same agent is reachable three ways — in the Warp app, through the Warp Agent CLI, and through the cloud Automation Platform — and the docs frame the choice as a matter of where you work, not what the agent can do (https://docs.warp.dev/agents/). Around it Warp sells an orchestration and 'software factory' layer that runs and coordinates agents at scale from triggers, schedules, and integrations (https://docs.warp.dev/platform/overview/).

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | The docs describe a parent/child model in which a parent agent decides what work needs doing, spawns child agents with their own prompt, environment and optionally a different model or runtime, and merges their results; orchestration is supported from the Warp app, the Oz CLI, the Oz web app, and the Warp Platform API. The stated limit is that a child agent does not spawn its own children, so an orchestration is exactly one level deep. | [src](https://docs.warp.dev/platform/orchestration/) |
| workflow_orchestration | ✅ yes | Multi-agent orchestration is a first-class platform primitive: the docs say to coordinate parent and child agents across local and cloud runs to build supervisor/worker, fan-out, critic, DAG, and swarm workflows in Warp. Orchestrations are started with the /orchestrate or /plan slash command in the app, or via the Oz CLI, the Oz web app, or the Warp Platform API, and can be dispatched through factory endpoints when running inside a Warp factory. | [src](https://docs.warp.dev/platform/orchestration/) |
| mcp | ✅ yes | Warp documents MCP support as a way to extend local agents with custom tools and data sources through a standardized interface, and the docs explicitly describe MCP servers as 'essentially acting as plugins for Warp'. MCP server access rules can be set per Agent Profile, and the connection protocols include Streamable HTTP. | [src](https://docs.warp.dev/agents/capabilities/mcp/) |
| hooks_lifecycle | ◐ partial | Warp documents lifecycle-style hooks only outside the interactive agent loop: the self-hosted Direct backend worker calls a configured setup_command and teardown_command around each task workspace, and the terminal supports notification hooks driven by the OSC 9 and OSC 777 escape sequences. A targeted search across the whole documentation set found no pre-tool, post-tool, or agent session start/stop hooks — the overwhelming majority of 'hook' references in Warp's docs are webhooks used as inbound triggers — so there is no hook mechanism for intercepting the agent's own tool calls or session lifecycle. | [src](https://docs.warp.dev/factories/self-hosting/direct-monorepo-worktrees/) |
| skills | ✅ yes | Skills let you create reusable, shareable instructions that agents can invoke when performing tasks, with project and global scopes and automatic discovery so agents are aware of all available skills. Warp also maintains a public collection of ready-to-use skills in the warpdotdev/oz-skills repository, and ships packaged skills such as a bundled modify-settings skill. | [src](https://docs.warp.dev/agents/capabilities/skills/) |
| memory_persistence | ◐ partial | Agent Memory is a persistent memory system that lives on Warp and is shared across supported agent harnesses — the built-in Warp Agent, Claude Code, Codex and others — so durable facts, decisions and outcomes from one conversation are available to the next. The limitation is availability, not capability: the page carries a caution that Agent Memory is in research preview and is enabled per team for design partners, with a waitlist to request access, and memory creation and retrieval run asynchronously. | [src](https://docs.warp.dev/agents/agent-memory/) |
| sandboxing | ✅ yes | Agent Profiles bound the agent with per-action autonomy levels — Agent Decides, Always ask, Always allow, and Never — applied to distinct permission types including applying code diffs, reading files, creating plans, executing commands and interacting with running commands. Command allowlists (empty by default) let matching commands auto-execute without confirmation, while a command denylist takes precedence over the other permission settings; cloud agent runs additionally execute in a Warp-hosted sandbox metered as compute credits. | [src](https://docs.warp.dev/agents/capabilities/agent-profiles-permissions/) |
| plan_mode | ✅ yes | Planning is native: the /plan slash command (or a natural-language request) generates a structured plan in a persistent rich-text plan editor with version history, and every agent edit creates a new version that can be compared and restored. Execution is explicitly gated on the user — 'When you're ready to start implementing, prompt the agent to run the plan' — and you can execute the full step set or only a named section such as 'Implement phase 1 of the plan', so the plan is reviewed and edited before anything runs. | [src](https://docs.warp.dev/agents/capabilities/planning/) |
| background_tasks | ✅ yes | Cloud agents are described as autonomous, background agents that run on Warp's cloud infrastructure or your own, triggered by system events, schedules or integrations like Slack and GitHub. Scheduled Agents additionally run unattended on a cron expression, each starting a fresh session, executing a fixed prompt, producing inspectable task and session history, and able to be paused, updated or deleted at any time. | [src](https://docs.warp.dev/platform/) |
| ide_integration | ✗ no | Warp is a standalone application rather than an IDE extension, and the docs state this directly in the VS Code migration guide: 'Warp doesn't have a VS Code importer because it's a standalone application, not a VS Code extension.' The documented path is to run Warp alongside VS Code as a richer terminal or to replace both with Warp's own built-in code editor; there is no VS Code or JetBrains extension in the documentation, and the migration guides cover moving away from the VS Code integrated terminal, Cursor, iTerm2, Ghostty, and Windows Terminal rather than integrating with them. | [src](https://docs.warp.dev/getting-started/migrate-to-warp/migrate-to-warp-from-vs-code-terminal/) |
| model_agnostic | ✅ yes | Warp lets you choose from a curated set of LLMs, with models from OpenAI, Anthropic, Google and open source providers available alongside configurable reasoning levels and per-profile defaults. It also offers Auto routing variants (auto, auto-efficient, auto-genius, auto-open), custom routers that pick a model per task using your own logic, and enterprise Bring Your Own LLM routing through AWS Bedrock or Google Cloud via Gemini Enterprise. | [src](https://docs.warp.dev/agents/inference/model-choice/) |
| plugins | ◐ partial | Warp documents no plugin or extension API of its own; the single extension surface it describes is MCP, with the docs framing MCP servers as 'essentially acting as plugins for Warp' and referring to them elsewhere as plugin-like modules. The other artifacts Warp calls plugins point the other way: Warp ships auto-installed notification plugins into third-party CLI agents such as Claude Code and OpenCode (for plugin source see the warpdotdev/claude-code-warp GitHub repository), rather than exposing plugin hooks for developers to extend Warp itself. | [src](https://docs.warp.dev/agents/capabilities/mcp/) |
| session_resume | ✅ yes | Conversations persist as you work and can be resumed after exiting: the CLI prints the exact command to continue, 'warp --resume YOUR_CONVERSATION_TOKEN', where the token is a conversation identifier generated by Warp. The docs also cover compacting context with /compact in long conversations, and the CLI can hand a local conversation off to a cloud agent or pick a finished cloud run back up in the terminal, which extends resumption across local and cloud execution. | [src](https://docs.warp.dev/agents/cli/agent-conversations/) |
| cost_controls | ✅ yes | Warp meters all agent work through credits split into three buckets — AI credits for the model call, compute credits for the sandbox an agent runs in, and platform credits for run lifecycle, integrations, dashboard, APIs and observability — with all three drawing from one pool managed under Settings > Billing and usage. Plans include a monthly allowance, add-on credit purchases, auto-reload, and a documented budget-exceeded error, and the model list itself is cost-aware (auto-efficient optimizes for lower credit consumption while auto-genius notes that it may consume credits more quickly). | [src](https://docs.warp.dev/support-and-community/plans-and-billing/credits/) |

## Architecture

Warp is a native desktop terminal application with a coding agent embedded in it, installed on macOS, Windows and Linux via a download, Homebrew (brew install --cask warp), WinGet (winget install Warp.Warp), or Debian/Ubuntu .deb packages backed by the Warp apt repository and signing key (https://docs.warp.dev/getting-started/quickstart/installation-and-setup/). Three surfaces reach the same agent — the Warp app, the Warp Agent CLI, and the cloud Automation Platform — and the docs frame the choice as depending on where you work rather than what the agent can do (https://docs.warp.dev/agents/). The agent itself is built to work through multi-step tasks on its own, running commands in a real terminal and using the output to decide what to do next, with a capability set covering planning, skills, rules, slash commands, agent notifications, codebase context, full terminal use, computer use and MCP (https://docs.warp.dev/agents/capabilities/). Above the single agent sits a platform layer: the Automation Platform is Warp's programmable system for running and coordinating agents at scale, where a trigger fires (a schedule, an integration event such as a Slack mention or CI failure, an API call, or a manual start), Warp creates a tracked task carrying the trigger's context, the agent executes on a host optionally inside an environment defining its image, repos and setup, and the task produces outputs such as a pull request, a Slack reply, a report, or a transcript and summary (https://docs.warp.dev/platform/overview/). Orchestration sits on a parent/child model: one parent agent spawns one or more child agents, each with its own prompt, environment and optionally a different model or agent runtime, and each with an independent run and its own log, with the constraint that orchestrations are exactly one level deep because a child does not spawn its own children (https://docs.warp.dev/platform/orchestration/). Beyond orchestration the platform extends into Warp Factories, which run 'software factories' with agent roles and definitions-as-code, and into a self-hosting story where an oz-agent-worker daemon can run tasks on Docker, Kubernetes, Direct or Command backends, including a documented pattern of one Git worktree per Direct backend task driven by setup and teardown hooks (https://docs.warp.dev/factories/self-hosting/direct-monorepo-worktrees/). Enterprise deployments separate a control plane (orchestration, observability, LLM inference) from an execution plane (where agents run, code is accessed and commands execute), letting teams choose where sensitive workloads execute (https://docs.warp.dev/enterprise/enterprise-features/architecture-and-deployment/). Warp's client source is published under AGPL v3 at warpdotdev/warp (https://docs.warp.dev/agents/).

## Context management

Context is assembled from several documented sources the agent can reach. Codebase Context indexes your local codebase to help agents understand the project (https://docs.warp.dev/agents/capabilities/codebase-context/), Rules provide reusable global and project-level guidelines that shape how agents respond, matching coding standards, project conventions and personal preferences (https://docs.warp.dev/agents/capabilities/rules/), and Skills add reusable scoped instructions that agents automatically discover and invoke when relevant, with project and global scopes plus a public warpdotdev/oz-skills collection (https://docs.warp.dev/agents/capabilities/skills/). Slash commands and saved prompts give quick access to frequent actions in Agent Mode (https://docs.warp.dev/agents/capabilities/slash-commands/). For long-running work the CLI exposes explicit context management: the docs note that long conversations eventually fill the model's context window which can degrade response quality, and the /compact command frees up context by asking the agent to summarize the conversation (https://docs.warp.dev/agents/cli/agent-conversations/). Planning adds a persistent plan document with version history that survives across a multi-step workflow and can be referenced with @ by the agent (https://docs.warp.dev/agents/capabilities/planning/). Cross-session persistence is handled by Agent Memory, a persistent memory system living on Warp that is shared across supported harnesses — the Warp Agent, Claude Code and Codex — so durable facts, decisions and outcomes from one conversation are available to the next regardless of which harness, machine or teammate triggers the work, with creation and retrieval running asynchronously; it is gated as a research preview enabled per team for design partners (https://docs.warp.dev/agents/agent-memory/). Task lists break agent work into tracked items (https://docs.warp.dev/agents/capabilities/task-lists/).

## Ecosystem

Warp's integration story runs mostly through the Automation Platform rather than a plugin marketplace. Integrations and triggers turn events in other tools into agent runs — mentioning @warp in Slack hands the agent the message and its thread, and the same pattern covers Linear, GitHub and CI failures — alongside cron-based Scheduled Agents (https://docs.warp.dev/platform/overview/). Webhooks are the dominant extensibility mention across the documentation set: Warp documents webhook-based triggers, webhook payload formats, a signed-secret reveal flow using the standard-webhooks format, and per-integration webhook filters (https://docs.warp.dev/platform/integrations/). A public API and SDK exist under the factories surface, with an Oz Agent API and a documented error catalog including budget-exceeded, insufficient-credits and environment-setup-failed (https://docs.warp.dev/factories/api-and-sdk/). For tool extension the documented mechanism is MCP, which the docs describe as extending local agents with custom tools or data sources through a standardized interface and as 'essentially acting as plugins for Warp', configurable per Agent Profile with Streamable HTTP among the supported protocols (https://docs.warp.dev/agents/capabilities/mcp/). Warp also treats third-party CLI coding agents as first-class citizens — Claude Code, Codex, OpenCode and others run inside Warp with rich input, agent notifications, inline code review and remote session control — and Warp ships auto-installed notification plugins into those agents, with plugin source published at warpdotdev/claude-code-warp (https://docs.warp.dev/agents/capabilities/agent-notifications/). On the collaboration side, Warp Drive and teams share Workflows, Notebooks, Prompts, Rules and Environment Variables with role-based permissions for admins and members (https://docs.warp.dev/knowledge-and-collaboration/teams/). Skills are shareable and Warp maintains a public collection in the warpdotdev/oz-skills repository (https://docs.warp.dev/agents/capabilities/skills/).

## Governance

Warp bounds its agent through Agent Profiles, which set autonomy level, base model, tool access and command permissions, and are editable under Settings > Agents > Profiles; a profile can be tuned toward 'Safe & cautious' or 'YOLO mode' (https://docs.warp.dev/agents/capabilities/agent-profiles-permissions/). Permissions are fine-grained across distinct action types — applying code diffs, reading files, creating plans, executing commands, interacting with running commands via Full Terminal Use, and asking clarifying questions — each with an autonomy level of Agent Decides (act when confident, prompt when uncertain), Always ask (explicit approval before any action), Always allow (no confirmation), or Never (https://docs.warp.dev/agents/capabilities/agent-profiles-permissions/). Three documented trust controls refine this: a command allowlist that auto-executes matching regular expressions, empty by default and commonly populated with read-only commands such as ls, grep and find; a command denylist that takes precedence over the other permission settings and will keep prompting even when permissions are set to Always allow; and 'Run until completion', which bypasses the denylist for the current task (https://docs.warp.dev/agents/capabilities/agent-profiles-permissions/). Troubleshooting error pages document the platform refusing work for auth, budget, credit and policy reasons, including authentication-required, budget-exceeded, insufficient-credits and content-policy-violation (https://docs.warp.dev/factories/api-and-sdk/troubleshooting/errors/). Spend is governed by the three-bucket credit model — AI credits for inference, compute credits for the sandbox an agent runs in, platform credits for the platform layer — all drawing from one balance managed under Settings > Billing and usage, with add-on credit purchases, auto-reload, and plan-specific allowances (https://docs.warp.dev/support-and-community/plans-and-billing/credits/). For organizations, the Admin Panel gives team administrators centralized control over organization-wide settings including agent autonomy, privacy controls, billing limits, codebase indexing and sharing policies, and settings configured there are enforced across all team members and override individual preferences (https://docs.warp.dev/knowledge-and-collaboration/admin-panel/). Enterprise security posture includes separation of control plane from execution plane, zero data retention from contracted LLM providers, team-managed API keys and endpoints, Bring Your Own LLM routing through AWS Bedrock or Google Cloud via Gemini Enterprise, telemetry controls, and an open source AGPL v3 client published for security review and audit (https://docs.warp.dev/enterprise/security-and-compliance/security-overview/).

## Limitations

Orchestration depth is capped: an orchestration is exactly one level deep — one parent and its direct children — and a child agent does not spawn its own children, so deeper hierarchies must be flattened into a single fan-out (https://docs.warp.dev/platform/orchestration/). Agent Memory, the persistent cross-session and cross-harness memory layer, is not generally available: it is in research preview and enabled per team for design partners, requiring a waitlist request for access (https://docs.warp.dev/agents/agent-memory/). There is no IDE integration: the docs state plainly that Warp doesn't have a VS Code importer because it's a standalone application, not a VS Code extension, and users are instead directed to run Warp alongside their editor or adopt Warp's built-in code editor (https://docs.warp.dev/getting-started/migrate-to-warp/migrate-to-warp-from-vs-code-terminal/). There are no agent lifecycle hooks — no pre-tool, post-tool, or session start/stop interception points — with the only documented hooks being worker-level workspace setup_command and teardown_command for the self-hosted Direct backend and OSC-driven terminal notification hooks (https://docs.warp.dev/factories/self-hosting/direct-monorepo-worktrees/). There is no general plugin or extension API for Warp itself; MCP is the documented extension surface and is framed as acting like plugins rather than being a plugin SDK (https://docs.warp.dev/agents/capabilities/mcp/). Cost and permission interactions can surprise: the command denylist overrides 'Always allow' so denied commands keep prompting, and the escape hatch, 'Run until completion', bypasses the denylist for the current task (https://docs.warp.dev/agents/capabilities/agent-profiles-permissions/). Local agent runs don't consume compute credits because they use your own machine, but platform credits apply to every cloud agent run and even to local agent runs on Business and Enterprise plans that use customer-supplied inference including BYOK, a ChatGPT subscription, a custom inference endpoint, or BYOLLM (https://docs.warp.dev/support-and-community/plans-and-billing/credits/). Self-hosted runs depend on the oz-agent-worker daemon and its documented failure modes, with a catalog of distinct errors including environment-setup-failed, infrastructure-timeout, agent-process-failed and resource-unavailable (https://docs.warp.dev/factories/api-and-sdk/troubleshooting/errors/).

## In its own words

> Cloud agents are autonomous, background agents that run on Warp’s cloud infrastructure or your own, triggered by system events, schedules, or integrations like Slack and GitHub.  
> — [https://docs.warp.dev/platform/](https://docs.warp.dev/platform/)

> MCP servers extend Warp’s local agents in a modular, flexible way by exposing custom tools or data sources through a standardized interface — essentially acting as plugins for Warp.  
> — [https://docs.warp.dev/agents/capabilities/mcp/](https://docs.warp.dev/agents/capabilities/mcp/)

> Warp doesn’t have a VS Code importer because it’s a standalone application, not a VS Code extension.  
> — [https://docs.warp.dev/getting-started/migrate-to-warp/migrate-to-warp-from-vs-code-terminal/](https://docs.warp.dev/getting-started/migrate-to-warp/migrate-to-warp-from-vs-code-terminal/)

> Warp’s client is open source under AGPL v3, so the editor and terminal that host your agents are fully auditable.  
> — [https://docs.warp.dev/agents/](https://docs.warp.dev/agents/)

> Models from OpenAI, Anthropic, Google, and open source providers are available, with configurable reasoning levels and per-profile defaults.  
> — [https://docs.warp.dev/agents/inference/model-choice/](https://docs.warp.dev/agents/inference/model-choice/)


## Notable

Warp's client is open source under AGPL v3 at warpdotdev/warp, which is unusual for a commercially-licensed terminal product and makes the host editor and terminal auditable (https://docs.warp.dev/agents/). Multi-agent orchestration is explicitly capped at one level deep — a parent plus its direct children, and a child runs its own work and does not spawn its own children (https://docs.warp.dev/platform/orchestration/). Agent Memory, the persistent cross-harness memory layer, is in research preview and enabled per team for design partners via a waitlist rather than being generally available (https://docs.warp.dev/agents/agent-memory/). A documented permission gotcha: the command denylist takes precedence over 'Always allow', so the agent keeps prompting for denied commands unless you use 'Run until completion', which bypasses the denylist for the current task (https://docs.warp.dev/agents/capabilities/agent-profiles-permissions/).

## Sources fetched

- https://docs.warp.dev/llms.txt
- https://docs.warp.dev/llms-small.txt
- https://docs.warp.dev/_llms-txt/terminal.txt
- https://docs.warp.dev/_llms-txt/agents.txt
- https://docs.warp.dev/_llms-txt/factories.txt
- https://docs.warp.dev/_llms-txt/warp-agent-cli.txt
- https://docs.warp.dev/_llms-txt/automation-platform.txt
- https://docs.warp.dev/_llms-txt/code.txt
- https://docs.warp.dev/_llms-txt/enterprise.txt
- https://docs.warp.dev/_llms-txt/getting-started.txt
- https://docs.warp.dev/_llms-txt/knowledge-and-collaboration.txt
- https://docs.warp.dev/_llms-txt/support.txt
- https://docs.warp.dev/_llms-txt/guides.txt
- https://docs.warp.dev/_llms-txt/changelog.txt
- https://docs.warp.dev/changelog/2026/
- https://api.github.com/repos/warpdotdev/warp
- https://docs.warp.dev/
- https://docs.warp.dev/agents/
- https://docs.warp.dev/agents/capabilities/
- https://docs.warp.dev/agents/capabilities/mcp/
- https://docs.warp.dev/agents/capabilities/skills/
- https://docs.warp.dev/agents/capabilities/planning/
- https://docs.warp.dev/agents/capabilities/rules/
- https://docs.warp.dev/agents/capabilities/agent-profiles-permissions/
- https://docs.warp.dev/agents/capabilities/agent-notifications/
- https://docs.warp.dev/agents/capabilities/slash-commands/
- https://docs.warp.dev/agents/capabilities/full-terminal-use/
- https://docs.warp.dev/agents/capabilities/codebase-context/
- https://docs.warp.dev/agents/agent-memory/
- https://docs.warp.dev/agents/inference/model-choice/
- https://docs.warp.dev/agents/cli/
- https://docs.warp.dev/agents/cli/agent-conversations/
- https://docs.warp.dev/agents/cli/cloud-and-orchestration/
- https://docs.warp.dev/agents/local-agents/interactive-code-review/
- https://docs.warp.dev/agents/local-agents/session-sharing/
- https://docs.warp.dev/agents/cli-agents/claude-code/
- https://docs.warp.dev/platform/
- https://docs.warp.dev/platform/overview/
- https://docs.warp.dev/platform/orchestration/
- https://docs.warp.dev/platform/orchestration/multi-agent-runs/
- https://docs.warp.dev/platform/triggers/scheduled-agents/
- https://docs.warp.dev/factories/
- https://docs.warp.dev/factories/api-and-sdk/
- https://docs.warp.dev/factories/api-and-sdk/troubleshooting/errors/
- https://docs.warp.dev/factories/self-hosting/reference/
- https://docs.warp.dev/factories/self-hosting/direct-monorepo-worktrees/
- https://docs.warp.dev/enterprise/
- https://docs.warp.dev/enterprise/enterprise-features/architecture-and-deployment/
- https://docs.warp.dev/enterprise/security-and-compliance/security-overview/
- https://docs.warp.dev/code/code-editor/
- https://docs.warp.dev/code/code-review/
- https://docs.warp.dev/code/git-worktrees/
- https://docs.warp.dev/knowledge-and-collaboration/warp-drive/
- https://docs.warp.dev/knowledge-and-collaboration/teams/
- https://docs.warp.dev/knowledge-and-collaboration/admin-panel/
- https://docs.warp.dev/getting-started/quickstart/installation-and-setup/
- https://docs.warp.dev/getting-started/migrate-to-warp/migrate-to-warp-from-vs-code-terminal/
- https://docs.warp.dev/support-and-community/plans-and-billing/
- https://docs.warp.dev/support-and-community/plans-and-billing/credits/
- https://docs.warp.dev/support-and-community/
- https://docs.warp.dev/terminal/more-features/notifications/
- https://docs.warp.dev/terminal/more-features/files-and-links/
- https://docs.warp.dev/terminal/settings/all-settings/

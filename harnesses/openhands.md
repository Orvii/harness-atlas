# OpenHands

- **repo:** All-Hands-AI/OpenHands (repo now redirects to OpenHands/OpenHands after org rename)
- **version pin:** `v1.24.0` — gh api repos/All-Hands-AI/OpenHands/releases/latest -> https://github.com/OpenHands/OpenHands/releases/tag/v1.24.0 (published 2026-09-25); corroborated by npm registry @openhands/agent-canvas latest = 1.24.0
- **docs home:** https://docs.openhands.dev

## What it promises

OpenHands Agent Canvas promises to turn your coding agents into a self-hosted, always-on engineering team — a developer control center for starting conversations and automating everyday tasks, run locally by default or across Docker, VM, and cloud backends with OpenHands, Claude Code, Codex, Gemini, or any ACP-compatible agent.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | SDK-level TaskToolSet: parent spawns typed sub-agents (register_agent), runs sequentially, resumable via task_id; file-based sub-agents can be plain Markdown. | [src](https://docs.openhands.dev/sdk/guides/task-tool-set) |
| workflow_orchestration | ◐ partial | Has sub-agent delegation (sequential, blocking), scheduled/event automations, and GitHub Actions workflow templates; no DAG/team/swarm orchestration primitives documented. | [src](https://docs.openhands.dev/sdk/guides/task-tool-set) |
| mcp | ✅ yes | MCP client; SSE/SHTTP/stdio transports; full support on CLI, SDK, Local GUI and Cloud. | [src](https://docs.openhands.dev/overview/model-context-protocol) |
| hooks_lifecycle | ✅ yes | PreToolUse, PostToolUse, UserPromptSubmit, Stop, SessionStart, SessionEnd; blocking + async hooks; Claude Code-compatible hooks.json format. | [src](https://docs.openhands.dev/openhands/usage/customization/hooks) |
| skills | ✅ yes | Follows Agent Skills spec (SKILL.md); keyword triggers, path-triggered rules, org/user/global registries. | [src](https://docs.openhands.dev/overview/skills) |
| memory_persistence | ✅ yes | Opt-in (load_memory=True); two-tier MEMORY.md (user ~/.openhands/memory/ + project workspace/.openhands/memory/); off by default. | [src](https://docs.openhands.dev/sdk/guides/persistent-memory) |
| sandboxing | ✅ yes | Docker/process/remote providers; permission modes: always-ask (default), --always-approve, --llm-approve; SDK confirmation policies AlwaysConfirm/ConfirmRisky/NeverConfirm. | [src](https://docs.openhands.dev/openhands/usage/sandboxes/overview) |
| plan_mode | ◐ partial | Plan-then-execute exists as a documented SDK pattern (planning agent writes PLAN.md, execution agent implements); CLI only has 'Plan - View agent plan'; no built-in interactive plan-approval gate in docs. | [src](https://docs.openhands.dev/sdk/guides/agent-custom) |
| background_tasks | ✅ yes | Agent-server REST API runs conversations in background; bash commands also have a background start endpoint; Agent Canvas conversations run server-side. | [src](https://docs.openhands.dev/sdk/guides/agent-server/api-reference/conversations/run-conversation) |
| ide_integration | ✅ yes | ACP-based: Zed + JetBrains native support, VS Code via community ACP extension; marked experimental; GUI also embeds a VS Code tab. | [src](https://docs.openhands.dev/openhands/usage/cli/ide/overview) |
| model_agnostic | ✅ yes | LiteLLM: Anthropic/OpenAI/Google/Azure/Bedrock/Groq/Moonshot/OpenRouter/local servers; also can drive Claude Code, Codex, Gemini CLI as ACP agents. | [src](https://docs.openhands.dev/openhands/usage/llms/llms) |
| plugins | ✅ yes | Claude Code plugin structure compatible (.claude-plugin/) plus portable Agent Plugins format with plugin.json at root. | [src](https://docs.openhands.dev/overview/plugins) |
| session_resume | ✅ yes | openhands --resume <id> / --resume --last; also works in ACP/IDE mode; automations' conversations can be continued too. | [src](https://docs.openhands.dev/openhands/usage/cli/resume) |
| cost_controls | ✅ yes | Token/cost/latency metrics per LLM and per conversation; Cloud org/user spending caps documented at https://docs.openhands.dev/openhands/usage/cloud/organizations/budgets. | [src](https://docs.openhands.dev/sdk/guides/metrics) |

## Architecture

Client-server split. Agent Canvas (React browser UI) sends requests to a chosen backend; a launcher can start Canvas, Agent Server, Automation Server and ingress together, or run frontend-only against local/remote backends — "Agent Server owns conversation execution" and streams events to the UI (https://docs.openhands.dev/openhands/usage/agent-canvas/architecture). The Software Agent SDK is "a composable Python library" split into four packages: core SDK, tools, workspace implementations, Agent Server (https://docs.openhands.dev/sdk/arch/overview). Tools follow a strict "Action → Observation" input-output contract; executors implement tool logic and return observations (https://docs.openhands.dev/sdk/arch/tool-system). Workspaces abstract environments: LocalWorkspace runs bash as host subprocesses, while Docker and RemoteAPI workspaces execute in containers or via HTTP to an agent server (https://docs.openhands.dev/sdk/arch/workspace). The CLI is the interactive default mode; headless mode runs a task non-interactively for CI (https://docs.openhands.dev/openhands/usage/cli/headless).

## Context management

The Condenser "reduces long event histories into condensed summaries while preserving critical information for reasoning," triggering automatically past a configured threshold (often a maximum event count) or on manual condensation requests after context-window errors (https://docs.openhands.dev/sdk/arch/condenser). Strategies include NoOpCondenser, LLMSummarizingCondenser (keeps selected early and recent events, LLM-summarizes the middle), RollingCondenser, and PipelineCondenser chaining steps such as removal, summarization, then truncation (https://docs.openhands.dev/sdk/guides/context-condenser). Persistent memory is opt-in and off by default: MEMORY.md indexes under ~/.openhands/memory/ and <workspace>/.openhands/memory/ join the system prompt when load_memory=True; dated daily logs stay on disk and are read on demand; AGENTS.md remains separate agent guidance (https://docs.openhands.dev/sdk/guides/persistent-memory). The Agent Server API also exposes a condense-conversation endpoint.

## Ecosystem

No counts of skills, plugins, or extensions are documented anywhere fetched. Distribution is git-centric: a plugin packages skills, tool-event hooks, MCP server settings, agent definitions, and slash commands around plugin.json metadata, installable from a local directory or GitHub repository (including subpath, branch, or tag); Cloud users can browse a plugin library (https://docs.openhands.dev/overview/plugins). "The official global skill registry is maintained at github.com/OpenHands/extensions"; skills live at .agents/skills/<name>/SKILL.md or ~/.agents/skills/ (https://docs.openhands.dev/overview/skills). Agent Plugins Packages v1.0.0 is a portable format whose goal is "a single package works across every compatible client" (https://docs.openhands.dev/overview/agent-plugins). Enterprise offers an opt-in marketplace catalog configured via MARKETPLACE_SOURCE — a GitHub repository or HTTPS URL serving catalog JSON (https://docs.openhands.dev/enterprise/plugin-marketplace).

## Governance

License is MIT, copyright "OpenHands contributors" (https://raw.githubusercontent.com/All-Hands-AI/OpenHands/main/LICENSE). "OpenHands is supported by the for-profit organization All Hands AI, Inc."; governance is currently described as a "Benevolent Dictator approach," with a possible future transfer to an open-source foundation (https://docs.openhands.dev/overview/community). Contributions: pull requests across public repositories, CI must pass, conventional title prefixes (feat:/fix:/docs:); maintainership by nomination after at least 3 days of maintainer discussion (https://docs.openhands.dev/overview/contributing). Issues pass automated readiness checks before the ready-for-dev label; PRs must reference a ready-for-dev issue (https://docs.openhands.dev/overview/issue-lifecycle). No release cadence is stated; sequential release notes (Agent Canvas 1.10–1.24; 1.24.0 "Released September 25, 2026") imply frequent releases (https://docs.openhands.dev/openhands/usage/agent-canvas/release-notes/v1.24.0).

## Limitations

Documented gaps: "Long-running processes: Sessions have time limits"; "Can't set breakpoints interactively"; "Can't see rendered UI easily"; "Previous sessions not remembered"; the agent cannot access the local environment outside its sandbox (https://docs.openhands.dev/openhands/usage/essential-guidelines/when-to-use-openhands). "OpenHands is meant to be run by a single user on their local workstation" — no built-in authentication, isolation, or scalability for shared multi-user deployments (https://docs.openhands.dev/overview/faqs). "IDE integration via ACP is experimental and may have limitations"; IDE integrations require the CLI on Linux/macOS, with Windows supported only via WSL (https://docs.openhands.dev/openhands/usage/cli/ide/overview). Critic is "highly experimental and subject to change" (https://docs.openhands.dev/openhands/usage/cli/critic). Headless mode "always runs in always-approve mode" — it "will execute all actions without any confirmation" (https://docs.openhands.dev/openhands/usage/cli/headless). Canvas "Apps (Beta)" is likewise flagged beta.

## In its own words

> Welcome to OpenHands, a community focused on AI-driven development.  
> — [https://docs.openhands.dev/overview/introduction.md](https://docs.openhands.dev/overview/introduction.md)

> The tool system follows a strict input-output contract: `Action → Observation`.  
> — [https://docs.openhands.dev/sdk/arch/tool-system.md](https://docs.openhands.dev/sdk/arch/tool-system.md)

> OpenHands is meant to be run by a single user on their local workstation.  
> — [https://docs.openhands.dev/overview/faqs.md](https://docs.openhands.dev/overview/faqs.md)

> OpenHands is supported by the for-profit organization All Hands AI, Inc.  
> — [https://docs.openhands.dev/overview/community.md](https://docs.openhands.dev/overview/community.md)


## Notable

Repo All-Hands-AI/OpenHands now redirects to OpenHands/OpenHands and its v1.x release is 'Agent Canvas', a control center that can host third-party agents (Claude Code, Codex, Gemini) via ACP, while the OpenHands agent core moved to the separate software-agent-sdk and automation repos; hooks/skills formats are deliberately Claude Code-compatible.

## Sources fetched

- https://docs.all-hands.dev/ (308 redirect to https://docs.openhands.dev/)
- https://docs.openhands.dev/
- https://docs.openhands.dev/llms.txt
- https://docs.openhands.dev/overview/introduction.md
- https://docs.openhands.dev/overview/community.md
- https://docs.openhands.dev/overview/contributing.md
- https://docs.openhands.dev/overview/issue-lifecycle.md
- https://docs.openhands.dev/overview/faqs.md
- https://docs.openhands.dev/overview/plugins.md
- https://docs.openhands.dev/overview/agent-plugins.md
- https://docs.openhands.dev/overview/skills.md
- https://docs.openhands.dev/openhands/usage/agent-canvas/architecture.md
- https://docs.openhands.dev/openhands/usage/agent-canvas/release-notes/v1.24.0.md
- https://docs.openhands.dev/openhands/usage/cli/terminal.md
- https://docs.openhands.dev/openhands/usage/cli/headless.md
- https://docs.openhands.dev/openhands/usage/cli/critic.md
- https://docs.openhands.dev/openhands/usage/cli/ide/overview.md
- https://docs.openhands.dev/openhands/usage/essential-guidelines/when-to-use-openhands.md
- https://docs.openhands.dev/sdk/arch/overview.md
- https://docs.openhands.dev/sdk/arch/tool-system.md
- https://docs.openhands.dev/sdk/arch/workspace.md
- https://docs.openhands.dev/sdk/arch/condenser.md
- https://docs.openhands.dev/sdk/guides/context-condenser.md
- https://docs.openhands.dev/sdk/guides/persistent-memory.md
- https://docs.openhands.dev/sdk/faq.md
- https://docs.openhands.dev/enterprise/plugin-marketplace.md
- https://raw.githubusercontent.com/All-Hands-AI/OpenHands/main/LICENSE

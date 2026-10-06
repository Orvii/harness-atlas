# Qoder

- **repo:** closed source; no public product repository
- **version pin:** `Qoder 0.4.2 (Qoder desktop app, 2026-09-24) / Qoder IDE 1.32.0 (2026-09-23); JetBrains plugin 2026.922.75102118 (2026-09-22)` — Release notes pages fetched this run: https://docs.qoder.com/release-notes/qoder (newest entry Qoder 0.4.2, September 24, 2026), https://docs.qoder.com/release-notes/desktop (newest entry 1.32.0, September 23, 2026), https://docs.qoder.com/release-notes/jetbrains-plugin (newest entry JetBrains 2026.922.75102118, September 22, 2026); all three pages checked on 2026-10-06.
- **docs home:** https://docs.qoder.com/

## What it promises

Qoder is documented as an agentic coding platform designed for real software development that integrates context engineering with intelligent agents to understand a codebase and tackle development tasks, with the slogan: bring the idea, and Qoder gets it done. In Qoder IDE, Editor keeps NEXT, Inline Chat and the Chat panel beside your code for in-flow collaboration, while Quest is a dedicated workspace for autonomous delegation of long-running, multi-step work.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | Installed Plugins supply specialized Agents the main Agent coordinates: the user selects one with / in the task input, or Qoder chooses a matching installed Agent from the task description, and hook events include SubagentStart/SubagentStop. Qoder IDE's Experts Mode goes further - a Lead Agent decomposes the task and runs Researcher, Full-Stack Engineer, QA, Code Reviewer, UI Operator and Debug Engineer sub-agents in parallel. | [src](https://docs.qoder.com/qoder/subagents) |
| workflow_orchestration | ✅ yes | Qoder CLI's Dynamic workflows move the orchestration plan into a JavaScript script that decides which subagents to start, how to group work into phases, how to combine intermediate results and what final output returns to the session, and they run in the background. Complementary primitives: Agent Teams (beta, QODER_AGENT_TEAMS=1) with a main Agent and teammates, Cloud Agents' coordinator/child-Agent/Advisor multiagent orchestration, and Business-plan Custom agent teams with one Team Leader plus 1-4 additional members. | [src](https://docs.qoder.com/cli/workflows) |
| mcp | ✅ yes | Connectors are a first-class extension type: a marketplace plus custom MCP servers added by form or JSON and saved under mcpServers in ~/.qoder/settings.json, with user-level scope. Qoder IDE documents STDIO and SSE transports and invokes discovered MCP capabilities based on user input and tool metadata. | [src](https://docs.qoder.com/qoder/connectors) |
| hooks_lifecycle | ✅ yes | Hooks are compatible with Qoder CLI and cover task, tool, permission, subagent, context, configuration, file and worktree events, including SessionStart/SessionEnd, UserPromptSubmit, PreToolUse, PostToolUse/PostToolUseFailure, PermissionRequest/PermissionDenied, SubagentStart/SubagentStop, PreCompact/PostCompact and WorktreeCreate/WorktreeRemove, with command, http, prompt and agent handler types. Configuration is merged from user-level ~/.qoder/settings.json, project .qoder/settings.json and .qoder/settings.local.json. | [src](https://docs.qoder.com/qoder/hooks) |
| skills | ✅ yes | Skills package instructions and supporting resources for a repeatable kind of work; they install from the Extensions > Skills marketplace or are created/uploaded as a SKILL.md file or ZIP, then selected explicitly with / or auto-matched from the task description. Persistent preferences and long-lived project context are a separate system (Settings > Memory), not part of the Skill mechanism. | [src](https://docs.qoder.com/qoder/skills) |
| memory_persistence | ✅ yes | Qoder retains information useful across tasks such as communication preferences, project background and collaboration conventions in long-term memory stored on this device, split into independently toggleable Global memory and Project memory groups backed by inspectable memory files that can be reviewed or deleted. Conversation history and memory are stored separately per product (Qoder desktop vs Qoder IDE), and the docs offer an import path for carrying IDE history and memories into the app. | [src](https://docs.qoder.com/qoder/memory) |
| sandboxing | ✅ yes | Three access-permission modes bound the agent: Ask for approval (the default) asks before running commands, editing files outside the workspace or accessing the network; Auto approve asks only when potential risk is detected; Full access stops asking and can freely use files, terminal and network. Tasks also run in a selectable execution environment (local workspace, isolated git Worktree, SSH workspace, or no workspace), and read-only terminal commands can run automatically even under Ask for approval. | [src](https://docs.qoder.com/qoder/approval-and-sandbox) |
| plan_mode | ✅ yes | Plan mode asks Qoder to prepare a reviewable plan before implementation, covering goals and non-goals, relevant files or modules, implementation steps, risks and dependencies and verification, with the composer showing Turn off plan mode while active. Qoder IDE Quest adds Spec-driven development where a structured Spec (requirements, design, task breakdown, acceptance criteria) is reviewed and annotated before clicking Build, and Qoder CLI's /plan explores in read-only mode until the plan is approved. | [src](https://docs.qoder.com/qoder/plan-driven) |
| background_tasks | ✅ yes | Qoder CLI runs Dynamic workflows and delegated subagents in the background, with /tasks listing currently running background tasks, and subagents support worktree isolation for parallel work. The Qoder app adds Automations that start an Agent task on a schedule in local or cloud execution and collect each result in Run history. | [src](https://docs.qoder.com/cli/parallel-tasks) |
| ide_integration | ✅ yes | Qoder itself is the IDE: Qoder IDE offers two primary workspaces, Editor and Quest, so this records a standalone agentic IDE rather than an extension for VS Code. A separate Qoder plugin brings agentic coding into JetBrains IDEs, with its own release channel (newest JetBrains plugin 2026.922.75102118), and Qoder CLI covers terminal workflows. | [src](https://docs.qoder.com/desktop/overview) |
| model_agnostic | ✅ yes | Qoder supports accessing third-party provider model resources via API keys, with preset providers including Alibaba Cloud Model Studio, DeepSeek, Z.ai, Kimi, MiniMax, Xiaomi MIMO, OpenAI, Google and OpenRouter, plus OpenAI-Compatible and Anthropic-Compatible custom endpoints. Doc-stated caveat: Repo Wiki uses a fixed model and is billed separately, and its generation prompts that additional credits will be consumed. | [src](https://docs.qoder.com/qoder/custom-models) |
| plugins | ✅ yes | A Plugin bundles related capabilities for a workflow or role - depending on the package it can include Skills, connectors, Agents, commands, rules or Hooks - and installs from the Extensions > Plugins marketplace after reviewing publisher, components and external requirements. Users can also create with Qoder or upload their own Plugin ZIP, Skill file or custom MCP connector on the current device. | [src](https://docs.qoder.com/qoder/plugins) |
| session_resume | ✅ yes | Qoder keeps each conversation as a task in the sidebar, organized by workspace or folder, with search across task title, user message or Agent response plus sorting, filtering, archiving and restore; reopening a task retains its earlier conversation and workspace information. Qoder CLI stores sessions per project (~/.qoder/projects/<project>/<session-id>.jsonl) and supports -c/--continue for the most recent session, -r/--resume for a specific one, naming, branching and explicit session IDs. | [src](https://docs.qoder.com/qoder/task-management) |
| cost_controls | ✅ yes | Usage is metered in Credits, the resource quota for AI models across Qoder products, with failed model requests not resulting in deductions and a limited daily allowance of basic model calls even after quota depletion. The model selector shows the Credit rate before sending (Auto ~0.5x, Performance ~1.1x, Ultimate ~2.0x), Qoder CLI's /usage panel reports plan, plan expiration, credits used and session statistics, and plans run Free/Pro/Pro+/Ultra. | [src](https://docs.qoder.com/Credits) |

## Architecture

Qoder is documented as a family of surfaces sharing one capability model: the new standalone Qoder desktop app (task-based, with Coding and General modes routed by workspace or folder), Qoder IDE (Editor and Quest workspaces), Qoder CLI, Cloud Agents, a JetBrains plugin, and mobile and web clients, with conversation history and memory stored separately per product (https://docs.qoder.com/qoder/overview). Qoder IDE pairs in-flow editing - Editor keeps NEXT, Inline Chat and the Chat panel beside the code - with autonomous delegation via Quest, a dedicated window with task boards, progress tracking and artifact review (https://docs.qoder.com/desktop/overview). The extension architecture is uniform: Plugins bundle Skills, connectors, Agents, commands, rules and Hooks, and connectors are MCP servers stored under mcpServers in ~/.qoder/settings.json (https://docs.qoder.com/qoder/plugins, https://docs.qoder.com/qoder/connectors). Multi-agent work appears at several levels: Qoder IDE Experts Mode (Lead Agent plus six expert roles executing in parallel) (https://docs.qoder.com/user-guide/quest/experts-mode); custom Agents and Business-plan agent teams with one Team Leader and 1-4 members (https://docs.qoder.com/qoder/custom-agent-teams); plugin-supplied specialist agents the main Agent coordinates, with SubagentStart/SubagentStop hook events (https://docs.qoder.com/qoder/subagents); and script-based orchestration in Qoder CLI Dynamic workflows plus Agent Teams and Cloud Agents coordinator/child/Advisor orchestration (https://docs.qoder.com/cli/workflows, https://docs.qoder.com/cli/agent-teams, https://docs.qoder.com/cloud-agents/multi-agents). Each task selects an execution environment at send time - local workspace, isolated git Worktree, SSH workspace, or no workspace - which determines where Qoder reads files, runs commands and inspects Git state (https://docs.qoder.com/qoder/execution-environments).

## Context management

Qoder monitors context usage and can compact earlier content into a shorter working summary while preserving important decisions, constraints, file references and progress; compaction is triggered from the context-usage control or /compact, does not delete task history, and can also fire automatically when the runtime needs room, though minor details may be generalized or omitted (https://docs.qoder.com/qoder/context-compaction). Durable context lives in Memory, split into Global and Project scopes with independent toggles and inspectable files, and the docs explicitly warn that memory must not become the only record of a requirement that must be reviewed or versioned (https://docs.qoder.com/qoder/memory). Model choice interacts with context handling: the model selector exposes Auto routing and performance tiers at different Credit rates (https://docs.qoder.com/qoder/model-selector), while Repo Wiki generation always uses a fixed model and is billed separately (https://docs.qoder.com/qoder/custom-models).

## Ecosystem

Extensions are distributed in-product: Extensions > Skills, Plugins and Connectors marketplaces with Popular/Newest sorting and search, and a published guide for creating or uploading personal Skills (SKILL.md or ZIP), Plugins (ZIP) and custom MCP connectors kept on the current device (https://docs.qoder.com/qoder/extension-publishing, https://docs.qoder.com/qoder/skills, https://docs.qoder.com/qoder/plugins). Model access extends to third-party providers through API keys, including OpenAI- and Anthropic-compatible endpoints (https://docs.qoder.com/qoder/custom-models). Accounts run on Free, Pro, Pro+ and Ultra individual plans or Teams and Enterprise business plans, with Credits as the shared unit across Qoder, Qoder IDE, the JetBrains plugin, Qoder CLI, QoderWake, Qoder Cloud Agents, mobile and web (https://docs.qoder.com/account/pricing, https://docs.qoder.com/Credits). JetBrains IDEs are served by a dedicated Qoder plugin with its own release channel, and Qoder CLI covers terminal-centric workflows (https://docs.qoder.com/plugins/introduction).

## Governance

Governance levers in the docs: three access-permission modes with an operation-by-operation permit table (file edits inside/outside the workspace, terminal commands, internet access) (https://docs.qoder.com/qoder/approval-and-sandbox); lifecycle Hooks usable as deterministic gates, with a prompt handler type that decides whether execution can continue and warnings to review commands and endpoints first (https://docs.qoder.com/qoder/hooks); and a security-and-authorization guide covering device sign-in hygiene, keeping credentials out of tasks, reviewing Skills/Plugins/Connectors including scripts and Hooks, SSH host verification and custom MCP configuration (https://docs.qoder.com/qoder/security-and-authorization). Business-plan agent features add ownership rules - in a discussion only an agent's owner can invoke it with @ - and per-agent tool rules where allowed tools can run without approval and denied tools are blocked (https://docs.qoder.com/qoder/custom-agents). Qoder CLI additionally ships built-in security scanning with L1 static check (free), L2 lightweight scan and L3 deep scan levels, enabled by default and available as a CI/CD gate (https://docs.qoder.com/cli/security).

## Limitations

Doc-stated limits: Custom agents and Custom agent teams are Business plans (Teams and Enterprise) only, not individual plans, and their collaboration runs execute on the current device, which must remain online (https://docs.qoder.com/qoder/custom-agents, https://docs.qoder.com/qoder/custom-agent-teams); Agent Teams in Qoder CLI is a beta feature not enabled by default and requires the QODER_AGENT_TEAMS=1 flag (https://docs.qoder.com/cli/agent-teams); Automations with cloud execution do not support adding Skills or local files or uploading your local environment (https://docs.qoder.com/qoder/automations); Repo Wiki uses a fixed model and is billed separately (https://docs.qoder.com/qoder/custom-models); agent and team names cannot be changed after creation, and turning off assignment interrupts unfinished tasks (https://docs.qoder.com/qoder/custom-agents); context compaction can generalize or omit minor details (https://docs.qoder.com/qoder/context-compaction); the compact action can be unavailable near the start of a task, while the Agent is responding, or when the model or runtime does not expose context usage (https://docs.qoder.com/qoder/context-compaction).

## In its own words

> Team tasks run on the current device, which must remain online.  
> — [https://docs.qoder.com/qoder/custom-agent-teams](https://docs.qoder.com/qoder/custom-agent-teams)

> Qoder supports accessing third-party provider model resources via API keys.  
> — [https://docs.qoder.com/qoder/custom-models](https://docs.qoder.com/qoder/custom-models)

> Credits are the resource quota for AI models in Qoder.  
> — [https://docs.qoder.com/Credits](https://docs.qoder.com/Credits)

> Dynamic workflows let Qoder CLI run a structured multi-agent process in the background.  
> — [https://docs.qoder.com/cli/workflows](https://docs.qoder.com/cli/workflows)

> Full access allows Qoder to read, modify, or delete files, run terminal commands, and access the internet without asking again.  
> — [https://docs.qoder.com/qoder/approval-and-sandbox](https://docs.qoder.com/qoder/approval-and-sandbox)


## Notable

Qoder is documented as two side-by-side products, not one: the new standalone Qoder desktop app (0.4.x) originated from Quest mode in Qoder IDE and is independent from Qoder IDE (1.32.x), with conversation history and memory stored separately per product and an import path between them. Hooks are shared with Qoder CLI and include agent-level events (SubagentStart/SubagentStop, Elicitation), so plugin-supplied subagents and permission decisions are scriptable. Experts Mode in Qoder IDE auto-assembles a fixed expert roster - a Lead Agent plus Researcher, Full-Stack Engineer, QA, Code Reviewer, UI Operator and Debug Engineer - that runs in parallel, while Business-plan custom agent teams and automated scheduled runs require the local device to remain online.

## Sources fetched

- https://docs.qoder.com/llms.txt
- https://docs.qoder.com/qoder/overview
- https://docs.qoder.com/qoder/subagents
- https://docs.qoder.com/qoder/custom-agents
- https://docs.qoder.com/qoder/custom-agent-teams
- https://docs.qoder.com/qoder/hooks
- https://docs.qoder.com/qoder/skills
- https://docs.qoder.com/qoder/plugins
- https://docs.qoder.com/qoder/connectors
- https://docs.qoder.com/qoder/memory
- https://docs.qoder.com/qoder/approval-and-sandbox
- https://docs.qoder.com/qoder/plan-driven
- https://docs.qoder.com/qoder/goal-driven
- https://docs.qoder.com/qoder/automations
- https://docs.qoder.com/qoder/custom-models
- https://docs.qoder.com/qoder/task-management
- https://docs.qoder.com/qoder/context-compaction
- https://docs.qoder.com/qoder/model-selector
- https://docs.qoder.com/qoder/execution-environments
- https://docs.qoder.com/qoder/terminal-and-sandbox
- https://docs.qoder.com/qoder/extension-publishing
- https://docs.qoder.com/qoder/security-and-authorization
- https://docs.qoder.com/qoder/quickstart
- https://docs.qoder.com/release-notes/qoder
- https://docs.qoder.com/release-notes/desktop
- https://docs.qoder.com/release-notes/jetbrains-plugin
- https://docs.qoder.com/Credits
- https://docs.qoder.com/account/pricing
- https://docs.qoder.com/plugins/introduction
- https://docs.qoder.com/desktop/overview
- https://docs.qoder.com/user-guide/quest/experts-mode
- https://docs.qoder.com/user-guide/quest/spec-driven
- https://docs.qoder.com/user-guide/chat/model-context-protocol
- https://docs.qoder.com/cli/workflows
- https://docs.qoder.com/cli/agent-teams
- https://docs.qoder.com/cli/sessions
- https://docs.qoder.com/cli/usage
- https://docs.qoder.com/cli/plan-mode
- https://docs.qoder.com/cli/subagent
- https://docs.qoder.com/cli/parallel-tasks
- https://docs.qoder.com/cli/security
- https://docs.qoder.com/cloud-agents/multi-agents

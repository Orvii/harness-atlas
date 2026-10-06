# Replit Agent

- **repo:** Replit (closed source; no public product repository)
- **version pin:** `no published version or release date (docs checked 2026-10-06)` — https://docs.replit.com/replitai/agent and https://docs.replit.com/billing/ai-billing state no version or date; the Agent page's embedded video title 'Agent 4' is not a dated product version — the pin is the checked date, labelled as such
- **docs home:** https://docs.replit.com/replitai/agent

## What it promises

Replit presents Agent as a system that can plan changes, write code, explain behavior, debug, and improve apps. Its docs say Agent tests its work and creates checkpoints that allow rollback.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ? unknown | The task docs describe separate background tasks, each with its own Agent, but do not establish child-agent spawning. | [src](https://docs.replit.com/core-concepts/agent/task-system) |
| workflow_orchestration | ◐ partial | Replit describes independent Agents working on parallel tasks and scheduling dependent tasks after prerequisites; concurrency depends on the plan, and the docs do not describe user-authored scripts, DAGs, teams, or swarms. | [src](https://docs.replit.com/learn/build-in-parallel) |
| mcp | ◐ partial | Replit Agent connects to external MCP tools; custom servers require HTTPS, and users are told to connect only trusted servers. | [src](https://docs.replit.com/chat/connect-through-mcp) |
| hooks_lifecycle | ? unknown | The Agent page describes planning, testing, and checkpoints but does not answer whether lifecycle hooks are supported. | [src](https://docs.replit.com/replitai/agent) |
| skills | ◐ partial | Skills are reusable instructions stored in a project's /.agents/skills directory and persist across Agent sessions; private repositories are not supported for the documented GitHub import flow. | [src](https://docs.replit.com/learn/agent-skills.md) |
| memory_persistence | ◐ partial | Replit documents user and Project memory, but Project memory stays with one Project and memories exclude personal or sensitive information. | [src](https://docs.replit.com/chat/memories) |
| sandboxing | ? unknown | The inspected Agent guide does not answer whether shell commands have sandboxing or permission modes. | [src](https://docs.replit.com/learn/build-with-agent) |
| plan_mode | ◐ partial | Plan Mode allows review before project files or data change; the docs say it is unavailable directly from Conversations and that its usage is billable. | [src](https://docs.replit.com/replitai/plan-mode) |
| background_tasks | ◐ partial | Background tasks run in separate threads and isolated project copies, with review before changes are applied; concurrency is plan-limited (Core 1, Pro 10, Enterprise 64). | [src](https://docs.replit.com/core-concepts/agent/task-system) |
| ide_integration | ? unknown | The Project Editor page describes Replit's own editor but does not answer whether VS Code or JetBrains extensions exist. | [src](https://docs.replit.com/learn/projects-and-artifacts/project-editor) |
| model_agnostic | ◐ partial | Replit offers several model providers and models, but manual selection is limited to the account's available models and eligible plans or modes; Enterprise policies can further restrict the pool. | [src](https://docs.replit.com/features/agent/model-selector) |
| plugins | ? unknown | The General Agent page describes connectors, not a third-party plugin or extension API. | [src](https://docs.replit.com/features/agent/general-agent) |
| session_resume | ? unknown | Chat docs say chats can be continued but do not answer whether a previous Agent session can be restored. | [src](https://docs.replit.com/chat) |
| cost_controls | ◐ partial | Replit documents usage tracking, alerts, and hard spending caps; organization budgets must be in $500 increments. | [src](https://docs.replit.com/billing/managing-spend) |

## Architecture

Replit's documentation presents Agent as operating on projects in the Replit environment, with Plan Mode separating planning from file-changing Build work. Background tasks use separate threads and isolated copies, and completed work includes a work log, test results, and preview before it is applied to the main project. Independent tasks can run concurrently, while dependent tasks wait for prerequisite work and approval; concurrency depends on the plan. (https://docs.replit.com/learn/plan-vs-build-mode, https://docs.replit.com/core-concepts/agent/task-system, https://docs.replit.com/learn/build-in-parallel)

## Context management

Agent can receive context such as files, screenshots, errors, and project annotations. Project Skills are stored in /.agents/skills, persist across Agent sessions, and can be version-controlled. Replit documents user and Project memories; Project memory is scoped to a single Project, and memories are private by default and contextual rather than executable instructions. (https://docs.replit.com/learn/build-with-agent, https://docs.replit.com/learn/agent-skills.md, https://docs.replit.com/chat/memories)

## Ecosystem

Replit connectors let Agent read and write to services such as BigQuery, Linear, Slack, and Notion after connection. Replit Agent can connect to external MCP servers, while compatible MCP clients can also use Replit's MCP Server to work with Replit Apps. Skills are described as portable across agents, and Routines can schedule recurring work associated with a chat. (https://docs.replit.com/features/agent/general-agent, https://docs.replit.com/chat/connect-through-mcp, https://docs.replit.com/learn/agent-skills.md, https://docs.replit.com/chat/routines)

## Governance

Plan Mode waits for user approval before changing project files, and background-task results normally remain separate until reviewed and applied. Replit says paid actions require confirmation and documents spending alerts and hard budget caps. Publishing includes user choices for deployment and access settings, security review, and a Publish action. (https://docs.replit.com/replitai/plan-mode, https://docs.replit.com/core-concepts/agent/task-system, https://docs.replit.com/replitai/agent, https://docs.replit.com/billing/managing-spend, https://docs.replit.com/features/publishing)

## Limitations

The inspected documentation does not publish a current Agent version, and no dedicated Agent 3 documentation page appeared in the docs index. Lifecycle hooks, shell sandbox or permission modes, a plugin API, VS Code or JetBrains extensions, and restoring a prior Agent session were not established by the fetched pages. Background tasks are documented as separate task Agents, not as child-agent spawning; orchestration concurrency is plan-limited. The model selector is limited to the available account-authorized models. Several requested Agent-specific paths returned 404, leaving the related capabilities unknown.

## In its own words

> Use Plan mode when you want Agent to think first and wait for your approval before changing files.  
> — [https://docs.replit.com/learn/build-with-agent](https://docs.replit.com/learn/build-with-agent)

> Background tasks are separate threads where Agent works independently in isolated copies of your project.  
> — [https://docs.replit.com/core-concepts/agent/task-system](https://docs.replit.com/core-concepts/agent/task-system)

> The Model Context Protocol (MCP) is an open standard for connecting AI products with tools and data sources  
> — [https://docs.replit.com/chat/connect-through-mcp](https://docs.replit.com/chat/connect-through-mcp)

> Project memory stays with one Project and is retrieved when relevant.  
> — [https://docs.replit.com/chat/memories](https://docs.replit.com/chat/memories)


## Notable

The Replit Agent page's embedded video title says 'Agent 4', but the page does not identify that as the current product version. Replit's documented parallel work is task-based and plan-gated; the inspected docs did not describe scripts or DAG-based workflows.

## Sources fetched

- https://docs.replit.com/replitai/agent
- https://docs.replit.com/replitai/agent/agent-3
- https://docs.replit.com/replitai/agent/checkpoints
- https://docs.replit.com/replitai/agent/deployments
- https://docs.replit.com/replitai/agent/workflows
- https://docs.replit.com/features/agent/general-agent
- https://docs.replit.com/billing/ai-billing#agent-billing
- https://docs.replit.com/features/collaboration/enterprise-model-controls
- https://docs.replit.com/llms.txt
- https://docs.replit.com/features/agent/plan-mode
- https://docs.replit.com/core-concepts/agent/task-system
- https://docs.replit.com/features/agent/skills
- https://docs.replit.com/billing/ai-billing
- https://docs.replit.com/learn/build-with-agent.md
- https://docs.replit.com/chat/connect-through-mcp.md
- https://docs.replit.com/build/connect-via-mcp.md
- https://docs.replit.com/learn/model-context-protocol.md
- https://docs.replit.com/learn/build-in-parallel.md
- https://docs.replit.com/learn/plan-vs-build-mode.md
- https://docs.replit.com/billing/managing-spend.md
- https://docs.replit.com/chat/routines.md
- https://docs.replit.com/learn/agent-skills.md
- https://docs.replit.com/chat/conversations.md
- https://docs.replit.com/chat/overview.md
- https://docs.replit.com/chat/model-selector.md
- https://docs.replit.com/chat/auto-mode.md
- https://docs.replit.com/build/publish-your-app.md
- https://docs.replit.com/learn/projects-and-artifacts/replit-deployments.md
- https://docs.replit.com/features/agent/agent-skills
- https://docs.replit.com/chat/agent-skills
- https://docs.replit.com/build/use-agent-skills
- https://docs.replit.com/features/agent/model-selector
- https://docs.replit.com/teams/enterprise-model-controls
- https://docs.replit.com/features/agent/checkpoints
- https://docs.replit.com/learn/build-with-agent
- https://docs.replit.com/chat/connect-through-mcp
- https://docs.replit.com/build/connect-via-mcp
- https://docs.replit.com/learn/model-context-protocol
- https://docs.replit.com/core-concepts/agent/task-system
- https://docs.replit.com/learn/build-in-parallel
- https://docs.replit.com/learn/projects-and-artifacts/project-editor
- https://docs.replit.com/chat/memories
- https://docs.replit.com/learn/agent-memory
- https://docs.replit.com/features/agent/agent-modes
- https://docs.replit.com/chat/model-selector
- https://docs.replit.com/chat/agent-modes
- https://docs.replit.com/chat/memories.md
- https://docs.replit.com/chat/connect-through-mcp

# Cursor

- **repo:** Anysphere (closed source; no public product repository)
- **version pin:** `Cursor 3.x (client builds up to 3.21.9 referenced in docs; latest changelog entry September 23, 2026)` — Closed-source product with no public repo, so vendor docs and the changelog are the source: the docs cite client versions up to 3.21.9 ("Enterprise teams need Cursor 3.21.9 or later", https://cursor.com/docs/agent/projects) and the agents window describes "Agents Window is generally available with Cursor 3" (https://cursor.com/docs/agent/agents-window); the changelog's newest entry is "Rollouts and Security Review", September 23, 2026 (https://cursor.com/changelog). The scripting package @cursor/sdk stood at 1.0.31 (https://cursor.com/docs/sdk/changelog).
- **docs home:** https://cursor.com/docs

## What it promises

In its own framing, "Cursor is a coding agent for building ambitious software. Use it to understand your codebase, plan and build features, fix bugs, review changes, and work with the tools you already use." Around that editor-era pitch, the docs now present an agent-first expansion: an Agents Window for running many parallel agents, Projects that "maintain context over months of work," and cloud agents that keep building while your laptop is closed.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | Custom subagents are markdown files in .cursor/agents/ or ~/.cursor/agents/ (with Claude and Codex compatibility paths), configurable with model, readonly, and is_background fields; since Cursor 2.5 subagents can spawn child subagents in a tree capped at two levels. Background subagents keep running after the parent turn, local agents only. | [src](https://cursor.com/docs/subagents) |
| workflow_orchestration | ✅ yes | Three orchestration surfaces: Projects (a coordinator agent that manages many parallel cloud agents with months-long shared context and event subscriptions), Automations (cloud agents triggered by schedules, GitHub/GitLab/Slack/webhooks/Linear events), and the SDK/Cloud Agents API for programmatic orchestrators. Nested subagent trees add in-run parallelism; there is no DAG DSL — orchestration is agent-mediated or scripted via SDK. | [src](https://cursor.com/docs/agent/projects) |
| mcp | ✅ yes | Supports stdio, SSE, and Streamable HTTP transports, static OAuth for remote servers, one-click marketplace install, MCP Apps extension, and team-admin distribution of MCP servers. | [src](https://cursor.com/docs/mcp) |
| hooks_lifecycle | ✅ yes | Also covers subagentStart/subagentStop, beforeShellExecution/afterShellExecution, beforeMCPExecution/afterMCPExecution, beforeReadFile/afterFileEdit, beforeSubmitPrompt, preCompact, afterAgentResponse/afterAgentThought, plus Tab and workspaceOpen app hooks. Command- or prompt-based scripts configured in .cursor/hooks.json or ~/.cursor/hooks.json. Cloud agents run only a command-based subset — session and MCP hooks are explicitly deferred there. | [src](https://cursor.com/docs/hooks) |
| skills | ✅ yes | Agent Skills open standard; discovered at startup from .cursor/skills, ~/.cursor/skills, and Claude/Codex-compatible directories; resources load progressively on demand; manual / invocation and a built-in /create-skill. | [src](https://cursor.com/docs/skills) |
| memory_persistence | ◐ partial | Persistence is file- and context-based: project rules (.cursor/rules/.mdc), user and team rules, nested AGENTS.md files, and cross-message @Chats references. Projects also maintain shared context files that sync across all their agents for months. An automatic Memories feature is referenced in community threads but is not documented in current vendor docs. | [src](https://cursor.com/docs/rules) |
| sandboxing | ✅ yes | Three run modes (Auto-review default, Allowlist, Run Everything) plus sandbox.json controlling network and file reach; OS-level enforcement via macOS Seatbelt and Linux user namespaces. Caveats documented: 'Auto-review is not a security boundary', and the classifier can misjudge calls; some commands bypass the sandbox and require approval. | [src](https://cursor.com/docs/agent/security/run-modes) |
| plan_mode | ✅ yes | Agent asks clarifying questions, researches, then produces an editable plan; you approve by clicking to build. Available in the editor (Shift+Tab) and CLI (--plan, /plan). Plans saved to home directory by default, movable to the workspace. | [src](https://cursor.com/docs/agent/plan-mode) |
| background_tasks | ✅ yes | Cloud Agents run long tasks server-side in isolated VMs; CLI persistent sessions keep agents running after disconnect (agent persist, /detach, agent persist attach, --resume); subagents have an is_background flag; Automations run cloud agents on schedules or events. | [src](https://cursor.com/docs/cloud-agent) |
| ide_integration | ✅ yes | Cursor's own desktop app is a VS Code-derived IDE plus an agent-first Agents Window; JetBrains IDEs get the agent over ACP (paid plan required, AI Assistant plugin 2025.1+), and Xcode 26.3+ connects via Apple's xcrun mcpbridge MCP server. A standalone CLI and web/iOS clients round out the surfaces. | [src](https://cursor.com/docs/integrations/jetbrains) |
| model_agnostic | ✅ yes | Per-model pages cover Claude, GPT-5.6 variants, Gemini, Grok, Z.ai models, and first-party Composer/Grok; Cursor Router auto-selects models; BYOK usage is supported on Teams/Enterprise (with a Cursor Token Rate on third-party models); subagents can pin specific models with parameters like effort and context size. | [src](https://cursor.com/docs/models-and-pricing) |
| plugins | ✅ yes | Supports its own Cursor Plugins format and the open Agent Plugins standard; distribution via the Cursor Marketplace, community cursor.directory, and team marketplaces admins curate for internal rules, skills, and plugins. | [src](https://cursor.com/docs/plugins) |
| session_resume | ✅ yes | CLI supports agent resume, --continue, /resume, and agent ls to reopen previous chats; persistent sessions survive disconnects. The SDK resumes local or cloud runs with conversation history and per-run stores (in-memory, SQLite, JSONL); the app keeps chat history with side chats, @Chats references, and conversation search. | [src](https://cursor.com/docs/cli/using) |
| cost_controls | ✅ yes | Two usage pools with per-model API rates, a usage dashboard, spend alerts, and admin APIs including Set User Spend Limit (/teams/user-spend-limit), daily usage data, filtered usage events, and team analytics; on-demand usage is opt-in pay-as-you-go at the same API rates. | [src](https://cursor.com/docs/models-and-pricing) |

## Architecture

Cursor ships as a desktop app — a VS Code-derived IDE with an agent-first Agents Window — plus a CLI, web app, iOS app, an SDK, and third-party IDE integrations via Agent Client Protocol and Apple's Xcode MCP bridge (https://cursor.com/docs/integrations/jetbrains). Locally, the agent loop runs in the editor, CLI, or your own Node process, while "all inference goes through Cursor's hosted models in both modes" (https://cursor.com/docs/sdk/typescript). Cloud Agents run the loop server-side in isolated cloud VMs with cloned repos and full development environments, independent of your machine (https://cursor.com/docs/cloud-agent); Projects and Automations execute entirely on those VMs, and self-hosted machines move that runtime onto private infrastructure (https://cursor.com/docs/cloud-agent/self-hosted).

## Context management

Every chat shares a fixed context window; as tokens fill, "Cursor compresses older parts of the conversation into a summary," an event observable through the preCompact hook (https://cursor.com/docs/agent/prompting). Subagents receive clean, isolated context windows and return only results, so long research does not consume the parent's window (https://cursor.com/docs/subagents). Skills load resources progressively and only when relevant (https://cursor.com/docs/skills), while rules inject persistent guidance at the start of the model context (https://cursor.com/docs/rules). Users attach files, folders, terminals, prior chats, diffs, and browser state with @ mentions (https://cursor.com/help/customization/context), and per-model context sizes are configurable, such as claude-opus-5[context=300k] (https://cursor.com/docs/subagents).

## Ecosystem

Plugins "package rules, skills, agents, commands, MCP servers, and hooks into distributable bundles," installed from the Cursor Marketplace or from team marketplaces admins curate for internal distribution (https://cursor.com/docs/plugins). Skills follow the open Agent Skills standard and load from .cursor/skills, ~/.cursor/skills, or Claude/Codex-compatible directories (https://cursor.com/docs/skills); subagents read the same compatibility paths (https://cursor.com/docs/subagents). MCP servers install with one-click OAuth from the marketplace or via hand-written mcp.json and can be pushed team-wide (https://cursor.com/docs/mcp). Automations are distributed as marketplace templates (https://cursor.com/docs/cloud-agent/automations), and a community directory at cursor.directory hosts third-party MCP servers and plugins.

## Governance

Cursor is proprietary, closed-source software: no public product repository exists, and vendor documentation is the source of record for its behavior. It is built by Anysphere, Inc., the San Francisco company founded in 2022 that also publishes the @cursor/sdk packages on npm and PyPI (https://cursor.com/docs/sdk/typescript). Corporate history is now significant — SpaceX confirmed it will acquire Anysphere for $60 billion in an all-stock transaction, announced June 2026 and expected to close in Q3 pending regulatory approvals (https://finance.yahoo.com/markets/stocks/article/spacex-announces-60-billion-cursor-deal-to-boost-ai-coding-125509159.html). Vendor enterprise controls include SSO/SCIM, audit logs, admin and analytics APIs, model-access management, and privacy/data-governance pages (https://cursor.com/docs/account/teams/admin-api).

## Limitations

Documented gaps: session-start/end hooks, MCP-execution hooks, Tab hooks, and workspaceOpen are unavailable or deferred in cloud agents, which also reject prompt-based hooks and user-level hooks (https://cursor.com/docs/hooks). Auto-review is "not a security boundary" and its classifier can misjudge calls (https://cursor.com/docs/agent/security/run-modes); Linux sandboxing needs distro AppArmor packages, and remote environments and the standalone CLI do not ship the sandbox profile. Subagent nesting stops after two levels (https://cursor.com/docs/subagents). Projects exclude Privacy Mode (Legacy) (https://cursor.com/docs/agent/projects). The cheapest plan omits the Other Models pool, on-demand usage, Automations, and the SDK (https://cursor.com/docs/models-and-pricing), and JetBrains integration requires a paid plan (https://cursor.com/docs/integrations/jetbrains).

## In its own words

> Subagents are specialized AI assistants that Cursor's agent can delegate tasks to. Each subagent operates in its own context window, handles specific types of work, and returns its result to the parent agent.  
> — [https://cursor.com/docs/subagents](https://cursor.com/docs/subagents)

> Cloud agents use the same agent fundamentals but run in isolated VMs in the cloud with full development environments instead of on your local machine.  
> — [https://cursor.com/docs/cloud-agent](https://cursor.com/docs/cloud-agent)

> The coordinator doesn't write code itself. It plans the work, delegates it to agents that write the code, and brings the finished work back to you to check.  
> — [https://cursor.com/docs/agent/projects](https://cursor.com/docs/agent/projects)

> Auto-review is not a security boundary. The classifier can make mistakes. It can allow a call you would have blocked, or block a call you would have allowed.  
> — [https://cursor.com/docs/agent/security/run-modes](https://cursor.com/docs/agent/security/run-modes)


## Notable

The orchestration stack is startlingly deep for a code editor — a non-coding coordinator agent that runs teams of cloud agents on Slack, PR, CI, and schedule subscriptions with months-long shared context and two-level subagent trees — while several lifecycle hooks (session start/end, MCP execution) remain explicitly unavailable inside that same cloud runtime.

## Sources fetched

- https://cursor.com/docs
- https://cursor.com/llms.txt
- https://cursor.com/changelog
- https://cursor.com/docs/subagents
- https://cursor.com/docs/hooks
- https://cursor.com/docs/skills
- https://cursor.com/docs/mcp
- https://cursor.com/docs/plugins
- https://cursor.com/docs/rules
- https://cursor.com/docs/agent/plan-mode
- https://cursor.com/docs/agent/security/run-modes
- https://cursor.com/docs/agent/projects
- https://cursor.com/docs/agent/agents-window
- https://cursor.com/docs/agent/prompting
- https://cursor.com/docs/agent/tools/terminal
- https://cursor.com/docs/cloud-agent
- https://cursor.com/docs/cloud-agent/capabilities
- https://cursor.com/docs/cloud-agent/automations
- https://cursor.com/docs/cloud-agent/self-hosted
- https://cursor.com/docs/models-and-pricing
- https://cursor.com/docs/cli/using
- https://cursor.com/docs/cli/headless
- https://cursor.com/docs/cli/changelog
- https://cursor.com/docs/sdk/typescript
- https://cursor.com/docs/integrations/jetbrains
- https://cursor.com/docs/integrations/xcode
- https://cursor.com/docs/account/teams/admin-api
- https://cursor.com/docs/enterprise/llm-safety-and-controls
- https://cursor.com/help/customization/context
- https://finance.yahoo.com/markets/stocks/article/spacex-announces-60-billion-cursor-deal-to-boost-ai-coding-125509159.html

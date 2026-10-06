# Lovable

- **repo:** closed source; no public product repository (only the MCP client skill and Claude Code plugin are OSS at lovablelabs/mcp)
- **version pin:** `no published version identifier (checked 2026-10-06)` — No product version number is published. The docs changelog (https://docs.lovable.dev/changelog) was fetched this run; its newest entry is labelled 'Oct 5, 2026' and carries no version identifier, and the docs index (https://docs.lovable.dev/llms.txt) lists no version page. The only version string in the docs is the REST API version '2026-09-11' (GA) at https://docs.lovable.dev/api-reference/changelog, which pins the API surface, not the product.
- **docs home:** https://docs.lovable.dev/

## What it promises

Lovable presents itself as a full-stack AI development platform: 'Lovable lets individuals and teams build production-grade web applications using natural language', generating frontend, backend, database, authentication and integrations backed by editable code. It claims the whole product lifecycle, 'from early exploration and prototyping to deployment and ongoing operation', and bundles the environment rather than selling it separately: 'Hosting is part of Lovable, not a separate product or add-on.'

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | Lovable starts temporary, read-only subagents (generic subagents plus an 'Explore' subagent that 'uses the most capable model available'), several of them in parallel for independent questions; findings go back to the main agent, since 'All file changes still come from the main Lovable agent.' The user cannot configure them: 'Lovable decides when subagents are useful based on your request.' | [src](https://docs.lovable.dev/features/subagents.md) |
| workflow_orchestration | ◐ partial | Limited to one main agent fanning out read-only investigators and merging their findings: 'Subagents do not coordinate directly with each other. Each one reports back to Lovable, and the main agent combines the findings before deciding what to do next.' There are no user-defined DAGs, scripts, teams or swarm primitives anywhere in the docs, and subagents cannot write. | [src](https://docs.lovable.dev/features/subagents.md) |
| mcp | ✅ yes | Both directions: the agent consumes MCP servers as chat connectors (remote, custom, and local desktop MCP servers reachable through the Lovable desktop app), and Lovable itself is an MCP server at https://mcp.lovable.dev, described as a way to 'Connect AI agents and developer tools to Lovable using the Model Context Protocol', with documented setup for ChatGPT, Claude, Claude Code, Cursor and VS Code, including knowledge/skill tools and plan_mode on send_message. | [src](https://docs.lovable.dev/integrations/lovable-mcp-server.md) |
| hooks_lifecycle | ? unknown | Nothing in the fetched documentation index or any page describes lifecycle hooks (pre/post tool, session start/stop, or equivalent automation callbacks); the only webhook mentions in the docs are app-level connector features such as Tally and Lovable payments. No hooks page exists in the docs index, so this cell is unresolved rather than denied. | [src](https://docs.lovable.dev/llms.txt) |
| skills | ✅ yes | Workspace skills are named playbooks with a name, a description telling Lovable when to use them, and markdown instructions; they load on demand and can be invoked as a '/' command, and Lovable also ships skills of its own. 'Skills are portable markdown-based files, so you can inspect exactly what Lovable is being told, share them with teammates, import them from GitHub or ZIP, and improve them over time.' | [src](https://docs.lovable.dev/features/skills.md) |
| memory_persistence | ✅ yes | Knowledge is persistent instruction text at two levels - workspace knowledge for rules that apply to every project, project knowledge for architecture, schema and domain context - and the docs state that it is always included in context, unlike skills which load on demand. It is user-authored, not auto-learned from sessions; there is no documented agent-generated memory. | [src](https://docs.lovable.dev/features/knowledge.md) |
| sandboxing | ✅ yes | What bounds the agent is a permission and confirmation system rather than a configurable sandbox: 'Agent permissions' offers Always allow / Ask each time / Never allow for creating projects from chat, project edits, and each connector, reviewable and withdrawable, and publishing is a separate explicit human gate. The docs never document shell or terminal access for the user, so the agent works on Lovable's managed infrastructure and users bound it through approvals and workspace policy (e.g. blocking publishes on critical security findings). | [src](https://docs.lovable.dev/introduction/lovable-account-settings.md) |
| plan_mode | ✅ yes | Plan mode is the first-class 'Plan' option in the project chat: it investigates files and logs, may ask clarifying questions, then writes a structured plan the user reviews, edits and approves before any code is written - 'Plan mode never modifies your code.' It is priced per message (1 credit plus subagent research), and the MCP server exposes the same idea via send_message with plan_mode. | [src](https://docs.lovable.dev/features/plan-mode.md) |
| background_tasks | ✅ yes | Work is asynchronous and server-side: 'Your request runs on Lovable's servers, not in your browser, so you can close the tab and come back later to find the finished result in chat', with a single build message running up to 10 hours and optional browser notifications when it finishes; project monitoring additionally runs scheduled checks of the app. Programmatically, the MCP send_message tool supports wait=false plus get_message polling. | [src](https://docs.lovable.dev/features/projects/chat.md) |
| ide_integration | ✗ no | No first-party VS Code or JetBrains extension is documented anywhere; Lovable integrates with IDEs from the other side, listing 'Claude Code', 'Cursor' and 'VS Code' among the AI clients that connect to its MCP server, and Git sync lets you clone the project and edit the generated codebase in your own editor. The desktop app is a native shell for Lovable itself, not an IDE plugin. | [src](https://docs.lovable.dev/integrations/lovable-mcp-server.md) |
| model_agnostic | ◐ partial | Multiple model families and providers are used under the hood - the EU inference page lists Claude models on Google Cloud Vertex AI and AWS Bedrock, GPT and OpenAI embedding models on Microsoft Azure AI Foundry, and Gemini models for image generation and embeddings (https://docs.lovable.dev/features/eu-inference.md), and it warns that the model serving a task can change. The limitation is that the user has no choice: 'Lovable uses current leading AI models and updates them for everyone automatically ... so you cannot pick a specific model for building', with no BYOK or provider selection documented. | [src](https://docs.lovable.dev/introduction/faq.md) |
| plugins | ◐ partial | Third-party extension happens through connectors and MCP rather than a plugin API for the builder: workspace admins can create custom connectors for any REST API, and any MCP server or MCP registry can be attached as a chat connector. The docs are explicit that this is bring-your-own - 'Lovable does not provide a built-in registry or a curated catalog. You bring your own' - and nothing documents plugins that add new commands, tools, or lifecycle behaviour to the agent itself. | [src](https://docs.lovable.dev/integrations/mcp-registries.md) |
| session_resume | ✅ yes | Sessions are durable server-side threads rather than processes to resume: the project chat keeps the conversation across Chat, Plan and Build modes, work continues while the browser is closed, and 'all changes made after that point stay in the project chat and can be reapplied anytime' alongside automatic per-change version history you can preview and revert. Workspace-level Chats are also continuous conversations with their own history across web, Slack and Telegram. | [src](https://docs.lovable.dev/features/projects/history.md) |
| cost_controls | ✅ yes | Credits are the single meter for building, chat, hosting, Cloud usage, connectors and app AI features, with a per-message cost shown in the chat; long-running messages pause at a credit check-in level (20 credits by default, adjustable between 20 and 100,000). Workspace controls add per-member credit limits, daily chat allowances, spend/auto top-up limits and alerts, and building stops with a blocking dialog when credits run out. | [src](https://docs.lovable.dev/introduction/credits-and-usage.md) |

## Architecture

Lovable is a closed-source, browser-hosted SaaS: the agent executes on Lovable's servers rather than the user's machine ('Your request runs on Lovable's servers, not in your browser', https://docs.lovable.dev/features/projects/chat.md), so there is no local file system, shell or package install to inspect - projects are workspaces the agent edits on the user's behalf. The user-facing surface is the project chat with three modes (Chat, Plan, Build; https://docs.lovable.dev/features/plan-mode.md and https://docs.lovable.dev/features/agent-mode.md) beside a live preview that the docs call a private staging environment sharing the published app's backend and data (https://docs.lovable.dev/features/projects/preview.md). Changes are checkpointed automatically as versions with diffs (https://docs.lovable.dev/features/projects/history.md), and publishing deploys a snapshot to a hosted URL (https://docs.lovable.dev/features/publish.md). The model layer is multi-provider but opaque to users: Claude models via Google Cloud Vertex AI and AWS Bedrock, GPT/OpenAI embedding models via Microsoft Azure AI Foundry, and Gemini models for image generation and embeddings, with 'Lovable may change which model serves a task' (https://docs.lovable.dev/features/eu-inference.md). Lovable is an MCP server at mcp.lovable.dev for external agents and an MCP client for chat connectors (https://docs.lovable.dev/integrations/lovable-mcp-server.md), with a REST API whose only version string is the GA API version 2026-09-11 (https://docs.lovable.dev/api-reference/changelog).

## Context management

Context is managed explicitly rather than automatically. Knowledge (workspace and project level) is always injected into context as persistent instructions, while skills load on demand only when the task matches (https://docs.lovable.dev/features/knowledge.md, https://docs.lovable.dev/features/skills.md); the docs frame this as the dividing line - always-relevant rules go in knowledge, task-specific playbooks become skills. Subagents are the containment mechanism for large investigations: 'Subagents start with fresh context. They do not automatically see the full chat, previous messages, or everything Lovable has already read', receiving only the briefing Lovable passes in, which keeps file contents, logs and abandoned paths out of the main thread (https://docs.lovable.dev/features/subagents.md). Users add context per message with '@' references to projects, connectors, code, designs and uploaded files, including cross-project referencing (https://docs.lovable.dev/features/projects/chat.md), and inspect exactly what changed through per-version diffs and the read_file/get_diff MCP tools (https://docs.lovable.dev/integrations/lovable-mcp-server.md). For very large work, the '/goal' command lets one message run up to 10 hours without pausing for questions (https://docs.lovable.dev/features/goal-runs.md).

## Ecosystem

The extension surface is connectors plus MCP. Lovable ships 50+ app and chat connectors (Linear, Slack, Twilio, Notion, HubSpot, Google Workspace, AWS S3, Stripe, Supabase and more), lets workspace admins build custom connectors for any REST API, and accepts any MCP server - remote, custom, or local ones exposed by desktop apps such as Figma Desktop and Paper - as a chat connector, with optional MCP registries that admins point at their company's directory (https://docs.lovable.dev/integrations/create-connector.md, https://docs.lovable.dev/integrations/mcp-registries.md, https://docs.lovable.dev/integrations/desktop-app.md). In the other direction, the Lovable MCP server at https://mcp.lovable.dev exposes project, deploy, code-inspection, knowledge and skill tools to ChatGPT, Claude, Claude Code, Cursor and VS Code (https://docs.lovable.dev/integrations/lovable-mcp-server.md), and a versioned REST API exists for scripts and services (https://docs.lovable.dev/api-reference/changelog). Generated apps are not locked in: Git sync to GitHub, GitLab or Bitbucket, codebase download and external deployment are documented (https://docs.lovable.dev/integrations/git-sync-overview.md), and users reach the same projects from the desktop app, mobile apps, Slack, Telegram and the ChatGPT app (https://docs.lovable.dev/integrations/desktop-app.md).

## Governance

Governance is workspace-scoped and policy-heavy, which is where a hosted builder can enforce what a local harness cannot. Workspaces carry roles, groups, project access, verified domains, SSO and SCIM provisioning (https://docs.lovable.dev/introduction/lovable-for-enterprise.md), and Privacy & security settings let admins restrict invitations, require 2FA, control who may publish externally, block publishing while unresolved critical security findings or PII findings exist, and gate remote MCP connectors, local desktop MCP servers and third-party MCP clients - the latter disabled by default on Enterprise (https://docs.lovable.dev/features/privacy-and-security-settings.md). Every publish runs a security scan automatically, with Quick/Deep scans, dependency and secret checks, and optional Wiz or Aikido integrations (https://docs.lovable.dev/features/security.md). Enterprise adds searchable audit logs with actor, IP and user agent retained about 90 days, a workspace security center, an insights dashboard, an EU-inference switch that keeps model requests on EU endpoints, and an extended-retention model switch that otherwise excludes some of the most capable models (https://docs.lovable.dev/features/privacy-and-security-settings.md). Cost governance is equally explicit: per-member credit limits, credit check-in thresholds, spend limits on auto top-up, and blocking dialogs when credits run out (https://docs.lovable.dev/introduction/credits-and-usage.md).

## Limitations

The product publishes no version identifier at all - only the changelog's dated entries and the API's 2026-09-11 GA version (https://docs.lovable.dev/changelog, https://docs.lovable.dev/api-reference/changelog) - so capability claims can only be pinned to a checked date. Users cannot choose or bring a model: 'you cannot pick a specific model for building' (https://docs.lovable.dev/introduction/faq.md). Subagents are read-only and do not coordinate with each other (https://docs.lovable.dev/features/subagents.md), and there is no documented hooks system, no plugin API that adds tools to the agent itself, and no IDE extension. Because the agent runs entirely in Lovable's hosted environment, there is no local shell, no sandbox permission modes in the local-harness sense, and the preview - the 'staging' space - shares the same backend and data as the published app (https://docs.lovable.dev/features/projects/preview.md). Long autonomous runs are bounded: credit check-ins pause a message at a threshold and a workspace with zero credits pauses work regardless of settings (https://docs.lovable.dev/introduction/credits-and-usage.md).

## In its own words

> Lovable lets individuals and teams build production-grade web applications using natural language.  
> — [https://docs.lovable.dev/introduction/welcome.md](https://docs.lovable.dev/introduction/welcome.md)

> Subagents can inform the work, but they cannot change your project.  
> — [https://docs.lovable.dev/features/subagents.md](https://docs.lovable.dev/features/subagents.md)

> Your request runs on Lovable's servers, not in your browser, so you can close the tab and come back later to find the finished result in chat.  
> — [https://docs.lovable.dev/features/projects/chat.md](https://docs.lovable.dev/features/projects/chat.md)

> Only the current version is deployed, and later changes are not automatically pushed live: when you keep working on a published project, republish to update your live app.  
> — [https://docs.lovable.dev/features/publish.md](https://docs.lovable.dev/features/publish.md)

> Lovable uses current leading AI models and updates them for everyone automatically.  
> — [https://docs.lovable.dev/introduction/faq.md](https://docs.lovable.dev/introduction/faq.md)


## Notable

For a browser-hosted builder most harness axes collapse into human gates rather than configurable machinery: the docs never mention a shell, terminal, or any IDE/editor extension. What bounds the agent is an explicit permission system with three modes per action and per connector (Always allow / Ask each time / Never allow) plus a separate Publish step, and the preview is a private staging environment that nonetheless shares the published app's backend and data. Lovable is also simultaneously an MCP client (chat connectors, including local desktop MCP servers) and an MCP server that external agents such as Claude Code, Cursor and VS Code connect to, and its subagents are strictly read-only investigators that 'do not coordinate directly with each other.'

## Sources fetched

- https://docs.lovable.dev/
- https://docs.lovable.dev/llms.txt
- https://docs.lovable.dev/changelog
- https://lovable.dev/changelog
- https://docs.lovable.dev/changelog.md
- https://docs.lovable.dev/api-reference/changelog.md
- https://docs.lovable.dev/introduction/welcome.md
- https://docs.lovable.dev/introduction/faq.md
- https://docs.lovable.dev/introduction/credits-and-usage.md
- https://docs.lovable.dev/introduction/lovable-for-enterprise.md
- https://docs.lovable.dev/introduction/lovable-account-settings.md
- https://docs.lovable.dev/features/subagents.md
- https://docs.lovable.dev/features/skills.md
- https://docs.lovable.dev/features/knowledge.md
- https://docs.lovable.dev/features/plan-mode.md
- https://docs.lovable.dev/features/agent-mode.md
- https://docs.lovable.dev/features/goal-runs.md
- https://docs.lovable.dev/features/chats.md
- https://docs.lovable.dev/features/projects/chat.md
- https://docs.lovable.dev/features/projects/history.md
- https://docs.lovable.dev/features/projects/preview.md
- https://docs.lovable.dev/features/drafts.md
- https://docs.lovable.dev/features/publish.md
- https://docs.lovable.dev/features/hosting.md
- https://docs.lovable.dev/features/security.md
- https://docs.lovable.dev/features/testing.md
- https://docs.lovable.dev/features/browser-testing.md
- https://docs.lovable.dev/features/project-monitoring.md
- https://docs.lovable.dev/features/project-usage.md
- https://docs.lovable.dev/features/cloud.md
- https://docs.lovable.dev/features/jobs.md
- https://docs.lovable.dev/features/ai.md
- https://docs.lovable.dev/features/eu-inference.md
- https://docs.lovable.dev/features/privacy-and-security-settings.md
- https://docs.lovable.dev/features/workspace-admin-settings.md
- https://docs.lovable.dev/features/agent-integrations.md
- https://docs.lovable.dev/integrations/lovable-mcp-server.md
- https://docs.lovable.dev/integrations/chat-connectors.md
- https://docs.lovable.dev/integrations/custom-mcp.md
- https://docs.lovable.dev/integrations/mcp-registries.md
- https://docs.lovable.dev/integrations/create-connector.md
- https://docs.lovable.dev/integrations/admin-controls.md
- https://docs.lovable.dev/integrations/desktop-app.md
- https://docs.lovable.dev/integrations/git-sync-overview.md

# Tabnine

- **repo:** https://github.com/codota/TabNine
- **version pin:** `v6.6.8` — vendor release notes list v6.6.8 as the latest version, without a date: https://docs.tabnine.com/main/administering-tabnine/release-notes.md (the GitHub repo is archived/read-only and holds no backend source)
- **docs home:** https://docs.tabnine.com/main

## What it promises

Tabnine presents Agent as an initiative-enhanced version of Chat for larger development tasks, including codebase-wide refactoring, test generation, documentation synthesis, and policy validation. It says Agent uses project state and context while maintaining a feedback loop with the developer.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ◐ partial | The CLI delegates to specialized child agents exposed as tools, but the documented implementation is CLI-only and the CLI is in maintenance mode with planned deprecation after 2026-12-31. | [src](https://docs.tabnine.com/main/getting-started/tabnine-cli/features/subagents.md) |
| workflow_orchestration | ◐ partial | CLI subagents can be invoked by the main agent, which combines their findings, and custom commands provide reusable prompt workflows; the documentation does not describe DAG, team, or swarm orchestration. | [src](https://docs.tabnine.com/main/getting-started/tabnine-cli/features/subagents.md) |
| mcp | ✅ yes | Tabnine IDE and CLI support MCP servers, including STDIO, SSE, and HTTP transports; the IDE MCP list requires an open project folder. | [src](https://docs.tabnine.com/main/getting-started/tabnine-agent/mcp-intro-and-setup/mcp-server-config.md) |
| hooks_lifecycle | ◐ partial | CLI hooks cover session, prompt, model, tool, compression, and notification events; the documentation describes CLI hooks, not IDE hooks. | [src](https://docs.tabnine.com/main/getting-started/tabnine-cli/features/hooks.md) |
| skills | ◐ partial | Reusable skills are documented for the CLI and IDE Agent instructions describe project and user skill directories; workspace-level CLI skills load only for trusted workspaces. | [src](https://docs.tabnine.com/main/getting-started/tabnine-cli/features/agent-skills.md) |
| memory_persistence | ◐ partial | CLI settings support persistent context files, session checkpointing, and session retention; the documentation does not establish automatic cross-session conversational memory. | [src](https://docs.tabnine.com/main/getting-started/tabnine-cli/features/settings/settings-reference.md) |
| sandboxing | ◐ partial | CLI commands can run in OS-specific sandboxes with write and network controls; available backends depend on the operating system and installed runtime. | [src](https://docs.tabnine.com/main/getting-started/tabnine-cli/features/sandboxing.md) |
| plan_mode | ◐ partial | CLI Plan Mode presents a plan for approval before implementation, but in headless or CI use the plan tools are auto-approved and execution switches to YOLO mode. | [src](https://docs.tabnine.com/main/getting-started/tabnine-cli/features/plan-mode.md) |
| background_tasks | ◐ partial | CLI docs expose a background-shells view and release notes refer to CLI background tasks; the fetched docs do not detail a general asynchronous agent-job lifecycle. | [src](https://docs.tabnine.com/main/getting-started/tabnine-cli/features/commands.md) |
| ide_integration | ✅ yes | Tabnine documents support for VS Code, JetBrains IDEs, Eclipse, and Visual Studio; supported platforms vary by IDE. | [src](https://docs.tabnine.com/main/welcome/readme/supported-ides.md) |
| model_agnostic | ◐ partial | Tabnine Chat documents models from multiple providers and enterprise admins can configure private model endpoints, but availability is admin-controlled and the Tabnine OpenCode distribution locks its provider to Tabnine. | [src](https://docs.tabnine.com/main/welcome/readme/ai-models.md) |
| plugins | ◐ partial | CLI extensions can add tools, context, commands, and workflows; the extension documentation does not define a general public plugin API or compatibility guarantees. | [src](https://docs.tabnine.com/main/getting-started/tabnine-cli/features/extensions.md) |
| session_resume | ◐ partial | CLI commands support browsing and resuming previous sessions and saved conversations; this is documented for the maintenance-mode CLI. | [src](https://docs.tabnine.com/main/getting-started/tabnine-cli/features/commands.md) |
| cost_controls | ✅ yes | Admins can set organization, user, and team monthly spending caps and view usage analytics. | [src](https://docs.tabnine.com/main/administering-tabnine/managing-your-team/settings/agent-settings.md) |

## Architecture

Tabnine describes a platform composed of an IDE client, a Kubernetes cluster, and Tabnine AI models. The IDE plugin requests assistance from a remote Tabnine cluster using the relevant context window; the architecture page says code is not stored or sent to its analytics data plane. SaaS deployments run in Tabnine's cloud, while Enterprise customers can use VPC, on-premises, or air-gapped private installations. (https://docs.tabnine.com/main/welcome/readme/architecture.md, https://docs.tabnine.com/main/welcome/readme/architecture/deployment-options.md)

## Context management

Tabnine documents context from open and related files, conversation history, workspace indexing, and retrieval-augmented generation. Repository-wide context can connect to GitHub, GitLab, or Bitbucket, subject to repository access permissions. CLI settings support persistent context files and optional session checkpoints; the documentation does not establish automatic long-term conversational memory. (https://docs.tabnine.com/main/welcome/readme/personalization.md, https://docs.tabnine.com/main/welcome/readme/personalization/tabnines-personalization-in-depth.md, https://docs.tabnine.com/main/getting-started/tabnine-cli/features/settings/settings-reference.md)

## Ecosystem

Tabnine supports multiple IDE families and offers MCP connections for external tools and data. Its model documentation lists Tabnine models and third-party model families; Enterprise admins can configure private endpoints. CLI extensions can contribute tools and workflows, but the documentation does not specify a general public extension API. (https://docs.tabnine.com/main/welcome/readme/supported-ides.md, https://docs.tabnine.com/main/getting-started/tabnine-agent/mcp-intro-and-setup.md, https://docs.tabnine.com/main/welcome/readme/ai-models.md, https://docs.tabnine.com/main/getting-started/tabnine-cli/features/extensions.md)

## Governance

Users can configure native-tool and MCP approvals, including auto-approve, ask-first, and disable controls. Organization admins can apply MCP policies such as allow-all, remote-only, allow-list-only, or block-all. Admin controls also include monthly organization, team, and user cost caps; organization guidelines take precedence over personal guidelines. (https://docs.tabnine.com/main/getting-started/tabnine-agent/agent-settings.md, https://docs.tabnine.com/main/administering-tabnine/managing-your-team/settings/mcp-governance.md, https://docs.tabnine.com/main/administering-tabnine/managing-your-team/settings/agent-settings.md)

## Limitations

Tabnine CLI is in maintenance mode, with critical updates planned through 2026-12-31 and deprecation afterward. Several capabilities in the atlas — hooks, subagents, Plan Mode, CLI sandboxing — are documented for that CLI rather than established as general IDE-agent features. Plan Mode has a headless/CI exception that auto-approves the plan tools and enters YOLO mode; the IDE MCP list requires an open project folder.

## In its own words

> Tabnine Agent can be seen as an initiative-enhanced version of Tabnine Chat.  
> — [https://docs.tabnine.com/main/getting-started/tabnine-agent.md](https://docs.tabnine.com/main/getting-started/tabnine-agent.md)

> A subagent is a specialized agent that runs under the main Tabnine Agent.  
> — [https://docs.tabnine.com/main/getting-started/tabnine-cli/features/subagents.md](https://docs.tabnine.com/main/getting-started/tabnine-cli/features/subagents.md)

> Execution begins *only* after you approve the plan.  
> — [https://docs.tabnine.com/main/getting-started/tabnine-cli/features/plan-mode.md](https://docs.tabnine.com/main/getting-started/tabnine-cli/features/plan-mode.md)

> A project folder must be open for the MCP list to update.  
> — [https://docs.tabnine.com/main/getting-started/tabnine-agent/mcp-intro-and-setup.md](https://docs.tabnine.com/main/getting-started/tabnine-agent/mcp-intro-and-setup.md)


## Notable

Tabnine documents a broad set of CLI agent capabilities, but also says the CLI is in maintenance mode and planned for deprecation after 2026-12-31. The product documentation lists multiple model providers, while its OpenCode distribution documentation says that distribution's provider is locked to Tabnine.

## Sources fetched

- https://docs.tabnine.com/main/welcome
- https://docs.tabnine.com/main/welcome/readme/architecture.md
- https://docs.tabnine.com/main/welcome/readme/ai-models.md
- https://docs.tabnine.com/main/welcome/readme/integrations.md
- https://docs.tabnine.com/main/welcome/readme/supported-ides.md
- https://docs.tabnine.com/main/welcome/readme/personalization.md
- https://docs.tabnine.com/main/welcome/readme/tabnine-subscription-plans.md
- https://docs.tabnine.com/sitemap.xml
- https://docs.tabnine.com/main/llms.txt
- https://docs.tabnine.com/main/sitemap-pages.xml
- https://docs.tabnine.com/main/administering-tabnine/release-notes.md
- https://docs.tabnine.com/main/welcome/readme/personalization/tabnines-personalization-in-depth.md
- https://docs.tabnine.com/main/welcome/readme/architecture/deployment-options.md
- https://docs.tabnine.com/main/administering-tabnine/managing-your-team/settings/models-settings.md
- https://docs.tabnine.com/main/getting-started/tabnine-agent.md
- https://docs.tabnine.com/main/getting-started/tabnine-agent/how-to-use-tabnine-agent.md
- https://docs.tabnine.com/main/getting-started/tabnine-agent/guidelines.md
- https://docs.tabnine.com/main/getting-started/tabnine-agent/agent-settings.md
- https://docs.tabnine.com/main/getting-started/tabnine-agent/agents-in-action.md
- https://docs.tabnine.com/main/getting-started/tabnine-agent/mcp-intro-and-setup.md
- https://docs.tabnine.com/main/getting-started/tabnine-agent/mcp-intro-and-setup/mcp-server-config.md
- https://docs.tabnine.com/main/administering-tabnine/managing-your-team/settings/mcp-governance.md
- https://docs.tabnine.com/main/getting-started/tabnine-cli/features/subagents.md
- https://docs.tabnine.com/main/getting-started/tabnine-cli/features/agent-skills.md
- https://docs.tabnine.com/main/getting-started/tabnine-cli/features/hooks.md
- https://docs.tabnine.com/main/getting-started/tabnine-cli/features/plan-mode.md
- https://docs.tabnine.com/main/getting-started/tabnine-cli/features/sandboxing.md
- https://docs.tabnine.com/main/getting-started/tabnine-cli/features/extensions.md
- https://docs.tabnine.com/main/getting-started/tabnine-cli/features/settings.md
- https://docs.tabnine.com/main/administering-tabnine/managing-your-team/settings/agent-settings.md
- https://docs.tabnine.com/main/getting-started/tabnine-cli/features/hooks/event-reference.md
- https://docs.tabnine.com/main/getting-started/tabnine-cli/features/background-agents.md
- https://docs.tabnine.com/main/getting-started/tabnine-cli/features/settings/settings-reference.md
- https://docs.tabnine.com/main/getting-started/tabnine-cli/features/model-selection.md
- https://docs.tabnine.com/main/getting-started/tabnine-cli/features/ide-integration.md
- https://docs.tabnine.com/main/getting-started/tabnine-plugin-for-opencode.md
- https://docs.tabnine.com/main/getting-started/tabnine-cli/features/commands.md
- https://docs.tabnine.com/main/administering-tabnine/managing-your-team/user-management/service-accounts-and-token-limits.md
- https://github.com/codota/TabNine

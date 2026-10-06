# Augment Code

- **repo:** augmentcode/auggie
- **version pin:** `0.36.0` — npm latest dist-tag for @augmentcode/auggie at https://registry.npmjs.org/@augmentcode%2Fauggie/latest
- **docs home:** https://docs.augmentcode.com/

## What it promises

Augment presents Auggie as a terminal coding agent combining an agent, Context Engine, and tools. Its Context Engine is positioned as providing codebase context for agents. Cosmos presents Experts and trigger-driven automations as building blocks for repeatable software workflows.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | Auggie supports configurable subagents that run in parallel with independent context. | [src](https://docs.augmentcode.com/cli/subagents) |
| workflow_orchestration | ✅ yes | Cosmos documents trigger-driven Expert sessions, manager-to-worker delegation, and software-factory workflows. | [src](https://docs.augmentcode.com/cosmos/automations) |
| mcp | ✅ yes | Auggie supports MCP servers, and the Context Engine is available to agents over MCP. | [src](https://docs.augmentcode.com/cli/integrations) |
| hooks_lifecycle | ✅ yes | Hooks cover tool and session lifecycle events; only PreToolUse can block a tool. | [src](https://docs.augmentcode.com/cli/hooks) |
| skills | ✅ yes | Reusable skills provide specialized guidance and workflows. | [src](https://docs.augmentcode.com/cli/skills) |
| memory_persistence | ✅ yes | Cosmos Experts can retain Markdown memory across sessions. | [src](https://docs.augmentcode.com/cosmos/experts-memory) |
| sandboxing | ◐ partial | Tool permissions can allow, deny, or delegate decisions, but the documented enforcement does not apply to the IDE extension. | [src](https://docs.augmentcode.com/cli/permissions) |
| plan_mode | ? unknown | Tasklists support breaking work into steps and reviewing it, but the fetched documentation does not establish an explicit plan-then-approve gate. | [src](https://docs.augmentcode.com/using-augment/tasklist) |
| background_tasks | ✅ yes | CLI print mode is documented for automation and background tasks; Cosmos also documents parallel worker sessions. | [src](https://docs.augmentcode.com/cli/overview) |
| ide_integration | ✅ yes | Official integrations include VS Code and JetBrains IDEs. | [src](https://docs.augmentcode.com/setup-augment/install-visual-studio-code) |
| model_agnostic | ✅ yes | The model catalog includes multiple providers and documents user model selection. | [src](https://docs.augmentcode.com/models/available-models) |
| plugins | ✅ yes | Auggie supports plugins distributed through Git-based marketplaces. | [src](https://docs.augmentcode.com/cli/plugins) |
| session_resume | ✅ yes | CLI options support continuing or selecting saved sessions; Cosmos conversations are saved indefinitely. | [src](https://docs.augmentcode.com/cli/reference) |
| cost_controls | ✅ yes | Usage dashboards support budgets and enforcement; the CLI can show credit usage. | [src](https://docs.augmentcode.com/analytics/credit-dashboard-and-quotas) |

## Architecture

Augment provides IDE integrations and the Auggie CLI, alongside a Context Engine exposed through MCP. Cosmos adds Experts, sessions, environments, and trigger-driven automations. Managers can delegate work to worker sessions, while subagents provide a lighter-weight parallel option. Cloud environments are isolated and use configured egress; self-hosted environments use the host machine's resources and network. (https://docs.augmentcode.com/cli/overview, https://docs.augmentcode.com/cosmos/environments)

## Context management

The Context Engine combines code search with relationships across files and repositories, and can incorporate sources such as commit history, documentation, and tickets. Auggie can index the current workspace, with controls over which files are indexed. The docs describe local indexing as updating in real time and remote repository indexing around default-branch commits. Cosmos adds independent agent contexts, persistent Expert memory, and saved sessions; long-paused environments may restart clean and lose uncommitted workspace changes. (https://docs.augmentcode.com/cli/integrations, https://docs.augmentcode.com/cosmos/sessions-overview)

## Ecosystem

Auggie supports MCP over stdio, HTTP, and SSE, and plugins can bundle rules, hooks, skills, subagents, and MCP integrations. IDE documentation covers VS Code and JetBrains, with Vim and Neovim also listed in the documentation index. Cosmos trigger sources include integrations such as GitHub, Linear, Slack, GitLab, and PagerDuty, plus webhooks and schedules; the model catalog spans multiple vendors. (https://docs.augmentcode.com/cli/plugins, https://docs.augmentcode.com/cosmos/config-triggers, https://docs.augmentcode.com/models/available-models)

## Governance

Tool permission rules can allow, deny, or delegate decisions, with documented precedence for matching rules. Cosmos Experts have configured prompts, capabilities, environments, and permissions, and worker access can be restricted. CLI hooks include tool and session events, although only PreToolUse can block a tool. Administrators can set monthly budgets and choose whether reaching them pauses access. (https://docs.augmentcode.com/cli/permissions, https://docs.augmentcode.com/cosmos/experts-memory, https://docs.augmentcode.com/analytics/credit-dashboard-and-quotas)

## Limitations

The fetched documentation does not establish an explicit plan-then-approve mode; Tasklist describes decomposition and review without documenting a mandatory execution gate. Tool permissions are documented as tool-call controls, and their enforcement explicitly excludes the IDE extension. Remote Context Engine indexing is described for connected repositories' default branches; the fetched page does not establish broader indexing or privacy guarantees. Cosmos documents event/Expert and worker primitives, but not a general DAG or swarm abstraction.

## In its own words

> Build features and debug issues with a standalone interactive agent.  
> — [https://docs.augmentcode.com/cli/overview](https://docs.augmentcode.com/cli/overview)

> Perfect for automation, CI/CD pipelines, and background tasks where you want the agent to act without follow-up from a person.  
> — [https://docs.augmentcode.com/cli/overview](https://docs.augmentcode.com/cli/overview)

> A Session's conversation is saved indefinitely — it doesn't expire.  
> — [https://docs.augmentcode.com/cosmos/sessions-overview](https://docs.augmentcode.com/cosmos/sessions-overview)

> Your selection can be changed at any time.  
> — [https://docs.augmentcode.com/models/available-models](https://docs.augmentcode.com/models/available-models)


## Notable

The documented product surface extends beyond the IDE plugin and CLI to Cosmos cloud Experts, worker sessions, trigger automations, and persistent Expert memory. The fetched docs do not establish a mandatory plan-approval mode, and the permissions documentation excludes IDE-extension enforcement.

## Sources fetched

- https://docs.augmentcode.com/
- https://docs.augmentcode.com/llms.txt
- https://docs.augmentcode.com/cli/subagents
- https://docs.augmentcode.com/cli/integrations
- https://docs.augmentcode.com/cli/hooks
- https://docs.augmentcode.com/cli/plugins
- https://docs.augmentcode.com/cli/skills
- https://docs.augmentcode.com/cli/permissions
- https://docs.augmentcode.com/cli/overview
- https://docs.augmentcode.com/cli/reference
- https://docs.augmentcode.com/cli/rules-guidelines
- https://docs.augmentcode.com/context-services/mcp
- https://docs.augmentcode.com/using-augment/tasklist
- https://docs.augmentcode.com/cosmos/automations
- https://docs.augmentcode.com/cosmos/sessions-overview
- https://docs.augmentcode.com/cosmos/experts-memory
- https://docs.augmentcode.com/cosmos/delegating-work
- https://docs.augmentcode.com/cosmos/software-factory
- https://docs.augmentcode.com/cosmos/environments
- https://docs.augmentcode.com/cosmos/config-triggers
- https://docs.augmentcode.com/models/available-models
- https://docs.augmentcode.com/analytics/credit-dashboard-and-quotas
- https://docs.augmentcode.com/usage/token-based-pricing
- https://docs.augmentcode.com/setup-augment/install-visual-studio-code
- https://docs.augmentcode.com/jetbrains/setup-augment/install-jetbrains-ides
- https://docs.augmentcode.com/cli/config
- https://docs.augmentcode.com/cli/autoupgrade
- https://registry.npmjs.org/@augmentcode%2Fauggie/latest

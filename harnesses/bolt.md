# Bolt

- **repo:** stackblitz/bolt.new
- **version pin:** `no published release tag or product version (release notes checked 2026-10-06; latest dated entry Sep 21-27, 2026)` — GitHub releases and tags pages list none (https://github.com/stackblitz/bolt.new/releases, /tags); Bolt release notes https://support.bolt.new/release-notes.md carry dated entries but no product version identifier — the pin is the checked date, labelled as such
- **docs home:** https://support.bolt.new/

## What it promises

Bolt says Plan Mode helps users plan, ask questions, and review changes before continuing. Skills are presented as reusable instructions that Bolt can apply manually or when prompt descriptions match. MCP connectors are presented as a way for Bolt to interact with external applications and data while chatting.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ? unknown | The agent documentation describes agent choices but does not say whether agents can spawn child agents. | [src](https://support.bolt.new/building/using-bolt/agents.md) |
| workflow_orchestration | ? unknown | The agent documentation does not address scripts, DAGs, teams, swarms, or multi-agent orchestration. | [src](https://support.bolt.new/building/using-bolt/agents.md) |
| mcp | ◐ partial | Bolt documents MCP connectors for interacting with external apps and data; connector availability can be set per project, but selected tools apply across projects. | [src](https://support.bolt.new/building/using-bolt/connect-mcp.md) |
| hooks_lifecycle | ? unknown | The project lifecycle page does not describe pre/post-tool or session lifecycle hooks. | [src](https://support.bolt.new/get-started/project-lifecycle.md) |
| skills | ◐ partial | Bolt documents reusable skills that can be applied manually or automatically when a prompt matches; manual application is limited to one skill per prompt. | [src](https://support.bolt.new/building/skills.md) |
| memory_persistence | ✅ yes | Project knowledge persists through long conversations and context clearing; Bolt automatically finds and uses agents.md. | [src](https://support.bolt.new/best-practices/manage-context.md) |
| sandboxing | ? unknown | The security page describes project security checks, not command sandboxing or permission modes. | [src](https://support.bolt.new/building/security.md) |
| plan_mode | ◐ partial | Plan Mode supports reviewing and revising a plan, but the docs do not specify a required approval gate; homepage use creates the app's base structure before presenting the plan. | [src](https://support.bolt.new/best-practices/plan-mode.md) |
| background_tasks | ◐ partial | Bolt queues prompts sent while it is building and processes them in order after the current prompt finishes; the docs do not describe independent concurrent background jobs. | [src](https://support.bolt.new/building/chat-tools.md) |
| ide_integration | ? unknown | The official documentation index does not identify a VS Code or JetBrains extension. | [src](https://support.bolt.new/llms.txt) |
| model_agnostic | ? unknown | Forge documents selectable open-source models, but the page does not identify their providers or establish support for multiple model providers. | [src](https://support.bolt.new/account-and-subscription/bolt-forge.md) |
| plugins | ? unknown | The official documentation index does not identify a third-party plugin or extension API. | [src](https://support.bolt.new/llms.txt) |
| session_resume | ? unknown | The project lifecycle documentation does not address resuming a previous session. | [src](https://support.bolt.new/get-started/project-lifecycle.md) |
| cost_controls | ✅ yes | Bolt documents token balance visibility, allocations, and limits, including free-plan monthly and daily ceilings. | [src](https://support.bolt.new/account-and-subscription/tokens) |

## Architecture

Bolt documents Standard and Max agents powered by large language models, alongside Forge, which offers selectable open-source models. Plan Mode provides a planning-and-review flow, while skills package reusable instructions at workspace or project level. MCP connectors let Bolt interact with external apps and data during chat; the documentation limits tool selection to a shared configuration across projects. (https://support.bolt.new/building/using-bolt/agents.md, https://support.bolt.new/building/using-bolt/connect-mcp.md)

## Context management

Project knowledge is described as persistent and available after context is cleared. Bolt automatically finds agents.md as an instruction entry point. Saved prompts are account-scoped and available across workspaces, while skills are configured at workspace or project level. (https://support.bolt.new/best-practices/manage-context.md, https://support.bolt.new/building/skills.md)

## Ecosystem

The GitHub integration documents repository sync and automatic saves; branch merges must be completed in GitHub. The documentation index lists integrations including Expo, Figma, GitHub, Netlify, Stripe, and Supabase. Forge offers several selectable models, but its documentation does not identify their providers. (https://support.bolt.new/integrations/git, https://support.bolt.new/llms.txt, https://support.bolt.new/account-and-subscription/bolt-forge.md)

## Governance

Plan Mode allows users to review plans and suggest changes, but the docs do not require approval before building. Token allocation and rollover balances are visible under My Subscription, and the free plan has documented monthly and daily ceilings. Bolt also documents project security checks. (https://support.bolt.new/best-practices/plan-mode.md, https://support.bolt.new/account-and-subscription/tokens, https://support.bolt.new/building/security.md)

## Limitations

The Plan Mode documentation says homepage use creates the app's base structure before presenting a plan and does not state that approval is mandatory. GitHub branch merging is not supported in-app; its integration docs also describe a rare timing conflict that can replace the GitHub version with Bolt's changes. MCP connector tools apply across projects even when connector activation is project-specific. Forge models are described as experimental and potentially less reliable than Standard or Max. No release tag or product version identifier was found in the checked release sources.

## In its own words

> You can review this plan, suggest changes, and continue building step by step.  
> — [https://support.bolt.new/best-practices/plan-mode.md](https://support.bolt.new/best-practices/plan-mode.md)

> When you connect an MCP server, Bolt can directly interact with your applications and data while chatting.  
> — [https://support.bolt.new/building/using-bolt/connect-mcp.md](https://support.bolt.new/building/using-bolt/connect-mcp.md)

> After you add an `agents.md` file, Bolt finds and uses it automatically.  
> — [https://support.bolt.new/best-practices/manage-context.md](https://support.bolt.new/best-practices/manage-context.md)

> Bolt currently doesn't support merging branches in-app.  
> — [https://support.bolt.new/integrations/git](https://support.bolt.new/integrations/git)


## Notable

Plan Mode is not documented as a strict plan-then-approve gate, and its homepage flow creates a base structure before showing the plan. MCP supports connected tools, but tool selection is shared across projects.

## Sources fetched

- https://support.bolt.new/
- https://support.bolt.new/llms.txt
- https://support.bolt.new/best-practices/prompting-effectively
- https://support.bolt.new/best-practices/plan-mode
- https://support.bolt.new/best-practices/plan-mode.md
- https://support.bolt.new/best-practices/manage-context
- https://support.bolt.new/best-practices/manage-context.md
- https://support.bolt.new/best-practices/managing-context
- https://support.bolt.new/best-practices/maximizing-token-efficiency
- https://support.bolt.new/best-practices/maximize-token-efficiency
- https://support.bolt.new/concepts/version-history-github
- https://support.bolt.new/building/using-bolt/agents
- https://support.bolt.new/building/using-bolt/agents.md
- https://support.bolt.new/building/agents
- https://support.bolt.new/building/plan-mode
- https://support.bolt.new/building/skills
- https://support.bolt.new/building/skills.md
- https://support.bolt.new/building/prompt-library
- https://support.bolt.new/building/prompt-library.md
- https://support.bolt.new/building/using-bolt/connect-mcp
- https://support.bolt.new/building/using-bolt/connect-mcp.md
- https://support.bolt.new/prompting/prompt-effectively
- https://support.bolt.new/integrations/git
- https://support.bolt.new/integrations/git.md
- https://support.bolt.new/integrations/git
- https://support.bolt.new/account-and-subscription/tokens
- https://support.bolt.new/account-and-subscription/tokens.md
- https://support.bolt.new/account-and-subscription/billing
- https://support.bolt.new/account-and-subscription/bolt-forge.md
- https://support.bolt.new/release-notes.md
- https://support.bolt.new/get-started/project-lifecycle.md
- https://support.bolt.new/building/chat-tools.md
- https://support.bolt.new/building/security.md
- https://support.bolt.new/settings/project-settings.md
- https://github.com/stackblitz/bolt.new
- https://api.github.com/repos/stackblitz/bolt.new/releases/latest
- https://github.com/stackblitz/bolt.new/releases
- https://github.com/stackblitz/bolt.new/tags

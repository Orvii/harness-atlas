# Windsurf

- **repo:** Cognition (formerly Codeium) - closed source; no public product repository. Canonical docs now at docs.devin.ai; docs.windsurf.com is a legacy redirect path.
- **version pin:** `3.10.48` — Closed-source product with no public repo or release tag, so the version is pinned from the vendor changelog: v3.10.48, September 29, 2026 (https://docs.devin.ai/desktop/changelog). The docs.windsurf.com domain is a legacy path that now redirects to docs.devin.ai. Note: the product was renamed "Devin Desktop" on June 2, 2026, and the legacy Cascade agent was removed in v3.9.19 (September 8, 2026).
- **docs home:** https://docs.devin.ai/desktop

## What it promises

Windsurf/Devin Desktop is framed as the command center for "managing teams of agents (local and cloud) working alongside you" - a flow-preserving AI IDE that pairs a local agent with cloud agents, unifies them in a Kanban view, and keeps the classic editor experience from Windsurf days.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | Devin Local spawns subagents in foreground or background; custom profiles are markdown files under agents/ (flat file or directory layout); built-in profiles subagent_explore and subagent_general plus a server-side-default model; the codebase retrieval feature Fast Context is itself described as a specialized subagent. Controlled by a Subagents (Preview) toggle in Devin Settings. | [src](https://docs.devin.ai/cli/subagents) |
| workflow_orchestration | ◐ partial | Kanban board over local and cloud agents, Spaces grouping sessions/PRs per task, parallel git-worktree sessions, background subagents, /handoff moving an in-progress local session to cloud, and legacy arena mode running multiple models in parallel. No documented DAG, scripted, or swarm orchestration primitive beyond managing agent sessions. | [src](https://docs.devin.ai/desktop/agent-command-center) |
| mcp | ✅ yes | Devin Local prompts for approval before any MCP tool call by default, with session/permanent grants per tool or server; enterprise admins can default-allow servers or tools. Legacy Cascade page documents mcp_config.json plus admin registry and allowlist controls. | [src](https://docs.devin.ai/cli/extensibility/mcp/overview) |
| hooks_lifecycle | ✅ yes | Events: PreToolUse, PostToolUse, PermissionRequest, UserPromptSubmit, Stop, PostCompaction, SessionStart, SessionEnd, with regex matcher on tool_name and per-session session_id in payloads. Legacy Cascade had its own shell-command hooks at system/user/workspace levels, blocking via exit code 2, distributable through an enterprise cloud dashboard. | [src](https://docs.devin.ai/cli/extensibility/hooks/lifecycle-hooks) |
| skills | ✅ yes | SKILL.md with YAML frontmatter under .devin/skills (legacy .windsurf/skills still read); progressive disclosure loads only name and description until invocation; skills can carry scoped permissions, pre-approved tools, model overrides, and run as subagents; follows the agentskills.io specification. | [src](https://docs.devin.ai/cli/extensibility/skills/overview) |
| memory_persistence | ◐ partial | Legacy Cascade auto-generated Memories and user-defined Rules persisted across conversations (Cascade-only, and the Cascade agent has since been removed). The current default agent persists context only through rules, AGENTS.md, and skills, not learned memory. | [src](https://docs.devin.ai/desktop/devin-local) |
| sandboxing | ✅ yes | Permission modes Normal/Accept Edits/Smart/Bypass/Autonomous with deny/ask/allow scopes across file reads, writes, commands, HTTP fetches, and MCP tools. Fail-closed: refuses to start if sandbox tooling is unavailable. Windows unsupported (hard-fail); Linux requires bubblewrap and socat. Enterprise team settings can require sandboxing. | [src](https://docs.devin.ai/cli/sandbox) |
| plan_mode | ✅ yes | Plans persist to ~/.devin/plans/plan-<session>.md for editing or reuse; the megaplan/ultraplan/masterplan keyword forces deeper planning with at least one clarifying question; /plan switches modes; Plan mode remains available even inside sandbox sessions. | [src](https://docs.devin.ai/desktop/devin-local#plan-mode) |
| background_tasks | ✅ yes | Background subagents run in parallel while the parent continues (unapproved tools auto-denied, parent notified on completion); long shell commands move to background with a shell ID; devin --cloud -p runs non-interactive cloud sessions that persist for later resume. | [src](https://docs.devin.ai/desktop/devin) |
| ide_integration | ✅ yes | Devin Desktop is itself an IDE-a VS Code fork for macOS, Windows, and Linux that imports VS Code or Cursor settings. Plugins ship for JetBrains, VS Code, Visual Studio, Vim, NeoVim, Jupyter, Chrome, Emacs, Xcode, Sublime Text, and Eclipse; the JetBrains plugin is in maintenance mode with Cascade inside it deprecated. | [src](https://docs.devin.ai/windsurf/plugins/getting-started) |
| model_agnostic | ✅ yes | Model catalog covers Anthropic, OpenAI, Google, xAI, DeepSeek, Moonshot, Qwen, Z.ai, NVIDIA, and Cognition's in-house SWE-1.x/SWE-2 and SWE-grep models. Adaptive is a model router that picks per request; Fusion pairs a frontier lead with a cheap sidekick; GPT usage can bill to a personal ChatGPT Plus/Pro plan via account sign-in. | [src](https://docs.devin.ai/desktop/models) |
| plugins | ✅ yes | Agent plugins work across Devin cloud, Devin CLI, and Devin Desktop; introduced June 16, 2026 in preview and enterprise opt-in (changelog v3.2.16), now documented as the standard extension path. Editor extensions install from Open VSX; other AI code-complete and proprietary extensions are incompatible. | [src](https://docs.devin.ai/cli/extensibility/plugins/overview) |
| session_resume | ✅ yes | devin -c/--continue resumes the most recent session, -r/--resume <id> reopens a specific one, and /resume opens an interactive picker; cloud sessions resume by URL or ID whether started from CLI, web app, or Desktop. | [src](https://docs.devin.ai/cli/essential-commands) |
| cost_controls | ✅ yes | Quota-based system replaced credits in March 2026: daily/weekly budgets by token cost per model, free models excluded, extra-usage purchase for Pro/Teams/Max, usage meter in-app, per-model price tables, enterprise ACUs, and admin analytics (personal analytics is off by default). Docs warn subagent fan-out multiplies spend. | [src](https://docs.devin.ai/desktop/accounts/quota) |

## Architecture

Devin Desktop (formerly Windsurf) is a local desktop IDE - a VS Code fork for macOS, Windows, and Linux - where the default Devin Local agent shares the Devin CLI harness and executes on the developer's machine with local file access, git-worktree isolation, an optional OS-level sandbox, and on-disk state under ~/.devin. Cloud autonomy is explicit and server-side: delegating to Devin hands work to an agent whose loop runs on an isolated cloud VM with shell, browser, and computer use, continuing after the laptop closes, and `devin --cloud` streams those sessions into a terminal. Previews proxy a local dev server into an in-editor browser pane.

## Context management

Fast Context - a specialized subagent built on SWE-grep retrieval models - fires on code-search queries, running parallel searches to cut retrieval time up to 20x while avoiding context pollution. A RAG context engine indexes the whole local codebase (remote repositories for Teams/Enterprise) and supports pinned and custom context. Skills use progressive disclosure: only name and description load until invocation. Prompt caching is a stated priority - Devin Local claims up to 30% fewer tokens than Cascade for the same task - and /compact forces conversation compaction, with PostCompaction a hookable event and a context-window indicator added in recent releases.

## Ecosystem

Three distribution layers. Editor extensions install inside the VS Code-fork IDE from Open VSX (competing AI completion extensions are blocked). Windsurf Plugins extend JetBrains, VS Code, Visual Studio, Vim, NeoVim, Jupyter, Chrome, Emacs, Xcode, Sublime Text, and Eclipse. Agent plugins bundle skills, rules, hooks, MCP servers, and custom subagents, installable from GitHub repos, git URLs, or local folders, and shared across Devin cloud, CLI, and Desktop. Skills follow the agentskills.io SKILL.md specification; rules load from .devin/rules, AGENTS.md, legacy .windsurfrules, and imported .cursor/rules; MCP servers get an enterprise registry and allowlist.

## Governance

Windsurf is closed source - a proprietary commercial IDE with no public product repository, so vendor documentation is the source of record. Codeium lineage shows in artifacts: settings live under ~/.codeium/, installers ship from windsurf-stable.codeiumdata.com, and the legacy `surf` command still ships. Cognition announced on July 14, 2025 that it had "signed a definitive agreement to acquire Windsurf, the agentic IDE," including its IP, product, trademark, and brand. Under Cognition the product became Devin Desktop (June 2, 2026) with Free/Pro/Max/Teams/Enterprise tiers, ACU-based enterprise billing, SSO/SCIM/RBAC, and system-level admin policies.

## Limitations

Documented gaps: the current Devin Local agent does not support memories, workflows, app deploys, or arena mode, and the former Cascade agent was removed in v3.9.19. OS-level sandboxing is unavailable on Windows - sessions hard-fail when --sandbox or Required enforcement is set - and needs bubblewrap plus socat on Linux. Premium models hit vendor rate limits when at capacity. Other AI code-complete and proprietary extensions are incompatible; the JetBrains plugin is in maintenance mode; the agent plugin system launched preview and enterprise-opt-in; MCP tools prompt for approval by default unless enterprises default-allow them.

## In its own words

> Subagents let the main agent spawn independent workers to handle subtasks.  
> — [https://docs.devin.ai/cli/subagents](https://docs.devin.ai/cli/subagents)

> Plan mode is read-only research: the agent investigates your codebase, writes up an approach, and asks for your approval before implementing anything.  
> — [https://docs.devin.ai/desktop/devin-local#plan-mode](https://docs.devin.ai/desktop/devin-local#plan-mode)

> Fast Context is a specialized subagent in Devin Desktop that retrieves relevant code from your codebase up to 20x faster than traditional agentic search.  
> — [https://docs.devin.ai/desktop/context-awareness/fast-context](https://docs.devin.ai/desktop/context-awareness/fast-context)

> We believe the future of software engineering is managing teams of agents (local and cloud) working alongside you.  
> — [https://docs.devin.ai/desktop/devin-desktop-faq](https://docs.devin.ai/desktop/devin-desktop-faq)


## Notable

The Windsurf brand is being retired mid-flight: the same IDE shipped as "Devin Desktop" on June 2, 2026, docs.windsurf.com now redirects to docs.devin.ai, and the Cascade agent was removed entirely in v3.9.19 (September 8, 2026) - yet GPT model usage can now be billed straight to a personal ChatGPT Plus/Pro plan.

## Sources fetched

- https://docs.windsurf.com/windsurf/getting-started (legacy path, redirects to docs.devin.ai/desktop/getting-started)
- https://docs.windsurf.com/llms.txt (legacy index)
- https://docs.devin.ai/llms.txt
- https://docs.devin.ai/_llms/en/desktop.md
- https://docs.devin.ai/desktop/getting-started
- https://docs.devin.ai/desktop/models
- https://docs.devin.ai/desktop/adaptive
- https://docs.devin.ai/desktop/fusion
- https://docs.devin.ai/desktop/agent-command-center
- https://docs.devin.ai/desktop/spaces
- https://docs.devin.ai/desktop/devin
- https://docs.devin.ai/desktop/devin-local
- https://docs.devin.ai/desktop/devin-desktop-faq
- https://docs.devin.ai/desktop/cascade/cascade
- https://docs.devin.ai/desktop/cascade/skills
- https://docs.devin.ai/desktop/cascade/memories
- https://docs.devin.ai/desktop/cascade/workflows
- https://docs.devin.ai/desktop/cascade/worktrees
- https://docs.devin.ai/desktop/cascade/arena
- https://docs.devin.ai/desktop/cascade/mcp
- https://docs.devin.ai/desktop/cascade/hooks
- https://docs.devin.ai/desktop/cascade/web-search
- https://docs.devin.ai/desktop/changelog
- https://docs.devin.ai/desktop/releases
- https://docs.devin.ai/desktop/accounts/usage
- https://docs.devin.ai/desktop/accounts/quota
- https://docs.devin.ai/desktop/accounts/analytics
- https://docs.devin.ai/desktop/context-awareness/fast-context
- https://docs.devin.ai/desktop/context-awareness/overview
- https://docs.devin.ai/desktop/context-awareness/remote-indexing
- https://docs.devin.ai/desktop/previews
- https://docs.devin.ai/desktop/terminal
- https://docs.devin.ai/desktop/troubleshooting/windsurf-common-issues
- https://docs.devin.ai/desktop/enterprise-policies
- https://docs.devin.ai/desktop/acp
- https://docs.devin.ai/windsurf/plugins/getting-started
- https://docs.devin.ai/windsurf/plugins/compatibility
- https://docs.devin.ai/cli/subagents
- https://docs.devin.ai/cli/extensibility/hooks/lifecycle-hooks
- https://docs.devin.ai/cli/extensibility/plugins/overview
- https://docs.devin.ai/cli/extensibility/skills/overview
- https://docs.devin.ai/cli/extensibility/mcp/overview
- https://docs.devin.ai/cli/reference/permissions
- https://docs.devin.ai/cli/reference/configuration/config-file
- https://docs.devin.ai/cli/essential-commands
- https://docs.devin.ai/cli/sandbox
- https://docs.devin.ai/cli/cloud
- https://docs.devin.ai/cli/handoff
- https://docs.devin.ai/cli/fusion
- https://cognition.com/blog/windsurf

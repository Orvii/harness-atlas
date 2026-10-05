# Factory Droid

- **repo:** factory-ai (github.com/factory-ai) — Droid CLI/app themselves are closed source; github.com/factory-ai/factory is a README+docs-only repo with no license, alongside public MIT/Apache-2.0 SDKs, droid-action, and editor extensions
- **version pin:** `v0.233.0 (Droid CLI), v0.190.0 (Desktop app) — October 3, 2026` — Vendor docs changelog page: "234 releases · latest CLI v0.233.0 · Desktop v0.190.0 · October 3, 2026" at https://docs.factory.ai/docs/changelog/release-notes. Closed-source product: no public source repo or release tags exist for the Droid CLI itself, so the docs' stated version is the source.
- **docs home:** https://docs.factory.ai/

## What it promises

"Plan, build, review, and ship software with autonomous agents across desktop, terminal, web, and CLI" — a platform framing where "Droids plan, build, review, test, and ship software across the tools engineering teams already use" (https://factory.com). For the multi-agent story: "Break large projects into subtasks and run them in parallel with multiple Droids. Migrations, refactors, and large features — shipped autonomously" (https://factory.ai/product/missions).

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | Markdown-defined 'custom droids' plus built-in worker and explorer subagents; each invocation runs fresh via the Task tool with its own model, tool policy, and autonomy level. Delegation is one level deep — a subagent cannot spawn its own subagents. | [src](https://docs.factory.ai/docs/harness/subagents) |
| workflow_orchestration | ✅ yes | Factory Missions: orchestrator plus model-configurable worker and validation subagents, launched with /missions or `droid exec --mission`; Mission Control overlay (Ctrl+T); docs give a heuristic sweet spot of ~1–500 features. | [src](https://docs.factory.ai/docs/missions/overview) |
| mcp | ✅ yes | Interactive TUI manager plus `droid mcp` CLI commands; registry quick-start; Factory-managed 'Connectors' offered as a simpler alternative for supported cloud apps. | [src](https://docs.factory.ai/docs/harness/mcp) |
| hooks_lifecycle | ✅ yes | Events: PreToolUse, PostToolUse, UserPromptSubmit, Notification, Stop, SubagentStop, PreCompact, SessionStart, SessionEnd. Configured in ~/.factory/hooks.json, .factory/hooks.json, or org-managed settings; docs warn hooks run with your local credentials. | [src](https://docs.factory.ai/docs/harness/hooks) |
| skills | ✅ yes | Team skills under .factory/skills/, model-invoked by description or user-invoked as /skill-name; Factory ships builtin skills (disable via --disable-builtin-skills). | [src](https://docs.factory.ai/docs/harness/skills) |
| memory_persistence | ◐ partial | No general cross-session agent memory store is documented. Persistence primitives instead: automations keep a memory/ folder across runs ('What carries over between runs so the automation gets better over time'), AGENTS.md provides durable project instructions loaded every session, sessions are resumable/searchable and cloud-synced, Droid Computers retain machine state between sessions, and AutoWiki keeps repo documentation current. | [src](https://docs.factory.com/web/automations) |
| sandboxing | ✅ yes | Seatbelt profiles on macOS, bubblewrap + seccomp on Linux/WSL2, outbound traffic through a filtering proxy with a domain allowlist; per-command (default) or whole-process isolation modes. Layered with Autonomy Levels (Off/Low/Medium/High), permission rules, and Droid Shield. | [src](https://docs.factory.ai/docs/autonomy-and-safety/sandbox) |
| plan_mode | ✅ yes | Droid researches read-only, proposes a plan, then calls ExitSpecMode for explicit approval before returning to Normal Mode; entered via Shift+Tab or --use-spec. Mission Mode is the related post-approval session state. | [src](https://docs.factory.ai/docs/autonomy-and-safety/specification-mode) |
| background_tasks | ✅ yes | Companion tools TaskOutput (block/poll) and TaskStop (SIGTERM then SIGKILL); also headless `droid exec`, scheduled/dashboard automations with HEARTBEAT.md, and cloud sessions that keep running off-terminal. | [src](https://docs.factory.ai/docs/harness/subagents) |
| ide_integration | ✅ yes | VS Code-family extension on the Marketplace shares active file, selection, diagnostics, and native diffs; JetBrains via AI Agents/ACP; Zed extension. /ide manages install/update/disconnect. | [src](https://docs.factory.ai/docs/ide-integrations) |
| model_agnostic | ✅ yes | Hosted catalog spans Anthropic, OpenAI, Google, xAI, and Factory 'Droid Core' open models with per-model reasoning-effort values and multipliers; custom models support OpenAI-compatible and other providers with ${ENV} key references. Per-subagent and per-mission worker/validator model overrides. | [src](https://docs.factory.ai/docs/model-independence/byok) |
| plugins | ✅ yes | droid plugin marketplace add/install/update at user or project scope, plugin IDs pluginName@marketplaceName, source pinning via git refs/SHAs and scoped npm packages; enterprises can run internal plugin marketplaces for approved catalogs. | [src](https://docs.factory.ai/docs/harness/plugins) |
| session_resume | ✅ yes | --fork resumes into a new copy; droid exec -s continues a session headlessly; droid search finds messages/documents/tool results across local sessions; Oct 3, 2026 release adds running a message on resume; sessions can be mirrored to the web app via cloud sync. | [src](https://docs.factory.ai/docs/droid-cli/cli-reference) |
| cost_controls | ✅ yes | Also /cost and /stats [period] usage statistics in the CLI, plus app-side Usage Limits settings, credit balances, bucket views, and credit-countdown in the changelog; per-model multipliers documented on the models page. | [src](https://docs.factory.ai/docs/droid-cli/cli-reference) |

## Architecture

Closed-source agent runtime delivered as a terminal UI (curl|sh installer or npm -g droid), desktop app, and web surface that share "the same Factory runtime" (https://docs.factory.ai/docs/droid-cli/overview). It runs interactively or headless via droid exec, which supports stream-jsonrpc for custom multi-turn flows (https://docs.factory.ai/docs/droid-exec/overview). Shell and MCP tool calls carry low/medium/high risk labels governed by permission rules and Autonomy Levels; shell commands execute in a separate OS-sandboxed process (Seatbelt on macOS, bubblewrap+seccomp on Linux/WSL2, egress through a filtering proxy) (https://docs.factory.ai/docs/autonomy-and-safety/sandbox). Hooks fire shell commands at lifecycle events; subagents execute through the Task tool in fresh context windows; Missions add an orchestrator plus model-configurable worker and validation subagents.

## Context management

Subagents run in fresh context windows for isolation — "the parent session stays focused and lean" (https://docs.factory.ai/docs/harness/subagents). Compaction exists as a lifecycle event (PreCompact hook), and the Oct 3, 2026 release notes state Droid "now shrinks an oversized request before sending it and stops retries that cannot shrink" (https://docs.factory.ai/docs/changelog/release-notes). Long sessions resume with full history and droid search queries messages, documents, and tool results across local sessions (https://docs.factory.ai/docs/droid-cli/cli-reference). Durable context comes from AGENTS.md, loaded before code is written, plus AutoWiki repository docs and automation memory folders that carry state between runs (https://docs.factory.ai/docs/harness/agents-md, https://docs.factory.ai/cli/features/wiki/overview).

## Ecosystem

Plugins bundle skills, commands, droids, output styles, hooks, and MCP servers, installed from marketplaces via droid plugin marketplace add <source> and droid plugin install <plugin@marketplace> at user or project scope, with version pins through git refs/SHAs and scoped npm packages (https://docs.factory.ai/docs/harness/plugins). Enterprises can run internal plugin marketplaces for org-approved catalogs (https://docs.factory.ai/docs/enterprise/internal-plugin-marketplaces). Factory's public GitHub org ships TypeScript and Python SDKs, the droid-action GitHub Action for automated PR review/security scans, and VS Code/Zed extensions, mostly MIT/Apache-2.0 (https://github.com/factory-ai). Skills and subagents also distribute as plain .factory/ directories committed to repos, so capabilities travel with the codebase even without the plugin system.

## Governance

Factory Droid is closed source: there is no public repository or license for the CLI runtime, so the vendor documentation is the authoritative spec for capabilities. Its GitHub home, github.com/factory-ai/factory, is a README-and-docs repository with no license file, while SDKs, the droid-action, and editor extensions are published under MIT/Apache-2.0 in the same org (https://github.com/factory-ai). Owner is Factory AI (San Francisco; factory.com). Cadence is fast and documented: the changelog header reads "234 releases · latest CLI v0.233.0 · Desktop v0.190.0 · October 3, 2026", with RSS/JSON feeds, and a defined maturity vocabulary (Private Preview, Deprecated; "Generally available" is the absence of a tag) (https://docs.factory.ai/docs/changelog/release-notes, https://docs.factory.ai/docs/changelog/feature-maturity).

## Limitations

Documented gates: subagents run non-interactively — AskUser is disabled and "a subagent cannot spawn its own subagents," so delegation is one level deep and wide fan-out requires Factory Missions (https://docs.factory.ai/docs/harness/subagents). Missions are heuristically scoped to "about 1–500 features"; larger efforts must be split (https://docs.factory.ai/docs/missions/overview). In Spec Mode Droid "should not edit files, change configuration, make commits, start services, or write to external systems" until the plan is approved (https://docs.factory.ai/docs/autonomy-and-safety/specification-mode). The sandbox "blocks rather than running without isolation" when host kernel primitives are unavailable (https://docs.factory.ai/docs/autonomy-and-safety/sandbox). BYOK custom models don't appear in Factory's hosted web or mobile platforms, sessions APIs are "enabled for selected organizations only," and droid exec stream-json input mode is deprecated.

## In its own words

> All shell commands initiated by Droid run in a separate process that is limited to the filesystem and network boundaries configured by users and enforced at the OS kernel level.  
> — [https://docs.factory.ai/docs/autonomy-and-safety/sandbox](https://docs.factory.ai/docs/autonomy-and-safety/sandbox)

> A custom droid is a reusable subagent defined in Markdown. Each droid carries its own system prompt, model preference, and tool policy, so Droid can hand off a focused task, such as code review, a security sweep, or research, without you re-typing instructions.  
> — [https://docs.factory.ai/docs/harness/subagents](https://docs.factory.ai/docs/harness/subagents)

> Instead of tackling everything in a single session, you collaborate with Droid upfront to build a plan (features, milestones, and the skills needed to accomplish each part), then hand off execution to an orchestration layer that manages the work.  
> — [https://docs.factory.ai/docs/missions/overview](https://docs.factory.ai/docs/missions/overview)

> Hooks are shell commands that run at defined points in a Droid session. Use them for deterministic behavior that should happen every time, such as validating tool calls, formatting changed files, injecting local context, logging activity, or enforcing team policy.  
> — [https://docs.factory.ai/docs/harness/hooks](https://docs.factory.ai/docs/harness/hooks)


## Notable

Despite being closed source, Droid enforces kernel-level sandboxing (Seatbelt / bubblewrap+seccomp with a domain-allowlisted network proxy) and refuses to run shell commands without it when host primitives are unavailable — yet delegation is hard-capped at one level, with wide fan-out reserved for the separate Missions orchestrator.

## Sources fetched

- https://docs.factory.ai/
- https://docs.factory.ai/docs/harness/subagents
- https://docs.factory.ai/docs/harness/hooks
- https://docs.factory.ai/docs/harness/skills
- https://docs.factory.ai/docs/harness/mcp
- https://docs.factory.ai/docs/harness/plugins
- https://docs.factory.ai/docs/harness/agents-md
- https://docs.factory.ai/docs/missions/overview
- https://docs.factory.ai/docs/missions/reference
- https://docs.factory.ai/docs/autonomy-and-safety/sandbox
- https://docs.factory.ai/docs/autonomy-and-safety/specification-mode
- https://docs.factory.ai/docs/autonomy-and-safety/auto-run
- https://docs.factory.ai/docs/autonomy-and-safety/permission-rules
- https://docs.factory.ai/docs/ide-integrations
- https://docs.factory.ai/docs/model-independence/byok
- https://docs.factory.ai/docs/models
- https://docs.factory.ai/docs/droid-cli/cli-reference
- https://docs.factory.ai/docs/droid-cli/overview
- https://docs.factory.ai/docs/droid-exec/overview
- https://docs.factory.ai/docs/software-factory/automations
- https://docs.factory.com/web/automations
- https://docs.factory.ai/docs/software-factory/droid-control
- https://docs.factory.ai/docs/changelog/release-notes
- https://docs.factory.ai/docs/changelog/feature-maturity
- https://docs.factory.ai/docs/api-reference/sessions
- https://docs.factory.ai/cli/features/wiki/overview
- https://github.com/factory-ai
- https://github.com/factory-ai/factory
- https://factory.com
- https://factory.ai/product/missions

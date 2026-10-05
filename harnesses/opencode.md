# OpenCode

- **repo:** anomalyco/opencode (formerly sst/opencode; default branch dev)
- **version pin:** `v1.18.34` — gh api repos/anomalyco/opencode/releases/latest → https://github.com/anomalyco/opencode/releases/tag/v1.18.34 (published 2026-09-30); cross-checked npm opencode-ai@1.18.34 via registry.npmjs.org
- **docs home:** https://opencode.ai/docs

## What it promises

An open source AI coding agent ("The open source AI coding agent") available as a terminal TUI, desktop app, or IDE extension, usable with any of 75+ LLM providers including local models. It promises a plan-first workflow (read-only Plan agent) with full-access Build agent, undo/redo, shareable sessions, and Claude Code-compatible AGENTS.md/CLAUDE.md conventions.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | Built-in General/Explore/Scout subagents; custom via JSON or markdown; @ mention or Task tool; task permission gates which subagents each agent may invoke. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/agents.mdx) |
| workflow_orchestration | ◐ partial | No DAG/team/swarm framework in docs; orchestration is fan-out via the task tool plus programmatic control through the SDK/server (sdk.mdx: control opencode programmatically) and a GitHub Actions bot. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/agents.mdx) |
| mcp | ✅ yes | MCP client only (local + remote, headers, OAuth/DCR, per-agent enable/disable); no MCP server mode documented. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/mcp-servers.mdx) |
| hooks_lifecycle | ✅ yes | Via plugin API: tool.execute.before/after, session.created/idle/deleted/error, file.edited, permission.asked, experimental.session.compacting; no hooks declared in plain config. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/plugins.mdx) |
| skills | ✅ yes | SKILL.md folders in .opencode/skills, ~/.config/opencode/skills, and Claude-compatible .claude/skills and .agents/skills; loaded on demand via native skill tool with per-pattern permissions. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/skills.mdx) |
| memory_persistence | ✅ yes | File-based memory: AGENTS.md (project + global) and CLAUDE.md fallback, plus extra instruction files/URLs; sessions persist and resume. No automatic memory extraction/retrieval system. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/rules.mdx) |
| sandboxing | ✅ yes | Permission modes allow/ask/deny global and per-tool with glob rules (e.g. bash command patterns), external_directory guard, doom_loop guard, and --auto mode. No OS-level filesystem/process sandbox found in docs. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/permissions.mdx) |
| plan_mode | ✅ yes | Built-in Plan primary agent, Tab to switch; edits and bash default to ask; README also documents build/plan agent cycle. | [src](https://opencode.ai/docs/) |
| background_tasks | ◐ partial | Behind OPENCODE_EXPERIMENTAL_BACKGROUND_SUBAGENTS flag; server also exposes POST /session/:id/prompt_async ('Send a message asynchronously (no wait)'). Not a general background-job system. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/cli.mdx) |
| ide_integration | ✅ yes | Auto-installing VS Code/Cursor/Windsurf/VSCodium extension with keybinds; JetBrains, Zed and Neovim via ACP (opencode acp) per acp.mdx. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/ide.mdx) |
| model_agnostic | ✅ yes | Any provider via /connect or config; custom baseURL for proxies; optional OpenCode Zen curated gateway; per-agent model overrides. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/providers.mdx) |
| plugins | ✅ yes | TS/JS plugin modules loaded from .opencode/plugins, ~/.config/opencode/plugins, or npm packages listed in config; can add custom tools; community ecosystem page. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/plugins.mdx) |
| session_resume | ✅ yes | --continue/-c resumes last session, --session/-s a specific ID, --fork branches while continuing; TUI session list; sessions deletable/exportable. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/cli.mdx) |
| cost_controls | ✅ yes | opencode stats with --days/--models breakdown; --verbose shows cost metadata; per-agent 'steps' cap limits agentic iterations to control cost; Zen pay-as-you-go pricing. | [src](https://raw.githubusercontent.com/anomalyco/opencode/dev/packages/web/src/content/docs/cli.mdx) |

## Notable

Deep Claude Code compatibility is a first-class fallback path (reads CLAUDE.md and .claude/skills unless disabled), plus a /oc GitHub bot that runs entire tasks inside your repo's GitHub Actions runners.

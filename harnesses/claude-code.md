# Claude Code

- **repo:** anthropics/claude-code
- **version pin:** `v2.1.289` — gh api repos/anthropics/claude-code/releases/latest (published 2026-10-03) → https://github.com/anthropics/claude-code/releases/tag/v2.1.289
- **docs home:** https://code.claude.com/docs/en/overview

## What it promises

An agentic coding tool that lives in your terminal, understands your codebase, and helps you code faster by executing routine tasks, explaining complex code, and handling git workflows — all through natural language commands. It reads your codebase, edits files, runs commands, and integrates with your development tools across terminal, IDE, desktop app, and browser. (README + docs overview.)

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | Claude delegates matching tasks to a subagent that works independently in its own context and returns results; supports foreground/background runs and persistent memory. | [src](https://code.claude.com/docs/en/sub-agents) |
| workflow_orchestration | ✅ yes | JS scripts run in background; agent teams exist too but are experimental and disabled by default (CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1). | [src](https://code.claude.com/docs/en/workflows) |
| mcp | ✅ yes | Client for MCP servers; also acts as an MCP server for other apps via `claude mcp serve`. | [src](https://code.claude.com/docs/en/mcp) |
| hooks_lifecycle | ✅ yes | Lifecycle events include SessionStart/SessionEnd, UserPromptSubmit, PreToolUse/PostToolUse, Stop/StopFailure. | [src](https://code.claude.com/docs/en/hooks) |
| skills | ✅ yes | Follows the Agent Skills open standard; Claude invokes automatically when relevant or directly via /skill-name. | [src](https://code.claude.com/docs/en/skills) |
| memory_persistence | ✅ yes | Two mechanisms: user-written CLAUDE.md/AGENTS.md files plus self-written auto memory, both loaded at session start. | [src](https://code.claude.com/docs/en/memory) |
| sandboxing | ✅ yes | Off by default (`/sandbox`); macOS/Linux/WSL2 only (native Windows unsandboxed); permission modes (default/acceptEdits/plan/auto/bypassPermissions) add approval control. | [src](https://code.claude.com/docs/en/sandboxing) |
| plan_mode | ✅ yes | Edits stay blocked until the user approves the plan; `claude --permission-mode plan` or Shift+Tab cycle. | [src](https://code.claude.com/docs/en/permission-modes) |
| background_tasks | ✅ yes | Ctrl+B backgrounds bash/agents; /tasks shows running shells and subagents; workflows also execute in background. | [src](https://code.claude.com/docs/en/interactive-mode) |
| ide_integration | ✅ yes | VS Code extension too (inline diffs, @-mentions, plan review, resume past conversations), per docs index and vs-code page. | [src](https://code.claude.com/docs/en/jetbrains.md) |
| model_agnostic | ◐ partial | Multiple cloud providers and LLM gateways supported, but all serve Anthropic's Claude models only — no non-Anthropic LLMs (no GPT/Gemini). | [src](https://code.claude.com/docs/en/third-party-integrations.md) |
| plugins | ✅ yes | Distributed via marketplaces; install with /plugin (Discover tab); users can also build and publish their own. | [src](https://code.claude.com/docs/en/plugins/overview) |
| session_resume | ✅ yes | `claude --continue`, `claude --resume` (picker or named), `/resume`, `--from-pr`; transcripts stored locally as .jsonl. | [src](https://code.claude.com/docs/en/sessions) |
| cost_controls | ✅ yes | /usage command, team spend limits, org-wide usage monitoring (monitoring-usage page), model selection and context management to reduce cost. | [src](https://code.claude.com/docs/en/costs) |

## Architecture

Claude Code is terminal-first: one process per session, shipping as a native binary — the npm package needs Node.js 22+, but "downloads a native binary that doesn't use your Node.js at runtime" (setup). The Agent SDK "spawns and supervises a claude CLI subprocess that owns a shell, a working directory, and session files on disk" (agent-sdk/hosting). The CLI renders via a classic TUI or an alternate-screen "fullscreen" mode, a research preview (fullscreen). Tools execute inside the loop: Claude emits tool calls, the harness runs them, results feed back; PreToolUse hooks can block a call (agent-sdk/agent-loop). `claude remote-control` adds a server mode bridging claude.ai/code or mobile clients while "code execution and filesystem access stay on your machine" (remote-control).

## Context management

Each request re-sends the full context — system prompt, project context, prior messages, tool results — with automatic prompt caching keeping the unchanged prefix cheap (prompt-caching). Startup loads CLAUDE.md, auto memory, MCP tool names, and skill descriptions (context-window). Near the limit, auto-compaction "replaces the conversation with a structured summary"; most startup content re-injects afterward, except the auto-memory listing, and invoked-skill bodies re-inject capped at 5,000 tokens each. Manual controls: `/compact` with focus instructions, `/rewind` → Summarize from here, `/autocompact <tokens>`, and a "Compact Instructions" CLAUDE.md section; a thrashing guard stops refill loops (troubleshooting). Persistent memory layers CLAUDE.md/AGENTS.md with auto memory loading "first 200 lines or 25KB" per session (memory).

## Ecosystem

Plugins are directories of skills, agents, hooks, and MCP servers installed as one unit via a `.claude-plugin/plugin.json` manifest; marketplaces are catalogs defined by `.claude-plugin/marketplace.json` (plugins/overview). Anthropic publishes three general-purpose marketplaces — official (`claude-plugins-official`), community, and demo — plus topic-specific ones like `anthropics/skills` (anthropic-marketplaces). Distribution routes: share a folder or zip, publish your own marketplace repository, or submit to Anthropic's directory for account-synced installs (plugins/publish). Installing works from the `/plugin` Discover tab across terminal, desktop, IDE, and cloud sessions (plugins/install). No docs page states a plugin count; the web catalog shows install counts and "Anthropic verified" marks.

## Governance

Anthropic PBC owns Claude Code; its LICENSE.md on github.com/anthropics/claude-code reads: "© Anthropic PBC. All rights reserved. Use is subject to Anthropic's Commercial Terms of Service." The legal page routes Team/Enterprise/API users to Commercial Terms and Free/Pro/Max to Consumer Terms, forbids modifying the binary or restricting its authentication, and bars reselling or intermediating usage (legal-and-compliance). Feedback flows through `/bug` or GitHub issues per the repo README; no external contribution process is documented. Release cadence is fast and versioned: a weekly "What's new" digest (Week 37 covered v2.1.263–v2.1.269, September 2026) plus a changelog generated from GitHub's CHANGELOG.md, latest 2.1.289 on October 3, 2026.

## Limitations

Computer use is a macOS-only research preview for Pro/Max, unavailable on Team/Enterprise and in `-p` non-interactive mode (computer-use). Fullscreen rendering is a research preview (fullscreen), agent teams are "experimental and disabled by default" (glossary), and Desktop on Linux is beta, officially limited to Ubuntu 22.04+/Debian 12+ (desktop-linux). Sandboxed Bash is unsupported on native Windows and WSL 1 (setup); sandboxing "is not a complete isolation boundary" — no TLS inspection by default, domain-fronting exfiltration risk, Unix-socket escalation (sandboxing). Remote Control is unavailable with API keys, Bedrock, Google's Agent Platform, Foundry, or any non-api.anthropic.com base URL (remote-control). Troubleshooting documents an auto-compaction "thrashing" error with staged recovery steps.

## In its own words

> Claude Code is an agentic coding tool that reads your codebase, edits files, runs commands, and integrates with your development tools. Available in your terminal, IDE, desktop app, and browser.  
> — [https://code.claude.com/docs/en/overview](https://code.claude.com/docs/en/overview)

> A turn is one round trip inside the loop: Claude produces output that includes tool calls, the SDK executes those tools, and the results feed back to Claude automatically.  
> — [https://code.claude.com/docs/en/agent-sdk/agent-loop](https://code.claude.com/docs/en/agent-sdk/agent-loop)

> Each time you send a message in Claude Code, it makes a new API request. The model doesn't remember anything between requests, so Claude Code re-sends the full context: the system prompt, your project context, every prior message and tool result, and your new message.  
> — [https://code.claude.com/docs/en/prompt-caching](https://code.claude.com/docs/en/prompt-caching)

> When a long session compacts, Claude Code summarizes the conversation history to fit the context window.  
> — [https://code.claude.com/docs/en/context-window](https://code.claude.com/docs/en/context-window)


## Notable

Despite the multi-agent story, agent teams are experimental and off by default (CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1), and since v2.1.283 the default interactive permission mode is "auto", where a second classifier model — not the user — reviews actions.

## Sources fetched

- https://code.claude.com/docs/en/overview
- https://code.claude.com/docs/llms.txt
- https://code.claude.com/docs/en/how-claude-code-works
- https://code.claude.com/docs/en/context-window
- https://code.claude.com/docs/en/memory
- https://code.claude.com/docs/en/prompt-caching
- https://code.claude.com/docs/en/sessions
- https://code.claude.com/docs/en/checkpointing
- https://code.claude.com/docs/en/tools-reference
- https://code.claude.com/docs/en/remote-control
- https://code.claude.com/docs/en/sandboxing
- https://code.claude.com/docs/en/fullscreen
- https://code.claude.com/docs/en/glossary
- https://code.claude.com/docs/en/setup
- https://code.claude.com/docs/en/troubleshooting
- https://code.claude.com/docs/en/platforms
- https://code.claude.com/docs/en/computer-use
- https://code.claude.com/docs/en/desktop-linux
- https://code.claude.com/docs/en/feature-availability
- https://code.claude.com/docs/en/changelog
- https://code.claude.com/docs/en/data-usage
- https://code.claude.com/docs/en/security
- https://code.claude.com/docs/en/features-overview
- https://code.claude.com/docs/en/legal-and-compliance
- https://code.claude.com/docs/en/whats-new/index
- https://code.claude.com/docs/en/vs-code
- https://code.claude.com/docs/en/jetbrains
- https://code.claude.com/docs/en/corporate-launcher
- https://code.claude.com/docs/en/agent-sdk/hosting
- https://code.claude.com/docs/en/agent-sdk/overview
- https://code.claude.com/docs/en/agent-sdk/agent-loop
- https://code.claude.com/docs/en/plugins/overview
- https://code.claude.com/docs/en/plugins/anthropic-marketplaces
- https://code.claude.com/docs/en/plugins/install
- https://code.claude.com/docs/en/plugins/publish
- https://code.claude.com/docs/en/plugins/create
- https://raw.githubusercontent.com/anthropics/claude-code/main/LICENSE.md
- https://raw.githubusercontent.com/anthropics/claude-code/main/README.md

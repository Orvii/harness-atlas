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

## Notable

Despite the multi-agent story, agent teams are experimental and off by default (CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1), and since v2.1.283 the default interactive permission mode is "auto", where a second classifier model — not the user — reviews actions.

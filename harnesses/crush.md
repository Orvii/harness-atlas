# Crush

- **repo:** charmbracelet/crush
- **version pin:** `v0.97.1` — GitHub releases API, repos/charmbracelet/crush/releases/latest: tag v0.97.1, published 2026-09-29 (https://github.com/charmbracelet/crush/releases/tag/v0.97.1)
- **docs home:** No standalone docs site; documentation lives in the repository itself — README.md plus docs/config/ and docs/hooks/ directories (fetched as raw GitHub URLs). Repo: https://github.com/charmbracelet/crush

## What it promises

In its own framing, Crush is "Your new coding bestie, now available in your favourite terminal. Your tools, your code, and your workflows, wired into your LLM of choice." It promises a multi-model, session-based agent that runs great with no configuration — "switch LLMs mid-session while preserving context" — enhanced by LSPs and extensible through MCP servers and Agent Skills, working in every terminal on macOS, Linux, Windows, Android, and BSD.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | The agent tool spawns read-only explorer sub-agents; agentic_fetch is a second delegated tool. Hooks doc confirms: "Sub-agents (the `agent` task tool, `agentic_fetch`, etc.) run without hook interception." Coordinator manages named agents ("coder", "task"); plan mode may delegate exploration to sub-agents. | [src](https://raw.githubusercontent.com/charmbracelet/crush/main/internal/agent/templates/agent_tool.md) |
| workflow_orchestration | ✗ no | Only delegation primitive is one-off sub-agent launches for search/exploration. No DAGs, teams, swarms, or scripted multi-agent pipelines; multi-client workspaces (crush serve) share state but are not orchestration. | [src](https://raw.githubusercontent.com/charmbracelet/crush/main/internal/agent/templates/agent_tool.md) |
| mcp | ✅ yes | Built-in OAuth 2.1 flow (dynamic and pre-registered clients), per-server tool allow/deny (--enabled-tools/--disabled-tools), timeouts, sessionless-server auto-detection, header/env expansion. | [src](https://raw.githubusercontent.com/charmbracelet/crush/main/README.md) |
| hooks_lifecycle | ◐ partial | Only PreToolUse today (session start/stop, post-tool etc. planned in docs/hooks/FUTURE.md). Shell-command hooks can block (exit 2), halt the turn (exit 49), rewrite tool input, inject context, and auto-approve; explicitly Claude Code-compatible; run in parallel, compose in config order, before permission checks. | [src](https://raw.githubusercontent.com/charmbracelet/crush/main/docs/hooks/README.md) |
| skills | ✅ yes | SKILL.md folders discovered from ~/.config/crush/skills, ~/.agents/skills, ~/.claude/skills, .crush/skills, .claude/skills, .cursor/skills and skills_paths; builtin skills (e.g. crush-config, crush-hook); user-invocable frontmatter flags (user-invocable, disable-model-invocation); skills can be disabled. | [src](https://raw.githubusercontent.com/charmbracelet/crush/main/README.md) |
| memory_persistence | ◐ partial | Persistent instruction files (global ~/.config/crush/CRUSH.md and ~/.config/AGENTS.md, project AGENTS.md/CRUSH.md/CLAUDE.md/GEMINI.md, crush init creates AGENTS.md) plus SQLite-backed session history and resume; no automatic learned-memory store across sessions. | [src](https://raw.githubusercontent.com/charmbracelet/crush/main/README.md) |
| sandboxing | ◐ partial | Permission prompts gate every tool call; permissions allow/deny lists, PreToolUse hooks can pre-approve, and the dangerous --yolo flag skips all prompts. No OS-level isolation/container sandbox — bash runs through an embedded in-process POSIX shell, and crushrc/JSON configs are executed as trusted code. | [src](https://raw.githubusercontent.com/charmbracelet/crush/main/README.md) |
| plan_mode | ✅ yes | Plan agent has edit/write/bash tools physically absent; produces a plan bracketed by CRUSH_PLAN_START / CRUSH_PLAN_READY markers and "the UI will prompt the user to confirm" before implementation; delegation to sub-agents allowed for exploration only. | [src](https://raw.githubusercontent.com/charmbracelet/crush/main/internal/agent/templates/plan.md.tpl) |
| background_tasks | ✅ yes | run_in_background parameter, auto-background after 1 minute (configurable via auto_background_after); job_output tool reads/waits on a shell's stdout/stderr, job_kill terminates it. | [src](https://raw.githubusercontent.com/charmbracelet/crush/main/internal/agent/tools/bash.md.tpl) |
| ide_integration | ✗ no | No first-party VS Code or JetBrains extension in the repo or the charmbracelet org (org search for crush returns only the CLI repo). Terminal-first by design; integration with the herdr terminal multiplexer reports agent state over a Unix socket, not an IDE. | [src](https://raw.githubusercontent.com/charmbracelet/crush/main/README.md) |
| model_agnostic | ✅ yes | ~25+ built-in providers (Anthropic, OpenAI, Gemini, Groq, OpenRouter, Bedrock, Vertex, Azure, Hyper, Z.ai, MiniMax, Cerebras, Vercel...), custom OpenAI-/Anthropic-compatible endpoints, and auto-discovered local models (ollama, llamacpp, lmstudio, litellm); switch model slots mid-session ('switch LLMs mid-session while preserving context'). | [src](https://raw.githubusercontent.com/charmbracelet/crush/main/README.md) |
| plugins | ◐ partial | No plugin registry or plugin API; third-party extension surfaces are MCP servers, Agent Skills packages (distributed as folders, e.g. clone anthropics/skills), shell hooks, custom providers/models, and LSP servers. | [src](https://raw.githubusercontent.com/charmbracelet/crush/main/AGENTS.md) |
| session_resume | ✅ yes | crush -s <id> resumes a specific session, -C continues the most recent; sessions persist in SQLite and are listed in a session manager; shared workspaces let a second client attach to an in-progress session (IsBusy/AttachedClients signals). | [src](https://raw.githubusercontent.com/charmbracelet/crush/main/internal/cmd/root.go) |
| cost_controls | ✅ yes | "crush stats" renders an HTML usage dashboard (token usage, cost, activity, --all/--crawl-dir aggregation); per-model price flags (--price-input/output/cache-create/cache-hit), flat-rate billing provider option, per-model --default-max-tokens and context-window caps. | [src](https://raw.githubusercontent.com/charmbracelet/crush/main/internal/cmd/stats.go) |

## Architecture

Crush is a single Go binary (CGO disabled) with a Bubble Tea v2 TUI and an optional client/server split: `crush serve` runs a backend, and clients sharing a `--cwd` join one workspace over SSE, sharing sessions, permission queue, LSP, and MCP state. LLMs sit behind Charm's `fantasy` abstraction; sessions and messages persist in SQLite via sqlc. Tools are self-documenting Go files paired with Markdown descriptions; the bash tool runs an embedded mvdan.cc/sh POSIX interpreter in-process, dispatching shebang scripts via os/exec, with background job management. A coordinator manages named agents ("coder", "task") and a hooks engine executes PreToolUse shell commands before permission checks.

## Context management

Context windows are declared per model (`--context-window`). Crush auto-summarizes long conversations by default (`option auto-summarize`; `disable_auto_summarize` exists in the schema), compressing history through a summary template. Project instructions load from context files — AGENTS.md, CRUSH.md, CLAUDE.md, GEMINI.md and `.local` variants — plus global `~/.config/crush/CRUSH.md` and `~/.config/AGENTS.md`, extensible via `context-path` and excludable via `.crushignore`. Bash output over a size limit is truncated with a marker naming a file holding the complete output; LSPs contribute code intelligence; commands exceeding one minute auto-move to background shells.

## Ecosystem

Distribution spans Homebrew, npm (`@charmland/crush`), Arch AUR, Nix/NUR including NixOS and Home Manager modules, winget, Scoop, Charm's apt/yum repositories, and `go install`; binaries ship for Linux, macOS, Windows, FreeBSD, OpenBSD and NetBSD. Provider and model metadata come from Catwalk, a community-editable open source catalog Crush auto-updates (overridable via CATWALK_URL). Skills follow the agentskills.io open standard with example packs from anthropics/skills, discovered from .claude/skills, .cursor/skills and related directories. MCP servers (stdio/http/sse, OAuth) and shell hooks provide further extension points; community lives on Charm's Discord and Slack. The repo has roughly 28.5k stars.

## Governance

Owned and maintained by Charmbracelet, Inc. (Charm), licensed FSL-1.1-MIT — Functional Source License with an MIT future license, so each release converts to MIT after two years but restricts competing commercial use in the interim; it is not OSI-approved during that window. Contributions require the repo's CLA.md. The project is active, not archived: latest release v0.97.1 (2026-09-29) with pushes through 2026-10-04 on a fast 0.x cadence. Telemetry is pseudonymous PostHog usage metadata with opt-out via CRUSH_DISABLE_METRICS or DO_NOT_TRACK, and prompts and responses are never collected.

## Limitations

Documented gaps: hooks support only PreToolUse today, with the rest planned in docs/hooks/FUTURE.md; there is no OS-level sandbox — safety rests on permission prompts, allow/deny lists and the dangerous `--yolo` flag, and config files (crushrc, JSON expansions) are explicitly "trusted code" executed with shell privileges. Sub-agents are read-only (glob, grep, ls, view) search helpers rather than parallel coding agents, and the agent tool is the only delegation primitive. No first-party VS Code or JetBrains extension exists; the interface is terminal-only. JSON config is deprecated in favor of the Bash crushrc format, which may be removed in a future release.

## In its own words

> Your new coding bestie, now available in your favourite terminal. Your tools, your code, and your workflows, wired into your LLM of choice.  
> — [https://raw.githubusercontent.com/charmbracelet/crush/main/README.md](https://raw.githubusercontent.com/charmbracelet/crush/main/README.md)

> Hooks are user-defined shell scripts that run when various events happen during the agent lifecycle, allowing you to both build on top of Crush, customize its behavior, and exert deterministic control over an agent's wily behavior.  
> — [https://raw.githubusercontent.com/charmbracelet/crush/main/docs/hooks/README.md](https://raw.githubusercontent.com/charmbracelet/crush/main/docs/hooks/README.md)

> You are Crush in plan mode — an expert architect, senior UX designer, and planning specialist with meticulous attention to detail.  
> — [https://raw.githubusercontent.com/charmbracelet/crush/main/internal/agent/templates/plan.md.tpl](https://raw.githubusercontent.com/charmbracelet/crush/main/internal/agent/templates/plan.md.tpl)

> Execute shell commands; long-running commands automatically move to background and return a shell ID.  
> — [https://raw.githubusercontent.com/charmbracelet/crush/main/internal/agent/tools/bash.md.tpl](https://raw.githubusercontent.com/charmbracelet/crush/main/internal/agent/tools/bash.md.tpl)


## Notable

Its config format is a Bash script (`crushrc`) executed by an embedded POSIX shell interpreter with Crush-specific builtins like `provider add` and `permissions allow`, replacing Crush's own now-deprecated JSON config — and its hook system is deliberately Claude Code-compatible.

## Sources fetched

- https://github.com/charmbracelet/crush
- https://github.com/charmbracelet/crush/releases/tag/v0.97.1
- https://raw.githubusercontent.com/charmbracelet/crush/main/README.md
- https://raw.githubusercontent.com/charmbracelet/crush/main/AGENTS.md
- https://raw.githubusercontent.com/charmbracelet/crush/main/LICENSE.md
- https://raw.githubusercontent.com/charmbracelet/crush/main/docs/config/README.md
- https://raw.githubusercontent.com/charmbracelet/crush/main/docs/hooks/README.md
- https://raw.githubusercontent.com/charmbracelet/crush/main/docs/hooks/FUTURE.md
- https://raw.githubusercontent.com/charmbracelet/crush/main/schema.json
- https://raw.githubusercontent.com/charmbracelet/crush/main/internal/cmd/root.go
- https://raw.githubusercontent.com/charmbracelet/crush/main/internal/cmd/stats.go
- https://raw.githubusercontent.com/charmbracelet/crush/main/internal/agent/tools/bash.md.tpl
- https://raw.githubusercontent.com/charmbracelet/crush/main/internal/agent/tools/job_output.md
- https://raw.githubusercontent.com/charmbracelet/crush/main/internal/agent/tools/job_kill.md
- https://raw.githubusercontent.com/charmbracelet/crush/main/internal/agent/templates/plan.md.tpl
- https://raw.githubusercontent.com/charmbracelet/crush/main/internal/agent/templates/agent_tool.md
- https://raw.githubusercontent.com/charmbracelet/crush/main/internal/agent/templates/task.md.tpl

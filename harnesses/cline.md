# Cline

- **repo:** cline/cline
- **version pin:** `desktop-v0.0.43` — gh api repos/cline/cline/releases/latest (https://api.github.com/repos/cline/cline/releases/latest) -> tag desktop-v0.0.43, published 2026-10-02, https://github.com/cline/cline/releases/tag/desktop-v0.0.43. Concurrent trains in same repo: VS Code/JetBrains extension v4.1.22, CLI cli-v3.0.68 (npm cline@3.0.68), SDK sdk/sdk/v0.0.90.
- **docs home:** https://docs.cline.bot/

## What it promises

Open source coding agent that lives in your IDE, terminal, and desktop: it reads files, writes code, and runs commands. Its pitch stresses control — every action requires your explicit approval, so you stay in charge.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | Experimental; read-only (cannot edit, use MCP, or nest), own context/token budget; enabled by default across VS Code, JetBrains, CLI; per-subagent cost tracked. | [src](https://docs.cline.bot/features/subagents.md) |
| workflow_orchestration | ✅ yes | Coordinator/teammate tools (spawn, delegate, status, result) via SDK team_spawn_teammate; persistent team state; Kanban worktrees + dependency chains. Warning on page: not applicable to VS Code/JetBrains extension for now. | [src](https://docs.cline.bot/cli/agent-teams.md) |
| mcp | ✅ yes | Client-side: local STDIO + remote Streamable HTTP/SSE, .cline/mcp.json, CLI wizard (`cline mcp`), autoApprove allowlists, enterprise allowlisting. No Cline-as-MCP-server mode documented. | [src](https://docs.cline.bot/mcp/mcp-overview.md) |
| hooks_lifecycle | ◐ partial | Stages include session_start, tool_call_before/after, run_end, session_shutdown; CLI flags --hooks-dir and `cline hook`. Scoped to SDK/CLI/Kanban; extension hooks doc is a stub pointing at SDK plugins. | [src](https://docs.cline.bot/sdk/plugins.md) |
| skills | ✅ yes | SKILL.md + YAML frontmatter with progressive loading (metadata ~100 tokens); activated by description match via use_skill tool or explicit slash command; subagents can load skills. | [src](https://docs.cline.bot/customization/skills.md) |
| memory_persistence | ✅ yes | Official Memory Bank methodology: markdown files in-repo wired via .clinerules custom instructions; document-driven rather than automatic. Session/task history and checkpoints also persist. | [src](https://docs.cline.bot/best-practices/memory-bank.md) |
| sandboxing | ✅ yes | Per-tool-category permission modes (read/edit/commands/browser/MCP) plus YOLO mode; CLI adds CLINE_SANDBOX env and CLINE_COMMAND_PERMISSIONS allow/deny glob policy. OS-level sandbox details not documented. | [src](https://docs.cline.bot/features/auto-approve.md) |
| plan_mode | ✅ yes | Plan mode read-only, Act executes; conversation carries over on switch; CLI -p/--plan flag; ACP clients get mode selector. | [src](https://docs.cline.bot/core-workflows/plan-and-act.md) |
| background_tasks | ✅ yes | Background terminal output monitoring; CLI -z/--zen starts session in background hub daemon; cron-scheduled agents persist across restarts (schedule docs scoped to SDK/CLI/Kanban). | [src](https://raw.githubusercontent.com/cline/cline/main/README.md) |
| ide_integration | ✅ yes | VS Code/Cursor/Windsurf extension, JetBrains plugin, ACP mode for Zed/Neovim/Emacs, plus CLI/TUI and Desktop app surfaces. | [src](https://docs.cline.bot/cline-overview.md) |
| model_agnostic | ✅ yes | BYOK cloud and local (Ollama/LM Studio); docs list 40+ providers: Anthropic, OpenAI/Codex, Gemini, OpenRouter (200+ models), Bedrock, Vertex, Cerebras, Groq, Qwen, DeepSeek, Z AI and an 'Other 30+ Providers' page. | [src](https://raw.githubusercontent.com/cline/cline/main/README.md) |
| plugins | ◐ partial | AgentPlugin API; `cline plugin install` from npm, git, file URL, or local path; global (~/.cline/plugins) or project scope; reference typescript-lsp-plugin. Warning on page: applies to SDK/CLI/Kanban only, not VS Code/JetBrains extension for now. | [src](https://docs.cline.bot/customization/plugins.md) |
| session_resume | ✅ yes | CLI --id resumes a session; `cline history` lists/manages saved sessions; ACP persists conversations so clients restore threads after restart; team state persists across sessions. | [src](https://docs.cline.bot/cli/cli-reference.md) |
| cost_controls | ✅ yes | UI shows per-subagent and task token/cost; token usage visible in task header; SDK getAccumulatedUsage(sessionId); production guide shows abort-on-cost-limit pattern; schedule history and enterprise show tokens/cost. | [src](https://docs.cline.bot/features/subagents.md) |

## Architecture

Cline runs one shared agent core across surfaces: IDE extensions (VS Code, Cursor, Windsurf, VSCodium, Antigravity; the JetBrains plugin is a closed-source client), CLI/TUI, Kanban web board, Desktop app, and the SDK — TypeScript packages @cline/core, @cline/agents, @cline/llms, @cline/shared, requiring Node.js 22+ (docs.cline.bot/sdk/overview.md). Production SDK deployments use hub-spoke: a singleton local daemon on 127.0.0.1:25463 coordinates sessions over WebSocket, spoke workers run the agent loop and call tools, clients attach as peers (docs.cline.bot/sdk/architecture/hub-spoke.md). Tools are functions the model calls; Cline executes and returns results — built-ins bash, editor, read_files, apply_patch, ripgrep search, fetch_web, ask_question, with per-tool approval or auto-approval (docs.cline.bot/tools-reference/all-cline-tools.md). Kanban binds 127.0.0.1:3484 (docs.cline.bot/kanban/remote-access.md); README: Desktop app is a Tauri shell, Bun sidecar, and Next.js UI (raw.githubusercontent.com/cline/cline/main/README.md).

## Context management

Cline auto-compacts: it monitors token usage, summarizes the conversation — preserving technical details, code changes, and decisions — replaces history, and continues; summarization reuses the prompt cache, and "with other models" it falls back to rule-based truncation (docs.cline.bot/features/auto-compact.md). Checkpoints (shadow Git repo) and message editing restore state from before a summarization. Memory Bank adds structured markdown files — projectbrief.md, activeContext.md, progress.md — read at task start, with "update memory bank" and "follow your custom instructions" workflows (docs.cline.bot/best-practices/memory-bank.md). Conditional rules with `paths` frontmatter activate only for matching files, saving context tokens (docs.cline.bot/customization/cline-rules.md). Experimental subagents run parallel research in separate context windows, returning relevant file paths (docs.cline.bot/features/subagents.md). Focus Chain was deprecated; the new harness manages task execution and context without it (docs.cline.bot/resources/deprecations.md).

## Ecosystem

Cline Desktop's Marketplace browses or searches skills, MCP servers, and plugins, filterable by categories such as software development, data and analytics, productivity, and research and docs (docs.cline.bot/usage/cline-desktop.md). Plugins install via `cline plugin install` from file URLs, Git repositories, npm packages, or local paths — globally in ~/.cline/plugins or per-project in .cline/plugins — with a cline.plugins field in package.json declaring entry points (docs.cline.bot/customization/plugins.md). MCP servers are local STDIO or remote Streamable HTTP/SSE, configured in ~/.cline/mcp.json (docs.cline.bot/mcp/mcp-overview.md). Distribution channels: VS Code Marketplace (saoudrizwan.claude-dev), Open VSX, JetBrains Marketplace plugin 28247, and npm. Docs claim 300+ models via the Cline provider; repo release notes list 6,386 models across 209 providers (github.com/cline/cline/releases.atom). Marketplace item counts are not documented.

## Governance

Cline is Apache 2.0, copyright "Cline Bot Inc." (raw.githubusercontent.com/cline/cline/main/README.md; LICENSE). Contributions are issue-first: feature work needs maintainer approval before implementation — "PRs without approved issues may be closed" — while small fixes are exempt; security vulnerabilities go through GitHub's private advisory tool; conventional commits; CI runs lint, format, and tests, plus Playwright E2E (raw.githubusercontent.com/cline/cline/main/CONTRIBUTING.md). Contributors do not write changelog entries: "Maintainers handle release versioning and changelog curation during the release process." The JetBrains plugin is not open-sourced (README). No cadence is stated, but github.com/cline/cline/releases.atom shows ships every few days: v4.1.21 and v4.1.20 (2026-09-22/24), CLI v3.0.65, Desktop v0.0.35/v0.0.36, SDK v0.0.86.

## Limitations

Subagents are experimental and read-only: no file edits, browser, MCP servers, or nested subagents (docs.cline.bot/features/subagents.md). Kanban is labeled "(preview)"; Desktop requires your own model access and its Windows build "is currently in beta" (docs.cline.bot/getting-started/installing-cline.md). Auto Compact doesn't cover every model: "With other models, Cline falls back to standard rule-based context truncation" (docs.cline.bot/features/auto-compact.md). .clineignore is "Deprecating soon" and "should not be treated as a security boundary"; Focus Chain and Explain Changes are deprecated, Focus Chain with "No direct replacement" (docs.cline.bot/resources/deprecations.md). Plugins and custom tools "currently only appl[y] to Cline SDK, CLI, and Kanban… not applicable on VSCode and JetBrains Extension for now" (docs.cline.bot/customization/plugins.md). Local models need "Use Compact Prompt" and 16-64GB RAM guidance (docs.cline.bot/running-models-locally/overview.md).

## In its own words

> Cline is an AI coding agent that lives in your editor and your terminal. It can read and write files, run terminal commands, use a browser, and help you build features through natural conversation. Every action requires your explicit approval. You're always in control.  
> — [https://docs.cline.bot/cline-overview.md](https://docs.cline.bot/cline-overview.md)

> The single rule that keeps it clean: clients participate, spokes execute, the hub coordinates. No two roles should overlap.  
> — [https://docs.cline.bot/sdk/architecture/hub-spoke.md](https://docs.cline.bot/sdk/architecture/hub-spoke.md)

> Memory Bank is a documentation methodology that transforms Cline from a stateless assistant into a persistent development partner.  
> — [https://docs.cline.bot/best-practices/memory-bank.md](https://docs.cline.bot/best-practices/memory-bank.md)

> When your conversation approaches the model's context window limit, Cline automatically summarizes it to free up space and keep working.  
> — [https://docs.cline.bot/features/auto-compact.md](https://docs.cline.bot/features/auto-compact.md)


## Notable

Far beyond its VS Code-extensions origin, Cline now ships an SDK with a hub-spoke background daemon, CLI, desktop app, and a Kanban multi-agent board — yet agent teams, plugins, hooks, and scheduling are explicitly 'not applicable on VSCode and JetBrains Extension for now', and GitHub's 'latest release' is desktop-v0.0.43 while the extension train sits at v4.1.22.

## Sources fetched

- https://docs.cline.bot/llms.txt
- https://docs.cline.bot/cline-overview.md
- https://docs.cline.bot/getting-started/installing-cline.md
- https://docs.cline.bot/getting-started/cline-provider.md
- https://docs.cline.bot/features/auto-compact.md
- https://docs.cline.bot/features/subagents.md
- https://docs.cline.bot/best-practices/memory-bank.md
- https://docs.cline.bot/mcp/mcp-overview.md
- https://docs.cline.bot/core-workflows/plan-and-act.md
- https://docs.cline.bot/core-workflows/checkpoints.md
- https://docs.cline.bot/customization/cline-rules.md
- https://docs.cline.bot/customization/plugins.md
- https://docs.cline.bot/kanban/remote-access.md
- https://docs.cline.bot/usage/cline-desktop.md
- https://docs.cline.bot/cline-sdk/overview.md
- https://docs.cline.bot/running-models-locally/overview.md
- https://docs.cline.bot/resources/deprecations.md
- https://docs.cline.bot/tools-reference/all-cline-tools.md
- https://docs.cline.bot/sdk/architecture/hub-spoke.md
- https://raw.githubusercontent.com/cline/cline/main/README.md
- https://raw.githubusercontent.com/cline/cline/main/LICENSE
- https://raw.githubusercontent.com/cline/cline/main/CONTRIBUTING.md
- https://github.com/cline/cline/releases.atom

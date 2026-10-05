# Roo Code

- **repo:** RooCodeInc/Roo-Code
- **version pin:** `v3.54.0` — gh api repos/RooCodeInc/Roo-Code/releases/latest → https://github.com/RooCodeInc/Roo-Code/releases/tag/v3.54.0 (published 2026-05-15)
- **docs home:** https://roocodeinc.github.io/Roo-Code/

## What it promises

Roo Code promises "Your AI-Powered Dev Team, Right in Your Editor" — a whole team of AI agents inside VS Code that generate code from natural language, adapt with Code/Architect/Ask/Debug and custom modes, refactor and debug existing code, write documentation, answer codebase questions, automate repetitive tasks, and plug into external tools via MCP.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | Built-in Orchestrator mode delegates via new_task tool; child task runs in isolated context, parent pauses and resumes with the child's summary. Subtask creation/completion auto-approvable. | [src](https://roocodeinc.github.io/Roo-Code/features/boomerang-tasks) |
| workflow_orchestration | ◐ partial | Parent→child subtask chains with summary handoff only (sequential, no scripts/DAGs/swarms/YAML workflows). Worktrees allow parallel tasks in separate windows; message queueing sequences input. | [src](https://roocodeinc.github.io/Roo-Code/basic-usage/using-modes) |
| mcp | ✅ yes | MCP client with stdio/SSE/streamable-HTTP transports, global mcp_settings.json + project .roo/mcp.json, per-tool auto-approve, marketplace install. No evidence Roo itself acts as an MCP server. | [src](https://roocodeinc.github.io/Roo-Code/features/mcp/using-mcp-in-roo) |
| hooks_lifecycle | ? unknown | No lifecycle-hook feature (pre/post tool, session start/stop) found in any docs page or in the repo source (no hook files/config keys). Nearest extension points are MCP tools, custom modes, and experimental custom tools; nothing documented either way. | [src](https://roocodeinc.github.io/Roo-Code/) |
| skills | ✅ yes | SKILL.md with progressive disclosure; ~/.roo/skills and .roo/skills (also cross-agent ~/.agents/skills), mode targeting, bundled scripts/templates, project overrides global. | [src](https://roocodeinc.github.io/Roo-Code/features/skills) |
| memory_persistence | ◐ partial | No memory-bank/long-term memory feature. Persistence comes from shadow-git checkpoints, resumable task history (conversations stored and reopened), and file-based rules (.roorules / AGENTS.md loaded each session). | [src](https://roocodeinc.github.io/Roo-Code/features/checkpoints) |
| sandboxing | ◐ partial | Permission modes exist: per-action auto-approve tiles (read/edit/commands/MCP/browser/mode-switch), command whitelisting, CLI --require-approval. No OS-level sandbox — rooignore docs state '.rooignore ... does not create a system-level sandbox.' | [src](https://roocodeinc.github.io/Roo-Code/features/auto-approving-actions) |
| plan_mode | ◐ partial | Architect mode is a dedicated planning persona restricted to markdown-only edits. No formal plan-then-approve gate; the user approves implicitly by switching to Code/Debug mode. | [src](https://roocodeinc.github.io/Roo-Code/basic-usage/using-modes) |
| background_tasks | ◐ partial | Long-running terminal commands keep running, later checked via read_command_output; message queueing and the headless CLI (--print/--oneshot) are async-ish. No managed background-task queue for agent tasks. | [src](https://roocodeinc.github.io/Roo-Code/advanced-usage/available-tools/execute-command) |
| ide_integration | ✅ yes | VS Code Marketplace + Open VSX; works in Cursor, VSCodium, Windsurf. No JetBrains plugin. CLI also ships (apps/cli, npm-free shell installer) for terminal use. | [src](https://roocodeinc.github.io/Roo-Code/getting-started/installing) |
| model_agnostic | ✅ yes | Docs list ~28 providers (Anthropic, OpenAI, Gemini, Bedrock, Vertex, OpenRouter, xAI, Mistral, DeepSeek, Z.ai, Ollama, LM Studio, OpenAI-compatible, etc.); per-mode sticky model selection; API configuration profiles. | [src](https://roocodeinc.github.io/Roo-Code/providers/) |
| plugins | ◐ partial | Third-party distribution via marketplace (MCP servers + custom modes) and experimental defineCustomTool TS/JS tool API. No formal plugin/extension API with lifecycle or packaging spec beyond this. | [src](https://roocodeinc.github.io/Roo-Code/features/marketplace) |
| session_resume | ✅ yes | Task history persists conversations and tasks can be reopened/resumed (resumeTask+isTaskInHistory also in the extension API); CLI supports session/task IDs (--create-with-session-id, taskId in stdin stream mode). | [src](https://roocodeinc.github.io/Roo-Code/features/api-configuration-profiles) |
| cost_controls | ✅ yes | Per-request input/output token counts and estimated cost shown in chat (incl. reasoning tokens); 'Max Requests' cap for auto-approved actions forces re-approval; per-profile rate limits; supports free local models. | [src](https://roocodeinc.github.io/Roo-Code/advanced-usage/rate-limits-costs) |

## Architecture

Roo Code is primarily a VS Code extension: "The Roo Code VS Code extension works locally in your IDE" (https://docs.roocode.com/). The repo is a TypeScript pnpm/Turbo monorepo whose packages/core, ipc, and vscode-shim back a prerelease CLI, @roo-code/cli v0.1.17, running the agent in Node 20+ TUI mode "without VSCode" (https://raw.githubusercontent.com/RooCodeInc/Roo-Code/main/apps/cli/README.md). src/package.json declares engine vscode ^1.84.0, node 20.19.2, main ./dist/extension.js (https://raw.githubusercontent.com/RooCodeInc/Roo-Code/main/src/package.json). The model never executes tools itself; the extension runs an in-process tool loop — read_file, apply_diff, execute_command, codebase_search, MCP tools — with per-call approval or auto-approval (https://roocodeinc.github.io/Roo-Code/basic-usage/how-tools-work). MCP servers connect via STDIO, Streamable HTTP, or legacy SSE (https://roocodeinc.github.io/Roo-Code/features/mcp/overview).

## Context management

Layered context management. Intelligent Context Condensing summarizes earlier dialogue automatically at a configurable threshold (e.g., 80% of the window) or via a manual button, always with the active provider/model, plus automatic recovery from context-limit errors (https://roocodeinc.github.io/Roo-Code/features/intelligent-context-condensing). Older messages are truncated automatically to stay inside the window (https://roocodeinc.github.io/Roo-Code/advanced-usage/large-projects). Checkpoints snapshot workspace state into a shadow Git repository before file modifications (https://roocodeinc.github.io/Roo-Code/features/checkpoints). Codebase indexing maintains a Qdrant-backed embedding index for semantic codebase_search (https://roocodeinc.github.io/Roo-Code/features/codebase-indexing). Custom instructions via .roorules and @-mentions inject targeted context (https://roocodeinc.github.io/Roo-Code/faq); poisoned sessions are documented as disposable, not repairable (https://roocodeinc.github.io/Roo-Code/advanced-usage/context-poisoning).

## Ecosystem

Distribution: the VS Code Marketplace entry RooVeterinaryInc.roo-cline shows 2,020,991 installs and 350 reviews (https://marketplace.visualstudio.com/items?itemName=RooVeterinaryInc.roo-cline); Open VSX mirrors it with 1,991,053 downloads, latest v3.54.0 dated 2026-05-15 (https://open-vsx.org/api/RooVeterinaryInc/roo-cline). GitHub records 24,291 stars and 3,423 forks (https://api.github.com/repos/RooCodeInc/Roo-Code). An in-IDE Marketplace installs two item types, MCP servers and Modes, one click, project- or global-scoped (https://roocodeinc.github.io/Roo-Code/features/marketplace); MCP servers attach via STDIO, Streamable HTTP, or SSE (https://roocodeinc.github.io/Roo-Code/features/mcp/overview). Docs claim compatibility with "dozens of providers and hundreds of models" (https://docs.roocode.com/); the sitemap lists 24 provider pages. No numeric marketplace-item counts are published; community fork ZooCode continues development (https://raw.githubusercontent.com/RooCodeInc/Roo-Code/main/README.md).

## Governance

License: Apache-2.0 — README states "Apache 2.0 © 2026 Roo Code, Inc." (https://raw.githubusercontent.com/RooCodeInc/Roo-Code/main/README.md); the GitHub API returns spdx_id apache-2.0 (https://api.github.com/repos/RooCodeInc/Roo-Code). Owning org: Roo Code, Inc.; billing runs through billing@roocode.com, and roocode.com now redirects to the company's newer Roomote product (https://roocode.com). Contribution model: GitHub issues/PRs while active (CODEOWNERS, issue templates, workflows under .github), docs hosted in RooCodeInc/Roo-Code-Docs, also Apache-2.0. Release cadence: stable tags v3.51.0 (Mar 5, 2026), v3.52.0 (Apr 8), v3.53.0 (Apr 23), v3.54.0 (May 15, 2026) — roughly 1-4 weeks apart — plus a documented Nightly channel (https://roocodeinc.github.io/Roo-Code/advanced-usage/roo-code-nightly). The repo is archived, so no further releases are expected.

## Limitations

Documented limits: an Experimental tier — background editing, concurrent file edits, custom tools — whose docs warn of potential data loss or security vulnerabilities (https://roocodeinc.github.io/Roo-Code/features/experimental/experimental-features). Checkpoints are not created before command execution, so terminal side effects are uncaptured (https://roocodeinc.github.io/Roo-Code/features/checkpoints). Shell integration needs manual fixes per shell: VS Code 1.93+, PowerShell execution-policy changes, profile lines for bash/zsh/fish (https://roocodeinc.github.io/Roo-Code/features/shell-integration). The prerelease CLI lists only macOS Apple Silicon and Linux x64 as supported platforms (https://raw.githubusercontent.com/RooCodeInc/Roo-Code/main/apps/cli/README.md). FAQ documents .md write failures caused by other installed VS Code extensions (https://roocodeinc.github.io/Roo-Code/faq). Overriding all: the extension shut down May 15, 2026; the repo is archived with 1,033 open issues frozen (https://api.github.com/repos/RooCodeInc/Roo-Code).

## In its own words

> Leverage model agnosticism: Roo isn't an LLM model, it needs an LLM provider to work. But it's compatible with dozens of providers and hundreds of models, so you're free to experiment, optimize and switch around, by design. No lock-ins in a world where "the best model" changes every other week.  
> — [https://docs.roocode.com/](https://docs.roocode.com/)

> Roo's approach is to trade tokens for quality. If you want the best and most effective AI coding experience available, this is it.  
> — [https://docs.roocode.com/](https://docs.roocode.com/)

> The Roo Code Extension was shut down on May 15th.  
> — [https://docs.roocode.com/](https://docs.roocode.com/)

> Experimental features may have unexpected behavior, including potential data loss or security vulnerabilities. Enable them at your own risk.  
> — [https://roocodeinc.github.io/Roo-Code/features/experimental/experimental-features](https://roocodeinc.github.io/Roo-Code/features/experimental/experimental-features)


## Notable

The project is discontinued: the README states the extension "was shut down on May 15th" (2026) — the same date as the final v3.54.0 release — and redirects users to the community fork ZooCode or to Cline.

## Sources fetched

- https://docs.roocode.com/
- https://roocodeinc.github.io/Roo-Code/sitemap.xml
- https://roocodeinc.github.io/Roo-Code/features/intelligent-context-condensing
- https://roocodeinc.github.io/Roo-Code/features/checkpoints
- https://roocodeinc.github.io/Roo-Code/features/codebase-indexing
- https://roocodeinc.github.io/Roo-Code/features/marketplace
- https://roocodeinc.github.io/Roo-Code/features/experimental/experimental-features
- https://roocodeinc.github.io/Roo-Code/features/mcp/overview
- https://roocodeinc.github.io/Roo-Code/features/shell-integration
- https://roocodeinc.github.io/Roo-Code/faq
- https://roocodeinc.github.io/Roo-Code/basic-usage/how-tools-work
- https://roocodeinc.github.io/Roo-Code/advanced-usage/available-tools/tool-use-overview
- https://roocodeinc.github.io/Roo-Code/advanced-usage/roo-code-nightly
- https://roocodeinc.github.io/Roo-Code/advanced-usage/context-poisoning
- https://roocodeinc.github.io/Roo-Code/advanced-usage/large-projects
- https://raw.githubusercontent.com/RooCodeInc/Roo-Code/main/README.md
- https://raw.githubusercontent.com/RooCodeInc/Roo-Code/main/src/package.json
- https://raw.githubusercontent.com/RooCodeInc/Roo-Code/main/apps/cli/package.json
- https://raw.githubusercontent.com/RooCodeInc/Roo-Code/main/apps/cli/README.md
- https://api.github.com/repos/RooCodeInc/Roo-Code
- https://api.github.com/repos/RooCodeInc/Roo-Code/releases?per_page=8
- https://api.github.com/repos/RooCodeInc/Roo-Code/contents/
- https://api.github.com/repos/RooCodeInc/Roo-Code/contents/.github
- https://api.github.com/repos/RooCodeInc/Roo-Code-Docs
- https://marketplace.visualstudio.com/items?itemName=RooVeterinaryInc.roo-cline
- https://open-vsx.org/api/RooVeterinaryInc/roo-cline
- https://roocode.com/

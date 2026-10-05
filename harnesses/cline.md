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

## Notable

Far beyond its VS Code-extensions origin, Cline now ships an SDK with a hub-spoke background daemon, CLI, desktop app, and a Kanban multi-agent board — yet agent teams, plugins, hooks, and scheduling are explicitly 'not applicable on VSCode and JetBrains Extension for now', and GitHub's 'latest release' is desktop-v0.0.43 while the extension train sits at v4.1.22.

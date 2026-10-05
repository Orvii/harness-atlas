# Aider

- **repo:** Aider-AI/aider
- **version pin:** `v0.86.0 (latest GitHub release; PyPI aider-chat latest is 0.86.2)` — gh api https://api.github.com/repos/Aider-AI/aider/releases/latest -> tag v0.86.0 (published 2025-08-09); PyPI JSON https://pypi.org/pypi/aider-chat/json -> 0.86.2 (docs evidence read from aider.chat, main branch)
- **docs home:** https://aider.chat/docs/

## What it promises

Aider is "AI Pair Programming in Your Terminal": it lets you pair program with LLMs to start a new project or build on your existing codebase, with AI changes automatically committed using sensible git commit messages.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✗ no | No sub-agent/child-agent concept in v0.86 docs or code; architect mode's two LLM roles are a fixed pipeline, not spawnable agents. | [src](https://aider.chat/docs/config/options.html) |
| workflow_orchestration | ✗ no | Only multi-model construct is architect/editor, a single fixed two-role pipeline; no DAGs, teams, swarms, or orchestration scripting. | [src](https://aider.chat/docs/usage/modes.html) |
| mcp | ✗ no | No MCP client or server support: zero mentions of MCP anywhere in v0.86 docs or code, and no MCP flags or config. | [src](https://aider.chat/docs/config/options.html) |
| hooks_lifecycle | ✗ no | No lifecycle hook API; closest are default-on auto-lint/auto-test after edits and --notifications-command. Only 'hooks' option is a git pre-commit --no-verify toggle. | [src](https://aider.chat/docs/config/options.html) |
| skills | ✗ no | No skill/prompt-pack registry; closest is a CONVENTIONS.md markdown file (or --read files) added to chat as static prompt context. | [src](https://aider.chat/docs/usage/conventions.html) |
| memory_persistence | ◐ partial | Per-project chat transcript persisted to disk and reloadable; no structured long-term memory store. | [src](https://aider.chat/docs/config/options.html) |
| sandboxing | ◐ partial | Shell commands and edits to unadded files require explicit y/n approval by default (code-verified); --yes-always/dry-run bypass. No OS sandbox or graded permission modes. | [src](https://aider.chat/docs/config/options.html) |
| plan_mode | ◐ partial | Ask/architect modes support plan-then-execute ('go ahead' in code mode) but there is no plan artifact or approval gate. | [src](https://aider.chat/docs/usage/modes.html) |
| background_tasks | ✗ no | No background/async task execution; --watch-files is a foreground watcher for 'AI!' code comments. | [src](https://aider.chat/docs/config/options.html) |
| ide_integration | ✗ no | No official VS Code/JetBrains extension; 'Aider in your IDE' means watch mode reacting to AI comments from any editor, run alongside the terminal. | [src](https://aider.chat/docs/usage/watch.html) |
| model_agnostic | ✅ yes | Docs cover OpenAI, Anthropic, Gemini, DeepSeek, xAI, OpenRouter, Azure, Bedrock, Groq, local Ollama/LM Studio, and OpenAI-compatible endpoints. | [src](https://aider.chat/docs/llms.html) |
| plugins | ✗ no | No plugin or extension API in docs or code; third parties can only wrap the CLI externally. | [src](https://aider.chat/docs/config/options.html) |
| session_resume | ✅ yes | --restore-chat-history reloads the project's last transcript (.aider.chat.history.md) into the LLM conversation (code-verified); no multi-session picker. | [src](https://aider.chat/docs/config/options.html) |
| cost_controls | ✅ yes | /tokens reports context tokens; aider also prints per-message and session dollar cost after each reply (code-verified). | [src](https://aider.chat/docs/usage/commands.html) |

## Notable

Despite huge popularity, v0.86 ships no MCP, plugin, subagent, or lifecycle-hook support, and the GitHub "latest release" (v0.86.0) lags the PyPI version users actually install (0.86.2).

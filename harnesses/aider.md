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

## Architecture

Aider is a Python terminal application: `aider` is launched from a project directory and presents an interactive chat prompt, with no server, daemon, or GUI documented; distribution is via aider-install, shell/PowerShell installers, uv, pipx, or pip (https://aider.chat/docs/install.html). Model edits arrive through selectable edit formats — whole-file, search/replace diff blocks, diff-fenced/udiff/editor variants chosen per model (https://aider.chat/docs/more/edit-formats.html). Every edit is applied to the working tree and git-committed automatically with a descriptive message (https://aider.chat/docs/git.html). External tool execution: auto-lint runs by default after edits, auto-test is off by default, and `/test` / `--test-cmd` run test suites, with failures prompting attempted repairs (https://aider.chat/docs/usage/lint-test.html). Architect mode runs two models: architect proposes, editor edits (https://aider.chat/docs/usage/modes.html).

## Context management

Context is assembled from chat files plus a repo map: "Aider uses a concise map of your whole git repository" showing symbols and signatures (https://aider.chat/docs/repomap.html). Map size is governed by `--map-tokens`, default 1k, and grows when no files are in chat. Users manage context explicitly with `/add`, `/drop` ("Remove files from the chat session to free up context space"), `/read-only`, `/reset`, while `/tokens` reports token usage and `/context` and `/map` inspect context (https://aider.chat/docs/usage/commands.html). The FAQ warns extra files "distract or confuse" models (https://aider.chat/docs/faq.html). Prompt caching (`--cache-prompts`) reuses system instructions, read-only files, repo map, and editable files, with a default 5-minute Anthropic cache extendable via keepalive pings (https://aider.chat/docs/usage/caching.html). Fetched pages describe no conversation summarization or compaction step.

## Ecosystem

Fetched docs describe no plugin marketplace or extension registry; distribution is package-managed — aider-install, uv, pipx, pip, and shell installers (https://aider.chat/docs/install.html). Breadth comes from model providers: 16 listed provider/API categories including OpenAI, Anthropic, Gemini, Groq, xAI, Azure, Cohere, DeepSeek, Ollama, OpenRouter, GitHub Copilot, Vertex AI, Amazon Bedrock, plus OpenAI-compatible endpoints (https://aider.chat/docs/llms.html). The README advertises 6.8M installs, 15B tokens per week, and OpenRouter Top 20 (https://raw.githubusercontent.com/Aider-AI/aider/main/README.md). The public leaderboard compares 69 model configurations on a 225-exercise polyglot benchmark across C++, Go, Java, JavaScript, Python, and Rust, last updated November 20, 2025 (https://aider.chat/docs/leaderboards/). The languages page lists 149 language labels (https://aider.chat/docs/languages.html); community discussion is on Discord (https://aider.chat/docs/more-info.html).

## Governance

License is Apache 2.0 per the repo's LICENSE.txt ("Apache License, Version 2.0"); its copyright-owner line is the unfilled placeholder "[name of copyright owner]" (https://raw.githubusercontent.com/Aider-AI/aider/main/LICENSE.txt). The FAQ states "Aider AI LLC is the company behind the aider AI coding tool" (https://aider.chat/docs/faq.html). Contribution model: bugs and feature requests go to GitHub issues; small changes can go straight to a PR, large changes should be discussed in an issue first, and "All contributors will be asked to complete the agreement as part of the PR process" — an Individual CLA (https://raw.githubusercontent.com/Aider-AI/aider/main/CONTRIBUTING.md). HISTORY.html shows vMAJOR.MINOR.PATCH versioning with frequent patch releases, latest v0.86.1, but no dates, so calendar cadence cannot be computed (https://aider.chat/HISTORY.html).

## Limitations

Documented constraints: "Currently aider can only work with one repo at a time" and extra files "distract or confuse the LLM" (https://aider.chat/docs/faq.html). Weaker models "get easily overwhelmed and confused by the content of the repo map," with a `--map-tokens 1024` workaround (same FAQ). Auto-test is off by default while auto-lint defaults to True (https://aider.chat/docs/config/options.html). The options reference currently flags no options as experimental, and no fetched page lists experimental flags (https://aider.chat/docs/config/options.html). Troubleshooting covers file editing problems, model warnings, and token limits, but names no Windows- or terminal-specific gaps (https://aider.chat/docs/troubleshooting.html). Infinite output stitches extra model continuations using "heuristics" (https://aider.chat/docs/more/infinite-output.html). The architecture page https://aider.chat/docs/more/arch.html returned HTTP 404.

## In its own words

> Aider is AI pair programming in your terminal.  
> — [https://aider.chat/docs/](https://aider.chat/docs/)

> Aider will git commit all of its changes, so they are easy to track and undo.  
> — [https://aider.chat/docs/usage.html](https://aider.chat/docs/usage.html)

> Aider uses a concise map of your whole git repository  
> — [https://aider.chat/docs/repomap.html](https://aider.chat/docs/repomap.html)

> Currently aider can only work with one repo at a time.  
> — [https://aider.chat/docs/faq.html](https://aider.chat/docs/faq.html)


## Notable

Despite huge popularity, v0.86 ships no MCP, plugin, subagent, or lifecycle-hook support, and the GitHub "latest release" (v0.86.0) lags the PyPI version users actually install (0.86.2).

## Sources fetched

- https://aider.chat/docs/
- https://aider.chat/docs/more/arch.html (404, not found)
- https://aider.chat/docs/faq.html
- https://aider.chat/docs/repomap.html
- https://aider.chat/docs/usage.html
- https://aider.chat/docs/more-info.html
- https://aider.chat/docs/install.html
- https://aider.chat/docs/more/edit-formats.html
- https://aider.chat/docs/usage/commands.html
- https://aider.chat/docs/llms.html
- https://aider.chat/docs/config.html
- https://aider.chat/docs/config/options.html
- https://aider.chat/docs/git.html
- https://aider.chat/docs/usage/caching.html
- https://aider.chat/docs/usage/lint-test.html
- https://aider.chat/docs/usage/watch.html
- https://aider.chat/docs/usage/modes.html
- https://aider.chat/docs/languages.html
- https://aider.chat/docs/troubleshooting.html
- https://aider.chat/docs/more/infinite-output.html
- https://aider.chat/docs/leaderboards/
- https://aider.chat/HISTORY.html
- https://raw.githubusercontent.com/Aider-AI/aider/main/README.md
- https://raw.githubusercontent.com/Aider-AI/aider/main/LICENSE.txt
- https://raw.githubusercontent.com/Aider-AI/aider/main/CONTRIBUTING.md

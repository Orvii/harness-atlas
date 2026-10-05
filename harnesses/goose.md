# Goose

- **repo:** block/goose (redirects to aaif-goose/goose)
- **version pin:** `v1.53.0` — https://github.com/aaif-goose/goose/releases/tag/v1.53.0 — read via gh api repos/block/goose/releases/latest (2026-10-02), which now redirects to aaif-goose/goose
- **docs home:** https://goose-docs.ai/

## What it promises

Goose promises a general-purpose AI agent that "runs on your machine" — "Not just for code" but research, writing, automation, and data analysis, extensible via 70+ MCP extensions and working with 15+ model providers.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | Natural-language delegation; subagents cannot spawn further subagents; disabled in manual approval, smart approval, and chat-only modes. | [src](https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/docs/guides/context-engineering/subagents.mdx) |
| workflow_orchestration | ✅ yes | Recipes (YAML scripts) compose subrecipes sequentially or in parallel (up to 10 workers, isolated sessions); no DAG/team/swarm abstractions. | [src](https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/docs/tutorials/subrecipes-in-parallel.md) |
| mcp | ✅ yes | MCP client for extensions; also ships bundled MCP servers ('goose mcp' runs one) and an ACP agent server. | [src](https://raw.githubusercontent.com/aaif-goose/goose/main/README.md) |
| hooks_lifecycle | ✅ yes | Events include SessionStart, SessionEnd, PreToolUse/PostToolUse, BeforeShellExecution, AfterFileEdit; defined in plugins via hooks/hooks.json. | [src](https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/docs/guides/context-engineering/hooks.md) |
| skills | ✅ yes | SKILL.md with YAML frontmatter; global, project, or plugin scope; built-in Skills extension enabled by default. | [src](https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/docs/guides/context-engineering/using-skills.md) |
| memory_persistence | ✅ yes | File-based storage: project .goose/memory/ and global ~/.config/goose/memory/; no database. | [src](https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/docs/mcp/memory-mcp.md) |
| sandboxing | ◐ partial | Four permission modes (completely autonomous, manual approval, smart approval, chat only) but no OS-level command sandboxing/container isolation documented. | [src](https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/docs/guides/managing-tools/goose-permissions.md) |
| plan_mode | ✗ no | Current CLI command list has no plan command or plan-mode flag; blog post promoting plan mode carries a removal warning. | [src](https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/blog/2025-12-19-does-your-ai-agent-need-a-plan/index.md) |
| background_tasks | ✅ yes | 'goose schedule add' runs recipes on cron; docs note scheduled runs 'run in the background (no window, results saved)'. Remote 'goose serve' also runs as a background service. | [src](https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/docs/guides/recipes/session-recipes.md) |
| ide_integration | ✅ yes | Extension lives under the experimental docs dir ('in active development'); JetBrains support is via the JetBrains MCP Server extension, not a native plugin. | [src](https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/docs/experimental/vs-code-extension.md) |
| model_agnostic | ✅ yes | Includes local models (Ollama, 'goose local-models'); provider integrations are declarative definitions. | [src](https://raw.githubusercontent.com/aaif-goose/goose/main/README.md) |
| plugins | ✅ yes | plugin.json manifest with skills/ and hooks/; install from git repos via 'goose plugin install'; Gemini-style extensions also supported. | [src](https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/docs/guides/context-engineering/plugins.md) |
| session_resume | ✅ yes | CLI resume latest or by name; Desktop resumes from sidebar or Session History; scheduled recipe runs create resumable sessions. | [src](https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/docs/guides/goose-cli-commands.md) |
| cost_controls | ✅ yes | Desktop and CLI show token usage and live estimated session cost; docs stress estimates, not actual provider billing; no hard token/cost limits documented. | [src](https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/docs/guides/sessions/smart-context-management.md) |

## Notable

The block/goose repo now redirects to a renamed org, aaif-goose/goose, and plan mode — heavily promoted in a December 2025 blog post — has since been removed from the CLI.

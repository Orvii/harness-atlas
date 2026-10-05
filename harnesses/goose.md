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

## Architecture

Goose is built in Rust and ships as a desktop app, CLI, and API. Docs describe three components: the interface (Desktop or CLI), the agent running the interactive loop, and MCP extensions supplying tools (https://goose-docs.ai/docs/goose-architecture/). goose Desktop normally runs its own `goose serve` ACP server process in the background on the same machine; that server can also run remotely with TLS, a shared secret key, and certificate pinning (https://goose-docs.ai/docs/guides/remote-goose-server). `goose acp` also exposes goose as an ACP server over stdio for editors like Zed and JetBrains. In the loop, the model emits JSON tool calls; goose executes them and sends results back to the model. Optional Code Mode executes batched tool calls as JavaScript on pctx, a Deno-based runtime (https://goose-docs.ai/docs/guides/managing-tools/code-mode).

## Context management

Two-tier context management: auto-compaction proactively summarizes older conversation at 80% of the token limit by default (tunable with GOOSE_AUTO_COMPACT_THRESHOLD), and fallback strategies — summarize, truncate, clear, or prompt — are chosen via GOOSE_CONTEXT_STRATEGY; Desktop only summarizes while the CLI supports all four (https://goose-docs.ai/docs/guides/sessions/smart-context-management). /compact does manual compaction; /summarize is a deprecated alias. Older tool outputs are summarized in the background (GOOSE_TOOL_CALL_CUTOFF). Persistent instructions come from .goosehints and AGENTS.md files, global and per-directory, loaded as nested directories are accessed; CONTEXT_FILE_NAMES enables CLAUDE.md and .cursorrules reuse (https://goose-docs.ai/docs/guides/context-engineering/using-goosehints). Architecture docs describe context revision: summarizing with faster, smaller LLMs, algorithmic deletion of old content, ripgrep to skip system files, and find-replace instead of file rewrites (https://goose-docs.ai/docs/goose-architecture/).

## Ecosystem

README says goose connects to "70+ extensions" via MCP and works with "15+ providers", including existing Claude, ChatGPT, or Gemini subscriptions through ACP. The docs source contains 73 published MCP-server pages plus a template, consistent with the 70+ claim. Built-ins: Developer (enabled by default), Computer Controller, Memory, Tutorial, Auto Visualiser, plus platform extensions Analyze, Apps, Chat Recall, Code Mode, Extension Manager, Skills, Summon, Todo, Top of Mind (https://goose-docs.ai/docs/getting-started/using-extensions). Distribution: a central directory at https://goose-docs.ai/extensions, goose://extension deeplinks, config.yaml entries, any third-party MCP server, and remote Streamable HTTP servers. External extensions are checked against OSV malware advisories and blocked; the check covers only locally executed npx/uvx extensions (https://goose-docs.ai/docs/troubleshooting/known-issues).

## Governance

License: Apache-2.0 (LICENSE in aaif-goose/goose); documentation is CC-BY-4.0 (https://github.com/aaif-goose/goose/blob/main/GOVERNANCE.md). Block donated goose to the Agentic AI Foundation (AAIF) at the Linux Foundation, alongside MCP and AGENTS.md; the repo moved from block/goose to github.com/aaif-goose/goose (https://goose-docs.ai/blog/2026/04/07/goose-moves-to-aaif). GOVERNANCE.md defines Contributors, Maintainers, and 3-7 Core Maintainers approved by majority vote on merit; decisions happen publicly via PRs, issues, and Discord, with creator Bradley Axen as deadlock tie-breaker; LF Projects, LLC policies apply. CONTRIBUTING.md frames contributions as issue-driven — "The unit of contribution is taking a problem to a verified solution, not writing the patch" (https://github.com/aaif-goose/goose/blob/main/CONTRIBUTING.md). RELEASE.md: minor releases "typically done once per week" via Tuesday automation; patch releases are cherry-picked.

## Limitations

Experimental features — Ollama tool shim, remote access (mobile app, Telegram), VS Code extension — are documented as "still in development and may not be fully stable or ready for production use" (https://goose-docs.ai/docs/experimental/). Java and Kotlin extensions run only on Linux and macOS; DeepSeek models do not support tool calling, so all extensions must be disabled (https://goose-docs.ai/docs/getting-started/using-extensions). Code Mode supports only text tool results — images and binary are ignored (https://goose-docs.ai/docs/guides/managing-tools/code-mode). Desktop lacks context-limit overrides ("not yet available in the goose Desktop app") and truncate/clear strategies (https://goose-docs.ai/docs/guides/sessions/smart-context-management). Known issues document "doom spiral" sessions, macOS ~/.config permission failures, Windows expecting Node.js under C:\Program Files\nodejs\, and malware scanning limited to local npx/uvx extensions (https://goose-docs.ai/docs/troubleshooting/known-issues).

## In its own words

> goose is a general-purpose AI agent that runs on your machine.  
> — [https://github.com/aaif-goose/goose/blob/main/README.md](https://github.com/aaif-goose/goose/blob/main/README.md)

> In rare cases, goose may enter a "doom spiral" or become unresponsive during a long session.  
> — [https://goose-docs.ai/docs/troubleshooting/known-issues](https://goose-docs.ai/docs/troubleshooting/known-issues)

> goose operates autonomously by default. Combined with the Developer extension's tools, this means goose can execute commands and modify files without your approval.  
> — [https://goose-docs.ai/docs/getting-started/using-extensions](https://goose-docs.ai/docs/getting-started/using-extensions)

> Our goal is to make goose the most hackable agent available.  
> — [https://github.com/aaif-goose/goose/blob/main/GOVERNANCE.md](https://github.com/aaif-goose/goose/blob/main/GOVERNANCE.md)


## Notable

The block/goose repo now redirects to a renamed org, aaif-goose/goose, and plan mode — heavily promoted in a December 2025 blog post — has since been removed from the CLI.

## Sources fetched

- https://block.github.io/goose/docs/ (404; site redirected to https://goose-docs.ai/)
- https://goose-docs.ai/ (site root)
- https://goose-docs.ai/llms.txt
- https://goose-docs.ai/sitemap.xml
- https://goose-docs.ai/docs/goose-architecture/
- https://goose-docs.ai/docs/goose-architecture/extensions-design
- https://goose-docs.ai/docs/guides/sessions/smart-context-management
- https://goose-docs.ai/docs/guides/context-engineering/using-goosehints
- https://goose-docs.ai/docs/getting-started/using-extensions
- https://goose-docs.ai/docs/getting-started/installation
- https://goose-docs.ai/docs/experimental/
- https://goose-docs.ai/docs/guides/managing-tools/code-mode
- https://goose-docs.ai/docs/troubleshooting/known-issues
- https://goose-docs.ai/docs/guides/remote-goose-server
- https://goose-docs.ai/extensions
- https://goose-docs.ai/blog/2026/04/07/goose-moves-to-aaif
- https://raw.githubusercontent.com/aaif-goose/goose/main/README.md
- https://raw.githubusercontent.com/aaif-goose/goose/main/GOVERNANCE.md
- https://raw.githubusercontent.com/aaif-goose/goose/main/RELEASE.md
- https://raw.githubusercontent.com/aaif-goose/goose/main/CONTRIBUTING.md
- https://raw.githubusercontent.com/aaif-goose/goose/main/LICENSE
- https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/docs/goose-architecture/goose-architecture.md
- https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/docs/goose-architecture/extensions-design.md
- https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/docs/guides/sessions/smart-context-management.md
- https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/docs/guides/context-engineering/using-goosehints.md
- https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/docs/getting-started/using-extensions.md
- https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/docs/getting-started/installation.md
- https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/docs/experimental/index.md
- https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/docs/guides/managing-tools/code-mode.md
- https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/docs/troubleshooting/known-issues.md
- https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/docs/guides/remote-goose-server.md
- https://raw.githubusercontent.com/aaif-goose/goose/main/documentation/blog/2026-04-07-goose-moves-to-aaif/index.md
- https://api.github.com/repos/aaif-goose/goose
- https://api.github.com/repos/aaif-goose/goose/git/trees/main?recursive=1

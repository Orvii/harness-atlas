# Amazon Q Developer CLI

- **repo:** aws/amazon-q-developer-cli
- **version pin:** `v1.19.7` — gh api repos/aws/amazon-q-developer-cli/releases/latest — tag v1.19.7, published 2025-11-17 (latest release; no releases since)
- **docs home:** https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line.html

## What it promises

Repo description and README frame it as an "Agentic chat experience in your terminal. Build applications using natural language." The project docs promise customizable JSON-defined agents with MCP tools, a persistent knowledge base, lifecycle hooks, and experimental background delegation — all in an open-source (MIT/Apache-2.0) Rust CLI.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | Experimental `delegate` tool (github.com/aws/amazon-q-developer-cli/pull/3073). Source registers the experiment as enabling "launching and managing asynchronous subagent processes". Delegated agents use their own JSON config (tools, permissions); one task per agent at a time; output files under .amazonq/.subagents/. | [src](https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/experiments.md) |
| workflow_orchestration | ◐ partial | Main chat session acts as coordinator over multiple concurrently running delegated agents (completion notifications + auto-summaries in context), but primitives are only launch/status/list — no DAGs, teams, swarms, or scripting layer. | [src](https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/experiments.md) |
| mcp | ✅ yes | Per-agent MCP servers with env vars and per-request timeout (default 120000ms), tool namespacing (@server/tool) and aliases; local stdio plus remote HTTP/SSE with OAuth and headers (per changelog); legacy global/workspace mcp.json via useLegacyMcpJson; `q mcp add` management subcommand. | [src](https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/agent-format.md) |
| hooks_lifecycle | ✅ yes | Triggers: agentSpawn, userPromptSubmit, preToolUse (exit 2 blocks the tool call and returns STDERR to the LLM), postToolUse, stop (end of each assistant turn). Tool matchers with globs (@git/status, @builtin, *), JSON hook events on STDIN, 30s default timeout, optional result caching (cache_ttl_seconds). | [src](https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/hooks.md) |
| skills | ✗ no | Complete repo docs index shows no skills/prompt-pack subsystem. Nearest analogues: per-agent `prompt` field supporting inline text or file:// URIs, `resources` file globs (e.g. .amazonq/rules/**/*.md), and the /agent generate slash command. | [src](https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/SUMMARY.md) |
| memory_persistence | ✅ yes | Experimental /knowledge (opt-in via q settings chat.enableKnowledge). Semantic index (all-MiniLM-L6-v2) or BM25 'Fast' index; agent-scoped stores under ~/.aws/amazonq/knowledge_bases/ with no cross-agent access; background indexing with progress and cancel. Separate from conversation-level persistence (q chat --resume, /save, /load). | [src](https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/built-in-tools.md) |
| sandboxing | ◐ partial | Permission engine only, no OS/container isolation: allowedTools glob patterns; execute_bash allowedCommands/deniedCommands regex + denyByDefault; fs allowedPaths/deniedPaths gitignore-style globs; use_aws allowed/deniedServices + autoAllowReadonly; delegated default-agent tasks run with trust-all permissions (warning shown). Only 'sandbox' string in repo is a macOS signing entitlement. | [src](https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/built-in-tools.md) |
| plan_mode | ✗ no | No plan-then-approve mode documented in any fetched doc. Closest analogues: experimental todo_list tool with user-run /todos resume\|view\|delete (stored in .amazonq/cli-todo-lists/) and checkpointing (/checkpoint restore) to roll back file changes. | [src](https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/experiments.md) |
| background_tasks | ✅ yes | Experimental delegate tool; you continue the main conversation while tasks run, then get a prompt notification with SUCCESS/FAILED status, completion time, and an AI-generated summary automatically added to conversation context. | [src](https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/crates/chat-cli/src/cli/chat/tools/tool_index.json) |
| ide_integration | ✗ no | Repo is a standalone Rust terminal app (crates/chat-cli); no VS Code/JetBrains extension ships from it. Amazon Q Developer IDE plugins for VS Code, JetBrains, and Visual Studio are separate AWS products (docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-in-IDE-setup.html). The CLI can of course run inside an IDE's terminal. | [src](https://api.github.com/repos/aws/amazon-q-developer-cli) |
| model_agnostic | ✗ no | Single provider: models are served by the Amazon Q service (Claude family — changelog entries reference Sonnet 4/4.5). Model is selectable per agent via the `model` field or /model, but no third-party provider endpoints or provider config exist. | [src](https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/agent-format.md) |
| plugins | ✗ no | No plugin/extension API or marketplace; 'plugin' code hits are internal AWS SDK runtime plugins. Third-party capability is added exclusively through MCP servers plus JSON agent configs shared as files. | [src](https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/agent-format.md) |
| session_resume | ✅ yes | Changelog also lists `Commands /save and /load for saving and loading conversation state in q chat`. TODO lists can be resumed per directory (/todos resume); tangent mode has conversation checkpoints; delegated task outputs persist on disk. | [src](https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/crates/chat-cli/src/cli/feed.json) |
| cost_controls | ◐ partial | /usage estimates context-window consumption (shipped PR #1177); the Context Usage Percentage experiment adds a color-coded percentage to the prompt (green <50%, yellow 50-89%, red 90-100%). Token/context tracking only — no dollar-cost accounting, spend limits, or quotas documented. | [src](https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/experiments.md) |

## Architecture

Single Rust binary (`q`, crate `chat_cli`) runs as a local terminal chat process, authenticating to the Amazon Q service through browser-based PKCE/Builder ID login. Built-in tools (fs_read, fs_write, execute_bash, use_aws, knowledge, todo_list, delegate) execute directly on the user's machine under an explicit per-tool permission system — no container. Agent behavior is configured by JSON agent files (prompt, tool allowlists, resources, hooks). MCP servers are spawned as child processes (command, args, env; 120s default timeout) or connected remotely over HTTP/SSE with OAuth; hooks are shell commands invoked at lifecycle points with JSON events on STDIN. (Sources: raw README.md, docs/agent-format.md, docs/built-in-tools.md, docs/hooks.md at tag v1.19.7.)

## Context management

`/context show` separates agent context from session context; `/usage` estimates context-window consumption and an experiment adds a color-coded percentage to the prompt (green under 50%, yellow 50-89%, red 90-100%). Tangent mode creates conversation checkpoints so side questions do not pollute the main thread (single level, discarded on exit). Experimental checkpointing snapshots file changes into a shadow bare Git repo, and restoring a checkpoint unwinds conversation history. Sessions persist per working directory (`q chat --resume`, plus `/save` and `/load`); TODO lists and delegated-task outputs live under `.amazonq/`; the knowledge base retrieves via semantic or BM25 search. (Sources: docs/experiments.md, docs/tangent-mode.md, docs/knowledge-management.md, feed.json at v1.19.7.)

## Ecosystem

No package registry or plugin marketplace. Agents are plain JSON files dropped into `.amazonq/cli-agents/` (workspace; local overrides global with a warning) or `~/.aws/amazonq/cli-agents/` (global), so teams share them through version control; `/agent generate` builds them with model help. Third-party capability arrives via MCP servers, configured per agent (`mcpServers`) or through legacy `~/.aws/amazonq/mcp.json` and workspace `mcp.json`, managed with `q mcp add`. Supplementary technical docs live in the repo's `docs/` folder. After the shutdown, the ecosystem path is closed-source Kiro CLI (kiro.dev/cli), whose issues are tracked in a separate repository. (Sources: docs/agent-file-locations.md, docs/agent-format.md, raw README.md.)

## Governance

Owned by AWS. The README declares dual MIT/Apache-2.0 licensing; GitHub's API reports Apache-2.0 as the primary license. Release cadence: v1.19.0 on 2025-10-24 through v1.19.7 on 2025-11-17, then nothing. December 2025 commits added the Kiro transition notice; the final commit (2026-04-23) only touched the README. The repository is not formally archived and still lists 1,339 open issues, but AWS states it receives critical security fixes only, and official documentation now redirects CLI pages to Kiro. The successor, Kiro CLI, is closed-source and tracks issues in a separate repo. (Sources: raw README.md; gh api releases and commits endpoints.)

## Limitations

Discontinued: the README says it is "no longer being actively maintained and will only receive critical security fixes," and AWS docs state "The Q CLI has become the Kiro CLI" — CLI doc sub-pages now 301/302-redirect to Kiro, so the official user guide is gone. Supplementary repo docs self-describe as "experimental, work in progress... do not represent latest stable builds." Subagents/delegate, knowledge, TODO lists, tangent mode, checkpointing, and context percentage are all /experiment features that "may be changed or removed at any time." Specific gaps: tangent is single-level and discarded on exit; knowledge has no storage limits, no cleanup, irreversible clear, binary files ignored; delegate allows one task per agent and default-agent tasks run trust-all; no OS-level sandbox; 1,339 open issues frozen. (Sources: raw README.md, docs.aws command-line.html, docs/introduction.md, docs/experiments.md, docs/tangent-mode.md.)

## In its own words

> This open source project is no longer being actively maintained and will only receive critical security fixes. Amazon Q Developer CLI is now available as Kiro CLI, a closed-source product.  
> — [https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/README.md](https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/README.md)

> The Q CLI has become the Kiro CLI.  
> — [https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line.html](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line.html)

> Hooks allow you to execute custom commands at specific points during agent lifecycle and tool execution. This enables security validation, logging, formatting, context gathering, and other custom behaviors.  
> — [https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/hooks.md](https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/hooks.md)

> Launch and manage asynchronous background tasks. Enables running Q chat sessions with specific agents in parallel to your main conversation.  
> — [https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/experiments.md](https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/experiments.md)


## Notable

A discontinued open-source terminal CLI quietly shipped a power-user arsenal — preToolUse hooks that can block tool calls, background delegate subagents, and a persistent agent-scoped semantic knowledge base — all behind /experiment toggles, right as AWS handed the product to closed-source Kiro CLI.

## Sources fetched

- https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/command-line.html
- https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-in-IDE-setup.html
- https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/README.md
- https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/SUMMARY.md
- https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/introduction.md
- https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/agent-format.md
- https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/default-agent-behavior.md
- https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/built-in-tools.md
- https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/hooks.md
- https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/experiments.md
- https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/knowledge-management.md
- https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/tangent-mode.md
- https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/todo-lists.md
- https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/agent-file-locations.md
- https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/docs/introspect-tool.md
- https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/crates/chat-cli/src/cli/feed.json
- https://raw.githubusercontent.com/aws/amazon-q-developer-cli/v1.19.7/crates/chat-cli/src/cli/chat/tools/tool_index.json
- https://api.github.com/repos/aws/amazon-q-developer-cli
- https://api.github.com/repos/aws/amazon-q-developer-cli/releases/latest
- https://api.github.com/repos/aws/amazon-q-developer-cli/releases
- https://api.github.com/repos/aws/amazon-q-developer-cli/commits

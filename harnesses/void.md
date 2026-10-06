# Void

- **repo:** voideditor/void
- **version pin:** `v1.3.4` — Fetched this run: https://api.github.com/repos/voideditor/void/releases/latest returns HTTP 404 because every published release in this repo is marked prerelease, so GitHub's 'latest' endpoint has nothing to return. The releases list API (https://api.github.com/repos/voideditor/void/releases, fetched this run) shows exactly three tags: v1.0.0, v1.0.2 and v1.3.4 (published 2025-04-15, html_url https://github.com/voideditor/void/releases/tag/v1.3.4), which is the newest tag in the repo. The v1.3.4 body itself redirects users onward: 'Moving forward, our new releases page is here: https://github.com/voideditor/binaries/releases', whose latest release (https://api.github.com/repos/voideditor/binaries/releases/latest, fetched this run) is tag 1.99.30044 published 2025-06-23. The repository is archived (archived=true, pushed_at 2026-06-02).
- **docs home:** https://raw.githubusercontent.com/voideditor/void/main/README.md

## What it promises

Void billed itself as 'The open source AI code editor' and an 'open source AI IDE' that lets you 'Write code with the best AI tools, use any model, and retain full control over your data' (https://voideditor.com). The README promises: 'Use AI agents on your codebase, checkpoint and visualize changes, and bring any model or host locally. Void sends messages directly to providers without retaining your data.' Feature-wise the release notes advertise 'checkpoints, Agent mode for all OSS models (like GPT 4.1 and R1), auto-updates, SSH and WSL support' in the v1.3.4 beta.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✗ no | The built-in tool registry is exhaustive (read_file, ls_dir, get_dir_tree, search_pathnames_only, search_for_files, search_in_file, read_lint_errors, rewrite_file, edit_file, create_file_or_folder, delete_file_or_folder, run_command, run_persistent_command, open_persistent_terminal, kill_persistent_terminal) and contains no tool that spawns an agent or subtask, and the system prompt restricts the model to a single call ('Only use ONE tool call at a time.'). A repo-wide scan of the fetched source tree found no subagent/spawn code. | [src](https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/toolsServiceTypes.ts) |
| workflow_orchestration | ✗ no | There are no orchestration primitives (no DAGs, teams, swarms or multi-agent scripts); the only mode surface is ChatMode = 'agent' \| 'gather' \| 'normal', and tool execution is explicitly serialized in the agent prompt with 'Only use ONE tool call at a time.' | [src](https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/prompt/prompts.ts) |
| mcp | ✅ yes | Void ships a real MCP client built on @modelcontextprotocol/sdk with stdio, streamable-HTTP and SSE transports (mcpChannel.ts), a dedicated 'MCP' settings tab listing servers with on/off toggles, and a 'mcp.json' config file ('mcpServers') revealed from settings; MCP tools are only offered in agent mode and are gated behind the 'MCP tools' approval type. | [src](https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/electron-main/mcpChannel.ts) |
| hooks_lifecycle | ✗ no | The only 'hooks' in the codebase are internal IPC listener registries (e.g. listHooks/llmMessageHooks in sendLLMMessageService.ts) used to route streaming responses between the browser and electron-main processes; there is no user-configurable hook system for pre/post-tool or session start/stop events, and the fetched docs never mention hooks. | [src](https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/sendLLMMessageService.ts) |
| skills | ✗ no | No skill/prompt-pack registry with named, invocable skills. The closest mechanism is `.voidrules` (workspace file) plus the global `aiInstructions` setting, merged into the system prompt as static 'GUIDELINES' — the same shape as a CONVENTIONS.md rules file, which the atlas grades `no` on this axis, not a progressive-disclosure skill system. | [src](https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/browser/convertToLLMMessageService.ts) |
| memory_persistence | ◐ partial | Persistence exists but is limited to chat state and settings: storageKeys.ts enumerates the entire persisted surface as VOID_SETTINGS_STORAGE_KEY ('void.settingsServiceStorageII') and THREAD_STORAGE_KEY ('void.chatThreadStorageII'), so past conversations survive restarts, but there is no agent-managed long-term memory or knowledge store, and checkpoints/git history live only in the workspace. | [src](https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/storageKeys.ts) |
| sandboxing | ✅ yes | The harness bounds the agent with an approval gate: every file edit, terminal command and MCP tool maps to an approval type ('edits' \| 'terminal' \| 'MCP tools'), tool calls enter a tool_request state awaiting the user (stream state 'awaiting_user') with Approve/Reject in the chat UI, and settings expose autoApprove toggles per approval type. No OS-level sandbox is implemented - the bound is user confirmation, not isolation. | [src](https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/toolsServiceTypes.ts) |
| plan_mode | ✗ no | There is no plan-then-approve mode: ChatMode is exactly 'agent' \| 'gather' \| 'normal', and the only approval step operates per tool call rather than on a proposed plan. A scan of the fetched source for the word 'plan' found no planning mode implementation. | [src](https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/voidSettingsTypes.ts) |
| background_tasks | ◐ partial | Background execution exists but is terminal-level only: the agent can call open_persistent_terminal for an indefinitely running command ('Use this tool when you want to run a terminal command indefinitely, like a dev server (eg `npm run dev`), a background listener, etc.') and run_persistent_command returns after 5 seconds while the command 'continues running in background' (MAX_TERMINAL_BG_COMMAND_TIME = 5). There is no background agent/task queue - an agent turn still blocks on user approval of each tool call. | [src](https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/prompt/prompts.ts) |
| ide_integration | ✅ yes | Void is not an extension for an IDE - it IS the IDE: a full VS Code fork (Electron app) whose AI code lives in src/vs/workbench/contrib/void/, and the codebase guide states plainly 'Void is no longer an extension, so these links are no longer required, but they might be useful if we ever build an extension again.' | [src](https://raw.githubusercontent.com/voideditor/void/main/VOID_CODEBASE_GUIDE.md) |
| model_agnostic | ✅ yes | Yes and it is the core pitch: provider presets include local runtimes (ollama, vLLM, lmStudio) plus Anthropic, OpenAI, Gemini/Vertex, Azure, Bedrock, xAI, Mistral, Groq, DeepSeek, OpenRouter, OpenAI-compatible and LiteLLM, the marketing site says 'Any LLM, Anywhere ... Cut out the middleman and connect directly', and the README states 'Void sends messages directly to providers without retaining your data.' | [src](https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/voidSettingsTypes.ts) |
| plugins | ✅ yes | As a VS Code fork Void hosts the full VS Code extension API, and product.json configures the extension gallery against the Visual Studio Marketplace (serviceUrl https://marketplace.visualstudio.com/_apis/public/gallery, itemUrl https://marketplace.visualstudio.com/items); the plugin surface is VS Code's extension ecosystem, not a bespoke AI plugin API. | [src](https://raw.githubusercontent.com/voideditor/void/main/product.json) |
| session_resume | ✅ yes | Chat threads are persisted to storage under THREAD_STORAGE_KEY with the source comment 'ThreadsState // allThreads is persisted, currentThread is not', and the sidebar renders a past-threads list (PastThreadsList, sorted most-recent-first with a 'show more' expansion and delete) so a previous session can be reopened. | [src](https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/browser/chatThreadService.ts) |
| cost_controls | ✗ no | There is no token or cost tracking, spend display or budget limit: modelCapabilities.ts carries per-model price metadata (cost: { input, cache_read, cache_write, output }) but nothing else in the fetched source reads it, and the only usage-related service is anonymous telemetry with an opt-out ('void.app.optOutAll'). Context fit is managed by a rough CHARS_PER_TOKEN = 4 estimate, not by accounting. | [src](https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/metricsService.ts) |

## Architecture

Void is a VS Code fork: an Electron app with a main process and a browser (workbench) process, and all of its AI code lives under src/vs/workbench/contrib/void/ split into browser/, common/ and electron-main/ (https://raw.githubusercontent.com/voideditor/void/main/VOID_CODEBASE_GUIDE.md). The build pipeline was extended to mount React + Tailwind inside the workbench, which plain VS Code cannot do, and the AI provider layer was written from scratch so it can support autocomplete (FIM) and custom response formats; because the browser process may not import node_modules, LLM calls are implemented in electron-main and reached over an IPC channel (sendLLMMessageChannel.ts), with a separate mcpChannel.ts for MCP and a metrics channel for telemetry. The service layer is a set of decorator-registered singletons: chatThreadService (threads, streaming, checkpoints), editCodeService (streams diffs token-by-token and edits files via VoidModelService, which syncs OS files to text buffers in the background), contextGatheringService, toolsService, terminalToolService, mcpService and voidSettingsService. The agent loop is prompt-driven rather than API-tool-calls: prompts.ts builds an XML tool-call protocol with the available tools per ChatMode ('normal' = no tools, 'gather' = read-only tools, 'agent' = all builtin tools plus MCP tools), and re-parses the model's XML into tool calls.

## Context management

Context management is model-metadata driven: each provider/model entry in modelCapabilities.ts declares contextWindow (in input tokens) and reservedOutputTokenSpace, and convertToLLMMessageService.ts reserves max(contextWindow/2, reservedOutputTokenSpace ?? 4096) for output (the inline comment claims 'reserve at least 1/4 of the token window length' while the code halves it). Message fitting uses a crude CHARS_PER_TOKEN = 4 estimate to decide what fits. Workspace context is injected with hard caps: MAX_DIRSTR_CHARS_TOTAL_BEGINNING = 20,000 characters of directory structure, MAX_DIRSTR_RESULTS_TOTAL_BEGINNING = 100 search results, MAX_FILE_CHARS_PAGE = 500,000 characters per file page, and MAX_PREFIX_SUFFIX_CHARS = 20,000 for autocomplete prefix/suffix. User instructions are merged from the global aiInstructions setting and any .voidrules files found in workspace folders, then pushed into the system message as 'GUIDELINES (from the user's .voidrules file)'.

## Ecosystem

Void is deliberately provider-plural - the settings enumerate local runtimes (ollama, vLLM, lmStudio) plus every major hosted API and OpenAI-compatible endpoints (https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/voidSettingsTypes.ts) - and it consumes VS Code's extension ecosystem through the Marketplace gallery configured in product.json. Tooling extends via MCP servers declared in an mcp.json file ('mcpServers') that Void reveals and hot-toggles from its settings tab (https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/mcpService.ts). The org around the repo includes void-builder (packaging/build pipeline), void-updates-server, void-website, binaries (current release artifacts, latest 1.99.30044) and void-forks, a curated list of community forks that continue the project after deprecation (https://api.github.com/orgs/voideditor/repos). Contribution ran through a public roadmap project, GitHub issues and a Discord, per HOW_TO_CONTRIBUTE.md.

## Governance

Licensing is Apache-2.0 (repo metadata) with source headers 'Copyright 2025 Glass Devtools, Inc.'; the repository is archived and the README says 'Void is deprecated and no longer accepting contributions', so governance is effectively frozen while community forks carry on. As a product it configured itself as privacy-forward: the README claims 'Void sends messages directly to providers without retaining your data', the website pitches 'full privacy', and telemetry is opt-out via IMetricsService.setOptOut with OPT_OUT_KEY 'void.app.optOutAll' (https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/metricsService.ts). Safety governance in-product is the approval layer: file-edit, terminal and MCP tool calls all pass a user confirmation gate unless the corresponding autoApprove toggle is enabled (https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/toolsServiceTypes.ts).

## Limitations

The project is discontinued: archived on GitHub, README declares deprecation, contributions closed (https://raw.githubusercontent.com/voideditor/void/main/README.md). The hosted docs site is gone (https://docs.voideditor.com returns HTTP 404), the repo has no docs/ folder (https://api.github.com/repos/voideditor/void/contents/docs returns 404), and /releases/latest 404s because all releases are prereleases, so every claim must be read out of source. Capability-wise there are no subagents or multi-agent orchestration, no plan-then-approve mode, no lifecycle hooks, no token/cost accounting, and background execution is limited to persistent terminals plus background file writes. The permission model is a confirmation gate, not a sandbox, so once approved the agent's edits run with the user's full privileges. The agent loop also parses XML tool calls out of model text (one tool call at a time), which constrains reliability with weaker models.

## In its own words

> Use AI agents on your codebase, checkpoint and visualize changes, and bring any model or host locally.  
> — [https://raw.githubusercontent.com/voideditor/void/main/README.md](https://raw.githubusercontent.com/voideditor/void/main/README.md)

> Void is deprecated and no longer accepting contributions.  
> — [https://raw.githubusercontent.com/voideditor/void/main/README.md](https://raw.githubusercontent.com/voideditor/void/main/README.md)

> Void is no longer an extension, so these links are no longer required, but they might be useful if we ever build an extension again.  
> — [https://raw.githubusercontent.com/voideditor/void/main/VOID_CODEBASE_GUIDE.md](https://raw.githubusercontent.com/voideditor/void/main/VOID_CODEBASE_GUIDE.md)

> System instructions to include with all AI requests.  
> — [https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/browser/react/src/void-settings-tsx/Settings.tsx](https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/browser/react/src/void-settings-tsx/Settings.tsx)

> This version of Void comes with checkpoints, Agent mode for all OSS models (like GPT 4.1 and R1), auto-updates, SSH and WSL support, and lots of improvements!  
> — [https://github.com/voideditor/void/releases/tag/v1.3.4](https://github.com/voideditor/void/releases/tag/v1.3.4)


## Notable

The advertised docs site is dead (https://docs.voideditor.com returns HTTP 404 while the marketing site https://voideditor.com returns 200) and the repository has no docs/ folder at all - the authoritative documentation is the README plus VOID_CODEBASE_GUIDE.md and HOW_TO_CONTRIBUTE.md at the repo root, and the rest has to be read from source. The project is simultaneously deprecated and archived ('Void is deprecated and no longer accepting contributions') yet the AI machinery is fully implemented in-tree - a complete MCP client, checkpoints, a .voidrules rules system and an approval gate - frozen as a reference implementation. Also non-obvious: all three GitHub releases are prereleases (so /releases/latest 404s), and binaries moved to the separate voideditor/binaries repository (latest 1.99.30044, 2025-06-23).

## Sources fetched

- https://api.github.com/repos/voideditor/void/releases/latest (HTTP 404 - all releases are prereleases)
- https://api.github.com/repos/voideditor/void/releases
- https://api.github.com/repos/voideditor/void/releases/tags/v1.3.4
- https://github.com/voideditor/void/releases/tag/v1.3.4
- https://api.github.com/repos/voideditor/void
- https://api.github.com/repos/voideditor/void/contents/docs (HTTP 404 - no docs/ folder)
- https://api.github.com/repos/voideditor/void/contents
- https://api.github.com/repos/voideditor/void/contents/extensions
- https://api.github.com/repos/voideditor/void/contents/src/vs/workbench/contrib/void
- https://api.github.com/repos/voideditor/void/contents/src/vs/workbench/contrib/void/browser
- https://api.github.com/repos/voideditor/void/contents/src/vs/workbench/contrib/void/common
- https://api.github.com/repos/voideditor/void/contents/src/vs/workbench/contrib/void/electron-main
- https://api.github.com/repos/voideditor/void/contents/src/vs/workbench/contrib/void/browser/react/src
- https://api.github.com/repos/voideditor/void/contents/src/vs/workbench/contrib/void/browser/react/src/sidebar-tsx
- https://api.github.com/repos/voideditor/void/contents/src/vs/workbench/contrib/void/browser/react/src/void-settings-tsx
- https://api.github.com/repos/voideditor/void/git/trees/main?recursive=1
- https://api.github.com/orgs/voideditor/repos
- https://api.github.com/repos/voideditor/void-website/contents
- https://api.github.com/repos/voideditor/binaries/releases/latest
- https://raw.githubusercontent.com/voideditor/void/main/README.md
- https://raw.githubusercontent.com/voideditor/void/main/VOID_CODEBASE_GUIDE.md
- https://raw.githubusercontent.com/voideditor/void/main/HOW_TO_CONTRIBUTE.md
- https://raw.githubusercontent.com/voideditor/void/main/.voidrules
- https://raw.githubusercontent.com/voideditor/void/main/product.json
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/toolsServiceTypes.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/mcpServiceTypes.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/mcpService.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/chatThreadServiceTypes.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/voidSettingsTypes.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/voidSettingsService.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/prompt/prompts.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/sendLLMMessageTypes.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/sendLLMMessageService.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/metricsService.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/modelCapabilities.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/voidModelService.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/storageKeys.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/common/editCodeServiceTypes.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/electron-main/mcpChannel.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/browser/chatThreadService.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/browser/toolsService.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/browser/terminalToolService.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/browser/contextGatheringService.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/browser/convertToLLMMessageService.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/browser/voidSettingsPane.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/browser/void.contribution.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/browser/voidCommandBarService.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/browser/quickEditActions.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/browser/sidebarActions.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/browser/metricsPollService.ts
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/browser/react/src/sidebar-tsx/SidebarChat.tsx
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/browser/react/src/sidebar-tsx/SidebarThreadSelector.tsx
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/browser/react/src/void-settings-tsx/Settings.tsx
- https://raw.githubusercontent.com/voideditor/void/main/src/vs/workbench/contrib/void/ (bulk fetch: all 125 source files under this path that appear in the repo tree were downloaded from raw.githubusercontent.com/voideditor/void/main/ and grepped locally for subagent, plan, hook, cost, token, checkpoint and rules signals)
- https://voideditor.com (HTTP 200)
- https://docs.voideditor.com (HTTP 404)

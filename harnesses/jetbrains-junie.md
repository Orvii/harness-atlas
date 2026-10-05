# JetBrains Junie

- **repo:** JetBrains (closed source; product docs at jetbrains.com/help/junie and junie.jetbrains.com/docs; companion extension marketplace repo github.com/JetBrains/junie-extensions)
- **version pin:** `26.9.22 (3419.26)` — Vendor changelog: https://junie.jetbrains.com/whats-new shows "Release 26.9.22 (3419.26)" dated Oct 1, 2026 (Junie Lite) as the latest CLI release. Closed source, no public product repo — vendor docs are the authoritative source.
- **docs home:** https://www.jetbrains.com/help/junie/ (Junie CLI docs mirror: https://junie.jetbrains.com/docs/)

## What it promises

"The most cost efficient coding agent — the coding agent that works with any model you choose," with "Plan on a powerful model, implement on a fast one. Same quality, fraction of the cost." The homepage frames control as the companion promise: "Human in the Loop — Review, approve, and steer key actions as Junie works, so you stay in control," backed by Remote Control ("Start a migration from your laptop. Check progress from your phone.").

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | User-defined Markdown+YAML subagent files in .junie/agents/ or .agents/ (importable from .cursor/agents, .claude/agents, .codex/agents); auto-delegation with per-subagent model, tool restrictions, and permission mode. Subagent model-selection mode setting is currently EAP, and custom subagents cannot be invoked manually. | [src](https://junie.jetbrains.com/docs/junie-cli-subagents.html) |
| workflow_orchestration | ◐ partial | Primitives exist: automatic subagent delegation, parallel live sessions, git worktrees, recurring tasks (/loops), orchestrated /goal mode, headless/GitHub Action/GitLab CI runs. No DAG/team/swarm scripting layer is documented. | [src](https://junie.jetbrains.com/docs/slash-commands.html) |
| mcp | ✅ yes | Project (.junie/mcp/mcp.json) and user (~/.junie/mcp/mcp.json) scopes, /mcp management screen with installation assistant pulling from the official MCP registry; read-only in ACP clients. | [src](https://junie.jetbrains.com/docs/junie-cli-mcp-configuration.html) |
| hooks_lifecycle | ✅ yes | Events: SessionStart, UserPromptSubmit, PreToolUse, Stop, StopFailure, PermissionRequest, SessionEnd; Stop hooks can block/retry (exit code 2 or JSON decision). Gates: command-type hooks only, no parallel execution, UserPromptSubmit and all events fire only from TUI/batch hosts (not ACP/server), project-local hooks ignored unless passed via --config-location. | [src](https://junie.jetbrains.com/docs/junie-cli-hooks.html) |
| skills | ✅ yes | Loaded from .junie/skills/ (project) and ~/.junie/skills/ (user), plus .agents/skills/, extension-bundled skills, and custom --skill-location paths; progressive disclosure of name/description; imports suggested from .cursor/skills/, .claude/skills/, .codex/skills/. | [src](https://junie.jetbrains.com/docs/agent-skills.html) |
| memory_persistence | ✅ yes | Project .junie/AGENTS.md plus global ~/.junie/AGENTS.md with project precedence; homepage claims 'It remembers across sessions'. Persistence is file-based; no automatic learned memory system is documented. | [src](https://junie.jetbrains.com/docs/guidelines-and-memory.html) |
| sandboxing | ✅ yes | Permission modes (brave Off/Auto/On) plus ~/.junie/allowlist.json rules for fileEditing, executables, mcpTools, readOutsideProject, readSecretFile; PermissionRequest hook can auto-allow/deny. OS-level /sandbox is macOS/Linux only — 'srt' ships inside nightly/experimental macOS builds, Linux must provide it on PATH. | [src](https://junie.jetbrains.com/docs/action-allowlist-junie-cli.html) |
| plan_mode | ✅ yes | Shift+Tab cycle or /plan, --plan flag; plan is a living document updated when requirements change, and the homepage advertises plans stored in .junie/plans (editable, committable) with plan/implement allowed on different models. | [src](https://junie.jetbrains.com/docs/junie-cli-plan-mode.html) |
| background_tasks | ✅ yes | /new keeps parallel live sessions running; /remote tunnels the running session to a web UI for async monitoring; /loops schedules recurring tasks; cold sessions resume from /history. | [src](https://junie.jetbrains.com/docs/junie-cli-worktrees.html) |
| ide_integration | ✅ yes | Runs inside JetBrains IDEs (AI Chat / Junie tool window; IntelliJ, PyCharm, PhpStorm, CLion, Rider and more via the Junie plugin), with IDE awareness features (symbol-aware search, inspections, test workflows) for the CLI. No VS Code extension is documented; ACP mode serves other editors. | [src](https://www.jetbrains.com/help/ai-assistant/junie-agent.html) |
| model_agnostic | ✅ yes | BYOK for OpenAI, Anthropic, Google, xAI, OpenRouter, GitHub Copilot; OpenAI/Anthropic/Google API formats plus enterprise proxies; Junie Local local inference (macOS Apple Silicon). JetBrains AI paths provide Claude, GPT-6, Gemini, and Grok models. | [src](https://junie.jetbrains.com/docs/custom-llm-models.html) |
| plugins | ✅ yes | A single extension bundles skills, MCP servers, subagents, custom slash commands, guidelines, and hooks; distributed via marketplaces hosted as git repos, local directories, or HTTP marketplace.json — native .junie-extension/ or Claude plugin .claude-plugin/ format. Official JetBrains marketplace pre-registered at github.com/JetBrains/junie-extensions. | [src](https://junie.jetbrains.com/docs/junie-cli-extensions.html) |
| session_resume | ✅ yes | Stored sessions keep full context including LLM usage and prompt/response history; /link exposes junie://sessions/<id> links that the CLI can reopen; code review sessions are resumable for follow-ups; /branch forks a conversation into a new session. | [src](https://junie.jetbrains.com/docs/slash-commands.html) |
| cost_controls | ✅ yes | Live session cost in the toolbar (release 26.9.7); billing_error taxonomy includes a cost-cap-hit state; homepage markets plan/implement on different models for cost control and Junie Lite as a free tier. | [src](https://junie.jetbrains.com/docs/slash-commands.html) |

## Architecture

Junie is a local-first agent loop with four surfaces: a JetBrains IDE plugin inside AI Chat, an interactive terminal TUI (Junie CLI), headless batch runs for CI (headless mode, GitHub Action, GitLab CI/CD), and an ACP server for third-party editors. The CLI process runs on the developer's machine; Remote mode tunnels the running session to a web UI, while CI runs execute on the customer's own runners ("The action executes entirely on your GitHub runners"). Tool execution covers file edits, terminal commands, MCP servers, subagents, and IDE-backed operations such as debugger control and inspections. Sensitive actions pass through brave mode, allowlist.json rules, or a PermissionRequest hook; an optional OS-level sandbox constrains writes and network sockets. Extensions bundle skills, MCP configs, subagents, commands, guidelines, and hooks.

## Context management

/compress (alias /compact) collapses conversation context before the next task, with an explicit warning that information may be discarded. Sessions persist full context — prompts, responses, and LLM usage data — and resume through /history or junie://sessions/&lt;id&gt; links, while /branch forks a conversation into a new session. Skills use progressive disclosure: only names and descriptions enter context until a skill proves relevant. Subagents run in their own isolated context, keeping intermediate work out of the main conversation. Guidelines from AGENTS.md are injected into every task. Plan mode keeps a living design document (stored in .junie/plans per the homepage) instead of holding plan state only in the window.

## Ecosystem

Junie CLI extensions — bundles of skills, MCP servers, subagents, slash commands, guidelines, and hooks — install from marketplaces hosted as git repositories, local directories, or HTTPS URLs pointing at marketplace.json, in either the native .junie-extension/ format or the Claude plugin format (.claude-plugin/marketplace.json), so any Claude-compatible marketplace connects as-is. JetBrains pre-registers its own marketplace at github.com/JetBrains/junie-extensions (Java, Kotlin, Android, Spring Boot, SQL, Redis extensions). Skills, subagents, and guidelines are importable from .cursor/, .claude/, and .codex/ conventions via /import. The IDE plugin distributes through JetBrains Marketplace, and MCP servers come from config files or the official MCP registry via the installation assistant.

## Governance

Closed source. Junie is a JetBrains product (JetBrains s.r.o.), and the CLI is explicitly "currently in an Early Access Program (EAP)"; no public product repository exists — vendor documentation is the only specification, with an extensions repo (github.com/JetBrains/junie-extensions) as the lone public code artifact. Commercial model: JetBrains AI subscriptions (AI Free/Junie Lite, AI Pro, AI Ultimate credit tiers, governed by jb.gg/ai-tos) or BYOK billed at provider rates; the JUNIE_API_KEY path uses usage-based billing. Cadence is rapid and documented — releases 26.9.7, 26.9.14, 26.9.22 (three builds dated Sep 22–Oct 1, 2026 alone), plus an EAP channel for pre-release features.

## Limitations

The CLI is EAP, and several capabilities sit behind gates: subagent model-selection settings require the Early Access build; the OS-level /sandbox is macOS/Linux only, with "srt" shipping inside nightly and experimental macOS builds while Linux must supply it on PATH. Remote mode requires a JetBrains Account or JUNIE_API_KEY — BYOK alone is insufficient — and is unavailable under JetBrains AI Enterprise sign-in. Local code review requires a git repository; Debug mode requires a live debugger session connected to a JetBrains IDE. Hooks fire only from TUI and batch hosts (UserPromptSubmit is TUI-only), only command-type hooks run, and project-local hooks are ignored unless explicitly passed via --config-location. Non-interactive runs load project configuration trusted by design. Junie Local needs macOS 26+, Apple Silicon M5+, and 64 GB RAM; /goal is unavailable on the free Junie Lite model.

## In its own words

> Junie CLI is currently in an Early Access Program (EAP).  
> — [https://junie.jetbrains.com/docs/junie-headless.html](https://junie.jetbrains.com/docs/junie-headless.html)

> This means you can connect any Claude-compatible plugin marketplace to Junie CLI in addition to Junie's native marketplaces.  
> — [https://junie.jetbrains.com/docs/junie-cli-extensions.html](https://junie.jetbrains.com/docs/junie-cli-extensions.html)

> The subagent then works independently in its own context and returns the result to the main agent.  
> — [https://junie.jetbrains.com/docs/junie-cli-subagents.html](https://junie.jetbrains.com/docs/junie-cli-subagents.html)

> The coding agent that works with any model you choose.  
> — [https://junie.jetbrains.com/](https://junie.jetbrains.com/)


## Notable

JetBrains ships deliberate Claude-ecosystem parity: Junie CLI consumes Claude plugin marketplaces (.claude-plugin/marketplace.json), imports .claude/skills and .claude/agents, expands ${CLAUDE_PLUGIN_ROOT} in hook scripts, and even labels a Stop-hook behavior "Claude parity" in its docs.

## Sources fetched

- https://www.jetbrains.com/help/junie/
- https://www.jetbrains.com/help/ai-assistant/junie-agent.html
- https://junie.jetbrains.com/
- https://junie.jetbrains.com/whats-new
- https://junie.jetbrains.com/docs/get-started-with-junie.html
- https://junie.jetbrains.com/docs/junie-cli.html
- https://junie.jetbrains.com/docs/junie-cli-subagents.html
- https://junie.jetbrains.com/docs/junie-cli-plan-mode.html
- https://junie.jetbrains.com/docs/junie-cli-debug-mode.html
- https://junie.jetbrains.com/docs/junie-cli-remote-mode.html
- https://junie.jetbrains.com/docs/junie-cli-worktrees.html
- https://junie.jetbrains.com/docs/junie-review-agent.html
- https://junie.jetbrains.com/docs/junie-cli-hooks.html
- https://junie.jetbrains.com/docs/junie-cli-mcp-configuration.html
- https://junie.jetbrains.com/docs/agent-skills.html
- https://junie.jetbrains.com/docs/junie-cli-extensions.html
- https://junie.jetbrains.com/docs/guidelines-and-memory.html
- https://junie.jetbrains.com/docs/action-allowlist-junie-cli.html
- https://junie.jetbrains.com/docs/custom-llm-models.html
- https://junie.jetbrains.com/docs/junie-cli-model-selection.html
- https://junie.jetbrains.com/docs/junie-local.html
- https://junie.jetbrains.com/docs/slash-commands.html
- https://junie.jetbrains.com/docs/custom-slash-commands.html
- https://junie.jetbrains.com/docs/junie-headless.html
- https://junie.jetbrains.com/docs/junie-on-github.html
- https://junie.jetbrains.com/docs/junie-cli-acp.html
- https://junie.jetbrains.com/docs/junie-ide-plugin.html
- https://junie.jetbrains.com/docs/junie-cli-jetbrains-ide-integration.html
- https://plugins.jetbrains.com/plugin/26104-junie-the-ai-coding-agent-by-jetbrains

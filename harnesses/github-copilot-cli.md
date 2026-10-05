# GitHub Copilot CLI

- **repo:** github/copilot-cli
- **version pin:** `v1.0.91` — gh api repos/github/copilot-cli/releases/latest → tag v1.0.91 (published 2026-10-01; prerelease builds v1.0.92-0..4 exist on top). npm registry: @github/copilot@1.0.91, bin copilot → npm-loader.js.
- **docs home:** https://docs.github.com/en/copilot/how-tos/copilot-cli

## What it promises

"The power of GitHub Copilot, now in your terminal" — powered by "the same agentic harness as GitHub's Copilot coding agent," with GitHub integration (repos, issues, PRs) authenticated through your existing account. Marketing also promises "Full control: Preview every action before execution — nothing happens without your explicit approval."

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | Built-in agents: explore, task, general-purpose, code-review, research, rubber-duck, security-review. Subagents get a separate context window, can run in parallel, and can nest; /tasks shows an indented subagent tree you can teleport into and steer. Custom agent profiles in .github/agents/NAME.md (repo/org/enterprise scopes). | [src](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/invoke-custom-agents) |
| workflow_orchestration | ✅ yes | /fleet breaks a plan into independent subtasks run in parallel by subagents; headless --fleet flag for non-interactive runs. Orchestration is LLM-driven (dependency-aware), not a user-authored DAG/script DSL; no teams/swarm configuration object documented. | [src](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/fleet) |
| mcp | ✅ yes | Add servers via /mcp add, copilot mcp add, config file, or per-repo config; experimental /mcp search installs from the GitHub MCP Registry (github.com/mcp); org registry URL and allowlist policies apply. | [src](https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers) |
| hooks_lifecycle | ✅ yes | Events include sessionStart, sessionEnd, userPromptSubmitted, preToolUse (can approve/deny tool calls), postToolUse, agentStop, subagentStop, errorOccurred; hooks reference adds preCompact, permissionRequest, subagentStart. JSON files at .github/hooks/*.json plus personal ~/.copilot/hooks/*.json. | [src](https://docs.github.com/en/copilot/concepts/agents/hooks) |
| skills | ✅ yes | Project skills in .github/skills, .claude/skills, or .agents/skills; personal skills in ~/.copilot/skills or ~/.agents/skills. /skills dashboard; /chronicle skills subcommands draft repo skill proposals from observed usage. | [src](https://docs.github.com/en/copilot/concepts/agents/about-agent-skills) |
| memory_persistence | ✅ yes | Agent memory tool (store/vote/read) persists facts; --enable-memory flag (disabled by default in prompt mode). Sessions persist with saved context and resume; /chronicle provides session-history insights; sidebar lists resumable sessions. | [src](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference) |
| sandboxing | ✅ yes | /sandbox enable (experimental; OS-level on macOS Seatbelt, Linux bubblewrap, Windows 11 base-container tier). Permission modes: per-tool prompts, --allow-tool/--deny-tool, --allow-all-tools, --allow-all, --yolo, persisted permissions-config.json. copilot --cloud runs the whole session in a GitHub-hosted ephemeral sandbox. | [src](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/overview) |
| plan_mode | ✅ yes | Shift+Tab cycles plan mode; /plan command; --plan CLI flag; best-practices page: plan 'waits for your approval before implementing'; plan-then-autopilot chaining via --plan --mode autopilot; plan mode is hard-blocked from workspace-mutating tools at dispatch level per changelog. | [src](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/overview) |
| background_tasks | ✅ yes | Ctrl+X then b promotes a running task/shell to background; 'n' spawns a new background session; Esc twice stops background agents; /tasks manages task/subagent status; /delegate offloads to the cloud agent which 'works in the background' opening a draft PR; /every and /after schedule prompts (experimental). | [src](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference) |
| ide_integration | ◐ partial | VS Code integration is documented (CLI sessions appear in the sessions list; 'Resume in Terminal' action; /delegate from a session). No JetBrains integration for Copilot CLI is documented; JetBrains appears only as a surface for shared skills. | [src](https://code.visualstudio.com/docs/copilot/agents/copilot-cli) |
| model_agnostic | ✅ yes | /model picker groups by recommended/vendor/category, offers Auto selection, per-model long-context variants, reasoning effort, session/global/repo/local scoping, and vendor data-retention warnings. Multi-vendor: Anthropic (Claude) and OpenAI (GPT) models at minimum. | [src](https://github.com/github/copilot-cli) |
| plugins | ✅ yes | copilot plugin install from marketplace spec, GitHub repo, git URL, or local path; /plugin dashboard with Installed/Online/Marketplace views; bundled default marketplaces include copilot-plugins, awesome-copilot, claude-code-plugins. | [src](https://docs.github.com/en/copilot/concepts/agents/about-plugins) |
| session_resume | ✅ yes | copilot --continue resumes the most recent local session; /continue and --resume with session ID; a Copilot cloud agent session can be brought down to the local environment; resumable sessions listed in sidebar (sidebar.showResumableSessions). | [src](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/overview) |
| cost_controls | ✅ yes | Public preview; soft limit (in-flight response finishes), minimum 30 AI credits; set interactively via /limits set max-ai-credits or --max-ai-credits=NUMBER programmatically; /context shows token usage visualization; copilot help billing topic exists. | [src](https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/set-session-limit) |

## Architecture

Terminal-native TUI: running `copilot` opens an interactive session; no IDE, daemon, or server is required by default. GitHub distributes prebuilt binaries for macOS, Linux (glibc and musl) and Windows on x64/arm64 as tarballs and .msi/.zip, plus an npm wrapper package (@github/copilot, bin npm-loader.js), so Node.js ships alongside. Tools execute locally — shell commands, file edits, URL fetches, GitHub API calls through the built-in GitHub MCP server — each gated by per-tool permission prompts, with read-only operations auto-allowed. Extensions are separate Node.js processes that connect back to the session via the bundled SDK. Optional `copilot --cloud` runs the whole session in GitHub-hosted ephemeral Linux sandboxes.

## Context management

Automatic compaction is the centerpiece: near 80% of the context window Copilot summarizes history in the background, keeping ~20% headroom, and briefly pauses near 95% until compaction finishes. `/compact [focus instructions]` triggers it manually; the structured summary replaces old history while preserving goals, key details, files, and next steps, and a checkpoint is created at compaction. `/context` visualizes token usage. Custom instruction files (.github/copilot-instructions.md, .github/instructions/**/*.instructions.md, AGENTS.md) auto-load into prompts, `@path` attaches files, and /clear or /new reset the conversation. Docs market this as "infinite sessions."

## Ecosystem

Three extension channels. Plugins are "installable packages that extend Copilot with reusable agents, skills, hooks, and integrations," installed via `copilot plugin install` from a marketplace spec, GitHub repo, git URL, or local path; a `/plugin` dashboard has Installed, Online, and Marketplace views; bundled default marketplaces include copilot-plugins, awesome-copilot, and claude-code-plugins. MCP servers come from the built-in GitHub MCP server, `/mcp add`, config files, per-repo config, or the experimental GitHub MCP Registry (github.com/mcp) search; org registry/allowlist policies apply. CLI extensions live in .github/extensions or ~/.copilot/extensions. No plugin counts are published.

## Governance

GitHub (Microsoft) owns the project. github/copilot-cli is public but distribution-only — README.md, LICENSE.md, changelog.md, install.sh and .github; the CLI source is not published. The custom "GitHub Copilot CLI License" (SPDX NOASSERTION) grants install/run rights and permits redistributing only unmodified copies as part of a larger application. Contribution is feedback-driven: issues and discussions (about 11.2k stars, 2.2k open issues), no documented PR flow. Release cadence is aggressive — roughly two to three tagged builds per day across 2026-09-21 to 2026-10-04 (v1.0.88 through v1.0.92-4); latest release per API: v1.0.91.

## Limitations

Documented gaps: CLI extensions are experimental and JavaScript-only (TypeScript unsupported); `/every` and `/after` scheduling works only in experimental mode; local sandboxing is experimental — macOS Seatbelt (15+ recommended), Linux bubblewrap, Windows 11 base-container tier, no Windows proxy support, and Linux cannot control local network access for spawned processes. AI-credit session limits are public preview and soft (minimum 30 credits). Memory writes are root-agent-only (subagents get read-only read_memories), and --enable-memory is off by default in prompt mode. Classic PATs are unsupported for auth; an active Copilot subscription and org policy enablement are required. JetBrains CLI integration is undocumented.

## In its own words

> GitHub Copilot CLI brings AI-powered coding assistance directly to your command line, enabling you to build, debug, and understand code through natural language conversations. Powered by the same agentic harness as GitHub's Copilot coding agent, it provides intelligent assistance while staying deeply integrated with your GitHub workflow.  
> — [https://github.com/github/copilot-cli](https://github.com/github/copilot-cli)

> Full control: Preview every action before execution — nothing happens without your explicit approval.  
> — [https://github.com/github/copilot-cli](https://github.com/github/copilot-cli)

> If it decides to assign some or all of the subtasks to subagents, it will act as orchestrator, managing the workflow and dependencies between the subtasks.  
> — [https://docs.github.com/en/copilot/concepts/agents/copilot-cli/fleet](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/fleet)

> Compaction is the process that allows GitHub Copilot CLI to support long-running sessions without hitting the limits of the context window.  
> — [https://docs.github.com/en/copilot/concepts/agents/copilot-cli/context-management](https://docs.github.com/en/copilot/concepts/agents/copilot-cli/context-management)


## Notable

/fleet turns the main agent into a dependency-aware orchestrator that parallelizes subtasks across subagents, and the /tasks dialog exposes a live, nestable subagent tree you can "teleport" into and steer mid-run — supervision depth unusual for a chat-style CLI.

## Sources fetched

- https://docs.github.com/en/copilot/how-tos/copilot-cli
- https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/overview
- https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/allowing-tools
- https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/set-session-limit
- https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/invoke-custom-agents
- https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/delegate-tasks-to-cca
- https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/add-mcp-servers
- https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/change-settings
- https://docs.github.com/en/copilot/how-tos/copilot-cli/cli-best-practices
- https://docs.github.com/en/copilot/how-tos/copilot-cli/automate-copilot-cli/run-cli-programmatically
- https://docs.github.com/en/copilot/how-tos/copilot-cli/automate-copilot-cli/schedule-prompts
- https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference
- https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-custom-agents
- https://docs.github.com/en/copilot/concepts/agents/copilot-cli/about-cli-extensions
- https://docs.github.com/en/copilot/concepts/agents/copilot-cli/comparing-cli-features
- https://docs.github.com/en/copilot/concepts/agents/copilot-cli/fleet
- https://docs.github.com/en/copilot/concepts/agents/copilot-cli/autopilot
- https://docs.github.com/en/copilot/concepts/agents/copilot-cli/context-management
- https://docs.github.com/en/copilot/concepts/agents/hooks
- https://docs.github.com/en/copilot/concepts/agents/about-agent-skills
- https://docs.github.com/en/copilot/concepts/agents/about-plugins
- https://docs.github.com/en/copilot/concepts/about-cloud-and-local-sandboxes
- https://code.visualstudio.com/docs/copilot/agents/copilot-cli
- https://github.com/github/copilot-cli
- https://registry.npmjs.org/@github/copilot/latest

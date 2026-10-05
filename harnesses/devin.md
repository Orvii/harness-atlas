# Devin

- **repo:** Cognition/Devin — closed source, cloud autonomous agent; no public repository
- **version pin:** `Devin CLI stable v3000.11.3 (September 22, 2026); cloud release notes current through September 30, 2026` — Closed-source SaaS: no public repo or release tags exist, so the pin comes from the vendor's official docs. Latest Devin CLI stable changelog entry is v3000.11.3, dated September 22, 2026 (https://docs.devin.ai/cli/changelog/stable), and the cloud product release-notes feed's newest entry is September 30, 2026 (https://docs.devin.ai/release-notes/overview). A legacy beta-changelog path returns 404.
- **docs home:** https://docs.devin.ai

## What it promises

Cognition pitches Devin as "the AI software engineer, built to help ambitious engineering teams crush their backlogs," an autonomous teammate that writes, runs, and tests code. The stated bar: Devin "can handle most tasks, excluding extremely difficult tasks" — "if you can do it in three hours, Devin can most likely do it."

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | Devin CLI/Desktop local agent: foreground and background modes, custom subagent profiles (agents/<name>.md shippable in plugins), parent summarizes results. Cloud sessions instead delegate to managed Devins — child sessions each in an isolated VM. | [src](https://docs.devin.ai/cli/subagents) |
| workflow_orchestration | ✅ yes | Fan-out + staged pipeline primitives, recorded/resumable runs, output piped between stages; managed Devins for manual delegation; v3 REST API, Terraform provider, and automations for external orchestration. | [src](https://docs.devin.ai/work-with-devin/dynamic-workflows) |
| mcp | ✅ yes | Custom MCP servers plus plugin marketplace and legacy MCP marketplace; installed at personal, organization, or enterprise scope; OAuth connection flows. | [src](https://docs.devin.ai/work-with-devin/mcp) |
| hooks_lifecycle | ✅ yes | Events: PreToolUse, PostToolUse, PermissionRequest, UserPromptSubmit, Stop, PostCompaction, SessionStart, SessionEnd; JSON config in .devin/ (also reads .claude/ dirs); hooks can be bundled into plugins, which cloud sessions can install. | [src](https://docs.devin.ai/cli/extensibility/hooks/overview) |
| skills | ✅ yes | Open Agent Skills standard spec; .agents/skills/<name>/SKILL.md auto-discovered across connected repos; plugin-distributed skills exposed as /<plugin>:<skill> commands; skills can run as subagents with their own permissions and model. | [src](https://docs.devin.ai/product-guides/skills) |
| memory_persistence | ◐ partial | Cloud Knowledge gave trigger-based auto-recall across sessions, but it is deprecated — 'will be removed in a future update' — with automatic migration to Skills in Plugins. The Devin Local agent explicitly 'does not persist memories between sessions.' | [src](https://docs.devin.ai/product-guides/knowledge) |
| sandboxing | ✅ yes | Fail-closed (refuses to start if sandbox cannot resolve). Permission modes: Normal, Accept Edits, Smart (model-judged), Bypass, Autonomous. Windows unsupported; Linux needs bubblewrap + socat; enterprise can enforce sandbox, but team settings and permission rules are the primary control surface. | [src](https://docs.devin.ai/cli/sandbox) |
| plan_mode | ✅ yes | Plan mode toggled by /plan or Alt+P, plans written to a file; cloud sessions offer Ask mode (explore + plan, no code changes, generates context-rich prompts) before Agent mode executes; sandbox sessions keep Plan mode available. | [src](https://docs.devin.ai/cli/essential-commands) |
| background_tasks | ✅ yes | Background subagents; shell commands exceeding the wait window move to background with an ID; cloud sessions are asynchronous by nature — they sleep after 30 minutes idle and wake on message; schedules and event-driven automations run sessions unattended. | [src](https://docs.devin.ai/cli/subagents) |
| ide_integration | ✅ yes | Devin Desktop is itself a Cognition-built IDE (Windsurf successor) importing VS Code/Cursor settings; JetBrains via ACP (also Zed and Xcode); legacy Windsurf plugins cover VS Code, Visual Studio, Vim, NeoVim, Emacs, Sublime Text, Eclipse — in maintenance mode as Cascade is deprecated. | [src](https://docs.devin.ai/cli/acp/jetbrains) |
| model_agnostic | ✅ yes | Models from Anthropic, OpenAI, Google, and Cognition plus open-source DeepSeek, Kimi, GLM; short names resolve to latest; Adaptive router and Fusion lead+sidekick pairing; model switching mid-session; ChatGPT-plan token sharing bills GPT usage externally. | [src](https://docs.devin.ai/cli/models) |
| plugins | ✅ yes | In-app marketplace and Customize page; personal/organization/enterprise scopes shared across cloud, CLI, and Desktop; Cognition publishes plugin-template and team-marketplace-template repos; enterprise admins set allow/forbid plugin policies. | [src](https://docs.devin.ai/product-guides/plugins) |
| session_resume | ✅ yes | devin -c/--continue, --resume, -r <session-id>, /resume picker; cloud sessions resume by URL (devin --cloud -r); sleeping cloud sessions wake when messaged; /pickup and /handoff transfer PR branches between cloud and local. | [src](https://docs.devin.ai/cli/essential-commands) |
| cost_controls | ✅ yes | ACU metering (enterprise) or plan quota + on-demand credits; sleep pauses usage after 30 minutes idle; per-user monthly ACU limits via usage tiers (beta) and independent organization-level ACU limits; Devin Review usage exempt from per-user limits; usage dashboard in-app. | [src](https://docs.devin.ai/admin/billing/usage) |

## Architecture

Devin spans cloud and local surfaces. Cloud sessions run server-side — "Devin's agent loop (inference and planning) continues to run in Devin's cloud" — each executing in an isolated VM (Ubuntu, Windows, or macOS) with a terminal, editor, browser, and computer use inside it. Outposts keep execution on customer infrastructure: workers claim queued sessions and run every command, edit, and repository operation locally over an outbound-only connection while planning stays in Devin's cloud. Local surfaces — Devin CLI and the Devin Local agent in Devin Desktop — run the agent harness on the user's machine and hand off sessions to the cloud. Slack, Teams, the v3 REST API, and a Terraform provider drive the same cloud session model.

## Context management

Context is assembled from committed skills, rules, and AGENTS.md — "Devin automatically includes up to 16 KiB (16,384 bytes) from the beginning of each AGENTS.md file in its context" — plus MCP tools and repository indexing. Sessions expose a Context tab listing reports, images, and files, and long conversations are summarized automatically: the CLI's agent.compaction_threshold_tokens setting triggers compaction earlier than the context-window-based default, and a PostCompaction hook fires after compaction completes. Ask Devin and DeepWiki produce "context-rich prompts" for agent sessions. Knowledge items were retrieved automatically by trigger description before Cognition began migrating that feature into skills.

## Ecosystem

Distribution runs through plugins: "A plugin bundles skills — and optionally rules, hooks, MCP servers, and subagents — so it can be installed and reused as a unit," installed at personal, organization, or enterprise scope and shared across cloud, CLI, and Desktop. Cognition ships plugin-template and team-marketplace-template repositories plus an in-app marketplace; skills follow the open Agent Skills standard, so the same files work in other coding tools. MCP servers (stdio, SSE, HTTP) plug in external tools, while the v3 REST API, Terraform provider, automations, and Slack/GitHub/Linear/Teams integrations carry workflows into the platform.

## Governance

Devin is closed source — a proprietary SaaS from Cognition with no public repository, so every capability claim here rests on vendor documentation. Cognition states it has been "SOC 2 Type II certified since September 2024," runs production in AWS, and maintains a public Trust Center. The documentation also records corporate consolidation: "legacy Windsurf" enterprise authentication still works for Devin CLI, the Windsurf JetBrains plugin is in maintenance mode with Cascade deprecated, and Devin Desktop has replaced the Windsurf editor. Enterprise governance covers SSO, SCIM, RBAC, service users, audit logs, usage policies, and plugin allow/forbid controls.

## Limitations

Documented gaps: OS-level sandboxing is unavailable on Windows — sessions hard-fail when sandbox is required rather than silently run unsandboxed — and needs bubblewrap and socat on Linux. The Devin Local agent persists no memories between sessions and lacks workflows, app deploys, and Arena mode versus Cascade. Smart permission mode is a gradual rollout, per-user ACU limits are in beta, and Dynamic Workflows stay off in enterprise organizations until an admin enables them. ChatGPT-plan billing excludes fast and priority model variants; macOS session pricing is promotional. The docs themselves caution, "documentation may be out of date."

## In its own words

> Devin is an autonomous AI software engineer that can write, run and test code. Devin can handle most tasks, excluding extremely difficult tasks. As a rule of thumb, if you can do it in three hours, Devin can most likely do it.  
> — [https://docs.devin.ai/get-started/devin-intro](https://docs.devin.ai/get-started/devin-intro)

> Devin's agent loop (inference and planning) continues to run in Devin's cloud, while all command execution, file edits, and repository access happen on machines you operate.  
> — [https://docs.devin.ai/cloud/outposts/overview](https://docs.devin.ai/cloud/outposts/overview)

> Subagents let the main agent spawn independent workers to handle subtasks. A subagent shares tools and codebase context with the parent, but operates in its own conversation chain -- it does not inherit the parent's conversation history.  
> — [https://docs.devin.ai/cli/subagents](https://docs.devin.ai/cli/subagents)

> Knowledge is a collection of tips, advice, and instructions that Devin can reference in all sessions. You can continually add to Devin's bank of Knowledge over time, and Devin will automatically recall relevant Knowledge as necessary.  
> — [https://docs.devin.ai/product-guides/knowledge](https://docs.devin.ai/product-guides/knowledge)


## Notable

Cognition is deprecating Knowledge — the very feature that gave cloud Devin cross-session recall — into skills bundled in plugins, ships a local agent that keeps no memories at all, and now lets users bill GPT-model usage to a linked personal ChatGPT subscription instead of Devin credits.

## Sources fetched

- https://docs.devin.ai
- https://docs.devin.ai/get-started/devin-intro
- https://docs.devin.ai/get-started/first-run
- https://docs.devin.ai/cli/subagents
- https://docs.devin.ai/work-with-devin/dynamic-workflows
- https://docs.devin.ai/work-with-devin/mcp
- https://docs.devin.ai/work-with-devin/advanced-capabilities
- https://docs.devin.ai/work-with-devin/ask-devin
- https://docs.devin.ai/work-with-devin/devin-cli
- https://docs.devin.ai/cli/extensibility/hooks/overview
- https://docs.devin.ai/cli/extensibility/skills/overview
- https://docs.devin.ai/cli/sandbox
- https://docs.devin.ai/cli/reference/permissions
- https://docs.devin.ai/cli/essential-commands
- https://docs.devin.ai/cli/models
- https://docs.devin.ai/cli/index
- https://docs.devin.ai/cli/acp/jetbrains
- https://docs.devin.ai/cli/enterprise/controls
- https://docs.devin.ai/cli/enterprise/windsurf-auth
- https://docs.devin.ai/cli/changelog/stable
- https://docs.devin.ai/product-guides/skills
- https://docs.devin.ai/product-guides/knowledge
- https://docs.devin.ai/product-guides/plugins
- https://docs.devin.ai/product-guides/plugin-ecosystem
- https://docs.devin.ai/product-guides/automations
- https://docs.devin.ai/product-guides/session-insights
- https://docs.devin.ai/product-guides/creating-playbooks
- https://docs.devin.ai/admin/billing/usage
- https://docs.devin.ai/admin/billing/chatgpt
- https://docs.devin.ai/admin/security
- https://docs.devin.ai/enterprise/features/usage-policies
- https://docs.devin.ai/cloud/outposts/overview
- https://docs.devin.ai/onboard-devin/agents-md
- https://docs.devin.ai/essential-guidelines/when-to-use-devin
- https://docs.devin.ai/api-reference/overview
- https://docs.devin.ai/release-notes/overview

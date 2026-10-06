# Google Antigravity

- **repo:** closed source; no public product repository
- **version pin:** `Antigravity 2.0 v2.19.1 (September 30, 2026); Antigravity CLI v1.2.14 (September 30, 2026)` — Changelog page https://antigravity.google/docs/changelog lists 'v2.19.1' marked 'Latest' dated September 30, 2026 under the 'Antigravity 2.0' section, and 'v1.2.14' dated September 30, 2026 under 'Antigravity CLI'; fetched this run. The download table on https://antigravity.google/docs/getting-started referenced installer builds labeled 2.5.0, which is inconsistent with the changelog and was not used as the pin.
- **docs home:** https://antigravity.google/docs/getting-started/

## What it promises

Antigravity is documented as an agent-first development platform delivered across four surfaces: Antigravity 2.0 (a standalone desktop 'central command center' for orchestrating agents synchronously and asynchronously), the Antigravity CLI (a TUI surface with the same core agentic capabilities), Antigravity IDE (an agentic development environment), and Antigravity SDK (a Python framework for building custom agents on the Antigravity harness). The docs promise that agents can execute system commands, read and write files, search the web, integrate external tools via skills and MCP servers, manage subagents, interact with Chrome, and produce artifacts and implementation plans. It is offered at no charge for individuals with plan-tiered rate limits, and available to teams under Google Cloud terms in Gemini Enterprise.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | The parent agent calls the invoke_subagent tool to spawn a concurrent session with a dedicated role and prompt; subagents start with a clean context window, do not inherit the parent's conversation history, and a parent can invoke several concurrently. Built-in subagents are research, browser and self, and users can define reusable custom subagents as Markdown files with YAML frontmatter or transient ones with define_subagent. | [src](https://antigravity.google/docs/subagents/) |
| workflow_orchestration | ✅ yes | The /teamwork-preview command runs a collaborative multi-agent team with explicit orchestration, implementation and verification tiers (Sentinel coordinator, Project Orchestrator, Explorers, Workers, plus Critic, Challenger, Auditor and Success Auditor verification gates); /boost runs a three-phase multi-agent reasoning pipeline. Both are documented as available on paid plans only. | [src](https://antigravity.google/docs/teamwork/) |
| mcp | ✅ yes | Antigravity supports the Model Context Protocol as an open standard for connecting agents to local developer tools, databases, file parsers and remote APIs, with per-surface setup instructions for Antigravity 2.0, the CLI and the IDE. Plugins may also ship MCP server definitions via an mcp_config.json file. | [src](https://antigravity.google/docs/mcp/) |
| hooks_lifecycle | ✅ yes | Hooks run custom scripts or shell commands at specific points during Antigravity's execution loop; they intercept agent actions right before or immediately after execution (for example running prettier after writing files). Hooks are configured in hooks.json at workspace level (.agents/hooks.json), global level (~/.gemini/config/hooks.json), or packaged inside an installed plugin, and the SDK exposes inspect/decide/transform lifecycle hooks. | [src](https://antigravity.google/docs/hooks/) |
| skills | ✅ yes | Skills are an open standard for extending agent capabilities: a skill is a folder containing a required SKILL.md file with YAML frontmatter (name and description) plus optional scripts, examples and resources. Antigravity defaults to .agents/skills while keeping backward compatibility for .agent/skills, and there is a dedicated migration guide from the older workflows system to skills. | [src](https://antigravity.google/docs/skills/) |
| memory_persistence | ◐ partial | The docs list 'Knowledge' as one of the agent's core components and state that the local app data directory contains 'artifacts, knowledge items, and more' (with a changelog entry adding 'Settings to allow disabling conversation history and knowledge'), so a persisted knowledge store exists. The limitation is documentation depth: no fetched page describes what knowledge items capture or how they are recalled across sessions, so cross-session memory semantics remain undocumented. | [src](https://antigravity.google/docs/agent/) |
| sandboxing | ✅ yes | The terminal sandbox isolates agent shell commands inside OS-level boundaries built on native primitives (Linux kernel namespaces, macOS sandbox-exec Seatbelt/SBPL profiles) with no VMs or Docker images; sensitive files such as ~/.ssh and .env are blocked and network access is limited to approved domains. Enforcement is layered: the sandbox is on by default on macOS and Linux, permission presets are Default / Request Review / Turbo, and a unified engine evaluates every sensitive operation as action(target) across Deny, Ask and Allow lists with Deny > Ask > Allow precedence. | [src](https://antigravity.google/docs/sandbox/) |
| plan_mode | ✅ yes | The /plan command creates an intentional planning phase that explores the workspace without writing files, asks clarifying questions, and drafts a structured Implementation Plan artifact with task breakdowns and verification checkpoints. The agent typically requests review of the implementation plan before making changes, and the user clicks Proceed or leaves inline comments; unless the artifact review policy is set to 'Always proceed'. | [src](https://antigravity.google/docs/plan/) |
| background_tasks | ✅ yes | Concurrent background subagents do the work without blocking the active conversation, and the docs describe asynchronous task management with Git worktrees so agents operate in isolated background folders. Antigravity also supports scheduled tasks that send messages to agents on repeatable time-based triggers, and sidecars described as background processes whose lifecycle Antigravity manages by launching and restarting them automatically; the CLI exposes /tasks to monitor, view logs for, or terminate active background tasks. | [src](https://antigravity.google/docs/features/) |
| ide_integration | ✅ yes | Antigravity ships extensions for Visual Studio Code, Visual Studio 2026, JetBrains IDEs (IntelliJ IDEA, PyCharm, WebStorm, GoLand, CLion, Rider), Zed and Xcode, bringing agents into dedicated side panels with inline diffs and interactive plans under a unified auth system. Antigravity also ships its own IDE (Antigravity IDE), documented as an agentic development environment built for the agent-first era; no fetched page states that the IDE is a fork of VS Code, so that relationship is not confirmed by the docs read here. | [src](https://antigravity.google/docs/ide/extensions/) |
| model_agnostic | ✅ yes | The model selector offers multiple providers: Gemini 3.8 Flash, Gemini 3.7 Flash, Gemini 3.6 Flash and Gemini 3.1 Pro alongside Claude Sonnet 5.5 (thinking), Claude Opus 5.5 (thinking), Claude Sonnet 4.6, Claude Opus 4.6 and GPT-OSS-120b, with availability varying by plan. The SDK additionally supports local execution via LiteRT checkpoints and OpenAI-compatible local servers. | [src](https://antigravity.google/docs/models/) |
| plugins | ✅ yes | A plugin is a directory with a required plugin.json manifest that packages reusable skills, background subagents, linting rules, MCP servers and lifecycle hooks into a single deployable asset, with a JSON schema published at antigravity.google/schemas/v1/plugin.json. A curated Marketplace lets users discover, install and manage plugins, and plugins installed in Antigravity 2.0 are automatically updated and displayed in the CLI's Installed tab. | [src](https://antigravity.google/docs/plugins/) |
| session_resume | ✅ yes | The /resume command (aliases /switch and /conversation) opens an interactive Session Picker TUI panel to browse, search, page and load past conversation threads, with resumption also available from the host terminal via flags such as agy -c / agy --continue. CLI conversation histories are scoped to the current working directory, and the /fork (alias /branch) command clones an entire conversation history for parallel experimentation. | [src](https://antigravity.google/docs/cli/commands/resume/) |
| cost_controls | ✅ yes | Rate limits and model availability differ by Google AI plan, with quotas refreshed every five hours for Pro and Ultra tiers plus weekly rate limits, and the docs state that rate limits correlate with the amount of work done by the agent rather than a flat prompt count. The CLI surfaces remaining AI credits in the statusline, warns when credits drop below a threshold, opens a dedicated credits panel for usage statistics, and offers a 'Use G1 Credits' setting to control fallback billing after plan quotas are exhausted. | [src](https://antigravity.google/docs/plans/) |

## Architecture

Antigravity is documented as one platform across four surfaces with different roles (https://antigravity.google/docs/home/): Antigravity 2.0 is a standalone desktop command center that runs independently of an IDE and orchestrates agents synchronously and asynchronously (https://antigravity.google/docs/overview/), the Antigravity CLI is a keyboard-centric TUI with the same core agentic capabilities aimed at fast interactions and SSH sessions, Antigravity IDE is an agentic development environment for the editor/terminal/browser, and the Antigravity SDK is a Python framework for building custom agents, registering tools and implementing lifecycle hooks on top of the Antigravity harness. The CLI documentation recommends staging work in stages. Work is scoped through projects rather than bare workspaces: projects support Git worktrees so agents operate in isolated background folders, multi-folder access across codebases in a single conversation, and scoped settings and permissions per project (https://antigravity.google/docs/projects/, https://antigravity.google/docs/features/). The extension of the agent into the wider machine is deliberate: a browser agent actuates Chrome for dashboard reads, source control actions and UI testing, with browser recordings and URL allow/deny lists (https://antigravity.google/docs/ide/browser/, https://antigravity.google/docs/ide/allowlist-denylist/). The SDK documents a stateful runtime with background event triggers, session persistence and token cost auditing (https://antigravity.google/docs/sdk/overview/, https://antigravity.google/docs/sdk/lifecycle/).

## Context management

Context isolation is an explicit design principle. Subagents run with a clean slate and do not inherit the parent's existing conversation history, and the parent can choose whether a subagent inherits the same workspace, creates an isolated Git worktree, or shares directory storage (https://antigravity.google/docs/subagents/). Teamwork is framed around avoiding context bloat by breaking large tasks into modular milestones where agents coordinate through clean artifact handoffs instead of overloading a single conversation, and the Project Orchestrator hands off to a fresh successor between milestones to prevent context degradation (https://antigravity.google/docs/teamwork/). The CLI scopes conversation histories to the current working directory so that 'the agent's semantic memory and token limits remain focused solely on the relevant codebase', and /fork clones a conversation up to the current point so alternative designs can be explored without losing progress (https://antigravity.google/docs/cli/conversations/). Communication between the user and agent is mediated by artifacts, including implementation plans and walkthroughs (https://antigravity.google/docs/artifacts/, https://antigravity.google/docs/implementation-plan/). Customization surfaces that shape context include rules (persistent instructions, coding standards and architectural conventions), skills, and hooks (https://antigravity.google/docs/rules/, https://antigravity.google/docs/skills/, https://antigravity.google/docs/hooks/).

## Ecosystem

Distribution is deliberately multi-surface: desktop installers for macOS, Windows, Linux and Googlebook at antigravity.google/download (https://antigravity.google/docs/getting-started/), a CLI, an IDE, and editor extensions for Visual Studio Code, Visual Studio, JetBrains, Zed and Xcode under one unified authentication system that determines model entitlements, quota limits and data privacy policies (https://antigravity.google/docs/ide/extensions/). Third-party extensibility is packaged through plugins, which bundle skills, subagents, rules, MCP servers and hooks behind a plugin.json manifest, and distributed through a curated Marketplace with tips for building plugins (https://antigravity.google/docs/plugins/, https://antigravity.google/docs/marketplace/). Google-first bundles such as Android, Firebase and Google Maps Platform tooling are offered as ready-made capability packs (https://antigravity.google/docs/build-with-google/). Model access spans vendors, including Anthropic Claude and GPT-OSS models beside Gemini (https://antigravity.google/docs/models/), and the SDK adds local on-device models through LiteRT and OpenAI-compatible local servers (https://antigravity.google/docs/sdk/local-models/). For teams, the platform is offered through Gemini Enterprise under Google Cloud terms (https://antigravity.google/docs/enterprise/, https://antigravity.google/docs/plans/).

## Governance

The permission system is a unified fine-grained engine: every sensitive operation is a permission resource formatted as action(target), evaluated across Deny, Ask and Allow lists with a documented precedence rule of Deny > Ask > Allow, layered on top of a permission preset that is Default (sandbox enabled, commands allowed inside the sandbox and ask outside, workspace plus temp dirs), Request Review (sandbox disabled, always ask, workspace only) or Turbo (sandbox disabled, unrestricted terminal and full filesystem) (https://antigravity.google/docs/permissions/, https://antigravity.google/docs/agent-settings/). The terminal sandbox is enabled by default on macOS and Linux and blocks sensitive files such as ~/.ssh and .env, hides anything not explicitly mounted, and limits network access to approved domains (https://antigravity.google/docs/sandbox/). Strict mode layers browser URL allowlists and denylists plus artifact and terminal review policies on top, and non-workspace file access is off by default with the agent limited to project folders and the local app data directory (https://antigravity.google/docs/settings/, https://antigravity.google/docs/ide/allowlist-denylist/). The SDK lets builders define declarative safety policies programmatically (https://antigravity.google/docs/sdk/policies/), and hooks provide a scriptable enforcement point at tool boundaries (https://antigravity.google/docs/hooks/).

## Limitations

Several capabilities are gated by platform or plan. The updated permission system and terminal sandbox are currently available on macOS and Linux only, with Windows continuing to use the previous permission system and sandbox behavior (https://antigravity.google/docs/permissions/, https://antigravity.google/docs/sandbox/). The heaviest orchestration features, /teamwork-preview and /boost, are documented as available on paid plans across Antigravity 2.0 and the CLI (https://antigravity.google/docs/teamwork/, https://antigravity.google/docs/boost/). Model availability is plan-dependent rather than universal: Claude and GPT-OSS models are excluded from some tiers, and the docs note that model entries marked with an asterisk will be removed on November 2, 2026 (https://antigravity.google/docs/models/). Antigravity IDE is explicitly not supported for enterprise customers, who are directed to Antigravity 2.0 or the Antigravity CLI instead (https://antigravity.google/docs/ide/overview/). Rate limits are documented as correlating with the amount of work the agent performs rather than prompt count, so usage is workload-sensitive (https://antigravity.google/docs/plans/). Finally, persistent agent memory is only partially documented: 'Knowledge' appears as a core agent component name and as knowledge items in the local app data directory, but no page describes its scope or recall behavior (https://antigravity.google/docs/agent/).

## In its own words

> Delegate parallel builds, multi-file code generation, and research sweeps to concurrent background subagents while maintaining your active programming flow.  
> — [https://antigravity.google/docs/subagents/](https://antigravity.google/docs/subagents/)

> Teamwork solves this by pairing specialized agents together, running independent verification checks at every milestone, and working inside isolated project directories.  
> — [https://antigravity.google/docs/teamwork/](https://antigravity.google/docs/teamwork/)

> Antigravity supports the Model Context Protocol (MCP), an open standard that lets AI agents and editors securely connect to local developer tools, databases, file parsers, and external remote APIs.  
> — [https://antigravity.google/docs/mcp/](https://antigravity.google/docs/mcp/)

> The terminal sandbox isolates agent shell commands inside OS-level container boundaries to protect your workstation and sensitive files.  
> — [https://antigravity.google/docs/sandbox/](https://antigravity.google/docs/sandbox/)

> Hooks allow you to run custom scripts or shell commands at specific points during Antigravity’s execution loop to enforce rules, execute linters, or capture diagnostics.  
> — [https://antigravity.google/docs/hooks/](https://antigravity.google/docs/hooks/)


## Notable

The most striking finding is that multi-agent work is a first-class product primitive rather than a side feature: /boost runs a three-phase multi-agent reasoning pipeline and /teamwork-preview runs a named agent team (Sentinel, Project Orchestrator, Explorers, Workers, Critic, Challenger, Auditor, Success Auditor) with adversarial verification gates, though both are restricted to paid plans. Second, the harness is genuinely multi-provider at the model selector level in a Google product, offering Claude Sonnet 5.5 / Opus 5.5, Claude Sonnet 4.6 / Opus 4.6 and GPT-OSS-120b alongside Gemini 3.x models. Third, sandboxing is documented as OS-native rather than containerized: Linux kernel namespaces and macOS sandbox-exec (Seatbelt/SBPL) profiles, with no VMs or Docker images, and the updated permission engine plus sandbox are macOS/Linux only while Windows still runs the previous permission system.

## Sources fetched

- https://antigravity.google/
- https://antigravity.google/sitemap.xml
- https://antigravity.google/llms.txt
- https://antigravity.google/blog/introducing-google-antigravity-2/
- https://antigravity.google/blog/google-io-2026-feature-deep-dive/
- https://antigravity.google/docs
- https://antigravity.google/docs/home/
- https://antigravity.google/docs/getting-started/
- https://antigravity.google/docs/overview/
- https://antigravity.google/docs/build-with-google/
- https://antigravity.google/docs/models/
- https://antigravity.google/docs/features/
- https://antigravity.google/docs/agent/
- https://antigravity.google/docs/agent-settings/
- https://antigravity.google/docs/settings/
- https://antigravity.google/docs/permissions/
- https://antigravity.google/docs/sandbox/
- https://antigravity.google/docs/hooks/
- https://antigravity.google/docs/skills/
- https://antigravity.google/docs/mcp/
- https://antigravity.google/docs/plugins/
- https://antigravity.google/docs/marketplace/
- https://antigravity.google/docs/rules/
- https://antigravity.google/docs/subagents/
- https://antigravity.google/docs/teamwork/
- https://antigravity.google/docs/boost/
- https://antigravity.google/docs/plan/
- https://antigravity.google/docs/implementation-plan/
- https://antigravity.google/docs/artifacts/
- https://antigravity.google/docs/artifact-review/
- https://antigravity.google/docs/walkthrough/
- https://antigravity.google/docs/screenshots/
- https://antigravity.google/docs/tools/
- https://antigravity.google/docs/projects/
- https://antigravity.google/docs/sidecars/
- https://antigravity.google/docs/remote-control/
- https://antigravity.google/docs/plans/
- https://antigravity.google/docs/enterprise/
- https://antigravity.google/docs/faq/
- https://antigravity.google/docs/changelog/
- https://antigravity.google/docs/firebase-studio-migration/
- https://antigravity.google/docs/migration/workflows-to-skills/
- https://antigravity.google/docs/ide/overview/
- https://antigravity.google/docs/ide/extensions/
- https://antigravity.google/docs/ide/extensions/vscode/
- https://antigravity.google/docs/ide/extensions/visual-studio/
- https://antigravity.google/docs/ide/extensions/jetbrains/
- https://antigravity.google/docs/ide/extensions/zed/
- https://antigravity.google/docs/ide/extensions/xcode/
- https://antigravity.google/docs/ide/browser/
- https://antigravity.google/docs/ide/browser-recordings/
- https://antigravity.google/docs/ide/allowlist-denylist/
- https://antigravity.google/docs/ide/review-changes-editor/
- https://antigravity.google/docs/cli/overview/
- https://antigravity.google/docs/cli/install/
- https://antigravity.google/docs/cli/tutorial/
- https://antigravity.google/docs/cli/using/
- https://antigravity.google/docs/cli/features/
- https://antigravity.google/docs/cli/best-practices/
- https://antigravity.google/docs/cli/troubleshooting/
- https://antigravity.google/docs/cli/reference/
- https://antigravity.google/docs/cli/prompting/
- https://antigravity.google/docs/cli/headless/
- https://antigravity.google/docs/cli/artifacts/
- https://antigravity.google/docs/cli/conversations/
- https://antigravity.google/docs/cli/modes/
- https://antigravity.google/docs/cli/vim-editor-mode/
- https://antigravity.google/docs/cli/credits/
- https://antigravity.google/docs/cli/statusline/
- https://antigravity.google/docs/cli/title/
- https://antigravity.google/docs/cli/gcli-migration/
- https://antigravity.google/docs/cli/commands/agents/
- https://antigravity.google/docs/cli/commands/resume/
- https://antigravity.google/docs/cli/commands/usage/
- https://antigravity.google/docs/cli/commands/credits/
- https://antigravity.google/docs/cli/commands/permissions/
- https://antigravity.google/docs/cli/commands/codesearch/
- https://antigravity.google/docs/cli/commands/diff/
- https://antigravity.google/docs/cli/commands/statusline/
- https://antigravity.google/docs/cli/commands/title/
- https://antigravity.google/docs/cli/commands/voice/
- https://antigravity.google/docs/sdk/overview/
- https://antigravity.google/docs/sdk/lifecycle/
- https://antigravity.google/docs/sdk/subagents/
- https://antigravity.google/docs/sdk/policies/
- https://antigravity.google/docs/sdk/local-models/

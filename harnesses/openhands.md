# OpenHands

- **repo:** All-Hands-AI/OpenHands (repo now redirects to OpenHands/OpenHands after org rename)
- **version pin:** `v1.24.0` — gh api repos/All-Hands-AI/OpenHands/releases/latest -> https://github.com/OpenHands/OpenHands/releases/tag/v1.24.0 (published 2026-09-25); corroborated by npm registry @openhands/agent-canvas latest = 1.24.0
- **docs home:** https://docs.openhands.dev

## What it promises

OpenHands Agent Canvas promises to turn your coding agents into a self-hosted, always-on engineering team — a developer control center for starting conversations and automating everyday tasks, run locally by default or across Docker, VM, and cloud backends with OpenHands, Claude Code, Codex, Gemini, or any ACP-compatible agent.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ✅ yes | SDK-level TaskToolSet: parent spawns typed sub-agents (register_agent), runs sequentially, resumable via task_id; file-based sub-agents can be plain Markdown. | [src](https://docs.openhands.dev/sdk/guides/task-tool-set) |
| workflow_orchestration | ◐ partial | Has sub-agent delegation (sequential, blocking), scheduled/event automations, and GitHub Actions workflow templates; no DAG/team/swarm orchestration primitives documented. | [src](https://docs.openhands.dev/sdk/guides/task-tool-set) |
| mcp | ✅ yes | MCP client; SSE/SHTTP/stdio transports; full support on CLI, SDK, Local GUI and Cloud. | [src](https://docs.openhands.dev/overview/model-context-protocol) |
| hooks_lifecycle | ✅ yes | PreToolUse, PostToolUse, UserPromptSubmit, Stop, SessionStart, SessionEnd; blocking + async hooks; Claude Code-compatible hooks.json format. | [src](https://docs.openhands.dev/openhands/usage/customization/hooks) |
| skills | ✅ yes | Follows Agent Skills spec (SKILL.md); keyword triggers, path-triggered rules, org/user/global registries. | [src](https://docs.openhands.dev/overview/skills) |
| memory_persistence | ✅ yes | Opt-in (load_memory=True); two-tier MEMORY.md (user ~/.openhands/memory/ + project workspace/.openhands/memory/); off by default. | [src](https://docs.openhands.dev/sdk/guides/persistent-memory) |
| sandboxing | ✅ yes | Docker/process/remote providers; permission modes: always-ask (default), --always-approve, --llm-approve; SDK confirmation policies AlwaysConfirm/ConfirmRisky/NeverConfirm. | [src](https://docs.openhands.dev/openhands/usage/sandboxes/overview) |
| plan_mode | ◐ partial | Plan-then-execute exists as a documented SDK pattern (planning agent writes PLAN.md, execution agent implements); CLI only has 'Plan - View agent plan'; no built-in interactive plan-approval gate in docs. | [src](https://docs.openhands.dev/sdk/guides/agent-custom) |
| background_tasks | ✅ yes | Agent-server REST API runs conversations in background; bash commands also have a background start endpoint; Agent Canvas conversations run server-side. | [src](https://docs.openhands.dev/sdk/guides/agent-server/api-reference/conversations/run-conversation) |
| ide_integration | ✅ yes | ACP-based: Zed + JetBrains native support, VS Code via community ACP extension; marked experimental; GUI also embeds a VS Code tab. | [src](https://docs.openhands.dev/openhands/usage/cli/ide/overview) |
| model_agnostic | ✅ yes | LiteLLM: Anthropic/OpenAI/Google/Azure/Bedrock/Groq/Moonshot/OpenRouter/local servers; also can drive Claude Code, Codex, Gemini CLI as ACP agents. | [src](https://docs.openhands.dev/openhands/usage/llms/llms) |
| plugins | ✅ yes | Claude Code plugin structure compatible (.claude-plugin/) plus portable Agent Plugins format with plugin.json at root. | [src](https://docs.openhands.dev/overview/plugins) |
| session_resume | ✅ yes | openhands --resume <id> / --resume --last; also works in ACP/IDE mode; automations' conversations can be continued too. | [src](https://docs.openhands.dev/openhands/usage/cli/resume) |
| cost_controls | ✅ yes | Token/cost/latency metrics per LLM and per conversation; Cloud org/user spending caps documented at https://docs.openhands.dev/openhands/usage/cloud/organizations/budgets. | [src](https://docs.openhands.dev/sdk/guides/metrics) |

## Notable

Repo All-Hands-AI/OpenHands now redirects to OpenHands/OpenHands and its v1.x release is 'Agent Canvas', a control center that can host third-party agents (Claude Code, Codex, Gemini) via ACP, while the OpenHands agent core moved to the separate software-agent-sdk and automation repos; hooks/skills formats are deliberately Claude Code-compatible.

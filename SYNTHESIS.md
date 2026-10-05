# Synthesis — what the matrix actually says

As of 2026-10-05. Every claim below traces to a harness page, every harness page traces to a fetched doc.

## 1. The capability floor has moved

Two years ago "the agent runs commands for you" was the feature. Now the floor is: subagents, lifecycle hooks, skills, session resume, background tasks. Eight of ten harnesses ship at least eleven of the fourteen capabilities we tracked. The differentiators left are **orchestration depth** (scripted multi-agent runs vs. ad-hoc fan-out) and **where the trust boundary sits** (OS sandbox vs. permission prompts vs. a second model reviewing actions).

## 2. The ecosystem is eating itself — politely

The most striking pattern is cross-harness interop becoming a feature:

- **Qwen Code** ships built-in executors that delegate to separately installed **Claude Code** and **Codex CLI**, and installs extensions from the Claude Code and Gemini CLI marketplaces.
- **OpenHands** v1.x ("Agent Canvas") hosts third-party agents — Claude Code, Codex, Gemini — over ACP, having moved its own agent core into separate SDK repos.
- **OpenCode** reads `CLAUDE.md` and `.claude/skills` as a first-class compatibility path.

Harnesses are converging on shared surfaces (MCP, ACP, skill directories) while competing on runtime. The atlas implication: capability rows like "plugins" now mean different things per harness — marketplace-compatible vs. proprietary.

## 3. Half the field is in transition — check dates before citing

- **Roo Code**: discontinued; final release v3.54.0 (2026-05-15), README points to the community fork ZooCode or to Cline.
- **Gemini CLI**: officially superseded by Antigravity CLI for free/Pro/Ultra users (2026-06-18), yet still ships weekly releases for enterprise/API-key users — alive but transitioning.
- **Goose**: repo renamed to a new org; the heavily promoted plan mode was later **removed** from the CLI.
- **OpenHands**: repo redirected to a new org; the product split into canvas + SDK repos.
- **Aider**: GitHub "latest release" tag lags the PyPI version users actually install.

A capability matrix without version pins and dates is fiction within a quarter. That is why every row here carries both.

## 4. Trust models diverge where capability rows converge

- **Claude Code**: default interactive mode is now "auto" — a second classifier model, not the user, reviews actions; OS-level sandbox exists but is off by default.
- **Codex CLI**: subagents on by default, plan/goal modes, but the `codex mcp-server` binary was removed — it consumes MCP, no longer serves it.
- **Aider**: the popular outlier — no MCP, no plugins, no subagents, no hooks. A focused pair-programmer while everyone else became a platform.

## 5. What "dynamic workflows" actually means in the wild

Scripted multi-agent orchestration (a rerunnable script that spawns and pipelines subagents) is currently a **Claude Code** capability; everyone else offers fan-out via task tools, SDK control, or hosted canvases. If you need deterministic control flow across agents, the matrix narrows your field fast — which is exactly the question this atlas was built to answer.

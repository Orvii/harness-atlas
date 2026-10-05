# Synthesis — what the matrix actually says

As of 2026-10-05 (v3.3: 25 harnesses). Every claim below traces to a harness page, every harness page traces to a fetched doc.

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

Scripted multi-agent orchestration (a rerunnable script that spawns and pipelines subagents) is currently a **Claude Code** capability; everyone else offers fan-out via task tools, SDK control, or hosted canvases. The notable exception in v2: **GitHub Copilot CLI**'s `/fleet`, which turns the main agent into a dependency-aware orchestrator with a live, nestable subagent tree you can steer mid-run — supervision depth unusual for a chat-style CLI. If you need deterministic control flow across agents, the matrix narrows your field fast — which is exactly the question this atlas was built to answer.

## 6. The compatibility chain has a direction — and by v3.3 it points everywhere at once

The v3.3 rows finish the picture the earlier versions started: Cursor discovers skills and subagents from Claude- and Codex-compatible directories; Junie imports agent definitions from `.cursor/agents`, `.claude/agents` and `.codex/agents`; Windsurf/Devin Desktop and Kiro read the shared `AGENTS.md`/skills surface. What began as one vendor's filename becoming a de-facto standard is now a set of directories every major harness cross-reads. The direction is no longer A→B; it is convergence on a small shared set, with each vendor's native path kept as the home address.

v2's new rows sharpen §2 into a pattern with a direction: the ecosystem converges on **Claude Code's surfaces** as the de-facto interchange format.

- **Kilo Code**'s CLI descends from OpenCode and still deep-merges `opencode.json`; OpenCode reads `CLAUDE.md` and `.claude/skills`; **Continue** (now finished) shipped SKILL.md loading plus `CLAUDE.md`/`AGENTS.md`/`CODEX.md` memory-file support and a Claude Code-compatible hooks engine.
- v3 widens the chain: **Mistral's Vibe** imports Claude Code / Codex / Kimi / OpenCode plugin packages and ships OpenAI/Anthropic/Vertex adapters; **Crush** discovers skills from `~/.claude/skills` and `.claude/skills` alongside its own paths and documents its single hook as explicitly Claude Code-compatible.
- Read as a graph: Kilo → OpenCode → Claude Code conventions, Continue and Vibe pointing the same way from opposite ends (one finished, one migrating), Crush converging on the skill-directory layout.

The practical consequence: writing a skill or memory file to Claude Code's layout currently maximizes portability across four harnesses. That is an empirical observation about this snapshot, not an endorsement — the direction could reverse if another surface wins.

## 7. Governance is now a differentiator — and a mirror

Four governance facts deserve attention:

- **Zed**'s CONTRIBUTING.md states it does "not accept contributions from autonomous agents" and bans undisclosed LLM-written PR discussion — the strictest stance in the set, from a product built around agentic coding.
- **Kilo Code** was acquired by Anaconda while deprecating its signature Orchestrator mode; corporate ownership reshaping roadmaps is now visible inside capability tables.
- **Continue** is finished: read-only repo, frozen docs, dead Hub domain — yet its last release quietly carries the compatibility layer §6 describes.
- **Amazon Q Developer CLI** inverts the pattern: a discontinued open-source CLI whose last releases hid a power-user arsenal (blocking preToolUse hooks, delegate subagents, an agent-scoped semantic knowledge base) behind `/experiment` toggles — capability that shipped to no audience.

## 8. The closed-source cluster answers differently

The closed-source cluster began in v3.2 with **Sourcegraph Amp**, **Factory Droid** and **JetBrains Junie**, and v3.3 more than doubled it: **Cursor**, **Windsurf/Devin Desktop**, **Google Jules**, **Amazon Kiro** and **Devin** also have no public product repo. Eight of twenty-five rows now rest on vendor docs alone. That changes what a capability cell can mean.

- **Version pins move off release tags.** For open harnesses a pin is a git tag you can check out. For these three it is whatever the vendor publishes: Amp from the npm `dist-tag latest` of `@sourcegraph/amp`, Droid from its docs changelog page, Junie from `junie.jetbrains.com/whats-new`. A pin you cannot diff is weaker evidence, and the atlas says so per row instead of hiding it.
- **Deprecation is a policy, not a signal.** Amp states an explicit "no backward compatibility" posture and deletes unloved features (Amp Tab, custom commands replaced by skills). In an open repo that deletion is a commit you can read; here it is a chronicle post. Cells for fast-moving closed products should be treated as shorter-lived than identical-looking cells for open ones.
- **Trust claims concentrate in the vendor's own security page.** Droid documents a real OS sandbox (Seatbelt on macOS, bubblewrap+seccomp on Linux/WSL2, egress through a filtering proxy); Amp documents sandboxed cloud VMs for orbs while leaving local execution unsandboxed and unapproved by default. Both are vendor assertions with no source to audit — which is exactly the distinction [TRUST.md](TRUST.md) exists to make visible.
- **Capability depth is not lower, only unverifiable.** These three rows are among the fullest in the grid (Droid 13 ✅ + 1 ◐; Junie 13 ✅ + 1 ◐). The honest reading is not "closed means less capable" but "closed means every ✅ rests on a doc page rather than on code you can run."

A mirror, stated plainly: this atlas is itself agent-assisted research. We hold the line where Zed draws it for *contributions* — every cell cites a human-checkable source URL, and the prose is reviewable line by line. Governance rows exist so readers can apply their own line wherever they draw it.
## 9. Execution locality is now a first-class axis

v3.3 adds the first harnesses whose agent loop does not run on the developer's machine at all, and that changes what every other row means:

- **Three products are cloud-autonomous by design.** Google Jules runs its plan-execute loop in Google Cloud, one short-lived Ubuntu VM per task; Devin's sessions execute in isolated VMs (Ubuntu, Windows or macOS) while "Devin's agent loop (inference and planning) continues to run in Devin's cloud"; Kiro's cloud sessions run server-side and detach/reattach across IDE, CLI, web and mobile. Cursor spans both worlds — a local IDE plus Cloud Agents in server-side VMs.
- **The human gate relocates when the loop leaves the machine.** A per-command approval prompt is impossible when no human terminal is in the path. Jules has *no* per-command prompts at all; its human gate is plan approval, pause, and delete. Devin and Windsurf/Devin Desktop instead make the sandbox **fail-closed** — the product refuses to start when sandbox tooling is missing. The trust floor did not disappear in the cloud; it moved from "a human clicks yes" to "a VM is the boundary, and the boundary is someone else's computer". Jules' own FAQ states the VM has internet access and should be treated like shared compute — which is the sentence to read before any secret lands in a repo it can see.
- **Where the human left, a model was hired.** Cursor's default run mode is Auto-review — a classifier judging each command — with the docs' own caveat that "Auto-review is not a security boundary". Jules goes further: a critic agent adversarially reviews every proposed change before it lands, making model review the primary gate rather than a mode. Two products now ship a model reviewer as the routine control; [TRUST.md](TRUST.md) tracks who else offers one.
- **The capability grid's `background_tasks` row was doing two jobs.** It conflated *asynchronous* (the agent keeps working after you stop watching) with *remote* (the agent keeps working after you close the laptop, because it was never on it). Amp's orbs, Cursor's Cloud Agents, Jules, Devin and Kiro cloud sessions are remote; OpenCode's and Cline's background tasks are not. Read the row's note, not its symbol — and for a security decision read TRUST.md, where locality is the organizing column.


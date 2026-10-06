# Synthesis — what the matrix actually says

As of 2026-10-06 (v3.5: 37 harnesses). Every claim below traces to a harness page, every harness page traces to a fetched doc.

## 1. The capability floor has moved

Two years ago "the agent runs commands for you" was the feature. Now the floor is: subagents, lifecycle hooks, skills, session resume, background tasks. Thirty of thirty-seven harnesses ship at least eleven of the fourteen capabilities we tracked — and the seven that do not are not laggards, they are a different kind of product, in four different ways. **Aider** predates the whole convention stack. **Amazon Q CLI** and **Google Jules** are being superseded or were born narrow. **Qodo**, **Bolt** and **Replit Agent** do not own the loop at all — Qodo reviews inside someone else's agent, Bolt and Replit run the loop in a hosted environment whose surfaces they document only halfway. And **Void** (v3.5) is below the floor for a reason none of the others share: it is *abandoned* — the repo is archived and its README opens "Void is now deprecated… no longer accepting contributions," so its missing hooks, plan mode and cost controls are not a design choice but a project that stopped. The capability floor is now a *category* boundary, not a maturity ladder, and one of the categories is death. The differentiators left are **orchestration depth** (scripted multi-agent runs vs. ad-hoc fan-out) and **where the trust boundary sits** (OS sandbox vs. permission prompts vs. a second model reviewing actions).

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

The closed-source cluster began in v3.2 with **Sourcegraph Amp**, **Factory Droid** and **JetBrains Junie**, and v3.3 more than doubled it: **Cursor**, **Windsurf/Devin Desktop**, **Google Jules**, **Amazon Kiro** and **Devin** also have no public product repo. v3.4 added **Replit**, whose agent has no public product repository, and v3.5 adds five more: **Trae**, **Google Antigravity**, **Qoder**, **Lovable** and **v0**. Fourteen of thirty-seven rows now rest on vendor docs alone — and the pattern in wave 7 is stark: of the seven new rows, five are closed-source, and only **Warp** (AGPL-3.0 client) and **Void** (archived but public) have inspectable code. That changes what a capability cell can mean: for the closed rows the cell records what the vendor *says*, with no source to cross-read.

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
| Harness | Where the loop runs | Human gate |
|---|---|---|
| Google Jules | Google Cloud; one short-lived Ubuntu VM per task | plan approval, pause, delete — no per-command prompts exist |
| Devin | Devin's cloud; isolated VM per session (Ubuntu/Windows/macOS) | permission modes incl. fail-closed sandbox |
| Amazon Kiro | server-side cloud sessions (detach/reattach across surfaces) + local IDE/CLI | permissions.yaml prompts; per-task cloud sandbox |
| Cursor | local IDE/CLI **and** Cloud Agents in server-side VMs | Auto-review classifier (default), Allowlist, Run Everything |
| Windsurf / Devin Desktop | local desktop IDE (VS Code fork) | five permission modes; sandbox fail-closed |

- **The capability grid's `background_tasks` row was doing two jobs.** It conflated *asynchronous* (the agent keeps working after you stop watching) with *remote* (the agent keeps working after you close the laptop, because it was never on it). Amp's orbs, Cursor's Cloud Agents, Jules, Devin and Kiro cloud sessions are remote; OpenCode's and Cline's background tasks are not. Read the row's note, not its symbol — and for a security decision read TRUST.md, where locality is the organizing column.

## 10. v3.4: the stack is splitting — capability vendors that execute nothing

Five new rows and three of them do not fit the matrix's original shape. That misfit is the finding.

- **Qodo is a capability layer without an execution layer.** It ships review agents, standards enforcement, skills and an MCP surface *into whatever coding agent you already run* — Claude Code, Codex, Kiro, its own deprecated CLI's successor. Its sandboxing row is not "no": it is *not its axis*. The trust question for a Qodo-equipped setup is the host agent's trust question plus a review layer on top. The atlas has, until now, only listed harnesses that own the loop; v3.4 says the loop is becoming a platform other vendors build against.
- **Bolt and Replit Agent are web-native: the environment is the product.** Neither documents an OS sandbox because neither documents an OS the user touches — the boundary is a hosted project environment (Replit's isolated task copies, Bolt's project security checks), and in both the human gate is *review without a documented hard approval*: Replit's Plan Mode gates file changes, Bolt's Plan Mode lets you revise a plan the homepage flow has already started building. "Plan mode" means three different strengths across these rows; the note column is the only place the difference survives.
- **Deprecation is now a row property, not a footnote.** Tabnine's entire agent-capability surface (subagents, hooks, skills, sandbox, plan mode) is documented for a CLI the vendor calls maintenance-mode with deprecation after 2026-12-31; Qodo's own CLI is deprecated in favour of a toolbox that plugs into other agents. Two of thirty-seven rows carry a *future* expiry date on the capabilities themselves. Wave 7 adds a third and grimmer variant: **Void** is not expiring, it has already expired — the repo is archived and the README opens "Void is now deprecated… no longer accepting contributions," so its cells describe software that will never gain a hook or a plan mode. Three rows now have a half-life attached, in two directions: two scheduled to stop, one already stopped. A snapshot that records the date but not the half-life of a row would be lying by omission — hence the pin's source column and this paragraph.
- **The unknowns concentrated, and that is honest.** Bolt and Replit return `unknown` on six and five capabilities respectively — not because the research was thin (both cite 30+ fetched doc pages) but because web-native vendors document the happy path and stay silent on boundaries. Silence about a sandbox is not a sandbox. The grid keeps those cells `?`, and the pattern itself is data: *local* harnesses over-document gates; *hosted* harnesses under-document them.

## 11. v3.5: the platform vendors arrived, and documentation became a research variable

Seven new rows — **Warp**, **Trae**, **Google Antigravity**, **Qoder**, **Lovable**, **v0**, **Void** — and the shape of the finding changed again.

- **The floor is now what a platform vendor ships on day one.** Qoder (Alibaba) documents all fourteen capabilities as `yes`; Antigravity (Google) reaches fourteen of fourteen with only `memory_persistence` partial (the knowledge store is evidenced, its cross-session semantics are not documented); Warp and Trae land at thirteen of fourteen. These are not startups converging on a convention over years — they are platform companies that entered the space *after* the convention formed and built to it. Read against §1, that is what "table stakes" now means: a new entrant from a large vendor starts at the ceiling of the field, and the interesting variation moved to trust posture (Antigravity's default-on Seatbelt/namespace sandbox versus Qoder's prompts-without-sandbox) and to how many of those fourteen are gated behind a beta flag or a plan tier.
- **Documentation architecture is now a research variable.** Six of the seven publish a machine-readable surface — `llms.txt`, a full-markdown corpus, or a public repo — and were researched in one pass. Trae publishes *none*: no `llms.txt`, no `sitemap.xml`, no `.md` variants and no content API, because docs.trae.ai is a client-side SPA in which all four return the same 287 KB app shell. Reading it required extracting the server-rendered payload the SPA embeds, which is now checked into the repo as [`scripts/fetch-trae-docs.py`](scripts/fetch-trae-docs.py) so the row stays reproducible. The generalizable point: an evidence-based atlas can only cite what a vendor makes *fetchable*, and "the docs exist" is no longer the same claim as "the docs can be read by anything but a browser." Expect this to spread as doc platforms move client-side.
- **Warp breaks the closed-source expectation in this wave.** Five of the seven new rows rest on vendor docs alone, but Warp's client is **AGPL-3.0 and public** (`warpdotdev/warp`, Rust) — the assumption that a well-funded terminal-agent startup is closed does not hold. Void is the other inspectable one, for the opposite reason: public, archived, and dead.
- **The web-native cluster reached four rows, and it inverts an axis.** With Lovable and v0 joining Bolt and Replit, hosted builders are no longer an exception. Lovable and v0 are the two that document the inversion cleanly: `ide_integration` reads `no` while `mcp` reads `yes`, because the direction is reversed — IDEs connect *to them*, they do not ship into IDEs. The atlas grades that `no` (the Zed precedent: reverse-direction protocol access is not an extension), which means the same capability column now encodes two opposite integration geometries. Bolt and Replit stay `unknown` on the axis instead, which is §10's under-documentation pattern rather than an inversion. The note is the only place any of this is visible — the same caveat §9 raised for `background_tasks`, now on a second axis.

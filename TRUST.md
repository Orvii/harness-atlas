# Trust models — how each harness bounds what the agent may do

As of 2026-10-06, 30 harnesses. Sources: the sandboxing and hooks rows on each [harness page](harnesses/), which carry their own evidence URLs.

## The three layers

Every trust story in this set reduces to three mechanisms, used in different combinations:

1. **OS-level sandbox** — the operating system enforces a boundary around commands (Seatbelt, bubblewrap, Landlock, Docker, Mach-service allowlists).
2. **Permission prompts** — a human approves each tool call or category of calls, optionally with allow/deny rule lists.
3. **Model review** — a second model (classifier or LLM approver) judges actions instead of, or before, the human.

The capability matrix marks `sandboxing` yes/partial; this page says *which layer* that yes is made of, because the layers fail differently. The matrix's cell is the broader question — *does the harness bound what the agent may do, by any mechanism?* — so permission gating counts toward it. This page is stricter and separates the layers, which means the two can disagree: a harness can be `sandboxing ✅` in the matrix with **no** OS-level sandbox here (OpenCode and Cline are exactly that case). Where they disagree, this table is the one to trust for a security decision. An OS sandbox fails closed against the filesystem but sees nothing about intent; a prompt fails open the moment the user habitually clicks yes; a model reviewer fails silently, at scale, in the direction of its training.

## Who uses what

| Harness | OS sandbox | Prompts | Model review | Default posture |
|---|---|---|---|---|
| Claude Code | yes (off by default; macOS/Linux/WSL2) | yes (modes incl. plan/auto) | yes — `auto` mode is the default interactive mode since v2.1.283 | prompts + classifier |
| OpenCode | no | yes (allow/ask/deny, glob rules, external-dir + doom-loop guards) | no | prompts |
| Codex CLI | yes (read-only / workspace-write / full) | yes (approval policies) | no | sandboxed write scope |
| Gemini CLI | yes (Docker/Podman/seatbelt) | yes (default/auto-edit/plan/YOLO) | no | prompts + optional container |
| Aider | no | yes (y/n per shell command and unadded-file edit) | no | prompts |
| Goose | no | yes (four modes incl. smart approval) | partial — "smart approval" delegates judgment | prompts |
| OpenHands | yes (Docker/process/remote providers) | yes (always-ask default; --llm-approve option) | optional | container + prompts |
| Cline | partial (CLI env sandbox) | yes (per-category, YOLO mode) | no | prompts |
| Roo Code | no | yes (per-action auto-approve tiles, whitelists) | no | prompts |
| Qwen Code | yes (bwrap/Landlock/Docker/Seatbelt) | yes | no | sandbox available, prompts |
| Zed | partial (Agent terminal + fetch only; not LSPs/extensions/tasks) | yes | no | narrow sandbox |
| Continue | no | yes (permissions.yaml allow/ask/exclude) | no | prompts |
| Kilo Code | partial (Agent Manager /sandbox toggle) | yes (allow/ask/deny rules) | no | prompts |
| Copilot CLI | yes (experimental: Seatbelt/bubblewrap/base-container) | yes | no | prompts, sandbox opt-in |
| Crush | no | yes (per-call prompts, --yolo bypass) | no | prompts |
| Amazon Q CLI | no | yes (allowedTools globs, denyByDefault regexes) | no | prompts |
| Vibe | no | yes (per-tool ask/always/never, --yolo) | no | prompts |
| Factory Droid | yes (Seatbelt macOS; bubblewrap+seccomp Linux/WSL2; egress via domain-allowlist proxy) | yes (risk-labelled calls, Autonomy Levels Off/Low/Medium/High, permission rules) | partial — "Droid Shield" and Spec Mode gate edits before approval | sandbox by default, blocks rather than running without isolation |
| JetBrains Junie | yes (OS-level `/sandbox`, macOS/Linux only; `srt` in nightly/experimental macOS builds, on PATH for Linux) | yes (brave modes Off/Auto/On, `allowlist.json` rules, PermissionRequest hook) | optional — PermissionRequest hook can auto-allow/deny | prompts + allowlist, sandbox opt-in |
| Sourcegraph Amp | partial (orbs are sandboxed cloud VMs; local execution unsandboxed) | **no** — "By default, Amp does not ask for approval before running tools" | optional — policy plugins can gate tool calls; MCP allow/deny rules | **no local gate by default** |
| Cursor | yes (macOS Seatbelt, Linux user namespaces; docs: "Auto-review is not a security boundary") | yes (three run modes; Auto-review default; Allowlist; Run Everything) | yes — Auto-review is a classifier judging each command before it runs | classifier + sandbox, self-described as not a boundary |
| Windsurf / Devin Desktop | yes (bubblewrap+seccomp-style: bubblewrap + socat on Linux; hard-fails on Windows; fail-closed if sandbox tooling missing) | yes (Normal / Accept Edits / Smart / Bypass / Autonomous) | partial — Smart mode delegates the judgment to the model | fail-closed sandbox + prompts |
| Google Jules | yes (short-lived Ubuntu VM per task, server-side; FAQ warns the VM has internet access — treat as shared compute) | **no** — no per-command prompts exist; the human gate is plan approval, pause, delete | yes — a critic agent adversarially reviews every proposed change before it lands | cloud VM + plan-approval gate |
| Amazon Kiro | yes (per-task cloud sandbox for web/mobile/cloud sessions, configurable internet domains; headless Chrome inside) | yes (capability-based permissions.yaml: fs_read/fs_write/shell/mcp/subagent/skill; defaults to prompting when no policy exists) | no | prompts + per-task cloud sandbox |
| Devin | yes (isolated VM per session — Ubuntu, Windows or macOS; fail-closed if sandbox cannot resolve) | yes (Normal / Accept Edits / Smart / Bypass / Autonomous) | partial — Smart mode is model-judged | cloud VM + prompts |
| Augment Code | no (tool-permission rules are call-level controls, not an OS sandbox; enforcement documented for the CLI only, explicitly not the IDE extension) | yes (allow/deny/delegate permission rules with documented precedence) | no | permission rules, CLI-scoped |
| Tabnine | partial (CLI commands can run in OS-specific sandboxes with write and network controls; backends depend on OS and runtime) | yes (native-tool and MCP approvals: auto-approve, ask-first, disable; org MCP policies allow-all/remote-only/allow-list/block-all) | no | prompts + CLI sandbox — on a CLI in maintenance mode, deprecation planned after 2026-12-31 |
| Replit Agent | partial (background tasks run in isolated copies of the project; the interactive session's shell boundary is not documented) | yes (Plan Mode approval before file changes; paid actions require confirmation) | no | plan approval + paid-action confirmation, cloud environment |
| Qodo | n/a — Qodo does not execute shell commands; execution belongs to the host coding agent it plugs into | host agent's — Qodo's own gates are review standards checked during code review, not tool-call prompts | yes, but elsewhere — specialized review agents judge pull requests, not tool calls | review-layer over someone else's trust model |
| Bolt | unknown (project security checks documented; the execution boundary of the web environment was not established by the fetched pages) | partial (Plan Mode lets users review and revise plans, but approval before building is not documented as mandatory) | no | review-without-gate, web environment |

## What the table says

- **Prompts are the floor — with two exceptions, and the second is structural.** 26 of 30 ship permission prompts. **Sourcegraph Amp** documents that it does not ask for approval before running tools at all (gating only via policy plugins and MCP rules) — a hole by choice, in a local product. **Google Jules** has no per-command prompts either, but for the opposite reason: its loop runs in a cloud VM the user never touches, so per-command prompts are impossible by design; the human gate moves up to *plan approval*. The floor is not missing there, it relocated.
- **OS sandboxes are opt-in almost everywhere they exist locally — and mandatory in the cloud.** 8 of 30 have no OS-level sandbox at all (OpenCode, Aider, Goose, Roo Code, Continue, Crush, Amazon Q CLI, Vibe), Augment joins the permission-rules-without-sandbox camp, and Qodo does not belong on the axis at all — it executes nothing; 6 more have a partial one (Cline's CLI env sandbox, Kilo's `/sandbox` toggle, Zed's agent-terminal-and-fetch-only scope, Amp's cloud orbs, Tabnine's OS-specific CLI sandboxes, Replit's isolated task copies) (Cline's CLI env sandbox, Kilo's `/sandbox` toggle, Zed's agent-terminal-and-fetch-only scope, Amp's cloud orbs). Every cloud-autonomous row — Jules, Devin, Kiro's cloud sessions, Cursor's Cloud Agents — is VM-isolated by construction, and Windsurf/Devin Desktop and Devin are *fail-closed*: they refuse to start when sandbox tooling is missing. The split is clean: local harnesses treat the sandbox as a setting; cloud harnesses treat it as the product. Of those that do: Codex's scoped write sandbox and **Factory Droid's** kernel-level sandbox are on by default (Droid explicitly "blocks rather than running without isolation" when host primitives are unavailable); Claude Code's is off by default, Copilot's experimental, Gemini's flag-gated, Junie's macOS/Linux-only with a nightly-shipped helper, Amp's cloud-only (orbs) while local runs are unsandboxed.
- **Model review is no longer exotic — and in one product it is the main gate.** Claude Code's `auto` mode and **Cursor's Auto-review** (the default run mode) make a classifier the routine reviewer; Goose's "smart approval", OpenHands' `--llm-approve`, Junie's PermissionRequest hook, Droid's Shield and the Smart modes of Windsurf/Devin offer it as a mode. **Jules goes further: a critic agent adversarially reviews every proposed change** — with no per-command human prompt anywhere in the loop. Where the human left, a model was hired.
- **The closed-source rows cannot be audited, only quoted.** For Droid, Junie and Amp every claim above rests on a vendor doc page; there is no source to read the sandbox profile from. Treat their trust rows as vendor assertions, and note that Droid and Junie publish the *mechanism* (Seatbelt, bubblewrap+seccomp, `srt`) while Amp publishes only the boundary's absence locally and its presence in orbs.
- **v3.4 added a row that is not a harness.** Qodo ships capabilities *into* whichever coding agent you already run — its trust story is delegated by construction: the sandbox, the prompts and the execution boundary all belong to the host. A capability matrix that only lists execution harnesses misses an entire layer of the stack that is forming: review-and-standards vendors riding on other agents' trust models.
- **Scope honesty varies.** Zed documents precisely what its sandbox does *not* cover (LSPs, extensions, tasks, external agents). Most others describe what the sandbox does, not what escapes it. When choosing a harness for untrusted work, the "not covered" list is the specification.

## Choosing by failure mode

- Untrusted repo, arbitrary build scripts → require layer 1, on by default, with a documented escape list (Codex, OpenHands, Qwen, Zed-with-caveats).
- Trusted repo, routine drudgery → layer 2 with allow-lists beats layer 1 friction (OpenCode, Aider, Crush).
- Unattended runs → layer 2 rules plus layer 3 review, and read the classifier's failure literature first; a model reviewer is the only layer that can be wrong at scale without a prompt ever appearing.
- Work that must never touch your machine → a cloud-autonomous harness (Jules, Devin, Kiro cloud sessions): the VM is the boundary, and the boundary is someone else's computer — read what the VM can reach (Jules' FAQ says its VM has internet access and to treat it as shared compute) before pasting secrets into the repo.

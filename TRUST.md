# Trust models — how each harness bounds what the agent may do

As of 2026-10-05, 20 harnesses. Sources: the sandboxing and hooks rows on each [harness page](harnesses/), which carry their own evidence URLs.

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

## What the table says

- **Prompts are the floor — with one exception.** 19 of 20 ship permission prompts; **Sourcegraph Amp** documents that it does not ask for approval before running tools at all, and offers gating only through policy plugins and MCP allow/deny rules. The universal floor has its first hole, and it is in a closed-source product where the plugin code is the only inspection point.
- **OS sandboxes are opt-in almost everywhere they exist.** 8 of 20 have no OS-level sandbox at all (OpenCode, Aider, Goose, Roo Code, Continue, Crush, Amazon Q CLI, Vibe) and 4 more have a partial one (Cline's CLI env sandbox, Kilo's `/sandbox` toggle, Zed's agent-terminal-and-fetch-only scope, Amp's cloud orbs). Of those that do: Codex's scoped write sandbox and **Factory Droid's** kernel-level sandbox are on by default (Droid explicitly "blocks rather than running without isolation" when host primitives are unavailable); Claude Code's is off by default, Copilot's experimental, Gemini's flag-gated, Junie's macOS/Linux-only with a nightly-shipped helper, Amp's cloud-only (orbs) while local runs are unsandboxed.
- **Model review is exactly one default.** Claude Code's `auto` mode makes a classifier the routine reviewer; Goose's "smart approval", OpenHands' `--llm-approve`, Junie's PermissionRequest hook and Droid's Shield offer it as a mode or gate. Everyone else keeps the human in the loop by default — or, in Amp's case, keeps nothing.
- **The closed-source rows cannot be audited, only quoted.** For Droid, Junie and Amp every claim above rests on a vendor doc page; there is no source to read the sandbox profile from. Treat their trust rows as vendor assertions, and note that Droid and Junie publish the *mechanism* (Seatbelt, bubblewrap+seccomp, `srt`) while Amp publishes only the boundary's absence locally and its presence in orbs.
- **Scope honesty varies.** Zed documents precisely what its sandbox does *not* cover (LSPs, extensions, tasks, external agents). Most others describe what the sandbox does, not what escapes it. When choosing a harness for untrusted work, the "not covered" list is the specification.

## Choosing by failure mode

- Untrusted repo, arbitrary build scripts → require layer 1, on by default, with a documented escape list (Codex, OpenHands, Qwen, Zed-with-caveats).
- Trusted repo, routine drudgery → layer 2 with allow-lists beats layer 1 friction (OpenCode, Aider, Crush).
- Unattended runs → layer 2 rules plus layer 3 review, and read the classifier's failure literature first; a model reviewer is the only layer that can be wrong at scale without a prompt ever appearing.

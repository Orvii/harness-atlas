# Trust models — how each harness bounds what the agent may do

As of 2026-10-05, 17 harnesses. Sources: the sandboxing and hooks rows on each [harness page](harnesses/), which carry their own evidence URLs.

## The three layers

Every trust story in this set reduces to three mechanisms, used in different combinations:

1. **OS-level sandbox** — the operating system enforces a boundary around commands (Seatbelt, bubblewrap, Landlock, Docker, Mach-service allowlists).
2. **Permission prompts** — a human approves each tool call or category of calls, optionally with allow/deny rule lists.
3. **Model review** — a second model (classifier or LLM approver) judges actions instead of, or before, the human.

The capability matrix marks `sandboxing` yes/partial; this page says *which layer* that yes is made of, because the layers fail differently. An OS sandbox fails closed against the filesystem but sees nothing about intent; a prompt fails open the moment the user habitually clicks yes; a model reviewer fails silently, at scale, in the direction of its training.

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

## What the table says

- **Prompts are the universal floor.** All 17 ship them; 15 of 17 have no OS sandbox by default. The floor is a human clicking.
- **OS sandboxes are opt-in everywhere they exist.** Codex's scoped write sandbox is the notable exception in default posture; Claude Code's is off by default, Copilot's experimental, Gemini's flag-gated.
- **Model review is exactly one default.** Claude Code's `auto` mode makes a classifier the routine reviewer; Goose's "smart approval" and OpenHands' `--llm-approve` offer it as a mode. Everyone else keeps the human in the loop by default — or keeps nothing.
- **Scope honesty varies.** Zed documents precisely what its sandbox does *not* cover (LSPs, extensions, tasks, external agents). Most others describe what the sandbox does, not what escapes it. When choosing a harness for untrusted work, the "not covered" list is the specification.

## Choosing by failure mode

- Untrusted repo, arbitrary build scripts → require layer 1, on by default, with a documented escape list (Codex, OpenHands, Qwen, Zed-with-caveats).
- Trusted repo, routine drudgery → layer 2 with allow-lists beats layer 1 friction (OpenCode, Aider, Crush).
- Unattended runs → layer 2 rules plus layer 3 review, and read the classifier's failure literature first; a model reviewer is the only layer that can be wrong at scale without a prompt ever appearing.

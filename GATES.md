# Gates — the layer between "documented" and "shipped"

As of 2026-10-06. Capability rows answer "does the doc describe it?". This page answers the next question: **behind what gate?** A feature can be documented, real, and still unreachable without a flag, a plan tier, an OS, or a prayer. Sources: the limitations notes on each harness page.

## The gate types we found

1. **Env/flag gates** — off until you set something: Claude Code agent teams (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`), Codex memories (`[features] memories = true`), OpenCode Wayland (`OC_ALLOW_WAYLAND=1`), Kilo memory (per-project opt-in), Junie OS-level `/sandbox` (macOS/Linux only, `srt` shipped in nightly/experimental macOS builds and required on `PATH` for Linux), Junie subagent model-selection (Early Access build).
2. **Tier gates** — plan or payment: Claude Code computer use (Pro/Max only), Copilot Memory (paid preview), OpenHands cloud session limits, Amp Enterprise (SSO/SCIM, audit, per-user spend limits, workspace entitlements with per-user quotas), Junie Remote mode (requires a JetBrains Account or `JUNIE_API_KEY` — BYOK alone is insufficient, and unavailable under AI Enterprise sign-in).
3. **OS gates** — Claude Code sandbox (no native Windows/WSL1), Codex sandbox (WSL1 dropped at 0.115, bwrap required), Gemini CLI (macOS 15+/Win11 24H2+), Copilot sandbox tiers per OS, Goose extensions (Linux/macOS only for Java/Kotlin), Amp on Windows (WSL only), Junie Local (macOS 26+, Apple Silicon M5+, 64 GB RAM), Factory Droid sandbox (host kernel primitives required — it blocks rather than running without isolation), Windsurf/Devin sandbox (hard-fails on Windows; Linux needs bubblewrap + socat), Devin sandbox (same Windows/Linux constraints), Jules concurrency (60 parallel tasks only on the Ultra plan).
4. **Maturity labels** — "experimental", "preview", "beta", "research preview": Cline subagents (read-only, experimental), Kanban (preview), Roo's Experimental tier (docs warn of data loss), Crush hooks (PreToolUse only, rest in FUTURE.md), Copilot extensions (JS-only, experimental), Qwen serve (alpha, attachments deferred), the whole Junie CLI (EAP), Junie custom subagents (cannot be invoked manually), Google Jules' REST API (self-labelled `v1alpha`), Cursor JetBrains integration (paid plan + AI Assistant 2025.1+).
5. **Deprecation gates** — the inverse: documented but leaving. Kilo Orchestrator mode and Console deprecated; Goose plan mode removed after being promoted; Amazon Q CLI discontinued in favor of Kiro CLI; Amp deletes features outright under a stated "no backward compatibility" posture (Amp Tab completion, custom commands replaced by skills); Factory Droid deprecates `droid exec` stream-json input mode; Amazon Q CLI's successor Kiro replaces 2.x trust flags with `permissions.yaml` in CLI 3.0.

## A seventh kind: the locality gate

v3.3's cloud-autonomous rows add a gate the local rows never had: **the loop is not on your machine**, so the controls you would reach for locally do not exist.

- **No per-command prompt is possible** in Jules — the human gate is plan approval, pause, delete. A row that reads `sandboxing ✅` there means "VM-per-task", not "you were asked".
- **The sandbox is fail-closed** in Windsurf/Devin Desktop and Devin: the product refuses to start when sandbox tooling is missing. That is a gate in the reader's favour, and the opposite of opt-in.
- **The VM reaches the internet.** Jules' FAQ says so and warns to treat the VM like shared compute. For these rows the gate to check is not "is there a sandbox" but "what can the sandbox reach".

## A sixth kind: the closed-source gate

Fourteen rows now have no public product repo — v3.2's **Sourcegraph Amp**, **Factory Droid**, **JetBrains Junie**, v3.3's **Cursor**, **Windsurf/Devin Desktop**, **Google Jules**, **Amazon Kiro**, **Devin**, v3.4's **Replit**, and v3.5's **Trae**, **Google Antigravity**, **Qoder**, **Lovable** and **v0** — so their gates cannot be checked against code. (Mistral Vibe sits at the edge of this list: its product ships from the public repo `mistralai/mistral-vibe`; only the `mistralai/vibe` spelling of the URL 404s.) Two consequences the open rows do not have:

- **The gate's implementation is unreadable.** Droid documents kernel-level isolation (Seatbelt; bubblewrap+seccomp; a domain-allowlist egress proxy) and Junie documents an OS-level `/sandbox`, but neither profile is in a repo you can read. The gate is a vendor assertion.
- **Deprecation arrives without a diff.** Amp's stated posture is "no backward compatibility": features are removed and announced in a chronicle post. A capability cell for a closed product should be treated as having a shorter half-life than an identical-looking cell for an open one, even on the same snapshot date.

## Why the gate layer matters more than the capability layer

- **Benchmarks and reviews routinely measure gated features as if default.** A "Claude Code supports agent teams" headline without the env flag is a description of a research preview.
- **Security posture lives here.** Roo's Experimental tier warns of data loss; Crush's config is "trusted code" with shell privileges; Vibe's protected-path interception is "a heuristic, not a boundary". A trust decision made from the capability row alone misses the sentence that says what the boundary is not.
- **Deprecation is a gate with a countdown.** Amazon Q's docs now 301-redirect to Kiro: the capability exists in the repo and not in the product. Only dated snapshots catch that state.

## Reading rule

When a cell says ✅ or ◐, check the row's limitations note for a gate. If the gate is a flag you must set, the honest sentence is "supports X when configured"; if it is a tier, "supports X for paying users"; if it is a maturity label, "supports X in preview". The atlas keeps cells binary and gates in notes on purpose: a matrix of five-valued cells would be unreadable, and the notes are where the truth fits.

## An eighth kind: the gate that opens under automation

v3.4's rows surface a gate failure mode the local cluster never had: **the approval gate that silently disables itself when no human is watching.**

- **Tabnine CLI Plan Mode** presents a plan for approval — except in headless or CI use, where "the plan tools are auto-approved and execution switches to YOLO mode". The same product, the same flag: a gate for the human, none for the pipeline. Any benchmark or CI harness measuring Tabnine's "plan mode" is measuring YOLO.
- **Bolt Plan Mode** lets a user review and revise a plan — but the homepage flow creates the app's base structure *before* presenting the plan, and approval before building is not documented as mandatory. The gate exists after the first irreversible act.
- **Replit's Plan Mode** is billable: reviewing before building costs the same currency as building. A gate with a price is a gate some users will skip by arithmetic.
- **Augment's permission rules** apply to the CLI and explicitly not to the IDE extension — the gate's coverage depends on which door you walked in through.
- **Trae's Auto-Run** is the plainest case yet, and the vendor writes the warning itself. The sandbox is opt-in, its allowlisted prefixes "bypass the sandbox and execute directly outside the sandbox", and a separate Auto-Run switch removes confirmation entirely: "It is recommended not to enable 'Auto Run' mode unless necessary. This mode bypasses all security checks and may result in high-risk operations being executed without warning." An interactive session has a directory policy, an opt-in sandbox and a plan-confirmation gate; a pipeline configured with Auto-Run has none of the three. Note also what this does to measurement: a benchmark that reports Trae's "plan mode" or "sandbox" while Auto-Run is enabled is reporting a configuration in which both are switched off.

The reading rule from §1 still holds, sharpened: when a cell says ✅ or ◐ on `plan_mode` or `sandboxing`, ask *under which invocation* the gate exists. A gate that is present interactively and absent in automation is not a control; it is a courtesy. Five rows now carry one (Tabnine, Bolt, Replit, Augment, Trae) — enough that the question is no longer an edge case but a standing item on the audit list in [VERIFYING.md](VERIFYING.md).

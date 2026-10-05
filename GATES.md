# Gates — the layer between "documented" and "shipped"

As of 2026-10-05. Capability rows answer "does the doc describe it?". This page answers the next question: **behind what gate?** A feature can be documented, real, and still unreachable without a flag, a plan tier, an OS, or a prayer. Sources: the limitations notes on each harness page.

## The gate types we found

1. **Env/flag gates** — off until you set something: Claude Code agent teams (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`), Codex memories (`[features] memories = true`), OpenCode Wayland (`OC_ALLOW_WAYLAND=1`), Kilo memory (per-project opt-in), Junie OS-level `/sandbox` (macOS/Linux only, `srt` shipped in nightly/experimental macOS builds and required on `PATH` for Linux), Junie subagent model-selection (Early Access build).
2. **Tier gates** — plan or payment: Claude Code computer use (Pro/Max only), Copilot Memory (paid preview), OpenHands cloud session limits, Amp Enterprise (SSO/SCIM, audit, per-user spend limits, workspace entitlements with per-user quotas), Junie Remote mode (requires a JetBrains Account or `JUNIE_API_KEY` — BYOK alone is insufficient, and unavailable under AI Enterprise sign-in).
3. **OS gates** — Claude Code sandbox (no native Windows/WSL1), Codex sandbox (WSL1 dropped at 0.115, bwrap required), Gemini CLI (macOS 15+/Win11 24H2+), Copilot sandbox tiers per OS, Goose extensions (Linux/macOS only for Java/Kotlin), Amp on Windows (WSL only), Junie Local (macOS 26+, Apple Silicon M5+, 64 GB RAM), Factory Droid sandbox (host kernel primitives required — it blocks rather than running without isolation).
4. **Maturity labels** — "experimental", "preview", "beta", "research preview": Cline subagents (read-only, experimental), Kanban (preview), Roo's Experimental tier (docs warn of data loss), Crush hooks (PreToolUse only, rest in FUTURE.md), Copilot extensions (JS-only, experimental), Qwen serve (alpha, attachments deferred), the whole Junie CLI (EAP), Junie custom subagents (cannot be invoked manually).
5. **Deprecation gates** — the inverse: documented but leaving. Kilo Orchestrator mode and Console deprecated; Goose plan mode removed after being promoted; Amazon Q CLI discontinued in favor of Kiro CLI; Amp deletes features outright under a stated "no backward compatibility" posture (Amp Tab completion, custom commands replaced by skills); Factory Droid deprecates `droid exec` stream-json input mode.

## A sixth kind: the closed-source gate

Three rows — **Sourcegraph Amp**, **Factory Droid**, **JetBrains Junie** — have no public product repo, so their gates cannot be checked against code. Two consequences the open rows do not have:

- **The gate's implementation is unreadable.** Droid documents kernel-level isolation (Seatbelt; bubblewrap+seccomp; a domain-allowlist egress proxy) and Junie documents an OS-level `/sandbox`, but neither profile is in a repo you can read. The gate is a vendor assertion.
- **Deprecation arrives without a diff.** Amp's stated posture is "no backward compatibility": features are removed and announced in a chronicle post. A capability cell for a closed product should be treated as having a shorter half-life than an identical-looking cell for an open one, even on the same snapshot date.

## Why the gate layer matters more than the capability layer

- **Benchmarks and reviews routinely measure gated features as if default.** A "Claude Code supports agent teams" headline without the env flag is a description of a research preview.
- **Security posture lives here.** Roo's Experimental tier warns of data loss; Crush's config is "trusted code" with shell privileges; Vibe's protected-path interception is "a heuristic, not a boundary". A trust decision made from the capability row alone misses the sentence that says what the boundary is not.
- **Deprecation is a gate with a countdown.** Amazon Q's docs now 301-redirect to Kiro: the capability exists in the repo and not in the product. Only dated snapshots catch that state.

## Reading rule

When a cell says ✅ or ◐, check the row's limitations note for a gate. If the gate is a flag you must set, the honest sentence is "supports X when configured"; if it is a tier, "supports X for paying users"; if it is a maturity label, "supports X in preview". The atlas keeps cells binary and gates in notes on purpose: a matrix of five-valued cells would be unreadable, and the notes are where the truth fits.

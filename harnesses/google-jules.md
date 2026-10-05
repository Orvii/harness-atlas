# Google Jules

- **repo:** Google (closed-source cloud service; no public repository)
- **version pin:** `No public product semver (closed source). Latest published CLI package: @google/jules 0.1.42 (published 2025-12-16); REST API self-labeled alpha (v1alpha); docs changelog newest entry 2026-03-09` — Closed-source cloud product, so versioning comes from vendor artifacts rather than a release tag: the npm registry dist-tag for the official CLI (@google/jules latest = 0.1.42, registry.npmjs.org), the API reference's own wording that the "Jules REST API is in an alpha release" (developers.google.com/jules/api), and the docs changelog at jules.google/docs/changelog/, whose newest entry is March 9, 2026 (Gemini 3.1 Pro). No public source repository exists, so no commit- or tag-based pin is possible.
- **docs home:** https://jules.google/docs/

## What it promises

Jules “does coding tasks you don’t want to do”: pick a GitHub repo and branch, write a prompt, and it “works autonomously — so you can move on while it handles the task.” The landing page scales that promise to “fully async, multi-agent development,” with higher plans unlocking more parallel agent capacity (60 concurrent tasks on Ultra).

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ◐ partial | Multi-agent only internally: a critic agent adversarially reviews every proposed change and a planning critic vets auto-approved plans, but users cannot define, spawn, or address subagents, and there is no fan-in construct inside a task. | [src](https://jules.google/docs/changelog/) |
| workflow_orchestration | ◐ partial | Scripting primitives exist (REST API sessions/activities, scheduled tasks, CLI --parallel capped at 5 runs of one prompt), but there is no built-in DAG, team, or swarm construct; orchestration logic lives in the caller's own scripts and pipelines. | [src](https://jules.google/docs/api/reference/) |
| mcp | ◐ partial | MCP client support with API-key authentication configured in Settings, launched February 2, 2026. Only hand-picked servers are accepted — the announcement says the restriction is deliberate ('we are wanted to start with a focus on security') and 'We plan to expand this list' — so there is no bring-your-own or local MCP server support, and the docs site has no MCP page. | [src](https://jules.google/docs/changelog/) |
| hooks_lifecycle | ✗ no | The official docs enumerate no lifecycle hooks (pre/post tool, session start/end). The closest analogues are timers and event triggers: scheduled tasks (daily/weekly/monthly), proactive suggested-task scanning, a CI fixer that reacts to failed GitHub Actions checks on Jules PRs, and a Render integration that wakes Jules on deployment failures — none user-programmable as a hook. | [src](https://jules.google/docs/) |
| skills | ✗ no | Repository instructions live in AGENTS.md, plus per-repo memory; the home page offers static sample prompts and the changelog points to a community 'Jules Awesome Prompts' repo. No invocable, user-authored skill or prompt-pack system with progressive loading is documented. | [src](https://jules.google/docs/) |
| memory_persistence | ✅ yes | Per-repository memory (September 30, 2025) saves preferences, nudges, and corrections during a task and replays them on similar future tasks in that repo; the toggle lives in repo settings under 'Knowledge'. Gemini 3 Pro release notes also tout 'agentic memories'. Scope is repository-level preference memory, not a user-browsable memory store. | [src](https://jules.google/docs/changelog/) |
| sandboxing | ✅ yes | Isolation is VM-per-task, each with its own logs, environment setup, and code changes; the FAQ adds that the VM has internet access and warns to treat it with the caution of public or shared compute. There are no per-command permission prompts or local permission modes — the human gate is plan approval plus pause/delete. | [src](https://jules.google/docs/environment/) |
| plan_mode | ✅ yes | Plans are reviewed, edited via chat, and approved before any code is written; an Interactive Plan mode asks clarifying questions first. If you navigate away, 'Jules will eventually auto-approve the plan, which is set on a timer' — auto-approved plans get vetted by the Planning Critic instead of a human. | [src](https://jules.google/docs/review-plan/) |
| background_tasks | ✅ yes | Fully asynchronous by design: tasks run in background cloud VMs, notify you when a plan is ready or a task completes, support multiple simultaneous tasks 'running in the background', plus scheduled recurring tasks and proactive suggested tasks. A task can also be started and kept running while you navigate elsewhere in the app. | [src](https://jules.google/docs/faq/) |
| ide_integration | ✗ no | Official surfaces are the web app, the GitHub app ('Google Labs Jules'), the Jules Tools CLI with a TUI, and the REST API; the docs enumerate no VS Code or JetBrains extension. Reporting at the CLI/API launch (TechCrunch, fetched during research) said Google was 'keen to build specific plug-ins for IDE' third parties — planned, not shipped; third parties can call the API from their own IDE tooling. | [src](https://jules.google/docs/) |
| model_agnostic | ✗ no | Gemini-only: 2.5 Pro at launch, Gemini 3 Pro and 3.1 Pro for paid tiers, and Gemini 3 Flash as the base model for all users on all tiers (January 30, 2026). No other model provider and no bring-your-own-model option is documented. | [src](https://jules.google/docs/usage-limits/) |
| plugins | ✗ no | No third-party plugin or extension API and no marketplace. Integration coverage is first-party (Render deployment logs; a GitHub Actions CI fixer) and runs read-only by default; MCP is the nearest third-party surface but is restricted to six vetted servers. Stitch's scheduled-task templates are prompt presets, not plug-ins. | [src](https://jules.google/docs/integrations/) |
| session_resume | ✅ yes | Tasks can be paused and resumed, reopened from the repo view 'to review the plan, or continue feedback', listed via the CLI ('jules remote list --session' shows 'all active and past sessions'), enumerated through the REST API's ListSessions, and rerun from the summary view after failures. | [src](https://jules.google/docs/tasks-repos/) |
| cost_controls | ◐ partial | Hard plan quotas: 15/100/300 daily tasks and 3/15/60 concurrent tasks for free/Pro/Ultra, on a rolling 24-hour window, with the new-task button disabled at the cap. No token, credit, or dollar spend tracking or visibility is documented. | [src](https://jules.google/docs/usage-limits/) |

## Architecture

Jules is a cloud-autonomous agent: the plan-execute loop runs server-side in Google Cloud, not on the developer's machine. Each task gets its own secure, short-lived Ubuntu VM (20 GB disk, internet access, preinstalled Node.js, Bun, Python, Go, Java, Rust, Docker, Playwright); Jules clones the repository there, runs setup scripts and tests, and reuses environment snapshots for speed. The web app, GitHub app, npm-published CLI, and v1alpha REST API are thin submit, monitor, and pull-patch surfaces. After plan approval, an internal critic reviews changes before a branch or PR is published. Sources: jules.google/docs/environment/, jules.google/docs/cli/reference/, developers.google.com/jules/api, jules.google.

## Context management

No token window or budget is published; context is managed server-side. Jules clones the full repository into each task VM and reads AGENTS.md plus README hints for conventions, setup, and test commands. User-facing context knobs are narrow: a file selector to pin specific files, non-code visual attachments (PNG/JPEG under 5 MB, only at task creation), autonomous web search for current library documentation, environment snapshots, and opt-in repository memory that carries preferences between similar tasks. Changelog entries advertise “smarter context” and Gemini 3’s agentic memories but quantify nothing. Sources: jules.google/docs/running-tasks/, jules.google/docs/environment/, jules.google/docs/changelog/.

## Ecosystem

Distribution runs through a GitHub app (Google Labs Jules) that also picks up issues labeled “jules”, the web app, the npm-published Jules Tools CLI (@google/jules) with a TUI, side-by-side diffs, repo inference, and shell completions, and the v1alpha REST API for Slack, Linear, Jira, or CI pipelines. Extension points are deliberately narrow: first-party integrations such as Render deployment logs and a GitHub Actions CI fixer, plus six hand-picked MCP servers (Linear, Stitch, Neon, Tinybird, Context7, Supabase) configured with API keys. Repository customization uses AGENTS.md, memory, and scheduled-task templates; a community “Jules Awesome Prompts” repo supplies prompt examples. Sources: jules.google/docs/integrations/, jules.google/docs/cli/reference/, jules.google/docs/changelog/, jules.google/docs/.

## Governance

Jules is closed source, built and operated by Google under Google Labs (GitHub app: “Google Labs Jules”), with no public repository or community license. It was previewed December 2024, entered public beta May 2025, and left beta August 6, 2025; no acquisitions feature in its history. Commercial access bundles with Google AI Pro/Ultra subscriptions (a free tier exists), paid tiers initially restricted to @gmail.com accounts, minimum age 18. Vendor commitments: no model training on private repositories, encrypted integration keys, API keys auto-disabled if exposed, maximum three keys. Sources: blog.google/innovation-and-ai/models-and-research/google-labs/jules/, jules.google/docs/usage-limits/, jules.google/docs/faq/, jules.google/docs/api/reference/.

## Limitations

GitHub is the only supported version-control provider (“In the future, Jules will work with more version control systems”). Long-lived processes like npm run dev are unsupported in setup scripts. The REST API is alpha and may change; MCP has no bring-your-own servers; suggested tasks cap at five repositories; image attachments work only at task creation; quotas gate everything (15/100/300 daily tasks, 3/15/60 concurrent). Paid plans were @gmail.com-only at launch, age 18+. Documentation drift observed during research: the FAQ still says “Public Beta”, the scheduled-tasks page contradicts the newer changelog on editing, and the plan table still lists Gemini 2.5 Pro. The legacy developers.google.com/jules landing path 404s; the newest changelog entry is March 9, 2026.

## In its own words

> Jules is an experimental coding agent that helps you fix bugs, add documentation, and build new features. It integrates with GitHub, understands your codebase, and works autonomously — so you can move on while it handles the task.  
> — [https://jules.google/docs/](https://jules.google/docs/)

> Jules runs each task inside a secure, short-lived virtual machine (VM). This lets it clone your repository, install dependencies, and run tests.  
> — [https://jules.google/docs/environment/](https://jules.google/docs/environment/)

> Once you start a task in Jules, it generates a plan before writing any code. This lets you know the direction Jules will take while it works on the task.  
> — [https://jules.google/docs/review-plan/](https://jules.google/docs/review-plan/)

> Jules is private by default, it doesn’t train on your private code, and your data stays isolated within the execution environment.  
> — [https://blog.google/innovation-and-ai/models-and-research/google-labs/jules/](https://blog.google/innovation-and-ai/models-and-research/google-labs/jules/)


## Notable

For a product promising “fully async, multi-agent development”, the surprise is how closed its extension story is: MCP is limited to six hand-picked servers with no bring-your-own option, there is no plugin API or IDE extension, and the only fan-out primitive is a CLI flag capped at five parallel runs of one prompt.

## Sources fetched

- https://jules.google/docs/
- https://jules.google/docs/environment/
- https://jules.google/docs/running-tasks/
- https://jules.google/docs/review-plan/
- https://jules.google/docs/scheduled-tasks/
- https://jules.google/docs/suggested-tasks/
- https://jules.google/docs/tasks-repos/
- https://jules.google/docs/repo/
- https://jules.google/docs/code/
- https://jules.google/docs/errors/
- https://jules.google/docs/usage-limits/
- https://jules.google/docs/faq/
- https://jules.google/docs/integrations/
- https://jules.google/docs/guides/continuous-ai-overview
- https://jules.google/docs/changelog/
- https://jules.google/docs/api/reference/
- https://jules.google/docs/cli/reference/
- https://developers.google.com/jules/api
- https://blog.google/innovation-and-ai/models-and-research/google-labs/jules/
- https://techcrunch.com/2025/10/02/googles-jules-enters-developers-toolchains-as-ai-coding-agent-competition-heats-up/
- https://registry.npmjs.org/@google/jules
- https://jules.google/

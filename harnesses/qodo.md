# Qodo

- **repo:** https://github.com/qodo-ai/command
- **version pin:** `Qodo 3.0 (vendor release label, changelog entry 2026-10-01)` — vendor changelog https://docs.qodo.ai/changelog — the deprecated Command CLI's GitHub releases page lists no releases and the npm page returned 403, so the vendor release label is the pin and is labelled as such
- **docs home:** https://docs.qodo.ai

## What it promises

Qodo presents Agentic Toolbox as bringing code understanding, coding standards, and review capabilities into an existing coding agent. Its Code Review documentation promises pull-request analysis using specialized agents and context beyond isolated diffs. The platform documentation presents repository and review context as supporting architectural, impact, and root-cause analysis.

## Capabilities

| capability | support | note | evidence |
|---|---|---|---|
| subagents | ? unknown | The review documentation describes specialized agents reviewing pull requests, but does not document a user-facing way to spawn child agents. | [src](https://docs.qodo.ai/code-review/overview) |
| workflow_orchestration | ◐ partial | The documentation offers suggested workflows as adaptable examples; it does not describe multi-agent orchestration primitives such as DAGs, teams, or swarms. | [src](https://docs.qodo.ai/agentic-toolbox/agentic-toolbox-suggested-workflows) |
| mcp | ✅ yes | Agentic Toolbox exposes workspace-managed skills to MCP clients over Streamable HTTP; clients must support Streamable HTTP and custom headers. | [src](https://docs.qodo.ai/agentic-toolbox/mcp) |
| hooks_lifecycle | ? unknown | The tools reference does not document lifecycle hooks such as pre/post-tool or session-start/stop hooks. | [src](https://docs.qodo.ai/agentic-toolbox/qodo-tools-reference) |
| skills | ✅ yes | Agentic Toolbox provides managed reusable skills for codebase understanding, review, review resolution, rules, and standards. | [src](https://docs.qodo.ai/agentic-toolbox/agentic-toolbox-overview) |
| memory_persistence | ? unknown | The Context Engine uses repository, review, and standards context, but the documentation does not specify persistent cross-session memory or retention. | [src](https://docs.qodo.ai/core-concepts/context-engine) |
| sandboxing | ? unknown | The CLI installation documentation does not describe command sandboxing or permission modes. | [src](https://docs.qodo.ai/agentic-toolbox/cli) |
| plan_mode | ? unknown | The CLI documentation does not describe an explicit plan-then-approve mode. | [src](https://docs.qodo.ai/agentic-toolbox/cli) |
| background_tasks | ? unknown | The CLI documentation does not describe user-facing background or asynchronous task execution. | [src](https://docs.qodo.ai/agentic-toolbox/cli) |
| ide_integration | ✅ yes | The platform overview says Qodo integrates with IDEs, pull requests, and command-line tools; it does not name VS Code or JetBrains extensions specifically. | [src](https://docs.qodo.ai/core-concepts/qodo-platform-overview) |
| model_agnostic | ? unknown | The reviewed documentation does not establish support for multiple model providers. | [src](https://docs.qodo.ai/agentic-toolbox/cli) |
| plugins | ? unknown | Qodo documents its own integrations, including Claude Code and Codex plugins, but does not describe a third-party plugin or extension API. | [src](https://docs.qodo.ai/agentic-toolbox/claude-code-plugin) |
| session_resume | ? unknown | The tools reference includes PR review-session findings, but does not document resuming previous coding-agent sessions. | [src](https://docs.qodo.ai/agentic-toolbox/qodo-tools-reference) |
| cost_controls | ? unknown | The tools reference does not document token or cost tracking or limits. | [src](https://docs.qodo.ai/agentic-toolbox/qodo-tools-reference) |

## Architecture

Qodo's platform architecture describes ingestion, knowledge storage, and agentic research layers. Ingestion uses parsing and AST chunking; the knowledge layer includes graph and vector databases, PR and commit history, and generated Markdown. Research tools use shared context ranking, while code review uses specialized agents. Agentic Toolbox is a separate product that supplies Qodo capabilities through a CLI, MCP, and coding-agent integrations; the docs explicitly distinguish it from the deprecated Qodo Command CLI. (https://docs.qodo.ai/core-concepts/qodo-platform-architecture, https://docs.qodo.ai/agentic-toolbox/agentic-toolbox-overview)

## Context management

The Context Engine documentation describes context from code intelligence, review history, organizational standards, repository knowledge and patterns, agent interactions, and SKILL.md definitions. Codebase Wisdom also uses repository relationships, pull-request history, and current Git state. The docs say the Context Engine evolves as codebases and standards change, but do not give a refresh schedule, retention policy, or persistent conversation-memory behavior. (https://docs.qodo.ai/core-concepts/context-engine, https://docs.qodo.ai/agentic-toolbox/agentic-toolbox-codebase-wisdom-skill)

## Ecosystem

Agentic Toolbox documents CLI, MCP, Claude Code, Codex, and Kiro integrations. The platform overview describes IDE, pull-request, and command-line integration; the installation matrix names GitHub, GitLab, Bitbucket Cloud and Data Center, and Azure DevOps. The MCP integration requires Streamable HTTP and custom headers, and access to managed skills depends on workspace permissions. (https://docs.qodo.ai/agentic-toolbox/agentic-toolbox-overview, https://docs.qodo.ai/agentic-toolbox/mcp, https://docs.qodo.ai/core-concepts/qodo-platform-overview, https://docs.qodo.ai/install-qodo/install)

## Governance

Qodo describes Review Standards as explicit rules checked during code review and offers rule creation from natural-language descriptions, supported files, or pull-request history. Governance documentation covers standards across repositories, teams, and services. Admin changes can become active immediately; changes from other users may be submitted as pending suggestions for approval. (https://docs.qodo.ai/governance/rule-enforcement, https://docs.qodo.ai/governance, https://docs.qodo.ai/agentic-toolbox/manage-standards-skill)

## Limitations

The largest distinction is product status: current docs call Qodo Command deprecated and Agentic Toolbox a separate product; the changelog labels Qodo Merge 1.5.0 as a 2025 release and identifies Qodo Review in newer releases. The selected Qodo 3.0 version is therefore the latest vendor release label, not a version for the deprecated CLI. The npm package page returned HTTP 403, so no current npm dist-tag or package version was verified; the Command GitHub releases page reported no releases. The docs reviewed did not answer whether Qodo supports user-spawned subagents, persistent memory, sandboxing, explicit plan approval, background tasks, multiple model providers, a third-party extension API, session resume, or cost controls; those remain unknown.

## In its own words

> The Agentic Toolbox is a separate product from the deprecated Qodo Command CLI (`@qodo/command`) and Qodo Gen CLI.  
> — [https://docs.qodo.ai/agentic-toolbox/agentic-toolbox-overview](https://docs.qodo.ai/agentic-toolbox/agentic-toolbox-overview)

> The Qodo Agentic Toolbox brings Qodo's code understanding, coding standards, and review capabilities into your existing coding agent.  
> — [https://docs.qodo.ai/agentic-toolbox/agentic-toolbox-overview](https://docs.qodo.ai/agentic-toolbox/agentic-toolbox-overview)

> Qodo analyzes pull requests using specialized review agents that evaluate code from multiple perspectives.  
> — [https://docs.qodo.ai/code-review/overview](https://docs.qodo.ai/code-review/overview)

> The workflows below are examples you can use as a starting point and adapt to your development process.  
> — [https://docs.qodo.ai/agentic-toolbox/agentic-toolbox-suggested-workflows](https://docs.qodo.ai/agentic-toolbox/agentic-toolbox-suggested-workflows)


## Notable

The vendor's current documentation explicitly calls Qodo Command deprecated, while describing Agentic Toolbox as a separate product rather than a renamed CLI. The available evidence supports Qodo-managed agent integrations and review workflows more clearly than the requested standalone harness controls such as memory, sandboxing, session resume, or cost limits.

## Sources fetched

- https://docs.qodo.ai
- https://docs.qodo.ai/llms.txt
- https://docs.qodo.ai/agentic-toolbox/agentic-toolbox-overview
- https://docs.qodo.ai/agentic-toolbox/cli
- https://docs.qodo.ai/agentic-toolbox/mcp
- https://docs.qodo.ai/agentic-toolbox/agentic-toolbox-suggested-workflows
- https://docs.qodo.ai/agentic-toolbox/qodo-tools-overview
- https://docs.qodo.ai/agentic-toolbox/qodo-tools-reference
- https://docs.qodo.ai/agentic-toolbox/claude-code-plugin
- https://docs.qodo.ai/agentic-toolbox/agentic-toolbox-codebase-wisdom-skill
- https://docs.qodo.ai/agentic-toolbox/agentic-toolbox-codebase-review-skill
- https://docs.qodo.ai/agentic-toolbox/agentic-toolbox-get-rules-skill
- https://docs.qodo.ai/agentic-toolbox/agentic-toolbox-review-resolver-skill
- https://docs.qodo.ai/agentic-toolbox/reviewer-skill
- https://docs.qodo.ai/agentic-toolbox/get-rules
- https://docs.qodo.ai/agentic-toolbox/manage-standards-skill
- https://docs.qodo.ai/agentic-toolbox/review-resolver
- https://docs.qodo.ai/agentic-toolbox/manage-standards-skill
- https://docs.qodo.ai/agentic-toolbox/codex-plugin
- https://docs.qodo.ai/core-concepts/qodo-platform-overview
- https://docs.qodo.ai/core-concepts/qodo-platform-architecture
- https://docs.qodo.ai/core-concepts/context-engine
- https://docs.qodo.ai/code-review
- https://docs.qodo.ai/code-review/overview
- https://docs.qodo.ai/code-review/use-qodo-in-prs
- https://docs.qodo.ai/install-qodo/install
- https://docs.qodo.ai/code-governance
- https://docs.qodo.ai/governance
- https://docs.qodo.ai/governance/rule-enforcement
- https://docs.qodo.ai/whats-new
- https://docs.qodo.ai/changelog
- https://github.com/qodo-ai/command
- https://github.com/qodo-ai/command/releases
- https://github.com/qodo-ai/pr-agent
- https://github.com/qodo-ai/pr-agent/releases
- https://api.github.com/orgs/qodo-ai/repos?per_page=100
- https://www.npmjs.com/package/@qodo/command

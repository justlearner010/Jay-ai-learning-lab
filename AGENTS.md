# AI Operating Rules

This repository is a CS and AI Agent learning lab. Agents should treat it as an operational learning system, not as a generic note dump.

## Repository Purpose

- Track the user's current learning roadmap, active tasks, projects, notes, logs, summaries, and spaced-review records.
- Preserve evidence of learning through code, tests, notes, review cards, and summaries.
- Keep the public-facing repo surface compact and understandable.

## First Files To Read

When starting work in this repository, read these files before making changes:

1. `README.md` for the repository map and learning loop.
2. `roadmap.md` for current phase direction.
3. `to do list.md` for active tasks.
4. `docs/ai-operating-manual.md` for the current AI/Obsidian workflow.
5. Relevant folder README files before editing inside that folder.

## Directory Contracts

| Path | Contract |
| --- | --- |
| `projects/` | Hands-on coding projects, usually Git submodules. Do not treat submodule changes as ordinary file edits without checking their own repo state. |
| `notes/` | Navigation layer for the independent notes repository. Actual technical notes live under `notes/library/`. |
| `logs/` | Lightweight progress logs. Record progress, evidence, and next action only. Do not turn logs into long retrospectives. |
| `summary/` | Weekly, monthly, and phase summaries. Use only after there is enough evidence to summarize. |
| `knowledge-review/` | Spaced-review system. Preserve the existing card schema and generation rules. |
| `incubator/` | Early ideas that are not yet projects. Keep them lightweight until they become actionable. |
| `templates/` | Reusable note, log, summary, and task templates. Prefer improving templates over creating one-off structure. |
| `archives/` | Historical material. Do not revive or edit unless the task explicitly asks for archive cleanup. |

## Knowledge Review Rules

- Always inspect existing review cards before generating or updating new ones.
- If a card is `pending`, update it only when the user has filled in enough self-rating or completion evidence.
- Do not infer learning performance from partial answers.
- Do not duplicate same-day, same-knowledge-point review files.
- Preserve front matter fields used by current cards, including `source_note`, `source_added_at`, `review_date`, `knowledge_point`, `new_or_old`, `review_round`, `interval_days`, `next_review_date`, and `status`.
- If the intended new:old review ratio cannot be met because candidates are missing, report the actual ratio instead of fabricating one.

## Editing Rules

- Keep changes scoped to the user's current request.
- Prefer adding navigation, templates, or rules that reduce future friction over adding new directories.
- Update `roadmap.md` only when a phase direction has actually changed.
- Update `to do list.md` only when the active task list changes.
- Update `logs/` when there is concrete work evidence from the day.
- Update `summary/` after a real weekly or phase review, not after every task.
- Do not commit, push, archive, or rewrite history unless the user explicitly asks.

## Git Sync And Merge Rules

- Daily sync automation should only stage and upload main-repo `*.md` files.
- Do not auto-stage scripts, config files, submodule changes, caches, build artifacts, or machine-local state during daily sync.
- Treat daily sync as backup and remote visibility, not as implicit merge to `main`.
- Batch-merge Markdown-only changes from the working branch into `main` on a weekly cadence by default.
- If the weekly batch contains non-Markdown files or submodule changes, stop the merge and leave that branch for manual review instead of partially guessing intent.

## AI Workflow Preference

The useful pattern for this vault is:

`roadmap -> current task -> project or note work -> lightweight log -> review card -> weekly or phase summary`

Avoid turning the vault into a broad personal knowledge graph. The priority is retrieval practice, project evidence, and reusable learning artifacts.

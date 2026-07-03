# AI Operating Manual

This page is the Obsidian-facing entry point for AI sessions. It translates the repository structure into a practical workflow for Codex, Claude, or any other agent working inside this vault.

## Current System Shape

This vault is organized around one loop:

`roadmap -> task -> work evidence -> review -> summary`

The repo is not meant to collect every interesting idea. A note or automation is useful only if it improves one of these outcomes:

- selecting the next learning action
- producing code, tests, or technical notes
- preserving evidence of progress
- creating retrieval practice
- summarizing what changed in understanding or direction

## Durable Context

| Area | Source of truth |
| --- | --- |
| Current phase and priorities | `roadmap.md` |
| Active tasks | `to do list.md` |
| Technical notes | `notes/library/` |
| Daily progress evidence | `logs/` |
| Weekly or phase synthesis | `summary/` |
| Spaced review records | `knowledge-review/content/` |
| Early project ideas | `incubator/` |
| Reusable structures | `templates/` |

## Agent Session Checklist

At the start of a session:

1. Read `AGENTS.md`.
2. Read `README.md`, `roadmap.md`, and `to do list.md`.
3. Read the README or nearest context file for the specific folder being changed.
4. Check `git status --short` before editing.
5. Treat unrelated existing changes as user-owned.

Before finishing:

1. Verify changed files directly.
2. Run relevant tests or validation when code changed.
3. Explain what changed and what was not touched.
4. Mention any skipped verification.

## Routing Rules

Use this routing table when new information appears:

| Input | Put it here | Notes |
| --- | --- | --- |
| A technical concept worth keeping | `notes/library/<topic>/` | Keep it focused and reusable. |
| A day-level progress record | `logs/Daily log/<phase>/` | Record action, evidence, and next step. |
| A task to do soon | `to do list.md` | Keep it actionable. |
| A phase-level direction change | `roadmap.md` | Update only after deliberate decision. |
| A rough project idea | `incubator/` | Keep the idea small until it has a next action. |
| A reusable workflow | `templates/` or `docs/` | Prefer improving existing templates first. |
| A recall or review item | `knowledge-review/content/` | Follow the review-card schema. |

## What Not To Do

- Do not create a new top-level system for every new idea.
- Do not over-link notes just to make the graph look dense.
- Do not convert lightweight logs into long essays.
- Do not update review-card status without user self-rating or clear completion evidence.
- Do not treat public-facing presentation as more important than actual learning evidence.
- Do not expand the repo surface unless the user explicitly decides to create a new repo or project.

## Useful Next Improvements

- Add a template for new learning topics that includes goals, source material, output, review prompts, and evidence.
- Add a small checklist for converting an incubator idea into a project.
- Keep `knowledge-review/generate_daily_review.py` aligned with the rules in `AGENTS.md`.

## Git Rhythm

- Daily repository sync is for uploading Markdown notes, logs, and review cards safely to the remote branch.
- Weekly merge is the default cadence for bringing Markdown-only updates from the working branch back into `main`.
- If a candidate weekly batch includes scripts, config changes, or submodule diffs, do not treat it as a routine notes merge.

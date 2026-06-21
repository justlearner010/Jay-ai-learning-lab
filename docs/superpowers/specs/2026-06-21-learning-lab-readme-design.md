# Learning Lab README Design

## Goal

Rewrite the repository README as the Chinese-first entry point for the CS and AI learning lab, with a short English summary for international readers.

## Structure

The README will contain:

1. A concise Chinese introduction explaining the purpose of the learning lab.
2. Current learning directions and expected outputs.
3. A directory map covering projects, notes, logs, templates, archive, roadmap, and task list.
4. A related-project section linking the three Git submodules:
   - AI Reader
   - TextLab CLI
   - Personal Website
5. Basic repository usage, including cloning with `--recurse-submodules` and initializing submodules after a normal clone.
6. Direct links to the roadmap and task list.
7. A short English summary at the end.

## Scope

This change only rewrites `README.md`. It does not restructure learning materials, modify child repositories, or change submodule revisions.

## Validation

- Confirm all Markdown links target existing files or repositories.
- Confirm `.gitmodules` matches the three projects described by the README.
- Run `git diff --check` before committing.

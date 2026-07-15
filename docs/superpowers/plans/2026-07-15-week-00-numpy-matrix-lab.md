# Week 0 NumPy Matrix Lab Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the Week 0 shape-only starter with a six-gate NumPy matrix lab whose later functions compose earlier ones.

**Architecture:** The public submodule contains only contracts, learner-facing instructions, and smoke tests. The local ignored `.grader/week_00.py` owns behavioral verification and emits category-only feedback. The starter file remains intentionally unimplemented, so the learner supplies all production logic.

**Tech Stack:** Python 3, NumPy, pytest, uv.

---

## File map

- Modify: `projects/transformer-from-scratch-lab/labs/week-00/src/contracts.py` — six unimplemented learner contracts.
- Modify: `projects/transformer-from-scratch-lab/labs/week-00/tests/test_week_00_smoke.py` — imports and starter-only smoke checks.
- Modify: `projects/transformer-from-scratch-lab/labs/week-00/README.md` — gate-by-gate learner guidance and constraints.
- Modify: `projects/transformer-from-scratch-lab/tasks/week-00.md` — align pre-lab tasks with matrix operations.
- Modify: `projects/transformer-from-scratch-lab/homework/week-00-engineering.md` — ask about evidence from the redesigned Lab.
- Modify: `projects/transformer-from-scratch-lab/.grader/week_00.py` — ignored local autograder, never committed.

### Task 1: Establish the hidden grading contract

**Files:**
- Create or modify: `projects/transformer-from-scratch-lab/.grader/week_00.py`

- [x] Write the hidden checks before changing the learner starter. They exercise each public function independently, use small non-square matrices, and compute expected matrix products with NumPy only inside the grader.
- [x] Run `uv run python labs/week-00/run_grade.py` and verify the existing two-function starter fails at the first gate under the new contract.
- [x] Keep grader output restricted to gate number, passed count, failure category, thinking prompt, and unlock state. It does not print hidden operands, expected arrays, assertion text, or solution logic.

### Task 2: Replace the learner contracts without an implementation

**Files:**
- Modify: `projects/transformer-from-scratch-lab/labs/week-00/src/contracts.py`
- Test: `projects/transformer-from-scratch-lab/.grader/week_00.py`

- [x] Define only the six signatures from the approved design: `require_matrix`, `matrix_shape`, `require_multipliable`, `dot_entry`, `matmul_from_entries`, and `describe_product`.
- [x] Give every function a docstring that states inputs, outputs, error boundaries, input immutability, and which earlier function it should reuse.
- [x] Leave each function at a `NotImplementedError`; do not add a reference implementation or any partial solution.
- [x] Run the hidden grader and verify it reports the first incomplete gate rather than a crash.

### Task 3: Keep public tests informational, not answer-bearing

**Files:**
- Modify: `projects/transformer-from-scratch-lab/labs/week-00/tests/test_week_00_smoke.py`
- Test: `projects/transformer-from-scratch-lab/labs/week-00/tests/test_week_00_smoke.py`

- [x] Replace the old two-function import check with a six-function export check.
- [x] Add a starter-state check that calls only the first function and accepts its intentional `NotImplementedError`.
- [x] Run `uv run pytest labs/week-00/tests -v`; the smoke suite passes without testing numerical answers.

### Task 4: Write the learner workflow and course links

**Files:**
- Modify: `projects/transformer-from-scratch-lab/labs/week-00/README.md`
- Modify: `projects/transformer-from-scratch-lab/tasks/week-00.md`
- Modify: `projects/transformer-from-scratch-lab/homework/week-00-engineering.md`

- [x] Describe one gate per function, including purpose, dependency, allowed NumPy tools, a thought prompt, and the precise condition to advance.
- [x] State that `matmul_from_entries` must compose `dot_entry` and may not use `@` or `np.matmul`; make the later manual-vs-NumPy comparison a mini demo instead of a starter function.
- [x] Replace shape-tuple-only tasks with a small token matrix, a projection matrix, a manual output entry, a full product, and a comparison to NumPy `@`.
- [x] Update engineering questions so every answer must point to the learner's Lab output or grader feedback.

### Task 5: Validate the course artifact end to end

**Files:**
- Verify: all files in Tasks 1–4.

- [x] Run `uv run pytest -v` from `projects/transformer-from-scratch-lab`: 4 tests passed.
- [x] Run `uv run python labs/week-00/run_grade.py`: the untouched starter emits a controlled first-gate feedback message.
- [x] Inspect `git diff --check` in the submodule and main repository. The submodule check is clean; the parent reports one pre-existing trailing-whitespace issue in `incubator/tokenization-lab/tokenization-method.py`.
- [x] Inspect `git status --short` in both repositories. `.grader/week_00.py` remains ignored and no user-owned paths outside the agreed Week 0 files were altered.

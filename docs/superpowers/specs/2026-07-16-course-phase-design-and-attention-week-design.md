# Course Phase Design Skill and Attention Week Design

## Purpose

This design establishes a reusable course-phase design process and applies it
to the next Transformer learning package. The course is mastery-paced rather
than calendar-paced: a "week" names a coherent knowledge package, not seven
fixed daily assignments. The learner may advance quickly when interested or
remain on one gate until the evidence is sufficient.

The immediate package answers one question:

> How does one token use content to decide how much information to read from
> other tokens?

It covers Q/K/V projections and single-sample, single-head scaled dot-product
attention. It does not include causal masking, batching, multi-head attention,
LayerNorm, residual connections, FFN, training, or generation.

## Reusable course-phase design protocol

The reusable skill will be named `course-phase-design`. It should trigger when
designing, extending, or revising a staged self-study course, especially when
the learner needs concept dependencies, progressive Labs, hidden assessment,
mastery gates, or a next phase derived from prior evidence.

For every new phase, the skill must:

1. Read the course purpose, operating system, weekly template, previous phase,
   current learner evidence, and nearest existing next-phase files.
2. Separate explicit evidence from learner claims and stale documentation.
   Claims guide scope; tests, graders, notes, and artifacts establish current
   readiness. Unknown evidence is reported as unknown rather than failed.
3. Identify one governing question and the minimum knowledge chain needed to
   answer it.
4. Present two or three possible scopes when the next boundary is ambiguous,
   recommend one, and obtain user approval before generating artifacts.
5. Organize work by knowledge dependency, never by arbitrary daily quotas.
   Time estimates may describe capacity but cannot become unlock conditions.
6. Give every knowledge point the same learning loop:

   ```text
   motivating problem
     -> bounded reading
     -> hand-worked minimal example
     -> prediction before execution
     -> dependent Lab gate
     -> public smoke check and hidden behavioral check
     -> failure explanation
     -> transfer or retrieval check
     -> next unlock
   ```

7. Keep public artifacts answer-free. Public tests may verify imports,
   signatures, starter behavior, and harmless invariants. Hidden graders may
   verify behavior but reveal only the current gate, failure category, thinking
   prompt, and unlock state.
8. Require later Lab functions to compose earlier functions. Do not allow the
   learner to bypass a failed mechanism by reimplementing it inside an
   integration function.
9. Define completion using multiple kinds of evidence: behavioral tests, an
   unseen transfer problem, a short closed-book explanation, one real or
   deliberately injected failure, and a learner-owned mini demo.
10. State non-goals and the exact next mechanism that becomes possible after
    completion.

The skill is a reusable personal Codex skill under `~/.codex/skills`, not a
project-specific copy of the Transformer syllabus. Transformer-specific
details remain in this repository.

## Attention knowledge chain

The next package follows this dependency graph:

```text
validated matrix projection from the previous phase
  -> Q/K/V projections
  -> query-key score matrix
  -> scale by sqrt(d_k)
  -> row-wise stable softmax
  -> weighted read from V
  -> complete scaled dot-product attention
  -> independent diagnostic demo
```

Each gate has one responsibility and must be independently explainable and
testable.

| Gate | Knowledge point | Learner must establish | Unlock evidence |
| --- | --- | --- | --- |
| 1 | Q/K/V projection | One input can be projected into three representations with distinct later roles. | Correct numeric projection, shape explanation, and no input mutation. |
| 2 | Attention scores | `scores[i, j]` is query `i` matched against key `j`; rows represent one query's competition over keys. | Correct `Q @ K.T`, non-square coverage, and transpose/inner-dimension diagnostics. |
| 3 | Scaling | Dot-product variance grows with `d_k`; division by `sqrt(d_k)` controls softmax saturation. | Derivation plus checks that use the key/query feature width rather than token count. |
| 4 | Stable softmax | Scores become a row-wise distribution without overflow. | Row sums, translation invariance, extreme values, and wrong-axis detection. |
| 5 | Weighted value read | Q/K choose the weights while V supplies the content and output feature width. | Correct `weights @ V`, non-square V coverage, and targeted mutation reasoning. |
| 6 | Integrated attention | Earlier functions form one traceable information path. | Composition checks, intermediate diagnostics, hand-calculated oracle, and complete hidden pass. |
| 7 | Transfer and diagnosis | The mechanism transfers beyond the Lab scaffold. | Unseen problem, closed-book explanation, failure record, and independent mini demo. |

## Learner-facing artifacts

The implementation will align the existing next-phase files rather than add a
parallel structure:

- `weeks/week-01/README.md`: governing question, prerequisites, knowledge
  chain, order, non-goals, and completion definition.
- `weeks/week-01/materials.md`: bounded reading ranges, one required question
  per source, and compact completion evidence.
- `weeks/week-01/exercises.md`: hand calculations, prediction tasks,
  counterexamples, and transfer prompts before coding.
- `weeks/week-01/homework.md`: concept, boundary, global-role, and hidden-test
  design questions.
- `weeks/week-01/notes-template.md`: actual misconception, grader category,
  changed understanding, retrieval check, and next unlock.
- `labs/week-01/src/attention.py`: answer-free dependent function contracts.
- `labs/week-01/tests/test_week_01_smoke.py`: public import/signature/starter
  checks without numerical answer cases.
- `labs/week-01/run_grade.py`: loader for the local ignored grader.
- `labs/week-01/README.md`: gate order, allowed tools, prompts, and boundaries.
- `.grader/week_01.py`: ignored behavioral checks and category-only feedback.

Existing `weeks/week-01` material should be revised in place. The older
top-level `lab/src/attention.py` is not silently deleted or repurposed; its
relationship to the current course structure must be inspected during
implementation and any cleanup must remain outside this package unless it is
required to avoid an ambiguous learner entry point.

## Lab contract ladder

Exact names may be adjusted during implementation only to match an established
repository convention, but responsibilities and dependencies must remain:

| Gate | Function responsibility | Required dependency |
| --- | --- | --- |
| 1 | Project one input matrix with one weight matrix; combine three calls for Q/K/V where appropriate. | Reuse or mirror the validated matrix boundaries established in Week 0 without importing learner answers across packages. |
| 2 | Compute query-key scores and validate the shared feature width. | Projection output contract. |
| 3 | Scale scores using `sqrt(d_k)` supplied or derived from Q/K feature width. | Score contract. |
| 4 | Compute numerically stable softmax along an explicit axis. | Valid numeric matrix contract. |
| 5 | Convert scaled scores into row-wise attention weights. | Scaling and stable-softmax functions. |
| 6 | Multiply weights by V and validate token/value dimensions. | Weight contract. |
| 7 | Compose the complete attention path and optionally return diagnostics defined by the contract. | Every earlier gate; no duplicate implementation. |

The learner implementation must not use a framework attention module. NumPy
matrix operations are allowed because the learning target is attention, not a
second manual matrix-multiplication exercise.

## Error and diagnostic boundaries

- Reject non-array, non-numeric, empty, or incorrectly ranked inputs at a
  documented boundary.
- Name operands and conflicting dimensions in shape errors.
- Reject non-positive `d_k` and inconsistent Q/K feature widths.
- Make the softmax axis explicit and test row-wise attention behavior.
- Reject incompatible weights/V token dimensions.
- Do not mutate Q, K, V, scores, or weights.
- Do not print hidden arrays, expected values, assertion bodies, or reference
  implementations.
- Categorize feedback as `input boundary`, `shape`, `transpose`, `scaling`,
  `numerical stability`, `axis`, `weighted read`, `composition`, or
  `immutability`.

## Verification design

Public verification confirms that the package is usable without disclosing
solutions. Hidden verification advances one gate at a time and should include:

1. non-square projection cases and input immutability;
2. score matrices where an incorrect transpose cannot pass accidentally;
3. scaling checks that distinguish feature width from token count;
4. large positive and negative softmax inputs, row sums, and translation
   invariance;
5. non-square V matrices and targeted changes to K versus V;
6. an integrated result checked against an independently composed oracle;
7. evidence that the integration function actually calls or behaviorally
   preserves earlier contracts rather than bypassing them.

The grader must first be observed failing against the untouched starter. After
artifact generation, public tests must pass while the answer-free starter
produces a controlled first-gate hidden response.

## Completion and transition

The package is complete only when the learner:

- passes all public and hidden checks;
- completes one unseen numerical transfer problem;
- explains the full mechanism for three to five minutes without notes;
- records one real or deliberately injected failure and an executable
  prevention strategy;
- builds a small diagnostic demo without copying the Lab implementation; and
- can point to where a future causal mask belongs without implementing it.

The next phase may then introduce causal masking. It must not also absorb
LayerNorm, residuals, FFN, batching, multi-head attention, and training unless
their own dependency analysis independently justifies that scope.

## Non-goals

- No daily schedule or deadline-based unlocks.
- No full reference implementation in public files.
- No hidden expected inputs or outputs in feedback.
- No framework attention, Agent framework, RAG, or model training.
- No edits to the learner's current Week 0 implementation.
- No commit or cleanup of unrelated parent-repository or submodule changes.

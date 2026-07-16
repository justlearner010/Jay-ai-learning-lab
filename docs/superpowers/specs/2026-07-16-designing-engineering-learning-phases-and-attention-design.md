# Designing Engineering Learning Phases Skill and Attention Application Design

## Purpose

This design establishes a domain-neutral process for turning engineering
knowledge into mastery-paced course phases, then applies that process to the
next Transformer learning package. The reusable process is intended for topics
such as programming, software engineering, computer systems, backend and data
engineering, ML/LLM systems, RAG, and Agents. Transformer is the first usage
case, not the skill's governing domain.

A course phase names a coherent capability package, not a fixed number of
days. The learner may advance quickly when interested or remain on one gate
until the evidence is sufficient.

The immediate package answers one question:

> How does one token use content to decide how much information to read from
> other tokens?

It covers Q/K/V projections and single-sample, single-head scaled dot-product
attention. It does not include causal masking, batching, multi-head attention,
LayerNorm, residual connections, FFN, training, or generation.

## Domain-neutral course-phase model

The reusable skill will be named `designing-engineering-learning-phases`. It
should trigger when
designing, extending, or revising a staged engineering self-study course,
especially when the learner needs concept dependencies, progressive practice,
Labs, assessment, mastery gates, or a next phase derived from prior evidence.

The skill operates on five domain-neutral objects:

| Object | Meaning | Examples |
| --- | --- | --- |
| Capability question | One observable ability the phase should create. | Explain a mechanism, implement an API boundary, debug a process, operate a service. |
| Dependency graph | The minimum prerequisite chain for that ability. | Types before parsing; processes before signals; retrieval before agentic routing. |
| Knowledge gate | One concept or engineering decision with an independent check. | Error propagation, file descriptors, cache invalidation, attention scores. |
| Practice artifact | The smallest environment that makes the gate observable. | Hand trace, focused function, CLI scenario, failing service, notebook experiment. |
| Mastery evidence | Evidence that survives beyond the scaffold. | Behavioral test, diagnosis, unseen transfer, oral explanation, independent mini project. |

Before selecting tasks, classify the phase by its dominant learning mode:

- **mechanism:** understand why a computation or system behavior occurs;
- **contract:** implement and defend an interface or boundary;
- **diagnosis:** reproduce, localize, explain, and prevent failures;
- **integration:** compose independently verified components;
- **operation:** observe, deploy, measure, recover, and make trade-offs.

A phase may combine modes, but one mode must dominate so that assessment does
not collapse into a generic checklist.

## Reusable course-phase design protocol

For every new phase, the skill must:

1. Read the course purpose, operating system, weekly template, previous phase,
   current learner evidence, and nearest existing next-phase files.
2. Separate explicit evidence from learner claims and stale documentation.
   Claims guide scope; tests, graders, notes, and artifacts establish current
   readiness. Unknown evidence is reported as unknown rather than failed.
3. Identify one capability question, dominant learning mode, and minimum
   dependency graph needed to answer it.
4. Present two or three possible scopes when the next boundary is ambiguous,
   recommend one, and obtain user approval before generating artifacts.
5. Organize work by knowledge dependency, never by arbitrary daily quotas.
   Time estimates may describe capacity but cannot become unlock conditions.
6. Give every knowledge point the same abstract learning loop:

   ```text
   motivating problem
     -> bounded source material
     -> minimal observable example or trace
     -> prediction before execution
     -> dependent practice gate
     -> behavior check
     -> failure explanation
     -> transfer or retrieval check
     -> next unlock
   ```

7. Select verification that matches the dominant mode. A mechanism phase may
   use derivation and controlled experiments; a contract phase may use unit and
   boundary tests; a diagnosis phase may use injected failures and incident
   traces; an integration phase may use end-to-end checks; an operation phase
   may use metrics, runbooks, and recovery drills.
8. Keep assessment artifacts answer-free when independent learning is the
   goal. Hidden graders are optional, not universal. When used, they may reveal
   only the current gate, failure category, thinking prompt, and unlock state.
   When hidden grading is unsuitable, use a black-box harness, review rubric,
   reproducible command, trace comparison, or observable acceptance scenario.
9. Require later practice gates to consume the contracts or evidence created
   by earlier gates. Do not allow an integration task to conceal a failed
   prerequisite through duplicate implementation or unexplained automation.
10. Define completion using multiple evidence types appropriate to the topic:
    reproducible behavior, unseen transfer, short closed-book explanation, one
    real or deliberately injected failure, and an independent artifact.
11. State non-goals and the exact next capability that becomes possible after
    completion.

The skill is a reusable personal Codex skill under `~/.codex/skills`, not a
project-specific syllabus template. Domain vocabulary, formulas, libraries,
function names, and grading cases remain in the target course repository.

## General practice and assessment selection

The skill must not force every topic into a numerical Lab. Choose the smallest
practice form that exposes the knowledge point:

| Knowledge type | Preferred practice | Typical evidence |
| --- | --- | --- |
| Computation or algorithm | Hand trace, minimal implementation, property checks | Derivation, tests, counterexample |
| API or module boundary | Contract-first function or service | Boundary tests, error behavior, consumer example |
| Linux or systems behavior | Command experiment, process/file/network observation | Reproducible commands, trace, explanation |
| Debugging technique | Seeded fault and constrained diagnosis | Reproduction, root cause, regression check |
| Architecture or integration | Small composed system with explicit interfaces | End-to-end check, failure isolation, trade-off memo |
| Operations and reliability | Instrumented service scenario | Metrics, alert evidence, runbook, recovery drill |
| ML/LLM behavior | Controlled experiment and evaluation set | Baseline, metric, failure slices, cost/latency record |

The universal requirement is not a particular tool. It is a visible chain from
claim to prediction, execution, evidence, explanation, and transfer.

## Generic output contract

For any repository, the skill should first reuse the local course structure.
If no structure exists, propose a minimal equivalent of:

- phase overview: capability question, prerequisites, scope, non-goals;
- bounded resources: exact ranges and reading questions;
- concept/practice tasks: dependency-ordered gates;
- practice environment: Lab, experiment, debugging scenario, or service;
- verification: public checks plus optional hidden or black-box assessment;
- evidence template: failure record, changed understanding, transfer result;
- completion decision: passed gates, unresolved P0 gaps, and next capability.

File names are repository decisions, not requirements imposed by the skill.

## First application: Transformer attention

### Attention knowledge chain

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

### Learner-facing artifacts

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

### Lab contract ladder

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

### Error and diagnostic boundaries

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

### Verification design

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

### Completion and transition

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

### Attention application non-goals

- No daily schedule or deadline-based unlocks.
- No full reference implementation in public files.
- No hidden expected inputs or outputs in feedback.
- No framework attention, Agent framework, RAG, or model training.
- No edits to the learner's current Week 0 implementation.
- No commit or cleanup of unrelated parent-repository or submodule changes.

## Skill non-goals

- Do not prescribe Transformer terminology outside Transformer courses.
- Do not require hand calculations when traces, commands, tests, or operational
  evidence better expose the target capability.
- Do not require hidden graders for open-ended design or operational work.
- Do not create a large course before the next capability boundary is clear.
- Do not equate elapsed time, content volume, or a passing demo with mastery.
- Do not replace project-local conventions with one global directory layout.

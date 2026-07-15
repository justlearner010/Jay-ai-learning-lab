# Week 0 NumPy Matrix Lab Design

## Purpose

Week 0 is the bridge between the course's linear-algebra material and Week 1
attention. Its purpose is not to implement attention early. It is to make the
mechanics that attention relies on observable: a two-dimensional NumPy array,
its row/column meaning, matrix-product compatibility, and how one output entry
is formed.

The previous two-function shape-checker design concentrated too much work in
each function and did not provide enough NumPy practice. This design replaces
it with small, dependent functions. Each one has a single responsibility and
creates evidence for the next one.

## Scope and boundaries

- The learner edits only `labs/week-00/src/contracts.py`.
- Inputs are small two-dimensional `numpy.ndarray` values, not shape tuples.
- The lab uses NumPy for arrays, shapes, indexing, slicing, and comparison.
- The learner may not use `@` or `np.matmul` inside the manual matrix-product
  function. A separate comparison step may use `@` as an oracle.
- The public starter contains contracts and light smoke tests only. Local,
  ignored hidden tests report failure categories and hints, never reference
  implementations or hidden expected values.
- This redesign intentionally replaces the current Week 0 starter contract.

## Function ladder

| Gate | Function | Single responsibility | Depends on |
| --- | --- | --- | --- |
| 1 | `require_matrix(value, *, name)` | Reject anything that is not a usable two-dimensional NumPy matrix. Return the validated value. | None |
| 2 | `matrix_shape(matrix, *, name)` | Return `(rows, columns)` for a validated matrix. | `require_matrix` |
| 3 | `require_multipliable(left, right)` | Validate two matrices and reject unequal inner dimensions. Return their shapes or validated operands as documented. | `matrix_shape` |
| 4 | `dot_entry(left, right, row, column)` | Compute exactly one entry of `left × right` from one row and one column. | `require_multipliable` |
| 5 | `matmul_from_entries(left, right)` | Build a complete product by repeatedly calling `dot_entry`; do not delegate to `@` or `np.matmul`. | `require_multipliable`, `dot_entry` |
| 6 | `describe_product(left, right)` | Produce a compact human-readable explanation of either the valid product shape or the incompatibility. It must not calculate the product. | `require_multipliable` |

The exact return values and error-message requirements will be documented in
the starter docstrings. Every function should be understandable without
reading the body of a later function.

## Learning progression

```text
NumPy matrix validity
  -> row and column shape
  -> inner-dimension compatibility
  -> one dot-product entry
  -> full manual product
  -> diagnostic explanation
  -> compare manual result with NumPy @
```

The final comparison is a learner-owned mini demo, not another production
function: choose at least two compatible non-square examples and one
incompatible example; compare the manual result to `left @ right`; record the
shapes and one output entry.

## Error handling

- Invalid type, non-NumPy input, or non-two-dimensional input: raise
  `ValueError` that contains the supplied operand name (`left`, `right`, or a
  caller-specified name).
- Empty or otherwise unsupported matrix dimensions: reject consistently and
  state the relevant boundary in the error message.
- Incompatible products: raise `ValueError` that names both inner dimensions,
  rather than exposing only a raw NumPy error.
- `dot_entry` must reject out-of-range row or column indexes rather than rely
  on accidental indexing behavior.
- Functions must not mutate their input matrices.

## Public and hidden verification

Public tests verify imports, signatures, starter behavior, and that each
function is independently callable. They do not contain numerical answers.

The local hidden grader checks, in order:

1. matrix validity and named error messages;
2. shape extraction and compatible/incompatible non-square cases;
3. a single entry against a separately computed dot product, including index
   boundaries;
4. manual full-product output against NumPy `@` on several small matrices;
5. input immutability and a diagnostic that names the relevant shapes.

Its feedback is limited to a current gate, pass count, a failure category
(`input type`, `shape`, `formula`, `index boundary`, or `diagnostic`), one
thinking prompt, and the next unlock state.

## Completion evidence

To finish Week 0, the learner must pass the local grader, write the engineering
homework using one actual failure or validation case, and complete the mini
demo. The Lab README should explicitly connect the resulting matrix product to
the later `Q = XW_Q` projection in Week 1.

## Non-goals

- No attention score, softmax, Q/K/V, causal mask, or training code in Week 0.
- No generic NumPy tutorial detached from the Transformer path.
- No reference implementation, generated solution code, or public hidden
  answer matrices.

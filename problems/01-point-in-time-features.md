# 01: Features you could actually have known

A model is scored at time `at`. An observation can describe the past but arrive later.
Reconstruct what the scoring system could have known, rather than what is known today.

Implement `features_at(observations, queries)` in `candidate/asof.py`.

## Contract

An observation has `entity` (string), `event_at` and `available_at` (integer UTC epoch
seconds), `revision` (positive integer), and `value` (finite number).
Queries have `entity` and `at` (integer UTC epoch seconds).
Both inputs are finite iterables; observations can be unordered or single-pass.
Inputs are valid. Observation keys `(entity, event_at, available_at, revision)` are unique.
Do not mutate input records.

For each query, keep observations for that entity where **both** timestamps are `<= at`.
Choose the lexicographic maximum `(event_at, available_at, revision)` among those rows.
Return its value, or `None` if no row is eligible. Preserve query order.
Availability cannot precede event time. A later-arriving older event does not displace
a newer event. A correction only becomes usable when its own availability time is reached.

## Minimal example

| entity | event_at | available_at | revision | value |
|---|---:|---:|---:|---:|
| a | 2 | 2 | 1 | 20 |
| a | 4 | 9 | 1 | 40 |

Query `{'entity': 'a', 'at': 5}` returns `[20]`, not `[40]`.

## Constraints and reference complexity

At most 2,000 observations and 2,000 queries. A clear `O(NQ)` solution is acceptable;
the reference uses `O(N+Q)` additional space. Indexing is optional and earns no extra
correctness credit. No external packages, network access, or timezone libraries are needed.

## Evaluation notes

`test_late_arrival_does_not_leak` rejects the baseline that filters only event time:
that baseline returns 40 even though the value does not arrive until time 9.
Other tests cover future corrections, revision ties, event precedence, exact boundaries,
entity isolation, zero values, missing values, permutations, generators, and mutation.

## Rubric (100 points)

| Criterion | Points | Evidence |
|---|---:|---|
| Both event and availability cutoffs | 30 | Late-arrival and correction tests |
| Event precedence and deterministic revision tie break | 25 | Precedence and tie tests |
| Entity isolation, missing/zero values, inclusive boundaries | 20 | Missing/boundary tests |
| Order independence, generator support, no mutation | 15 | Permutation/mutation test and review |
| Clear implementation, stated complexity, accurate explanation | 10 | Manual review |

A passing submission needs at least 80 points and must pass the late-arrival and
future-correction tests. Test counts are not point weights. The final 10 points require
human review; the test runner does not claim to compute a complete grade.

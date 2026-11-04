# 03: How long was the pool overloaded?

Reservations consume a shared pool. Report the duration for which concurrent units
strictly exceed capacity, clipped to a reporting window. Count time once, irrespective
of how many reservations overlap.

Implement `overloaded_minutes(reservations, window_start, window_end, capacity)` in
`candidate/capacity.py`.

## Contract

Time is measured in integer minutes relative to an arbitrary common origin. Each valid
record has integer `start`, `end` (`start <= end`) and positive integer `units`.
The window obeys `window_start <= window_end`; capacity is a nonnegative integer.
Reservations are half-open: **[start, end)**. The reporting window is also half-open.
Load equal to capacity is allowed. Zero-length reservations consume nothing.
Return an integer duration. Input can be unordered or a single-pass iterable. Do not
mutate it. Distinct identical rows represent distinct reservations and both consume units.

## Minimal example

One unit is reserved for `[0, 5)` and another for `[5, 10)`. At capacity 1, the pool
is never overloaded. Expected duration over `[0, 10)` is `0`.

With two units on `[0, 10)` and two units on `[2, 8)`, capacity 3 is exceeded for
6 minutes. Another reservation inside that overloaded span must not double-count time.

## Constraints and reference complexity

At most 100,000 reservations. Time coordinates may be as large as `10**12` in absolute
value. Target `O(N log N)` time and `O(N)` space. Iterating every minute is unacceptable
because runtime would depend on the coordinate range. Standard-library Python only.

## Evaluation notes

`test_adjacent_reservations_do_not_overlap` rejects the baseline's inclusive end check:
it counts both reservations at minute 5 and returns 1 instead of 0. The same baseline
also iterates the entire window, so **do not run it on the large sparse test**.
The counterexample runner intentionally selects only the short boundary case.

Other tests check exact capacity, clipping, nested overlap, empty intervals, zero capacity,
large sparse times, 150 seeded cases against an independent minute-by-minute oracle on
small windows, and split/shift invariance. The small-window oracle is a test method,
not a valid production algorithm for the stated constraints.

## Rubric (100 points)

| Criterion | Points | Evidence |
|---|---:|---|
| Half-open endpoints and strict capacity threshold | 25 | Adjacent and exact-capacity tests |
| Correct duration without double counting | 25 | Nested and seeded oracle tests |
| Clipping, empty intervals and zero capacity | 20 | Window and zero-length tests |
| Efficient handling of sparse, large timestamps | 20 | Large-window test and complexity review |
| Clear explanation, generator support and input integrity | 10 | Manual review and tests |

Pass: at least 80 points; adjacent-boundary and large sparse-window tests are mandatory.
Correct output on small examples alone is insufficient. Apply an external process timeout
when evaluating unknown code; this repository is not an execution sandbox.

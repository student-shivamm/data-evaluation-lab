# 02: Retries are not revenue

A payment webhook is delivered repeatedly. Some deliveries report pending or failed
states before a successful one. Compute net settled cents per account without double billing.

Implement `net_cents(events)` in `candidate/billing.py`.

## Contract

Each valid row contains strings `account`, `operation`, `delivery_id`, `kind`
(`charge` or `refund`), `status` (`pending`, `failed`, or `succeeded`), integer
`received_at` (UTC epoch seconds), and nonnegative integer `amount_cents`.
Input is a finite, unordered iterable, possibly a generator. Do not mutate records.

1. Ignore nonsuccessful deliveries **before** deduplicating.
2. A logical operation is identified by `(account, operation)`, not operation alone.
3. For each logical operation choose the successful delivery with the smallest
   `(received_at, delivery_id)`, using case-sensitive string ordering for delivery IDs.
4. Add its amount for a charge; subtract it for a refund. Return a dict of account
   totals. Include zero totals for accounts with successful operations; omit accounts
   with none. Negative totals are allowed. Do not use floating-point currency.

Exact repeated rows are valid. Rows with identical account, operation, received_at and
delivery_id have identical payloads. Later deliveries may conflict in amount or kind:
the earliest successful delivery remains authoritative. Refunds have their own operation
IDs and require no matching-charge lookup for this task.

## Minimal example

| account | operation | status | kind | amount_cents | received_at | delivery_id |
|---|---|---|---|---:|---:|---|
| a | x | pending | charge | 100 | 1 | d1 |
| a | x | succeeded | charge | 100 | 2 | d2 |

Expected: `{'a': 100}`. Seeing a pending delivery must not consume the logical operation.

## Constraints and reference complexity

At most 100,000 deliveries. Target `O(N)` expected time and `O(U)` space for U successful
logical operations. Python integers are sufficient. No external packages or services.

## Evaluation notes

`test_pending_then_success` rejects a first-delivery-wins baseline that marks a key seen
before checking status. It returns `{}` instead of `{'a': 100}`. Other tests cover duplicate
successes, account-scoped keys, independent refunds, conflicting retries, timestamp ties,
zero/negative totals, input permutations, generators, and mutation.

## Rubric (100 points)

| Criterion | Points | Evidence |
|---|---:|---|
| Successful status filtering before deduplication | 25 | Pending/success and failed tests |
| Correct scope and idempotence | 25 | Retry and account-scope tests |
| Earliest success and delivery-ID tie break | 20 | Conflicting delivery and tie tests |
| Refund signs, integer totals, zero and absent accounts | 15 | Refund and empty/zero tests |
| Permutation invariance and input integrity | 5 | Generator/mutation test |
| Clear explanation and linear expected complexity | 10 | Manual review |

Pass: at least 80 points, with pending/success, retry, and account-scope tests mandatory.
The manual 10 points are assessed separately; tests are not an automatic 100-point grade.

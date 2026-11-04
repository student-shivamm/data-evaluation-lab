# Two-minute walkthrough

Suggested screen route: README, each problem's example, reference implementation, then terminal.
This is a narration script, not a recorded video.

## 0:00 to 0:20: The idea

This repository tests three data-engineering mistakes that produce plausible answers.
Every problem specifies its input contract and edge cases before presenting code.
All examples are synthetic, and everything runs with the Python standard library.

## 0:20 to 0:50: Point-in-time features

Open the first problem. An event happened at time four, but arrived at time nine.
A prediction at time five cannot use it. The reference filters both clocks, then selects
by event time, arrival time, and revision. The wrong baseline filters only event time.
The counterexample proves that it leaks future knowledge, returning forty instead of twenty.

## 0:50 to 1:15: Billing retries

The second problem treats a webhook delivery and a logical payment as different things.
A pending delivery must not hide a later success. Deduplication uses both account and
operation, and cents stay as integers. The wrong baseline consumes a key too early.
Other tests check refunds, conflicting retries, timestamp ties, and input order.

## 1:15 to 1:40: Capacity windows

The third problem measures elapsed overload time. Reservations exclude their ending
instant, so adjacent intervals do not overlap. The reference clips to the window and
sweeps grouped changes. It scales with the number of reservations, even when timestamps
are a trillion minutes apart. A small independent oracle checks random cases.

## 1:40 to 2:00: Verify and grade

Run `python -m unittest discover -s tests -v` to check the references. Then run
`python tools/demonstrate_failures.py` to see the three expected baseline failures.
Each task has a rubric, mandatory correctness gates, and a human explanation component.
Public tests are useful evidence, but passing them alone does not establish general ability.

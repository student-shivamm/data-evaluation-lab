# Data Evaluation Lab

Three compact Python evaluation tasks about failures that can survive a convincing code
review: future-data leakage, retry-driven billing errors, and interval boundary mistakes.
Each task includes a precise contract, a reference implementation, a deliberately incorrect
baseline, executable counterexamples, and a grading rubric.

All records and examples are synthetic. No company data, credentials, or assessment material
is included. These are independent practice tasks, with no affiliation to any hiring platform.

## Run locally

Python 3.10 or newer. No third-party dependencies.

```sh
python -m unittest discover -s tests -v
python tools/demonstrate_failures.py
```

The first command runs 22 test methods against the reference solutions. The second runs
one targeted test against each incorrect baseline and succeeds only when all three produce
the expected assertion failures. Expected baseline failures are evidence, not a broken build.

## The tasks

| Task | What it measures | Counterexample |
|---|---|---|
| [Point-in-time features](problems/01-point-in-time-features.md) | Two-clock data reasoning and deterministic selection | Past event, future arrival |
| [Idempotent billing](problems/02-idempotent-billing.md) | Status handling, scoped keys, exact arithmetic | Pending delivery before success |
| [Capacity windows](problems/03-capacity-windows.md) | Half-open intervals, sweep-line reasoning, scale | Adjacent reservations |

Read a problem before opening its reference solution. `solutions/` contains the references;
`baselines/` contains intentionally wrong implementations; `tests/` contains the checks.
[The walkthrough](WALKTHROUGH.md) explains the design in about two minutes.

## Evaluate another implementation

Create an importable `candidate/` directory with `__init__.py`, `asof.py`, `billing.py`,
and `capacity.py`, implementing the functions specified in the problem documents.

PowerShell:

```powershell
$env:CANDIDATE_PACKAGE = 'candidate'
python -m unittest discover -s tests -v
Remove-Item Env:CANDIDATE_PACKAGE
```

macOS/Linux:

```sh
CANDIDATE_PACKAGE=candidate python -m unittest discover -s tests -v
```

Use a disposable environment and an external timeout for untrusted submissions. The
runner imports and executes Python directly; it is not a sandbox. Do not run the complete
suite against `baselines`, whose interval implementation intentionally scans every minute.

## Grading and limits

Each problem defines a 100-point rubric and mandatory correctness gates. Tests provide
behavioral evidence; explanation, complexity, and readability require human review.
The tests are public, so passing them is not evidence against overfitting and is not a
certification of general coding ability. No claim is made that any particular model has
been benchmarked. There are no secret tests or measured hiring outcomes.

## License

MIT. See [LICENSE](LICENSE).

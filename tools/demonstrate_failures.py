"""Run one targeted counterexample per deliberately incorrect baseline."""
import os
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[1]
targets = [
    'tests.test_asof.AsOfTests.test_late_arrival_does_not_leak',
    'tests.test_billing.BillingTests.test_pending_then_success',
    'tests.test_capacity.CapacityTests.test_adjacent_reservations_do_not_overlap',
]
env = dict(os.environ, CANDIDATE_PACKAGE='baselines')
unexpected = False
for target in targets:
    print('\nCounterexample:', target, flush=True)
    run = subprocess.run([sys.executable, '-m', 'unittest', '-v', target], cwd=root, env=env,
                         capture_output=True, text=True)
    print(run.stdout + run.stderr, end='')
    # A crashing/import-failing baseline is not evidence of a semantic counterexample.
    expected = run.returncode == 1 and 'FAIL:' in run.stderr and 'ERROR:' not in run.stderr
    print('EXPECTED COUNTEREXAMPLE' if expected else 'UNEXPECTED RESULT', flush=True)
    unexpected |= not expected
sys.exit(1 if unexpected else 0)

import copy
import importlib
import os
import random
import unittest

overloaded_minutes = importlib.import_module(os.getenv('CANDIDATE_PACKAGE', 'solutions') + '.capacity').overloaded_minutes

def reservation(start, end, units=1):
    return dict(start=start, end=end, units=units)

class CapacityTests(unittest.TestCase):
    def test_adjacent_reservations_do_not_overlap(self):
        self.assertEqual(overloaded_minutes([reservation(0, 5), reservation(5, 10)], 0, 10, 1), 0)

    def test_exact_capacity_is_not_overload(self):
        self.assertEqual(overloaded_minutes([reservation(0, 10, 2)], 0, 10, 2), 0)

    def test_clip_to_window(self):
        rows = [reservation(-10, 4, 3), reservation(8, 30, 3), reservation(30, 40, 9)]
        self.assertEqual(overloaded_minutes(rows, 0, 10, 2), 6)

    def test_nested_overlap_counts_elapsed_time_once(self):
        rows = [reservation(0, 10, 2), reservation(2, 8, 2), reservation(4, 6, 2)]
        self.assertEqual(overloaded_minutes(rows, 0, 10, 3), 6)

    def test_zero_length_empty_and_zero_capacity(self):
        self.assertEqual(overloaded_minutes([], 0, 10, 0), 0)
        self.assertEqual(overloaded_minutes([reservation(3, 3, 99)], 0, 10, 0), 0)
        self.assertEqual(overloaded_minutes([reservation(1, 4)], 2, 2, 0), 0)
        self.assertEqual(overloaded_minutes([reservation(1, 4)], 0, 10, 0), 3)

    def test_large_sparse_window(self):
        rows = [reservation(0, 10**12, 2), reservation(3, 7, 1)]
        self.assertEqual(overloaded_minutes(rows, 0, 10**12, 2), 4)

    def test_seeded_cases_against_independent_tick_oracle(self):
        rng = random.Random(41)
        for _ in range(150):
            rows = []
            for _ in range(rng.randrange(15)):
                a, b = sorted([rng.randrange(-5, 21), rng.randrange(-5, 21)])
                rows.append(reservation(a, b, rng.randrange(1, 5)))
            saved = copy.deepcopy(rows)
            cap = rng.randrange(6)
            expected = sum(sum(r['units'] for r in rows if r['start'] <= t < r['end']) > cap
                           for t in range(15))
            self.assertEqual(overloaded_minutes(iter(rows), 0, 15, cap), expected)
            self.assertEqual(rows, saved)

    def test_split_and_shift_invariance(self):
        original = [reservation(1, 9, 3), reservation(5, 12, 2)]
        split = [reservation(1, 4, 3), reservation(4, 9, 3), reservation(5, 12, 2)]
        shifted = [reservation(r['start']+100, r['end']+100, r['units']) for r in original]
        self.assertEqual(overloaded_minutes(original, 0, 15, 3), 4)
        self.assertEqual(overloaded_minutes(split, 0, 15, 3), 4)
        self.assertEqual(overloaded_minutes(shifted, 100, 115, 3), 4)

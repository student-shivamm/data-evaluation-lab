import copy
import importlib
import os
import random
import unittest

features_at = importlib.import_module(os.getenv('CANDIDATE_PACKAGE', 'solutions') + '.asof').features_at

def row(entity='a', event=1, available=1, revision=1, value=10):
    return dict(entity=entity, event_at=event, available_at=available, revision=revision, value=value)

class AsOfTests(unittest.TestCase):
    def test_late_arrival_does_not_leak(self):
        rows = [row(event=2, available=2, value=20), row(event=4, available=9, value=40)]
        self.assertEqual(features_at(rows, [dict(entity='a', at=5)]), [20])

    def test_future_correction_and_tie_break(self):
        rows = [row(event=2, available=2, value=10),
                row(event=2, available=4, revision=2, value=20),
                row(event=2, available=4, revision=3, value=30),
                row(event=2, available=8, revision=4, value=90)]
        self.assertEqual(features_at(rows, [dict(entity='a', at=t) for t in [2, 4, 8]]), [10, 30, 90])

    def test_event_time_precedes_ingestion_order(self):
        rows = [row(event=1, available=6, value=10), row(event=3, available=4, value=30)]
        self.assertEqual(features_at(rows, [dict(entity='a', at=7)]), [30])

    def test_missing_entities_zero_and_boundaries(self):
        rows = [row(value=0), row(entity='b', value=99)]
        queries = [dict(entity=e, at=t) for e, t in [('a', 0), ('a', 1), ('b', 1), ('c', 10)]]
        self.assertEqual(features_at(rows, queries), [None, 0, 99, None])

    def test_permutation_invariance_and_no_mutation(self):
        rows = [row(event=i, available=i+2, value=i) for i in range(20)]
        queries = [dict(entity='a', at=i) for i in range(25)]
        saved = copy.deepcopy(rows)
        expected = [None, None] + list(range(20)) + [19, 19, 19]
        rng = random.Random(7)
        for _ in range(12):
            shuffled = list(rows)
            rng.shuffle(shuffled)
            self.assertEqual(features_at(iter(shuffled), queries), expected)
        self.assertEqual(rows, saved)

    def test_empty(self):
        self.assertEqual(features_at([], [dict(entity='a', at=3)]), [None])
        self.assertEqual(features_at([], []), [])

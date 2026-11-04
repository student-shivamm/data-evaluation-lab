import copy
import importlib
import os
import random
import unittest

net_cents = importlib.import_module(os.getenv('CANDIDATE_PACKAGE', 'solutions') + '.billing').net_cents

def event(account='a', operation='x', status='succeeded', kind='charge', amount=100, at=1, delivery='d1'):
    return dict(account=account, operation=operation, status=status, kind=kind,
                amount_cents=amount, received_at=at, delivery_id=delivery)

class BillingTests(unittest.TestCase):
    def test_pending_then_success(self):
        rows = [event(status='pending'), event(at=2, delivery='d2')]
        self.assertEqual(net_cents(rows), {'a': 100})

    def test_retries_are_not_revenue(self):
        rows = [event(), event(at=3, delivery='retry'), event()]
        self.assertEqual(net_cents(rows), {'a': 100})

    def test_operation_ids_are_account_scoped(self):
        self.assertEqual(net_cents([event(), event(account='b', amount=70)]), {'a': 100, 'b': 70})

    def test_refund_is_separate_and_can_precede_charge(self):
        rows = [event(operation='refund', kind='refund', amount=40, at=0), event()]
        self.assertEqual(net_cents(rows), {'a': 60})

    def test_first_success_wins_even_if_later_delivery_conflicts(self):
        rows = [event(at=3, amount=900), event(at=1, amount=100)]
        self.assertEqual(net_cents(rows), {'a': 100})

    def test_delivery_id_breaks_timestamp_ties(self):
        rows = [event(delivery='z', amount=900), event(delivery='a', amount=100)]
        self.assertEqual(net_cents(rows), {'a': 100})

    def test_empty_failed_zero_and_negative_net(self):
        self.assertEqual(net_cents([]), {})
        self.assertEqual(net_cents([event(status='failed')]), {})
        self.assertEqual(net_cents([event(amount=0)]), {'a': 0})
        self.assertEqual(net_cents([event(kind='refund', amount=50)]), {'a': -50})

    def test_permutation_invariance_generators_and_no_mutation(self):
        rows = [event(status='pending'), event(at=2), event(at=4),
                event(operation='r', kind='refund', amount=30, at=5)]
        saved = copy.deepcopy(rows)
        rng = random.Random(23)
        for _ in range(20):
            shuffled = list(rows)
            rng.shuffle(shuffled)
            self.assertEqual(net_cents(iter(shuffled)), {'a': 70})
        self.assertEqual(rows, saved)

#!/usr/bin/python3.7

import unittest

import algebra
from algebra import bounded_miller_test
from hss import make_sum_program


class PrimeGeneration(unittest.TestCase):
    def test_low_bound(self):
        cases = [13, 1093, 55987, 131071, 132049, 524287]
        for n in cases:
            result = bounded_miller_test(n, bound=algebra.SIMPLE_PRIME_BOUND)
            self.assertTrue(result)

        comps = [2**8 * 5, 3**4 * 2**3, 1 * 2 * 3 * 4 * 5 * 6 * 7 * 8]
        for comp in comps:
            result = bounded_miller_test(comp, bound=algebra.SIMPLE_PRIME_BOUND)
            self.assertFalse(result)

class Metaprogramming(unittest.TestCase):
    def test_make_sum(self):
        n = 5
        correct = [
                ('load', 0, 0),
                ('load', 1, 1),
                ('load', 2, 2),
                ('load', 3, 3),
                ('load', 4, 4),
                ('add', 5, 0, 1),
                ('add', 6, 5, 2),
                ('add', 7, 6, 3),
                ('add', 8, 7, 4),
                ('out', 8)
        ]
        output = make_sum_program(n)
        for (o, c) in zip(output, correct):
            self.assertEqual(o, c)

if __name__ == "__main__":
    unittest.main()

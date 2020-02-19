#!/usr/bin/python3.7

import unittest

import algebra
from algebra import bounded_miller_test


class PrimeGeneration(unittest.TestCase):
    def test_low_bound(self):
        cases = [13, 1093, 55987, 131071, 132049, 524287]
        for n in cases:
            result = bounded_miller_test(n, bound=algebra.SIMPLE_PRIME_BOUND)
            self.assertTrue(result)

        exps = [4, 2, 2, 2, 2, 1]
        for (exp,n) in zip(exps,cases):
            result = bounded_miller_test(2**exp * n)
            self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()

import unittest
import algebra
from algebra import bounded_miller_test, crypto_prime, conversion_friendly_primes

class Prime(unittest.TestCase):
    def test_low_bound(self):
        cases = [13, 1093, 55987, 131071, 132049, 524287]
        for n in cases:
            result = bounded_miller_test(n, bound=algebra.SIMPLE_PRIME_BOUND)
            self.assertTrue(result)

        comps = [2**8 * 5, 3**4 * 2**3, 1 * 2 * 3 * 4 * 5 * 6 * 7 * 8]
        for comp in comps:
            result = bounded_miller_test(comp, bound=algebra.SIMPLE_PRIME_BOUND)
            self.assertFalse(result)

    def test_crypto_prime(self):
        security = 8
        iterations = 5
        divisor = 2**32
        for _ in range(iterations):
            p = crypto_prime(security)
            self.assertTrue(0 < p)
            self.assertTrue(p < divisor)
    
    def test_conversion_friendly_primes(self):
        λ = 8
        iterations = 10
        for _ in range(iterations):
            (p,q)=conversion_friendly_primes(λ)
#            print(f"(p,q)=({p},{q})")

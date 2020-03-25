import unittest

from algebra.modular import *
from algebra.prime import random_prime
import random

class ModularTest(unittest.TestCase):

    def test_modular_exp(self):
        self.assertEqual( modular_exp(base=2, exp=0, divisor=5), 1 )
        self.assertEqual( modular_exp(base=2, exp=1, divisor=5), 2 )
        self.assertEqual( modular_exp(base=2, exp=2, divisor=5), 4 )
        self.assertEqual( modular_exp(base=2, exp=3, divisor=5), 3 )
        self.assertEqual( modular_exp(base=2, exp=4, divisor=5), 1 )
        self.assertEqual( modular_exp(base=2, exp=5, divisor=5), 2 )
        self.assertEqual( modular_exp(base=2, exp=6, divisor=5), 4 )
        self.assertEqual( modular_exp(base=2, exp=47, divisor=5), 3 )

    def test_inv(self, iterations=5):
        # Testing mod 17
        A = [1, 2, 3, 4, 5, 8, 10, 11, 16]
        B = [1, 9, 6, 13, 7, 15, 12, 14, 16]
        f = lambda arr: [ModularInt(x, 17) for x in arr]
        A = f(A)
        B = f(B)
        for (a, b) in zip(A, B):
            self.assertEqual(b, a.inv())
            self.assertEqual(a, b.inv())

        self.assertIsNone( ModularInt(2,44).inv() )
        self.assertIsNone( ModularInt(4,44).inv() )
        self.assertIsNone( ModularInt(17,51).inv() )

        for _ in range(iterations):
            div = random_prime()
            x = ModularInt( random.randrange(div), div)
            x_inv = x.inv()
            self.assertIsNotNone(x_inv)
            self.assertEqual(x*x_inv, 1)

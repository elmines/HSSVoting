import unittest
from algebra import ModularInt
from hss import biterate, bit_length, additive_share
import random

class TestShares(unittest.TestCase):
    def test_biterate(self):
        x = ModularInt(0b0000000000000000010101111, 2**8)
        bits = list( biterate(x) )
        self.assertEqual(len(bits), 8)
        self.assertEqual(bits[0], 1)
        self.assertEqual(bits[1], 1)
        self.assertEqual(bits[2], 1)
        self.assertEqual(bits[3], 1)
        self.assertEqual(bits[4], 0)
        self.assertEqual(bits[5], 1)
        self.assertEqual(bits[6], 0)
        self.assertEqual(bits[7], 1)

    def test_bit_length(self):
        divisors = [2, 3, 4, 5]
        correct = [1, 2, 2, 3]
        for (div, correct) in zip(divisors, correct):
            self.assertEqual( bit_length(ModularInt(1, div)), correct )

    def test_additive_share(self, iterations=5):
        divisor = 37
        for _ in range(iterations):
            x = ModularInt( random.randrange(divisor), divisor )
            shares = additive_share(x)
            self.assertEqual( sum(shares), x)

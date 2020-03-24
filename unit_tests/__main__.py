#!/usr/bin/python3.7
import unittest

import algebra
from hss import make_sum_program

from .shares import *
from .prime import *
from .elgamal import *

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

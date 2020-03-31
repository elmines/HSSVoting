import unittest

from hss.rms import *

class TestRMS(unittest.TestCase):
    def test_concat_bits(self):
        x = 0b1010
        y = 0b1111

        self.assertEqual(concat_bits(x,y), 0b10101111)

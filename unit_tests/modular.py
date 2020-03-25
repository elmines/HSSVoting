import unittest

from algebra.modular import *

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

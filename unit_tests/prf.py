import unittest
from hss import *

class prf(unittest.TestCase):

#    def test_identity(self):
#        identifier = 0
#        Φ = PRFGen()
#
#        g = ModularInt(32,63)
#        self.assertNotEqual(g,Φ(0,g))
#        #cannot actually garauntee this since it's supposed to be random.
#        #As identifier approaches infinity, probability of g,Φ(g) being equal
#        #approaches zero
#        self.assertEqual(Φ(0,g),4)
#        #identifier=0, g=32 should give 4

    def test_prefix(self):
        x = ModularInt(0b10101111, 2**8)
        ident = lambda y: y
        first_4 = prefix(ident, 4)
        self.assertEqual(first_4(x), 0b1010)


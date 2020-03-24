import unittest
import algebra
from hss import enc_elgamal, cryptosystem, dec_elgamal

class ElGamal(unittest.TestCase):

    def test_encryption(self):
        (G, e, c) = cryptosystem(16)
        m = G.generator ** 5 # Makes calculating the discrete log go a lot faster
        ct = enc_elgamal(G.generator, e, m)
        m_cand = dec_elgamal(G, c, ct)
        assertEqual(m, m_cand)

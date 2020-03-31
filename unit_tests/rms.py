import unittest

from hss import *

import pdb

class TestRMS(unittest.TestCase):
    def test_concat_bits(self):
        x = 0b1010
        y = 0b1111

        self.assertEqual(concat_bits(x,y), 0b10101111)

    def test_rms_load(self, iterations=10):
        pass
        correct = 0
        print()
        for i in range(iterations):
            correct += self._rms_load_trial()
            #print(f"{correct}/{i+1} correct")

    def _rms_load_trial(self):
        (pk, ek0, ek1, φ) = gen(16)
        (G, e, one_enc, c_encs) = pk

        w = 1
        M = 2

        one0 = ek0[1]
        one1 = ek1[1]
        c0   = ek0[2]
        c1   = ek1[2]

        mem0 = (one0, c0)
        mem1 = (one1, c1)

        c = c0 + c1
        (w_enc, prod_encs) = enc(pk, w)
        self.assertEqual(w, dec_elgamal(G, c, w_enc))
        ct = (w_enc, prod_encs)

        δ = math.exp(-6)
        instr_no = 10
        statCon = StaticContext(G=G, φ=φ, M=M, δ_prime=δ)

        out0 = rms_mult(ct, mem0, statCon, RuntimeContext(0, instr_no))
        out1 = rms_mult(ct, mem1, statCon, RuntimeContext(0, instr_no))
        w_cand = out0[0] + out1[0]
        cw_cand = out0[1] + out1[1]

        return (w_cand == w) and (cw_cand == c*w)


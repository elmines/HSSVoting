import math
import unittest
from algebra import ModularInt, discrete_log
from hss import *
import random

import pdb

class TestShares(unittest.TestCase):
    def test_biterate(self):
        x = ModularInt(0b0000000000000000010101111, 2**8)
        bits = list( biterate(x) )
        self.assertEqual(len(bits), 8)
        correct = [1,1,1,1,0,1,0,1]
        for (correct_bit, bit) in zip(correct, bits):
            self.assertEqual(correct_bit, bit)

        y = ModularInt(1, 2**8)
        bits = list( biterate(y) )
        self.assertEqual(len(bits), 8)
        correct = [1,0,0,0,0,0,0,0]
        for (correct_bit, bit) in zip(correct, bits):
            self.assertEqual(correct_bit, bit)


    def test_bit_length(self):
        divisors = [2, 3, 4, 5]
        correct = [1, 2, 2, 3]
        for (div, correct) in zip(divisors, correct):
            self.assertEqual( bit_length(ModularInt(1, div)), correct )

    def test_additive_share(self, iterations=5):
        for _ in range(iterations):
            divisor = random.randrange(1000)
            x = random.randrange(divisor)
            (x0,x1) = additive_share(x, divisor)
            self.assertEqual( (x0+x1) % divisor, x)

    def test_bitwise_enc(self):
        (G, e, c) = cryptosystem(16)
        g = G.generator
        c_enc_bits = bitwise_enc(G, e, c)
        self._compare_bits(G, e, c, c_enc_bits)

    def _compare_bits(self, G, e, c, c_enc_bits):
        correct_c_bits = list(biterate(ModularInt(c, G.order)))
        self.assertEqual(len(correct_c_bits), len(c_enc_bits))
        cand_c_bits = map(lambda b: dec_elgamal(G, c, b), c_enc_bits)
        for (correct_bit, cand_bit) in zip(correct_c_bits, cand_c_bits):
            self.assertEqual(correct_bit, cand_bit)

    def test_gen(self):
        (pk, ekA, ekB, _) = gen(16)
        self.assertEqual(pk, ekA[0])
        self.assertEqual(pk, ekB[0])

        # 1 is additively shared
        self.assertEqual( ekA[1] + ekB[1], 1 )

        (G, e, one_enc, c_enc_bits) = pk

        # c is additively shared
        c = ekA[2] + ekB[2]
        self.assertEqual(dec_elgamal(G, c, one_enc), 1)
        self._compare_bits(G, e, c, c_enc_bits)

    def test_enc(self):
        (pk, ekA, ekB, _) = gen(16)

        (G, e, one_enc, c_enc_bits) = pk
        c = ekA[2] + ekB[2]

        w = random.randrange(G.order)

        (w_enc, prod_encs) = enc(pk, w)

        self.assertEqual(w, dec_elgamal(G, c, w_enc))

        correct_prod_bits = list(map(lambda b: w*b, biterate(ModularInt(c,G.order))))
        cand_prod_bits = list(map(lambda b: dec_elgamal(G, c, b), prod_encs))
        self.assertEqual(correct_prod_bits, cand_prod_bits)

    def test_mult_shares(self):
        (pk, ekA, ekB, _) = gen(16)
        (G, e, _, _) = pk
        g = G.generator
        c = ekA[2] + ekB[2]

        x = random.randrange(2, G.order // 2)
        y = 1 + random.randrange(G.order // x) # mult_shares only works for 0 <= xy < q


        # x as left operand
        cy = c * y 
        x_enc = enc_elgamal(G, e, x)
        self.assertEqual(x, dec_elgamal(G, c, x_enc))
        (yA, yB)   = additive_share(y,  G.order)
        (cyA, cyB) = additive_share(cy, G.order)
        xyA = mult_shares(x_enc, yA, cyA)
        xyB = mult_shares(x_enc, yB, cyB)
        self.assertEqual(xyA*xyB, g**(x*y))

        # x as right operand
        cx = c * x 
        y_enc = enc_elgamal(G, e, y)
        self.assertEqual(y, dec_elgamal(G, c, y_enc))
        (xA, xB)   = additive_share(x,  G.order)
        (cxA, cxB) = additive_share(cx, G.order)
        yxA = mult_shares(y_enc, xA, cxA)
        yxB = mult_shares(y_enc, xB, cxB)
        self.assertEqual(yxA*yxB, g**(x*y))


      

    def test_distributed_d_log(self, iterations=100):
        (pk, ekA, ekB, φ) = gen(16)
        (G, e, one_enc, c_enc_bits) = pk
        g = G.generator
        M = 5
        δ = math.exp(-7)

        correct = 0
        for i in range(iterations):
            x = random.randrange(1, G.order)
            instr_id = random.randrange(10, 100) # A little ways into a program
            φ_prime = Get_phi_prime(instr_id, φ)
            (x0, x1) = additive_share(x, G.order)
            (x0, x1) = (g**x0, g**x1)
            x0 = x0.inv()
            y0 = distributed_d_log(G, x0, δ, M, φ_prime)
            y1 = distributed_d_log(G, x1, δ, M, φ_prime)
            if (y0 - y1) % G.divisor == x: correct += 1
        self.assertTrue(correct > 0) #FIXME: Use a better lower probability bound than this

    def test_convert_shares(self, iterations=100):
        (pk, ekA, ekB, φ) = gen(16)
        (G, e, one_enc, c_enc_bits) = pk
        g = G.generator
        M = 5
        δ = math.exp(-7)

        correct = 0
        for i in range(iterations):
            x = random.randrange(1, G.order)
            instr_id = random.randrange(10, G.order) # A little ways into a program
            (x0, x1) = additive_share(x, G.order)
            (x0, x1) = (g**x0, g**x1)
            y0 = convert_shares(0, x0, instr_id, δ, M, G, φ)
            y1 = convert_shares(1, x1, instr_id, δ, M, G, φ)
            if y0 + y1 == x: correct += 1
        self.assertTrue(correct > 0) #FIXME: Use a better lower probability bound than this

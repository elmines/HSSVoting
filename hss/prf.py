from ctypes import CDLL
import random
from random import Random
from .types import *
from .elgamal import cryptosystem, enc_elgamal
#Pseudo-random function (PRF) from Goldreich-Goldwasser-Micali 1984 (GGM)
def PRFGen(grp: ModularGroup):
    g_length = len(bin(grp.divisor)[2:])
    right_mask = 2**g_length - 1 # A binary string of ones
    rng = CRandom()
    def φ(identifier: int, g: ModularInt):
        id_bits = bin(identifier)[2:] 
        λ = len(id_bits)
        g_val = g.value
        for i in range(λ):
            rand_bits = Random(g_val).getrandbits(2*g_length)
            rng.seed(g_val)
            rand_bits = rng.getrandbits(2*g_length)
            b = (identifier >> i) & 1
            if b: g_val = rand_bits & right_mask  # The right half of rand_bits
            else: g_val = (rand_bits >> g_length) # The left half of rand_bits
#            print(f"id={bin(identifier)},i={i},rand_bits={bin(rand_bits)},g_val={g_val},b={b},G={grp}")
        return ModularInt(g_val,grp.order) # Output must be l bits, so take g_val % G.order
    return φ

class CRandom(object):
    def __init__(self):
        self._libc = CDLL("libc.so.6")
        pass
    def seed(self,s: int):
        self._libc.srand(s)
    def getrandbits(self,n: int):
        return self._libc.random() >> (32 - n)


def Get_phi_prime(identifier:int,φ):
	def phi_prime(g : ModularInt):
		return φ(identifier,g)
	return phi_prime

def prefix(f, n: int):
    def g(*args, **kwargs):
        full = f(*args, **kwargs)
        full_bin = bin(full.value)
        msb = full_bin[2:3]
        new_truncate=full_bin[3:2+n+1]
        old_truncate=full_bin[2:2+n]
        version="old"
#        print(f"full={full},full_bin={full_bin},msb={msb},truncated={truncated}") 
        if (version=="new"):
            #do the optimization of searching for 10^d instead of 0^d from
            #optimizations and applications
            #makes things speedy
            if (msb == "1"):
                if (new_truncate == ''):
                    #stops some annoying error with null strings
                    return 0
                return int(new_truncate, 2)
            else:
                #doesn't matter as long as it isn't zero
                return 1
        else:
            return int(old_truncate,2)
    return g

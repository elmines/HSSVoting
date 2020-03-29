import random
from .types import *
from .elgamal import cryptosystem, enc_elgamal
#Pseudo-random function (PRF) from Goldreich-Goldwasser-Micali 1984 (GGM)
def PRFGen():
	#get binary string of security parameter 1^λ
	def φ(identifier:int,g : int):
		id_bits = str(bin(identifier))[2:] 
		λ = len(id_bits)
		g_length=len(str(bin(g)))-2
		for i in range(λ):
			random.seed(g)
			rand_bits = random.getrandbits(2*g_length)
			G = str(bin(rand_bits))[2:].zfill(2*g_length)
			if id_bits[λ-1-i] == "0":
				g= int(G[0 : g_length],2)
			elif id_bits[λ-1-i] == "1":
				g=int(G[g_length : g_length*2],2)
		return g
	return φ


def Get_phi_prime(identifier:int,φ):
	def phi_prime(g : int):
		return φ(identifier,g)
	return phi_prime

def prefix(f, n: int):
    def g(*args, **kwargs):
        full = f(*args)
        truncated = bin(full)[2:2+n]
        return int(truncated, 2)
    return g

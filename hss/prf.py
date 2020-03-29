import random
from .types import *
from .elgamal import cryptosystem, enc_elgamal
#Pseudo-random function (PRF) from Goldreich-Goldwasser-Micali 1984 (GGM)
def PRFGen():
	#get binary string of security parameter 1^λ
	def φ(identifier:int,g : ModularInt):
		id_bits = bin(identifier)[2:] 
		λ = len(id_bits)
		g_length=len(bin(g.divisor)[2:])
		g_val = g.value
		#g_length=g.divisor
	#	print("id_bits=",id_bits,"λ=",λ,"g_length=",g_length)
		for i in range(λ):
			random.seed(g.value)
			rand_bits = random.getrandbits(2*g_length)
			G = bin(rand_bits)[2:].zfill(2*g_length)
			if id_bits[λ-1-i] == "0":
				g_val= int(G[0 : g_length],2)
			elif id_bits[λ-1-i] == "1":
				g_val=int(G[g_length : g_length*2],2)
		#	print("i=",i,",rand bits=",rand_bits,"G=",G,"id_bits[λ-1-i]=",id_bits[λ-1-i],"g=",g) 
		return ModularInt(g_val,g.divisor)
	return φ


def Get_phi_prime(identifier:int,φ):
	def phi_prime(g : ModularInt):
		return φ(identifier,g)
	return phi_prime

def prefix(f, n: int):
    def g(*args, **kwargs):
        full = f(*args)
        truncated = bin(full)[2:2+n]
        return int(truncated, 2)
    return g

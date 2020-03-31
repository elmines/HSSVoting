from typing import Tuple, Union, List, Callable
from algebra import ModularGroup, ModularInt

PK = Tuple[ModularGroup,ModularInt,ModularInt,List[ModularInt]]
"""
A tuple (group, encryption key, 1_enc, c_encs)

n is the divisor for the three modular integers.
1_enc is the ElGamal encryption of 1 given the encryption key.
c_encs are the ElGamal encryptions of the individual bits of the secret key c.
"""

EK = Tuple[PK, int, int]
"""
A tuple (public key, <1>, <c>) where <x> is an additive share of x
"""

ResultAddress = int
OperandAddress = int
InputAddress = int
RMSAdd  = Tuple["add" , ResultAddress, OperandAddress, OperandAddress]
RMSMult = Tuple["mult", ResultAddress, InputAddress,   OperandAddress]
RMSLoad = Tuple["load", ResultAddress, InputAddress]
RMSOut  = Tuple["out" , OperandAddress]
RMSOp = Union[RMSAdd,RMSMult,RMSLoad,RMSOut]

Ciphertext = Tuple[ModularInt,List[ModularInt]]
"""
([[w]]_c, {[[c^(t)]]_c} for t=0,1,..l ) where w is the input and c is the ElGamal secret key
"""
MemoryVal = Tuple[ModularInt,ModularInt]
"""
(<y>, <cy>) where c is the ElGamal secret key
"""

PRF = Callable[[int, ModularInt],int]
PRFprime = Callable[[ModularInt],int]

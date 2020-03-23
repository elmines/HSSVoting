from typing import Tuple, Union, List
from algebra import ModularInt

PK = Tuple[int,ModularInt,ModularInt,ModularInt,List[ModularInt]]
"""
A tuple (n, generator, encryption key, 1_enc, c_encs)

n is the divisor for the three modular integers.
1_enc is the ElGamal encryption of 1 given the encryption key.
c_encs are the ElGamal encryptions of the individual bits of the secret key c.
"""

EK = Tuple[PK, ModularInt, ModularInt]
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

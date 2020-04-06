from collections import namedtuple
# Local
from .types import *
from .shares import mult_shares, convert_shares, bit_length

StaticContext  = namedtuple("StaticContext", ["G", "M", "φ", "δ_prime"])
RuntimeContext = namedtuple("RuntimeContext", ["b", "instr_no"])


def concat_bits(x: int, y: int):
    return (x << len(bin(y)[2:])) + y

class Evaluator(object):
    def __init__(self, G: ModularGroup, program: List[RMSOp], φ, M: int, δ: float):
        self.G = G
        self.program = program
        self.M = M
        self.φ = φ

        l = bit_length(ModularInt(1, G.order))
        self.δ_prime = δ / ((l+1) * M * self.S)

    @property
    def S(self):
        return len(self.program)

    def rms_mult(self, w: Ciphertext, y: MemoryVal, b: int, instr_no: int):
        (G, M, φ, δ_prime) = (self.G, self.M, self.φ, self.δ_prime)
        (w_enc, bitwise_encs) = w
        (y_share, cy_share) = y
        y_share = int(y_share)
        cy_share = int(cy_share)
        
        wy_mult_share = mult_shares(w_enc, y_share, cy_share)
        wy_add_share  = convert_shares(b, wy_mult_share, concat_bits(instr_no, 0), δ_prime, M, G, φ)
        
        cwy_bitwise_shares = []
        for (t, bitwise_enc) in enumerate(bitwise_encs):
            bitwise_mult_share = mult_shares(bitwise_enc, y_share, cy_share)
            cwy_bitwise_shares.append( convert_shares(b, bitwise_mult_share, concat_bits(instr_no,t), δ_prime, M, G, φ) )
        cwy_add_share = sum( map(lambda t: 2**t * cwy_bitwise_shares[t], range(len(cwy_bitwise_shares))) )
        return (wy_add_share, cwy_add_share)


    def public_key_eval(self, b, ek: EK, ct: List[Ciphertext]):
        """
        This is not a thread-safe function
        """
        memory: Dict[int,Tuple[ModularInt]] = dict()
        outputs = []
    
        (pk, one_share, c_share) = ek
    
        ONE = -1
        memory[ONE] = (one_share, c_share)
    
        instr_no = 1

        for (op, *operands) in self.program:
            if min(operands) < 0:
                raise Exception("Negative indices are reserved for the library programmer: {(op,*operands)}")

            if op == "load":
                [j, i] = operands
                memory[j] = self.rms_mult(ct[i], memory[ONE], b, instr_no)
            elif op == "mult":
                [k, i, j] = operands
                memory[k] = self.rms_mult(ct[i], memory[j], b, instr_no)
            elif op == "add":
                [k, i, j] = operands
                (y_i, cy_i) = memory[i]
                (y_j, cy_j) = memory[j]
                memory[k] = (y_i+y_j,cy_i+cy_j)
            elif op == "out":
                [i] = operands
                (y_share, cy_share) = memory[i]
                z_share = y_share
                offset = (self.φ)(instr_no,self.G.generator) 
                if b == 1: z_share = z_share - int(offset)
                else:      z_share = z_share + int(offset)
                outputs.append(z_share)
            else:
                raise Exception(f"Invalid RMS instruction {op}")
            instr_no += 1
        return outputs



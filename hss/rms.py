from .types import *
import operator

def concat_bits(x: int, y: int):
    return (x << len(bin(y)[2:])) + y

def rms_mult(w: Ciphertext, y: MemoryVal, b, φ, δ_prime: float):
    (w_enc, bitwise_encs) = w
    (y_share, cy_share) = y
    y_share = int(y_share)
    cy_share = int(cy_share)
    
    wy_mult_share = mult_shares(w, y_share, cy_share)
    wy_add_share  = convert_shares(self.b, wy_mult_share, concat_bits(self.instr_no, 0), δ_prime, M, self.φ)
    
    cwy_bitwise_shares = []
    for (t, bitwise_enc) in enumerate(bitwise_encs):
        bitwise_mult_share = mult_shares(bitwise_enc, y_share, cy_share)
        cwy_bitwise_shares.append( convert_shares(self.b, bitwise_mult_share, concat_bits(self.instr_no,t), δ_prime, M, self.φ) )
    cwy_add_share = sum( map(lambda t: 2**t * cwy_bitwise_shares[t], range(len(cwy_bitwise_shares))) )
    return (wy_add_share, cwy_add_share)


class Evaluator(object):
    def __init__(G: ModularGroup, program: List[RMSOp], M: int, δ: float):
        self.G = G
        self.program = program
        self.M = M
        self.δ_prime = δ / ((l+1) * M * S)
        self.φ = PRFGen()

    @property
    def S(self):
        return len(self.program)

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

        def _apply_add(self, instr: RMSAdd):
            (_, k, i, j) = instr
            (y_i, cy_i) = memory[i]
            (y_j, cy_j) = memory[j]
            memory[k] = (y_i+y_j,cy_i+cy_j)
        def _apply_mult(self, instr: RMSMult):
            (_, k, i, j) = instr
            memory[k] = rms_mult(ct[i], memory[j])
        def _apply_load(self, instr: RMSLoad):
            (_, j, i) = instr
            memory[j] = rms_mult(ct[i], memory[ONE])
        def _apply_out(self, instr: RMSOut):
            (_, i) = instr
            (y_share, cy_share) = memory[i]
            z_share = y_share
            #FIXME: Add this in later once we know everything else is working
            #offset = (self.φ)(self.instr_no,G.generator) 
            #if b == 1: z_share = z_share - offset
            #else:      z_share = z_share + offset
            outputs.append(z_share)
            
        op_dict = { "add": lambda op: self.apply_add(op),  "mult": lambda op: self.apply_mult(op),
                   "load": lambda op: self.apply_load(op),  "out": lambda op: self.apply_out(op)
        }
        for op in program:
            op_dict[op[0]](op)
            instr_no += 1
        return outputs



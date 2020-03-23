from .types import *
import operator



class Evaluator(object):
    def __init__(group_order: int, g: ModularInt, b: int):
        self.group_order = group_order
        self.g = g
        self.φ = None #FIXME
        self.b = b

    def public_key_eval(self, ek: EK, ct: List[Tuple[ModularInt,ModularInt]], program: List[RMSOp], δ: float):
        """
    
        :param ct: The ciphertexts for each input: ct_i is ( [[w_i]]_c , [[c^(t)w_i]]_c for t in [l] )
    
        Do not use negative indices for any of your RMSOps; those are reserved for the library programmer
        """
        self.memory: Dict[int,Tuple[ModularInt]] = dict()
        self.outputs = []
        self.instr_no = 1
    
        (pk, one_share, c_share) = ek
        δ_prime = δ #TODO: Perform the actual calculation
    
        ONE = -1
        self.memory[ONE] = (one_share, c_share)
    
        instr_no = 1
        op_dict = {
                "add":  lambda op: self.apply_add(op),
                "mult": lambda op: self.apply_mult(op),
                "load": lambda op: self.apply_load(op),
                "out":  lambda op: self.apply_out(op)
        }
        for op in program:
            op_dict[op[0]](op)
            self.instr_no += 1
        return self.outputs

    def _apply_add(self, instr: RMSAdd):
        (_, k, i, j) = instr
        (y_i, cy_i) = self.memory[i]
        (y_j, cy_j) = self.memory[j]
        self.memory[k] = (y_i+y_j,cy_i+cy_j)
    def _apply_mult(self, instr: RMSMult):
        (_, k, i, j) = instr
        result = _mult_no_store(i, j)
        self.memory[k] = result
    def _apply_load(self, instr: RMSLoad):
        (_, j, i) = instr
        result = _mult_no_store(i, ONE)
        self.memory[j] = result
    def _apply_out(self, instr: RMSOut):
        (_, i) = instr
        (y_share, cy_share) = self.memory[i]
        z_share = y_share
        if self.b == 1: z_share *= -1
        z_share += (self.φ)(self.instr_no,self.g) 
        
    def _mult_no_store(self, i: int, j: int) -> Tuple[ModularInt,ModularInt]:
        (w_enc, bitwise_encs) = inputs[i]
        (y_share, cy_share) = self.memory[j]

        wy_mult_share       = mult_shares(ct[i], y_share, cy_share)
        wy_add_share        = convert_shares(b, wy_mult_share, (self.instr_no, 0), δ_prime, M, self.φ)

        cwy_bitwise_shares = []
        for (t, bitwise_enc) in enumerate(bitwise_encs):
            bitwise_mult_share = mult_shares(bitwise_enc, y_share, cy_share)
            cwy_bitwise_shares.append( convert_shares(self.b, bitwise_mult_share, (self.instr_no,t), δ_prime, M, self.φ) )
        cwy_add_share = sum( map(lambda t: 2**t * cwy_bitwise_shares[t], range(len(cwy_bitwise_shares))) )

        return (wy_add_share, cwy_add_share)




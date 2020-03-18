from .shares import EK

class RMSOp(object):
    pass


class RMSAdd(RMSOp):
    def __init__(self, y_i_ind, y_j_ind, y_k_ind):
        self.i = y_i_ind
        self.j = y_j_ind
        self.k = y_k_ind

class RMSMult(RMSOp):
    def __init__(self, w_i_ind, y_j_ind, y_k_ind):
        self.i = w_i_ind
        self.j = y_j_ind
        self.k = y_k_ind

class RMSLoad(RMSOp):
    def __init__(self, w_i_ind, y_k_ind):
        self.i = w_i_ind
        self.k = w_k_ind

class RMSOut(RMSOp):
    def __init__(self, y_i_ind):
        self.i = y_i_ind



def public_key_eval(b: int, ek: EK, ct: Tuple[ModularInt,ModularInt], program: List[RMSOp], error_toler: float):
    """
    Do not use negative indices for any of your RMSOps; those are reserved for the library programmer
    """
    symbol_table: Dict[int,ModularInt] = dict()
    outputs = []

    (pk, one_share, c_share) = ek

    symbol_table[-1] = (one_share, c_share)

    def apply_add(instr: RMSAdd):
        (y_i, cy_i) = symbol_table[instr.i]
        (y_j, cy_j) = symbol_table[instr.j]
        symbol_table[instr.k] = (y_i+y_j,cy_i+cy_j)
    def apply_mult(instr: RMSMult):
        raise NotImplementedError
    def apply_load(instr: RMSLoad):
        mult_instr = 
        raise NotImplementedError
    def apply_out(instr: RMSOut):
        raise NotImplementedError

    def _mult_no_store(i: int, j: int) -> Tuple[ModularInt,ModularInt]:
        pass




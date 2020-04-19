import netsquid as ns

def X(q, prg, *args, **kwargs): prg.apply(INSTR_X, q); return q
def Y(q, prg, *args, **kwargs): prg.apply(INSTR_Y, q); return q
def Z(q, prg, *args, **kwargs): prg.apply(INSTR_Z, q); return q
def H(q, prg, *args, **kwargs): prg.apply(INSTR_H, q); return q
def K(q, prg, *args, **kwargs): prg.apply(INSTR_S, q); return q
def T(q, prg, *args, **kwargs): prg.apply(INSTR_T, q); return q

def Tinv(q, prg, *args, **kwargs): prg.apply(INSTR_ROT_Z, q return q ##TBD should be defined properly

def CNOT(p, q, prg, *args, **kwargs): prg.apply(INSTR_CNOT, [p,q], *args, **kwargs); return p, q

def PREP(prg, *args, **kwargs): prg.apply(INSTR_INIT, q, *args, **kwargs); return q
def MEAS(q, prg, *args, **kwargs): prg.apply(INSTR_MEASURE, q, output_key="""outcome_{q}""", physical = True, *args, **kwargs)

def DISP(q): print(q, f"""QID: {q}"""); return None
def QID(q): return q

#def EPR(): return None
def SEND(q, target_id, node, *args, **kwargs): node.sendQubit(q, target_id, *args, **kwargs); return None ##TBD
def RECV(node, *args, **kwargs): return node.recvQubit(*args, **kwargs) ##TBD
#def TELE(): return None

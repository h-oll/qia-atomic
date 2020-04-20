import netsquid as ns
from netsquid.components.instructions import *

def X(q, host, *args, **kwargs): host.apply(INSTR_X, q); return q
def Y(q, host, *args, **kwargs): host.apply(INSTR_Y, q); return q
def Z(q, host, *args, **kwargs): host.apply(INSTR_Z, q); return q
def H(q, host, *args, **kwargs): host.apply(INSTR_H, q); return q
def K(q, host, *args, **kwargs): host.apply(INSTR_S, q); return q
def T(q, host, *args, **kwargs): host.apply(INSTR_T, q); return q

def Tinv(q, host, *args, **kwargs): host.apply(INSTR_ROT_Z, q); return q ##TBD should be defined properly

def CNOT(p, q, host, *args, **kwargs): host.apply(INSTR_CNOT, [p,q], *args, **kwargs); return p, q

def PREP(host, q = 0, *args, **kwargs): host.apply(INSTR_INIT, q, *args, **kwargs); return q
def MEAS(q, host, *args, **kwargs): host.apply(INSTR_MEASURE, q, output_key=f"""outcome_{q}""", physical = True, *args, **kwargs)

def DISP(q): print(q, f"""QID: {q}"""); return None
def QID(q): return q

def EPR(*args, **kwargs): return None
def SEND(q, target_id, node, *args, **kwargs): node.sendQubit(q, target_id, *args, **kwargs); return None ##TBD
def RECV(node, *args, **kwargs): return node.recvQubit(*args, **kwargs) ##TBD
def TELE(*args, **kwargs): return None

mapping = {
    "X": X,
    "Y": Y,
    "Z": Z,
    "H": H,
    
    "K": K,
    "T": T,
    "Tinv":Tinv,

    "CNOT": CNOT,

    "PREP": PREP,
    "MEAS": MEAS,
    "DISP": DISP,
    "QID": QID,
    
    "EPR": EPR,
    "SEND": SEND,
    "RECV": RECV,
    "TELE": TELE
    }


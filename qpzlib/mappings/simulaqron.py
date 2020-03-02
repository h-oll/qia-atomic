from cqc.pythonLib import qubit

def X(q): q.X(); return q
def Y(q): q.Y(); return q
def Z(q): q.Z(); return q
def H(q): q.H(); return q

def K(q): q.K(); return q
def T(q): q.T(); return q

def CNOT(p,q): p.CNOT(q); return p, q

def PREP(node): return qubit(node)
def MEAS(q): return q.measure()
def DISP(q): print(q, f"""QID: {q._qID}"""); return None
def QID(q): return q._qID

#def EPR(): return None
def SEND(q, target_id, node): node.sendQubit(q, target_id); return None
def RECV(node): return node.recvQubit()
#def TELE(): return None

mapping = {
    "X": X,
    "Y": Y,
    "Z": Z,
    "H": H,
    
    "K": K,
    "T": T,

    "CNOT": CNOT,

    "PREP": PREP,
    "MEAS": MEAS,
    "DISP": DISP,
    "QID": QID,
    
    "EPR": None,
    "SEND": SEND,
    "RECV": RECV,
    "TELE": None
    }


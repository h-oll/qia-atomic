from cqc.pythonLib import qubit

def X(q): q.X(); return q
def Y(q): q.Y(); return q
def Z(q): q.Z(); return q
def H(q): q.H(); return q
def K(q): q.K(); return q
def T(q): q.T(); return q
def CNOT(p,q): p.CNOT(q); return p, q


mapping = {
    "X": X,
    "Y": Y,
    "Z": Z,
    "H": H,
    
    "K": K,
    "T": T,

    "CNOT": CNOT,

    "PREP": lambda node: qubit(node),
    "MEAS": lambda q: q.measure(),
    "DISP": lambda q: print(q, f"""QID: {q._qID}"""),
    "QID": lambda q: q._qID,
    
    "EPR": None,
    "SEND": lambda q, target_id, node: node.sendQubit(q, target_id),
    "RECV": lambda node: node.recvQubit(),
    "TELE": None,
    }


from cqc.pythonLib import qubit

def X(q, host, *args, **kwargs): q.X(*args, **kwargs); return q
def Y(q, host, *args, **kwargs): q.Y(*args, **kwargs); return q
def Z(q, host, *args, **kwargs): q.Z(*args, **kwargs); return q
def H(q, host, *args, **kwargs): q.H(*args, **kwargs); return q

def K(q, host, *args, **kwargs): q.K(*args, **kwargs); return q
def T(q, host, *args, **kwargs): q.T(*args, **kwargs); return q

def Tinv(q, host, *args, **kwargs): q.rot_Z(224, *args, **kwargs); return q

def CNOT(p, q, host, *args, **kwargs): p.cnot(q, *args, **kwargs); return p, q

def PREP(host, *args, **kwargs): return qubit(host, *args, **kwargs)
def MEAS(q, host, *args, **kwargs): return q.measure(*args, **kwargs)

def DISP(q, host, *args, **kwargs): print(q, f"""QID: {q._qID}"""); return None
def QID(q, host, *args, **kwargs): return q._qID

def EPR(*args, **kwargs): return None
def SEND(q, target_id, host, *args, **kwargs): host.sendQubit(q, target_id, *args, **kwargs); return None
def RECV(host, *args, **kwargs): return host.recvQubit(*args, **kwargs)
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


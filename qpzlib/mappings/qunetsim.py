#from components.host import Host as QNSHost
from objects.qubit import Qubit 

def X(q): q.X(); return q
def Y(q): q.Y(); return q
def Z(q): q.Z(); return q
def H(q): q.H(); return q

def K(q): q.K(); return q
def T(q): q.T(); return q

def CNOT(p,q): p.CNOT(q); return p, q

def PREP(node): return Qubit(node)
def MEAS(q): return q.measure()
def DISP(q): print(q, f"""QID: {q.id}"""); return None
def QID(q): return q.id

#def EPR(): return None
def SEND(q, target_id, node): node.send_qubit(target_id, q, await_ack=True); return None
def RECV(source_id, node): return node.get_data_qubit(host_id=source_id, wait=10)
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

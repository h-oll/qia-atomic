import netsquid as ns

def X(q, *args, **kwargs): ns.qubits.operate(q, ns.qubits.operators.X); return q
def Y(q, *args, **kwargs): ns.qubits.operate(q, ns.X); return q
def Z(q, *args, **kwargs): ns.qubits.operate(q, ns.X); return q
def H(q, *args, **kwargs): ns.qubits.operate(q, ns.X); return q
def K(q, *args, **kwargs): ns.qubits.operate(q, ns.X); return q
def T(q, *args, **kwargs): ns.qubits.operate(q, ns.X); return q

def Tinv(q, *args, **kwargs): q.rot_Z(224, *args, **kwargs); return q

def CNOT(p, q, *args, **kwargs): p.cnot(q, *args, **kwargs); return p, q

def PREP(node, *args, **kwargs): return qubit(node, *args, **kwargs)
def MEAS(q, *args, **kwargs): return q.measure(*args, **kwargs)

def DISP(q): print(q, f"""QID: {q._qID}"""); return None
def QID(q): return q._qID

#def EPR(): return None
def SEND(q, target_id, node, *args, **kwargs): node.sendQubit(q, target_id, *args, **kwargs); return None
def RECV(node, *args, **kwargs): return node.recvQubit(*args, **kwargs)
#def TELE(): return None

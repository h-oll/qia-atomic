from cqc.pythonLib import qubit

mapping = {
    "X": lambda q: q.X(),
    "Y": lambda q: q.Y(),
    "Z": lambda q: q.Z(),
    "H": lambda q: q.H(),
    "CNOT": lambda q1, q2: q1.cnot(q2),
    "S" : None,
    "T": lambda q: q.T(),
    "PREP": lambda node: qubit(node),
    "MEAS": lambda q: q.measure(),
    "DISP": lambda q: print(q),

    "EPR": None,
    "SEND": lambda q, target_id, node: node.sendQubit(q, target_id),
    "RECV": lambda node: node.recvQubit(),
    "UUID": lambda q: q._qID,
    "TELE": None,

    "Qubit": qubit #not useful anymore
    }


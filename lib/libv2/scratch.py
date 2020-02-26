import uuid
from cqc.pythonLib import CQCConnection, qubit

from undersqore import undersqore

#########################################################################
## settings for SimulaQron
## will be moved to separate file later on

class QQubit(qubit):
    def __init__(self, node):
        super().__init__(node)
        self.uq_uuid = uuid.uuid4()

    #def __str__(self):
    #    return super.__str__(self) + f""" | uq_uuid: {self.uq_uuid}"""

backend_mapping = {
    "X": lambda q: q.X(),
    "Y": lambda q: q.Y(),
    "Z": lambda q: q.Z(),
    "H": lambda q: q.H(),
    "CNOT": lambda q1, q2: q1.cnot(q2),
    "S" : None,
    "T": lambda q: q.T(),
    "MEAS": lambda q: q.measure(),
    "DISP": None,

    "EPR": None,
    "SEND": lambda q, target_id, node: node.sendQubit(q, target_id),
    "RECV": lambda node: node.recvQubit(),
    "TELE": None,

    "Qubit": QQubit
    }
#########################################################################




with CQCConnection("Alice") as Alice:

    _ = undersqore(backend_mapping, Alice)
    
    #use library to prepare a single qubit (with our uuid)
    
    # q = _.PREP(Alice)
    # print(q.uq_uuid)
    # print(q)
    # print(q.cqc)

    #q = qubit(Alice)
    #print(q)
    #print(q.cqc)

    

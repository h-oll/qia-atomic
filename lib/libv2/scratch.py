from cqc.pythonLib import CQCConnection

from undersqore import undersqore
from mappings.simulaqron import mapping

with CQCConnection("Alice") as Alice:

    _ = undersqore(mapping, Alice)
    
    #use library to prepare a single qubit (with our uuid)
    
    #q = QQubit(Alice)
    q = _.PREP()#Alice)
    #print(q.uq_uuid)
    print(q)
    # print(q.cqc)

    #q = qubit(Alice)
    #print(q)
    #print(q.cqc)

    _.SEND(q, "Bob")


with CQCConnection("Bob") as Bob:
    _ = undersqore(mapping, Bob)

    #q = _.RECV()
    #q = Bob.recvQubit()
    #q = backend_mapping["RECV"](Bob)
    q = _.RECV()
    #print(q.uq_uuid)
    print(q)

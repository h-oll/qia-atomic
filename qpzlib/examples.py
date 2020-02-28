from qpzlib import qpzlib

###################################
## Examples using SimulaQron / CQC

from cqc.pythonLib import CQCConnection
from mappings.simulaqron import mapping

with CQCConnection("Alice") as Alice:

    _ = qpzlib(mapping, Alice)
    
    #use library to prepare a single qubit
    # all commands are applied locally: no need to specify the node
    q = _.PREP() 

    # print command from the qubit class provided by the backend
    print(q) 

    # print command using the library
    _.DISP(q)

    # sending to Bob (need to pass the arguments using the syntax used by the backend used)
    _.SEND(q, "Bob") 


with CQCConnection("Bob") as Bob:
    _ = qpzlib(mapping, Bob)

    # receive a qubit
    q = _.RECV()

    # show info about this qubit
    _.DISP(q)

    _.qotp_enc(q)

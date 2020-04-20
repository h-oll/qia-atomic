import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

from qpzlib import qpzlib 

###################################
## Examples using SimulaQron / CQC

def simulaqron():

    from cqc.pythonLib import CQCConnection
    from mappings.simulaqron import mapping

    with CQCConnection("Alice") as Alice:

        _ = qpzlib(mapping, Alice)

        #use library to prepare a single qubit
        # all commands are applied locally: no need to specify the node
        q = _.PREP()

        # show info about created qubit
        _.DISP(q)

        # flip the qubit
        _.X(q)
        
        # sending to Bob (need to pass the arguments using the syntax used by the backend used)
        _.SEND(q, "Bob") 


    with CQCConnection("Bob") as Bob:
        _ = qpzlib(mapping, Bob)

        # receive a qubit
        q = _.RECV()

        # show info about this qubit
        _.DISP(q)

if __name__ == '__main__':
    simulaqron()

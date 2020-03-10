class Gate:
    def __init__(self, _): 
        def CSWAP(q0, q1, q2):        
            """
            controll swap on two qubits q1 and q2, q0 is a controll qubit
            implementation from https://www.mathstat.dal.ca/~selinger/quipper/doc/Quipper-Libraries-GateDecompositions.html
            params : 
            q0,q1,q2: qubits

            """
            _.CNOT(q2,q1)
            _.H(q2)
            _.T(q0)
            _.T(q1)
            _.T(q2)
            _.CNOT(q1,q0)
            _.CNOT(q2,q1)
            _.CNOT(q0,q2)
            _.Tinv(q1)
            _.T(q2)
            _.CNOT(q0,q1)
            _.Tinv(q0)
            _.Tinv(q1)
            _.CNOT(q2,q1)
            _.CNOT(q0,q2)
            _.CNOT(q1,q0)
            _.H(q2)
            _.CNOT(q2,q1)
            return

        self.CSWAP = CSWAP

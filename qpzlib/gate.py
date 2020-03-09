class Mixin:

    def gate_CSWAP(self, q0, q1, q2):
        
        """
        controll swap on two qubits q1 and q2, q0 is a controll qubit
        implementation from https://www.mathstat.dal.ca/~selinger/quipper/doc/Quipper-Libraries-GateDecompositions.html
        params : 
        q0,q1,q2: qubits
        
        """
        self.CNOT(q2,q1)
        self.H(q2)
        self.T(q0)
        self.T(q1)
        self.T(q2)
        self.CNOT(q1,q0)
        self.CNOT(q2,q1)
        self.CNOT(q0,q2)
        self.Tinv(q1)
        self.T(q2)
        self.CNOT(q0,q1)
        self.Tinv(q0)
        self.Tinv(q1)
        self.CNOT(q2,q1)
        self.CNOT(q0,q2)
        self.CNOT(q1,q0)
        self.H(q2)
        self.CNOT(q2,q1)
        return

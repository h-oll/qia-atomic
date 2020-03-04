class qpzlib:
    def __init__(self, backend_mapping, node):

        self.X = backend_mapping["X"]
        self.Y = backend_mapping["Y"]
        self.Z = backend_mapping["Z"]
        self.H = backend_mapping["H"]
        self.CNOT = backend_mapping["CNOT"]

        self.K = backend_mapping["K"]
        self.T = backend_mapping["T"]
        self.invT = backend_mapping["invT"]

        self.PREP = lambda *args: backend_mapping["PREP"](*args, node=node) 
        self.MEAS = backend_mapping["MEAS"]
        self.DISP = backend_mapping["DISP"]
        self.QID = backend_mapping["QID"]
        
        self.EPR = backend_mapping["EPR"]
        self.SEND = lambda *args: backend_mapping["SEND"](*args, node=node)
        self.RECV = lambda *args: backend_mapping["RECV"](*args, node=node)
        self.TELE = backend_mapping["TELE"]

        def check():
            reqs = {
                "qotp": ['X', 'Y', 'Z'],
            }

            for f in reqs:
                availability= True
                for g in reqs[f]:
                    if not(hasattr(self,g)) or (backend_mapping[g] is None): availability = False
                if availability:
                    print(f"""Quantum Protocol Zoo Lib: {f} is available""")
                else:
                    print(f"""Quantum Protocol Zoo Lib: {f} is unavailable""")
                    setattr(self, f, self.raiseException)

        check()

    def raiseException(*args, **kwargs):
        raise NameError(f"""Quantum Protocol Zoo Lib function is unavailable because the backend does not provide a necessary functionality""")


    def qotp(self, block, key):
        """
        Quantum One Time Pad Encryption/Decryption

        Qubit Iterable -> Integer Iterable -> Qubit Iterable

        Applies Quantum One Time Pad to an iterable of qubits and a iterable of ints  in 0..3 (0=I, 1=X, 2=Z, 3=Y). 
        Returns an iterable of qubits.
        Needs X,Y,Z operations.

        Tests: 
          - operation is self inverse 
          - output states are random
        """

        for q, k in zip(block, key):
            if k == 0: pass
            if k == 1: self.X(q)
            if k == 2: self.Z(q)
            if k == 3: self.Y(q)
            yield q


    
    def CSWAP(self, q0, q1, q2):

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
        self.invT(q1)
        self.T(q2)
        self.CNOT(q0,q1)
        self.invT(q0)
        self.invT(q1)
        self.CNOT(q2,q1)
        self.CNOT(q0,q2)
        self.CNOT(q1,q0)
        self.H(q2)
        self.CNOT(q2,q1)
        return

    def swap_test(self, conn, q1, q2):

        """
        launch the swap test
        params:
            conn: string, node to do the swap
            q1, q2: iterable of qubits

        """

        q=zip(q1,q2)
        q0 = self.PREP()
        self.H(q0)

        for q1,q2 in q:
            self.CSWAP(q0, q1, q2)
            print(self.MEAS(q1), self.MEAS(q2))

        self.H(q0)
        m = self.MEAS(q0)

        print ('q0 measure is ', m)
        
        return m

    def qrng(self) :

        """
        return random 0 or 1 via hadarmard gate
        param:
            location_strings: string, node where the q.h is happening, 'Alice' by default
        
        """
        q=self.PREP()
        self.H(q)
        number = self.MEAS()
        print('Outcome of the measure:', number)
        return number

    def pauli_prep(self, bit, base):
        if base == 1: 
            if bit == 0 : q = self.H(self.PREP())
            elif bit == 1 : q = self.H(self.X(self.PREP()))
        elif base == 2: 
            if bit == 0 : q = self.PREP()
            elif bit == 1 : q = self.X(self.PREP())
        if base == 3: 
            if bit == 0 : q = self.K(self.PREP())
            elif bit == 1 : q = self.K(self.X(self.PREP()))
        else: raise NameError("Cannot prepare this state")
        return q


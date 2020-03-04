class qpzlib:
    def __init__(self, backend_mapping, node):

        self.X = backend_mapping["X"]
        self.Y = backend_mapping["Y"]
        self.Z = backend_mapping["Z"]
        self.H = backend_mapping["H"]
        self.CNOT = backend_mapping["CNOT"]

        self.K = backend_mapping["K"]
        self.T = backend_mapping["T"]

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

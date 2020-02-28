import uuid

class undersqore:
    def __init__(self, backend_mapping, node):

        self.X = backend_mapping["X"]
        self.Y = backend_mapping["Y"]
        self.Z = backend_mapping["Z"]
        self.H = backend_mapping["H"]
        self.CNOT = backend_mapping["CNOT"]

        self.S = backend_mapping["S"]
        self.T = backend_mapping["T"]

        self.PREP = lambda: backend_mapping["PREP"](node) 
        self.MEAS = backend_mapping["MEAS"]
        self.DISP = backend_mapping["DISP"]

        self.EPR = backend_mapping["EPR"]
        self.SEND = lambda *args: backend_mapping["SEND"](*args, node=node)
        self.RECV = lambda: backend_mapping["RECV"](node)
        self.TELE = backend_mapping["TELE"]

        def check():
            reqs = {
                "qotp_enc": ['X', 'Y', 'Z'],
                "qotp_dec": ['X', 'Y', 'Z'],
                "display": ['DISP'],
                "stream": ['SEND']
            }

            for f in reqs:
                availability= True
                for g in reqs[f]:
                    if not(hasattr(self,g)) or (backend_mapping[g] is None): availability = False
                if availability:
                    print(f"""Undersqore: {f} is available""")
                else:
                    print(f"""Undersqore: {f} is unavailable""")
                    setattr(self, f, self.raiseException)

        check()

    def raiseException(*args, **kwargs):
        raise NameError(f"""Undersqore function is unavailable because the backend mapping didn't provide the necessary bindings""")

from functools import partial

import prep, gate, test, pres

class qpzlib(prep.Mixin, gate.Mixin, test.Mixin, pres.Mixin):
    def __init__(self, backend_mapping, node):

        self.X = backend_mapping["X"]
        self.Y = backend_mapping["Y"]
        self.Z = backend_mapping["Z"]
        self.H = backend_mapping["H"]
        self.CNOT = backend_mapping["CNOT"]

        self.K = backend_mapping["K"]
        self.T = backend_mapping["T"]
        self.Tinv = backend_mapping["Tinv"]

        self.PREP = partial (backend_mapping["PREP"], node=node)
        self.MEAS = backend_mapping["MEAS"]
        self.DISP = backend_mapping["DISP"]
        self.QID = backend_mapping["QID"]
        
        self.EPR = backend_mapping["EPR"]
        self.SEND = partial (backend_mapping["SEND"], node=node)
        self.RECV = partial (backend_mapping["RECV"], node=node)
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


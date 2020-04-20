from functools import partial

from atomics.prep import Prep
from atomics.pres import Pres
from atomics.gate import Gate
from atomics.util import Util
from atomics.test import Test

class qpzlib:
    def __init__(self, backend_mapping, host):
        self.X = partial (backend_mapping["X"], host=host)
        self.Y = partial (backend_mapping["Y"], host=host)
        self.Z = partial (backend_mapping["Z"], host=host)
        self.H = partial (backend_mapping["H"], host=host)
        self.CNOT = partial (backend_mapping["CNOT"], host=host)

        self.K = partial (backend_mapping["K"], host=host)
        self.T = partial (backend_mapping["T"], host=host)
        self.Tinv = partial (backend_mapping["Tinv"], host=host)

        self.PREP = partial (backend_mapping["PREP"], host=host)
        self.MEAS = partial (backend_mapping["MEAS"], host=host)
        self.DISP = partial (backend_mapping["DISP"], host=host)
        self.QID = partial (backend_mapping["QID"], host=host)

        self.EPR = partial (backend_mapping["EPR"], host=host)
        self.SEND = partial (backend_mapping["SEND"], host=host)
        self.RECV = partial (backend_mapping["RECV"], host=host)
        self.TELE = partial (backend_mapping["TELE"], host=host)

        mapp = self 
                        
        self.gate = Gate(mapp)
        self.prep = Prep(mapp)
        self.pres = Pres(mapp)
        self.util = Util(mapp)
        self.test = Test(mapp)
        
        # def check():
        #     reqs = {
        #         "qotp": ['X', 'Y', 'Z'],
        #     }

        #     for f in reqs:
        #         availability= True
        #         for g in reqs[f]:
        #             if not(hasattr(self,g)) or (backend_mapping[g] is None): availability = False
        #         if availability:
        #             print(f"""Quantum Protocol Zoo Lib: {f} is available""")
        #         else:
        #             print(f"""Quantum Protocol Zoo Lib: {f} is unavailable""")
        #             setattr(self, f, self.raiseException)

        # check()

    def raiseException(*args, **kwargs):
        raise NameError(f"""Quantum Protocol Zoo Lib function is unavailable because the backend does not provide a necessary functionality""")




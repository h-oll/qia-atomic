from classes import Qubit, Backend

from components.host import Host as QNSHost
from objects.qubit import Qubit as QNSQubit

class QuNetSimBackend(Backend):
    def __init__(self):
        super().__init__()

    def X(self, q): q.state.X()
    def Y(self, q): q.state.Y()
    def Z(self, q): q.state.Z()
    def H(self, q): q.state.H()
    def S(self, q): None
    def T(self, q): q.state.T()
    def CNOT(self, q, r): q.state.cnot(r)
    def PREP(self, host): return self.Qubit(host)
    def SEND(self, q, sourcehost, targethost):
        sourcehost.send_qubit(q, targethost.id)
    def TELE(self, q, host): None
    def MEAS(self, q): None
    def DISP(self, q): print(q.__str__())
    def EPR(self): None

    class Qubit(Qubit):
        def __init__(self, host):
            super().__init__(QNSQubit(host), host)
            self.host = self.state.host
            
    class Host(QNSHost):
        def __init__(self, id):
            super().__init__(id)
            self.id = id

        def __str__(self):
            return self.id



from classes import Qubit, Backend

class PauliBackend(Backend):
    def __init__(self):
        super().__init__()
    
    def X(self, q):
        if q.state == "I": new_state = "X" 
        if q.state == "X": new_state = "I" 
        if q.state == "Y": new_state = "Z" 
        if q.state == "Z": new_state = "Y" 
        q.state = new_state

    def Y(self, q):
        if q.state == "I": new_state = "Y"
        if q.state == "X": new_state = "Z"
        if q.state == "Y": new_state = "I"
        if q.state == "Z": new_state = "X"
        q.state = new_state

    def Z(self, q):
        if q.state == "I": new_state = "Z"
        if q.state == "X": new_state = "Y"
        if q.state == "Y": new_state = "X"
        if q.state == "Z": new_state = "I"
        q.state = new_state
        
    def H(self, q):
        if q.state == "I": new_state = "I"
        if q.state == "X": new_state = "Z"
        if q.state == "Y": new_state = "Y"
        if q.state == "Z": new_state = "X"

    def S(self, q): None
    def T(self, q): None
    def CNOT(self, q,r): None
    def PREP(self, host): return self.Qubit(host)
    def SEND(self, q, sourcehost, targethost): q.host = targethost
    def TELE(self, q): None
    def MEAS(self, q): None
    def DISP(self, q): print(q.__str__())
    def EPR(self): None

    class Qubit(Qubit):
        def __init__(self, host):
            super().__init__("I", host)
            self.host = host

    class Host:
        def __init__(self, host_id):
            self.id = host_id

        def __str__(self):
            return self.id

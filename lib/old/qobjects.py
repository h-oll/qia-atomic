from abc import ABC, abstractmethod
import uuid

class Backend(ABC):
    def __init__(self):
        super().__init__()
    @abstractmethod
    def X(self,q): pass

    @abstractmethod
    def Y(self,q): pass

    @abstractmethod
    def Z(self,q): pass

    @abstractmethod
    def H(self,q): pass

    @abstractmethod
    def S(self,q): pass

    @abstractmethod
    def T(self,q): pass

    @abstractmethod
    def CNOT(self,q,r): pass

    @abstractmethod
    def PREP(self, host): pass

    @abstractmethod
    def SEND(self,q, targethost): pass

    @abstractmethod
    def TELE(self,q,host): pass

    @abstractmethod
    def MEAS(self,q): pass

    @abstractmethod
    def DISP(self,q): pass

    @abstractmethod
    def EPR(self): pass

class Qubit:
    def __init__(self, state, host=None):
        self.state = state
        self.uuid = uuid.uuid4()
        self.host = host
    
    def __str__(self):
        return f"""Host: {self.host} | UUID: {self.uuid} | State: {self.state.__str__()}"""

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
    def PREP(self, host): return Qubit("I", host)
    def SEND(self, q, targethost):
        q.host = targethost
        return q
    def TELE(self, q, host): None
    def MEAS(self, q): None
    def DISP(self, q): print(q.__str__())
    def EPR(self): None

    class Qubit(Qubit):
        def __init__():
            super().__init__()
    
    class Host:
        def __init__(self, id):
            self.id = id

        def __str__(self):
            return self.id


class QuNetSimBackend(Backend):
    def __init__(self):
        super().__init__()

    def X(self, q): q.X()
    def Y(self, q): q.Y()
    def Z(self, q): q.Z()
    def H(self, q): q.H()
    def S(self, q): None
    def T(self, q): None
    def CNOT(self, q, r): q.CNOT(r)
    def PREP(self, host): return Qubit(host, host)
    def SEND(self, q, targethost): None
    def TELE(self, q, host): None
    def MEAS(self, q): None
    def DISP(self, q): print(q.__str__())
    def EPR(self): None

    class Qubit(Qubit):
        def __init__():
            super().__init__()
    
    class Host:
        def __init__(self, id):
            self.id = id

        def __str__(self):
            return self.id



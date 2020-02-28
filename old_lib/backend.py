from abc import ABC, abstractmethod

class Backend(ABC):
    def __init__(self):
        super().__init__()
    @abstractmethod
    def X(self): pass

    @abstractmethod
    def Y(self): pass

    @abstractmethod
    def Z(self): pass

    @abstractmethod
    def H(self): pass

    @abstractmethod
    def S(self): pass

    @abstractmethod
    def T(self): pass

    @abstractmethod
    def CNOT(self): pass

    @abstractmethod
    def PREP(self): pass

    @abstractmethod
    def SEND(self): pass

    @abstractmethod
    def TELE(self): pass

    @abstractmethod
    def MEAS(self): pass

    @abstractmethod
    def DISP(self): pass

    @abstractmethod
    def EPR(self): pass

class Qubit:
    def __init__(self, state, host=None):
        self.state = state
        self.uuid = uuid.uuidv4()
        self.host = host
        super.__init__()    
    
    def __str__(self):
        return f"""Host: {self.host} | UUID: {self.uuid} | State: {self.state.__str__()}"""

class PauliBackend(Backend):
    def __init__(self):
        super.__init__()
    
    def X(q):
        if q.state == "I": new_state = "X" 
        if q.state == "X": new_state = "I" 
        if q.state == "Y": new_state = "Z" 
        if q.state == "Z": new_state = "Y" 
        q.state = new_state

    def Y(q):
        if q.state == "I": new_state = "Y"
        if q.state == "X": new_state = "Z"
        if q.state == "Y": new_state = "I"
        if q.state == "Z": new_state = "X"
        q.state = new_state

    def Z(q):
        if q.state == "I": new_state = "Z"
        if q.state == "X": new_state = "Y"
        if q.state == "Y": new_state = "X"
        if q.state == "Z": new_state = "I"
        q.state = new_state
        
    def H(q):
        if q.state == "I": new_state = "I"
        if q.state == "X": new_state = "Z"
        if q.state == "Y": new_state = "Y"
        if q.state == "Z": new_state = "X"

    def S(q): None
    def T(q): None
    def CNOT(q,r): None
    def PREP(): Qubit("I")
    def SEND(q, targethost): q.host = targethost
    def TELE(q): None
    def MEAS(q): None
    def EPR(): None

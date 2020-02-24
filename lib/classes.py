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
        
    def __str__(self):
        return f"""Host: {self.host} | UUID: {self.uuid} | State: {self.state.__str__()}"""

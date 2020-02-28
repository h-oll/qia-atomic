import random
import inspect


class QRoutines:    
    def __init__(self, backend):
        self.X = backend.X
        self.Y = backend.Y
        self.Z = backend.Z
        self.H = backend.H
        self.T = backend.T
        self.CNOT = backend.CNOT
        self.SEND = backend.SEND
        self.TELE = backend.TELE
        self.MEAS = backend.MEAS
        self.DISP = backend.DISP
        self.EPR = backend.EPR

        reqs = {
            "qotp_enc": ['X', 'Y', 'Z'],
            "qotp_dec": ['X', 'Y', 'Z'],
            "display": ['DISP'],
            "stream": ['SEND']
        }

        def check():
            for f in reqs:
                availability = True
                for g in reqs[f]:
                    if not(hasattr(self, g)) or not(inspect.isfunction(getattr(self, g))): availability = False
                if availability: print("QRoutines:", f, "is available")
                else: 
                    print("QRoutines:", f, "is unavailable")
                    setattr(self, f, None)
        # check()
        
    def qotp_enc(self, block):
        '''
        Quantum One Time Pad Encrypt
        Qubit Iterable -> (Qubit, Integer) Iterable
        Applies Quantum One Time Pad to an iterable of qubits. Returns the encryption key as an iterable of integers in 0..3 (0=I, 1=X, 2=Z, 3=Y).
        Needs X,Y,Z.
        '''
        for q in block:
            k = random.randint(0,3)
            if k == 0: pass
            if k == 1: self.X(q)
            if k == 2: self.Z(q)
            if k == 3: self.Y(q)
            yield q, k

    def qotp_dec(self, block, key):
        '''
        Quantum One Time Pad Decrypt
        Qubit Iterable -> Integer Iterable -> Qubit Iterable
        Decrypts Quantum One Time Pad with an iterable of qubits and a key. Returns an iterable of qubits.
        '''
        for q, k in zip(block, key):
            if k == 0: pass
            if k == 1: self.X(q)
            if k == 2: self.Z(q)
            if k == 3: self.Y(q)
            yield q
            
    def display(self, block):
        '''
        Qubit Iterable -> ()
        Displays the state of qubits.
        '''
        for q in block:
            self.DISP(q)

    def stream(self, block, sourcehost, targethost):
        '''
        Qubit Iterable -> Host -> ()
        Streams qubits to host.
        '''
        for q in block:
            self.SEND(q, sourcehost, targethost)
    

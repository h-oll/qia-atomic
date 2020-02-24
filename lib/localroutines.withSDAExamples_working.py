import cmath
import uuid
import random
import time
import inspect
from math import sqrt

from components.host import Host
from components.network import Network
from objects.qubit import Qubit
from components.logger import Logger

class Backend:
    def __init__(self, X, Y, Z, H, T, CNOT, SEND, TELE, MEAS, DISP, EPR):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.H = H
        self.T = T
        self.CNOT = CNOT
        self.SEND = SEND
        self.TELE = TELE
        self.MEAS = MEAS
        self.DISP = DISP
        self.EPR = EPR

class TensorQubit:
    def __init__(self, localhost):
        self.state = (complex(1.0,0.0),complex(0.0,0.0))
        self.uuid = uuid.uuid4()
        self.host = localhost
    def X(self):
        new_state = (self.state[1], self.state[0])
        self.state = new_state
    def Y(self):
        new_state = (complex(0, 1) * self.state[1], - complex(0, 1) * self.state[0])
        self.state = new_state
    def Z(self):
        new_state = (self.state[0], -self.state[1])
        self.state = new_state
    def H(self):
        new_state = ((self.state[0] + self.state[1]) / sqrt(2), (self.state[0] - self.state[1]) / sqrt(2))
    def send(self, targethost):
        self.host = targethost
    def __str__(self):
        return f"""Qubit: {self.uuid}; Host: {self.host}; State: {self.state[0]}|0> + {self.state[1]}|1>"""

class PauliQubit:
    def __init__(self, localhost):
        self.state = "I"
        self.uuid = uuid.uuid4()
        self.host = localhost
    def X(self):
        if self.state == "I": new_state = "X" 
        if self.state == "X": new_state = "I" 
        if self.state == "Y": new_state = "Z" 
        if self.state == "Z": new_state = "Y" 
        self.state = new_state
    def Y(self):
        if self.state == "I": new_state = "Y"
        if self.state == "X": new_state = "Z"
        if self.state == "Y": new_state = "I"
        if self.state == "Z": new_state = "X"
        self.state = new_state
    def Z(self):
        if self.state == "I": new_state = "Z"
        if self.state == "X": new_state = "Y"
        if self.state == "Y": new_state = "X"
        if self.state == "Z": new_state = "I"
        self.state = new_state
    def H(self):
        if self.state == "I": new_state = "I"
        if self.state == "X": new_state = "Z"
        if self.state == "Y": new_state = "Y"
        if self.state == "Z": new_state = "X"
    def send(self, targethost):
        self.host = targethost
    def __str__(self):
        return f"""Qubit: {self.uuid}; Host: {self.host}; State: {self.state}"""
    
# class Host:
#     def __init__(self, id):
#         self.id = id
#     def __str__(self):
#         return self.id
        
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
                    setattr(self, g, None)
        check()
                    
        
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

    def stream(self, block, targethost):
        '''
        Qubit Iterable -> Host -> ()
        Streams qubits to host.
        '''
        for q in block:
            self.SEND(q, targethost)

def ex_qotp(host):
    clear_block = [Qubit(host) for i in range(10)]
    flip_block = [random.randint(0,1) for i in range(10)]
    for q,k in zip(clear_block, flip_block):
        if k == 1: q.X()

    print('Clear block')
    qr.display(clear_block)
    
    print('## Applying QOTP')
    enc_block, key = zip(*qr.qotp_enc(clear_block))

    #print('Encrypted block') 
    #qr.display(enc_block)
    #print('Used key')
    #print(key)

    print('## Decripting')
    dec_block = list(qr.qotp_dec(enc_block, key))
    print('Decrypted block') 
    qr.display(dec_block)
        
def ex_stream(sourcehost, targethost):
    block = [Qubit(sourcehost) for i in range(10)]
    qr.stream(block, targethost)
    print('Send done, checking qubit location')
    qr.display(block)
    
def main():
    # Initialize a network
    network = Network.get_instance()

    # Define the host IDs in the network
    nodes = ['Alice', 'Bob', 'Eve']

    network.delay = 0.0

    # Start the network with the defined hosts
    network.start(nodes)

    # Initialize the host Alice
    host_alice = Host('Alice')

    # Add a one-way connection (classical and quantum) to Bob
    host_alice.add_connection('Bob')
    host_alice.delay = 0

    # Start listening
    host_alice.start()

    host_bob = Host('Bob')
    # Bob adds his own one-way connection to Alice and Eve
    host_bob.add_connection('Alice')
    host_bob.add_connection('Eve')
    host_bob.delay = 0
    host_bob.start()

    host_eve = Host('Eve')
    host_eve.add_connection('Bob')
    host_eve.delay = 0
    host_eve.start()

    # Add the hosts to the network
    # The network is: Alice <--> Bob <--> Eve
    network.add_host(host_alice)
    network.add_host(host_bob)
    network.add_host(host_eve)

    #host_alice = Host('Alice')
    #host_bob = Host('Bob')
    
    ex_qotp(host_alice)
    #ex_stream(host_alice, host_bob)
    
if __name__ == '__main__':
    # Defining Backend

    #Qubit = PauliQubit
    
    sq = Backend(
        lambda q: q.X(), #x
        lambda q: q.Y(), #Y
        lambda q: q.Z(), #Z
        lambda q: q.H(), #H
        None,  #T
        None,  #CNOT
        lambda q, targethost: q.send_to(targethost.host_id),  #SEND
        None,
        None,
        lambda q: print(q.measure(True)),
        None)

    simple = Backend(
        lambda q: q.X(), #x
        lambda q: q.Y(), #Y
        lambda q: q.Z(), #Z
        lambda q: q.H(), #H
        None,  #T
        None,  #CNOT
        lambda q, targethost: q.send(targethost),  #SEND
        None,
        None,
        lambda q: print(q),
        None)
    
    # Instantiating QRoutines library
    qr = QRoutines(sq)
    #qr = QRoutines(simple)
    
    main()

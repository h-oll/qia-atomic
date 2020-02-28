import random

from simbackends.pauli import PauliBackend
from simbackends.qunetsim import QuNetSimBackend
from qroutines import QRoutines

from components.network import Network


def ex_qotp(backend, host):
    clear_block = [backend.PREP(host) for i in range(10)]
    flip_block = [random.randint(0,1) for i in range(10)]

    for q,k in zip(clear_block, flip_block):
        if k == 1: backend.X(q)

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
        
def ex_stream(backend, sourcehost, targethost):
    print(sourcehost)
    print(backend.PREP(sourcehost))
    

    block = [backend.PREP(sourcehost) for i in range(10)]
    print('Preparation done, checking qubit host')
    qr.display(block)
    qr.stream(block, sourcehost, targethost)
    print('Send done, checking qubit host')
    qr.display(block)

def qunetsim_setup(backend):
    #############################################################
    # For QuNetSim 
    #############################################################
    # Initialize a network
    network = Network.get_instance()

    # # Define the host IDs in the network
    nodes = ['Alice', 'Bob', 'Eve']

    network.delay = 0.0

    # Start the network with the defined hosts
    network.start(nodes)

    # Initialize the host Alice
    host_alice = backend.Host('Alice')

    # Add a one-way connection (classical and quantum) to Bob
    host_alice.add_connection('Bob')
    host_alice.delay = 0

    # Start listening
    host_alice.start()

    host_bob = backend.Host('Bob')
    # Bob adds his own one-way connection to Alice and Eve
    host_bob.add_connection('Alice')
    host_bob.add_connection('Eve')
    host_bob.delay = 0
    host_bob.start()

    host_eve = backend.Host('Eve')
    host_eve.add_connection('Bob')
    host_eve.delay = 0
    host_eve.start()

    # Add the hosts to the network
    # The network is: Alice <--> Bob <--> Eve
    network.add_host(host_alice)
    network.add_host(host_bob)
    network.add_host(host_eve)
    
    return host_alice, host_bob, host_eve, network
    
def pauli_setup(backend):
    #############################################################
    # For PauliBackend
    #############################################################
    host_alice = backend.Host('Alice')
    host_bob = backend.Host('Bob')

    return host_alice, host_bob

if __name__ == '__main__':
    #############################################################
    # Defining Backend
    #############################################################    
    be = QuNetSimBackend(); host_alice, host_bob, host_eve, network = qunetsim_setup(be)
    #be = PauliBackend(); host_alice, host_bob = pauli_setup(be)
    
    #############################################################
    # Instantiating QRoutines library    
    #############################################################
    qr = QRoutines(be)
    
    #ex_qotp(be, host_alice)
    ex_stream(be, host_alice, host_bob)

    # Si on met un send_qubit avec un wait_ack true : il bloque jusqua l'envoi. 
    # Si on met pas de wait_ack, il passe a l'instruction prochaine

    # Si on met un recv avec un wait, donne un timout. Sinon il regarde s'il y a un qubit dans le buffer et retourne None si pas. 
    # Si on passe un id, il cherche l'id qui correspond => permet de reordonner les packets a partir du buffer.

# def qunetsim_send_recv(backend, source, target):
#     def protocol_1(host, receiver):
#         # Here we write the protocol code for a host.
#         for i in range(5):
#             q = Qubit(host)
#             # Apply Hadamard gate to the qubit
#             q.H()
#             print('Sending qubit %d.' % (i+1))
#             # Send qubit and wait for an acknowledgement
#             backend.SEND(receiver, q, await_ack=True)
#             print('Qubit %d was received by %s.' % (i+1, receiver))


#     def protocol_2(host, sender):
#         # Here we write the protocol code for another host.
#         for _ in range(5):
#             # Wait for a qubit from Alice for 10 seconds.
#             q = backend.RECV(sender, target, wait=10)
#             # Measure the qubit and print the result.
#             print('%s received a qubit in the %d state.' % (host.host_id, q.measure()))

#    source.run_protocol(protocol_1, (target.id,))
#    target.run_protocol(protocol_2, (source.id,))


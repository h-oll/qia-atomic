import numpy as np
import netsquid as ns
from netsquid.nodes.node import Node
from netsquid.protocols import Protocol,LocalProtocol,NodeProtocol
from netsquid.qubits import create_qubits
from netsquid.qubits.operators import X,H,Z
from netsquid.nodes.connections import DirectConnection
from netsquid.components  import ClassicalFibre,QuantumFibre,QuantumMemory
from netsquid.components.models import  FibreDelayModel
from netsquid.pydynaa import Entity,EventHandler,EventType
from netsquid.components.qchannel import QuantumChannel

from random import randint

from netsquid.qubits.qformalism import *
from netsquid.components.qprocessor import *
from netsquid.components.instructions import *
from netsquid.components.qprogram import *
from netsquid.components.models.qerrormodels import *


#################
# Constants

noise_model = None
fibre_len=10**-9
loss_init=0
loss_len=0


#################
# nodes

alice_node = Node("alice_node", port_names=["to_bob_q","to_bob_c"])
bob_node = Node("bob_node"  , port_names=["from_alice_q","from_alice_c"])


#################
# processors

class send_capable_processor(QuantumProcessor):
    '''processor class created by chinte / adds send from mem => to send from a q. processor sender port name is determining the receiver. ## processor class created by chinte / adds send from mem => to send from a q. processor sender port name is determining the receiver.'''
    def send(self, inx, senderNode, senderPortName):
        payload=self.pop(inx)
        senderNode.ports[senderPortName].tx_output(payload)


alice_processor = send_capable_processor(
    "alice_processor",
    num_positions=100,
    mem_noise_models=None,
    phys_instructions=[
        PhysicalInstruction(INSTR_INIT, duration=1, parallel=True),
        PhysicalInstruction(INSTR_X, duration=1, q_noise_model=noise_model),
        PhysicalInstruction(INSTR_Z, duration=1, q_noise_model=noise_model),
        PhysicalInstruction(INSTR_H, duration=1, q_noise_model=noise_model),
        PhysicalInstruction(INSTR_CNOT,duration=1,q_noise_model=noise_model),
        PhysicalInstruction(INSTR_MEASURE, duration=1, parallel=True),
        PhysicalInstruction(INSTR_MEASURE_X, duration=1, parallel=True)])


bob_processor = send_capable_processor(
    "bob_processor",
    num_positions=100,
    mem_noise_models=None,
    phys_instructions=[
        PhysicalInstruction(INSTR_INIT, duration=1, parallel=True),
        PhysicalInstruction(INSTR_X, duration=1, q_noise_model=noise_model),
        PhysicalInstruction(INSTR_Z, duration=1, q_noise_model=noise_model),
        PhysicalInstruction(INSTR_H, duration=1, q_noise_model=noise_model),
        PhysicalInstruction(INSTR_CNOT,duration=1,q_noise_model=noise_model),
        PhysicalInstruction(INSTR_MEASURE, duration=1, parallel=True),
        PhysicalInstruction(INSTR_MEASURE_X, duration=1, parallel=True)])


#################
# fibres

alice_to_bob_q_fiber = QuantumFibre(
    "alice_to_bob_q_fiber",
    length = fibre_len,
    quantum_loss_model = None,
    p_loss_init = loss_init,
    p_loss_length = loss_len)

alice_to_bob_c_fiber = ClassicalFibre(
    "alice_to_bob_c_fiber",
    length = fibre_len)

# alice_to_bob_c_connection = DirectConnection(
#     "alice_to_bob_c_connection",
#     ClassicalFibre("alice_to_bob_c_fiber", length = fibre_len))

# bob_to_alice_c_connection = DirectConnection(
#     "bob_to_alice_c_connection",
#     ClassicalFibre("bob_to_alice_c_fiber", length = fibre_len))


#################
# connect nodes with fibers

alice_node.connect_to(
    bob_node,
    alice_to_bob_q_fiber,
    local_port_name = "to_bob_q",
    remote_port_name = "from_alice_q")

alice_node.connect_to(
    bob_node,
    alice_to_bob_c_fiber,
    local_port_name = "to_bob_c",
    remote_port_name = "from_alice_c")

# alice_node.connect_to(
#     bob_node,
#     alice_to_bob_c_connection,
#     local_port_name = "to_bob_c",
#     remote_port_name = "from_alice_c"
#     )


#################
# programs

class qOTP(QuantumProgram): # currently not used
    def __init__(self, pauli):
        self.num_bits = 1
        self.pauli = pauli
        super().__init__()

    def program(self): 
        if self.pauli == 0:
            pass
        elif self.pauli == 1:
            self.apply(INSTR_X, 0)
        elif self.pauli == 2:
            self.apply(INSTR_Z, 0)
        elif self.pauli == 3:
            self.apply(INSTR_X, 0)
            self.apply(INSTR_Z, 0)
        else:
            raise ValueError('pauli argument must be 0, 1, 2, 3')

        yield self.run(parallel = False)


#################
# protocols

class alice_protocol(NodeProtocol):
    def __init__(self, node, processor, to_q_port_name, to_c_port_name):
        super().__init__(node = node)
        # self.node = node # necessary ? is in parent's class
        self.processor = processor
        self.to_q_port_name = to_q_port_name
        self.to_c_port_name = to_c_port_name

    def send_qubit(self):
        self.processor.send(0, self.node, self.to_q_port_name)
                
    def run(self):
        print('Launching alice_protocol')
        
        class prepare_program(QuantumProgram):
            def __init__(self, init_state, pauli):
                super().__init__()
                self.num_bits = 1
                self.pauli = pauli
                self.init_state = init_state
            def program(self):
                print("Prepare_program", "run")
                self.apply(INSTR_INIT, 0)

                if self.init_state == 0:
                    pass
                elif self.init_state == 1:
                    self.apply(INSTR_X, 0)
                elif self.init_state == 2:
                    self.apply(INSTR_H, 0)
                elif self.init_state == 3:
                    self.apply(INSTR_H, 0)
                    self.apply(INSTR_Z, 0)
                
                if self.pauli == 0:
                    pass
                elif self.pauli == 1:
                    self.apply(INSTR_X, 0)
                elif self.pauli == 2:
                    self.apply(INSTR_Z, 0)
                elif self.pauli == 3:
                    self.apply(INSTR_X, 0)
                    self.apply(INSTR_Z, 0)
                else:
                    raise ValueError('pauli argument must be 0, 1, 2, 3')

                yield self.run(parallel = False)

        plain_text_state = randint(0,3)
        key = randint(0,3)

        print("Alice", "plain", plain_text_state, "key", key)
        
        pp = prepare_program(plain_text_state, key)

        print("Alice", "exec pp")
        
        self.processor.execute_program(pp)

        print("Alice", "done pp")
        
        #yield self.await_program(self.processor)

        print("Alice", "exec send qubit")

        self.processor.set_program_done_callback(self.send_qubit, once = True)    
        #self.processor.send(0, node, self.to_q_port_name)

        print("Alice", "exec send classical")
        
        self.node.ports[self.to_c_port_name].tx_output({"plain_text_state": plain_text_state, "key": key})

        print("Alice", "done")
        
        # self.processor.set_program_done_callback(...
        
class bob_protocol(NodeProtocol):
    def __init__(self, node, processor, from_q_port_name, from_c_port_name):
        super().__init__(node = node)
        self.processor = processor
        self.from_q_port_name = from_q_port_name
        self.from_c_port_name = from_c_port_name

    def run(self):
        print('Launching bob_protocol')
        
        class receive_program(QuantumProgram):
            def __init__(self, compare_state, pauli):
                super().__init__()
                self.num_bits = 1
                self.compare_state = compare_state
                self.pauli = pauli
                
            def program(self):
                if self.pauli == 0:
                    pass
                elif self.pauli == 1:
                    self.apply(INSTR_X, 0)
                elif self.pauli == 2:
                    self.apply(INSTR_Z, 0)
                elif self.pauli == 3:
                    self.apply(INSTR_X, 0)
                    self.apply(INSTR_Z, 0)
                else:
                    raise ValueError('pauli argument must be 0, 1, 2, 3')

                if self.compare_state == 0:
                    pass
                elif self.compare_state == 1:
                    self.apply(INSTR_X, 0)
                elif self.compare_state == 2:
                    self.apply(INSTR_H, 0)
                elif self.compare_state == 3:
                    self.apply(INSTR_Z, 0)
                    self.apply(INSTR_H, 0)

                self.apply(INSTR_MEASURE, qubit_indices = 0, output_key = "outcome", physical = True)
                
                yield self.run(parallel = False)

        print("Bob", "wait c input")

        yield self.await_port_input(self.node.ports[self.from_c_port_name])

        print("Bob", "c input received")
        
        message = self.node.ports[self.from_c_port_name].rx_input().items[0]

        print("Bob", "c input read", message)
        
        print("Bob", "wait q input")
                
        yield self.await_port_input(self.node.ports[self.from_q_port_name])

        received_qubits = self.node.ports[self.from_q_port_name].rx_input().items[0]

        print("Bob", "qubit received")
        
        self.processor.put(received_qubits, positions = 0)

        print("Bob", "storing in memory")
        
        rp = receive_program(message["plain_text_state"], message["key"])

        self.processor.execute_program(rp)

        yield self.await_program(self.processor)

        print(rp.output)

        
#################
# orchestration

ns.sim_reset() # reset simulation


ap = alice_protocol(alice_node, alice_processor, "to_bob_q", "to_bob_c")
bp = bob_protocol(bob_node, bob_processor, "from_alice_q", "from_alice_c")

bp.start()
ap.start()
ns.logger.setLevel(1)
ns.sim_run()


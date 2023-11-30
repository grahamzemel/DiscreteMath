from cryptography.fernet import Fernet
# Classical Encryption/Decryption
def classical_encrypt_decrypt():
    # Generate a key
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    text = b"Hello, Quantum World!"
    
    # Encrypt the text
    encrypted_text = cipher_suite.encrypt(text)
    print(f"Encrypted: {encrypted_text}")

    # Decrypt the text
    decrypted_text = cipher_suite.decrypt(encrypted_text)
    print(f"Decrypted: {decrypted_text}")

# Quantum Computing (Simulation)
from qiskit import QuantumCircuit, transpile, Aer, assemble
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from matplotlib import pyplot as plt

def quantum_teleportation():
    circuit = QuantumCircuit(3, 2) # Create a quantum circuit with 3 qubits and 2 classical bits

    # Prepare the initial state as a superposition
    circuit.h(0)  

    # Store the initial state of qubit 0
    circuit.measure(0, 0)  # Measure qubit 0 and store in classical bit 0

    # Reset qubit 0 to reuse it in the teleportation protocol
    circuit.reset(0)

    # Teleportation protocol
    circuit.h(1) # Superposition on qubit 1
    circuit.cx(1, 2) # Entangle qubit 1 and 2
    circuit.cx(0, 1) # Entangle qubit 0 and 1
    circuit.h(0) # Superposition on qubit 0
    circuit.measure([0, 1], [0, 0])  # Measure qubit 0 and 1 and store in classical bits 0 and 1
    circuit.cx(1, 2) # Entangle qubit 1 and 2
    circuit.cz(0, 2) # Apply a Z-gate to qubit 2 if the value of qubit 0 is 1

    # Measure the final state of qubit 2
    circuit.measure(2, 1)  # Measure qubit 2 and store in classical bit 1

    # Simulate the circuit
    simulator = Aer.get_backend('aer_simulator')
    job = simulator.run(transpile(circuit, simulator), shots=1024) # shots = number of times to run the circuit
    result = job.result()

    # Plot the results
    counts = result.get_counts(circuit)
    plot_histogram(counts)
    plt.xlabel('Qu0 initState = bit 0, Qu2 finState = bit 1')
    plt.title('Quantum Teleportation: State Transfer from Qubit 0 to Qubit 2')
    plt.show()

    # In a perfect superposition state, the measurement 
    # outcomes should be evenly distributed between 0 and 1. 
    # However, due to the probabilistic nature of quantum mechanics 
    # and potential small imperfections in the quantum simulation 
    # (or quantum noise), the results might not be exactly 50-50, 
    # but they should be close to an even split.

import cirq
import random

def quantum_eavesdrop():
    # Initialize qubits
    alice_qubit, bob_qubit = cirq.LineQubit.range(2) # Create 2 qubits

    # Create a circuit
    circuit = cirq.Circuit()

    # Alice prepares a qubit in a random state
    if random.choice([True, False]):
        circuit.append(cirq.X(alice_qubit))  # Apply X gate (flip state) with 50% probability
    circuit.append(cirq.H(alice_qubit))  # Apply Hadamard gate to create superposition

    eavesdrop = False
    # Eavesdropper (Eve) tries to intercept
    if random.choice([True, False]):
        circuit.append(cirq.measure(alice_qubit, key='eve_intercept'))  # Eve measures the qubit
        eavesdrop = True

    # Entangle Alice's and Bob's qubits
    circuit.append(cirq.CNOT(alice_qubit, bob_qubit)) # CNOT will flip the target qubit (Bob's) if the control qubit (Alice's) is in the |1> state

    # Bob measures the qubit
    circuit.append(cirq.H(bob_qubit)) # Apply Hadamard gate to create superposition
    circuit.append(cirq.measure(bob_qubit, key='bob_measure')) # Bob measures the qubit
    # Simulate the circuit
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)

    print("Circuit:")
    print(circuit)
    print("Measurement results:")
    print(result)
    # print tampered with + explanation
    print("Eavesdropper intercepted the message: ", eavesdrop)

def qkd_eavesdropper_detection_extended(num_qubits=10):
    # Step 1: Key and basis generation by Alice
    alice_bits = [random.choice([0, 1]) for _ in range(num_qubits)]
    alice_bases = [random.choice(['s', 'h']) for _ in range(num_qubits)] # s = standard, h = hadamard

    # Step 2: Encoding qubits
    qubits = [cirq.LineQubit(i) for i in range(num_qubits)]
    circuit = cirq.Circuit()
    for i in range(num_qubits):
        if alice_bases[i] == 'hadamard':
            circuit.append(cirq.H(qubits[i]))
        if alice_bits[i] == 1:
            circuit.append(cirq.X(qubits[i]))

    # Step 3: Bob chooses measurement bases
    bob_bases = [random.choice(['s', 'h']) for _ in range(num_qubits)]
    for i in range(num_qubits):
        if bob_bases[i] == 'hadamard':
            circuit.append(cirq.H(qubits[i]))
    circuit.append(cirq.measure(*qubits, key='measurement'))

    # Step 4: Simulate the circuit
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)
    measurements = result.measurements['measurement'][0]

    # Step 5: Basis reconciliation
    shared_key = []
    for i in range(num_qubits):
        if alice_bases[i] == bob_bases[i]:
            shared_key.append(measurements[i])

    print("Alice's bits:", alice_bits) #[1 0 0 0 1 0 1 0 1 1]
    print("Alice's bases:", alice_bases) #['h', 's', 'h', 's', 'h', 'h', 's', 'h', 'h', 'h']
    print("Bob's bases:", bob_bases)     #['s', 'h', 'h', 's', 's', 's', 's', 'h', 's', 's']
    print("Bob's measurements:", measurements) #[1 1 0 0 0 1 1 0 0 1]

    print("Shared Key:", shared_key) # Shared key will be the bits that at a specific index, have the same base for both ppl, so indexes 2, 3, 6, 7



print()
print("Basic Quantum Eavesdropping")
print("---------------------------")
quantum_eavesdrop()
print()
print("Quantum Eavesdropping with Multiple Qubits")
print("------------------------------------------")
qkd_eavesdropper_detection_extended()
print()
# Run the experiments
# classical_encrypt_decrypt()
# quantum_experiment()
# quantum_teleportation()
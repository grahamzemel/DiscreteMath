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
    # Eavesdropper (Eve) tries to intercept. THE ONLY REASON THIS IS HERE IS TO SHOW THAT THE CIRCUIT IS TAMPERED WITH, NOT TO READ ANY DATA (QBITS CANNOT BE READ ACCURATELY DUE TO FUNDAMENTAL LAWS OF QUANTUM MECHANICS)
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

def qkd_eavesdropper_detection_extended(num_qubits=25):
     # Initialize qubits
    qubits = [cirq.LineQubit(i) for i in range(num_qubits)]

    # Key and basis generation by Alice
    alice_bits = [random.choice([0, 1]) for _ in range(num_qubits)]
    alice_bases = [random.choice(['s', 'h']) for _ in range(num_qubits)]

    # Create a circuit
    circuit = cirq.Circuit()

    # Encoding qubits
    for i in range(num_qubits):
        if alice_bases[i] == 'h':
            circuit.append(cirq.H(qubits[i]))
        if alice_bits[i] == 1:
            circuit.append(cirq.X(qubits[i]))

    # Eve's interception chance of 50% THE ONLY REASON THIS IS HERE IS TO SHOW THAT THE CIRCUIT IS TAMPERED WITH, NOT TO READ ANY DATA (QBITS CANNOT BE READ ACCURATELY DUE TO FUNDAMENTAL LAWS OF QUANTUM MECHANICS)
    eavesdrop = False
    random.seed(random.randint(0, 100))
    prob = random.random()
    if prob < .25:
        # Eve tries to intercept
        for i in range(num_qubits):
            try:
                circuit.append(cirq.measure(qubits[i], key=f'eve_intercept_{i}')) # Eve measures the qubit (out of superposition), if she could place back she would break quantum mechanics
                eavesdrop = True
                # NOTE: TAKES FAR LONGER WITH MORE QUBITS
            except:
                pass

    # Bob chooses measurement bases
    bob_bases = [random.choice(['s', 'h']) for _ in range(num_qubits)]
    for i in range(num_qubits):
        if bob_bases[i] == 'h':
            circuit.append(cirq.H(qubits[i]))

    # Bob's measurement
    circuit.append(cirq.measure(*qubits, key='bob_measure'))

    # Simulate the circuit
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)
    measurements = result.measurements['bob_measure'][0]

    # Basis reconciliation and discrepancy check
    shared_key = []
    discrepancy_count = 0
    # case 1: no eavesdropping, establish baseline QBER level
    # if(not eavesdrop):
    #     for i in range(num_qubits):
    #         if alice_bases[i] == bob_bases[i]:
    #             shared_key.append(measurements[i])
    #             # Check for discrepancies in a subset of the bits
    #             if alice_bits[i] != measurements[i]:
    #                 print(f"Discrepancy detected at index {i} (Alice's bit: {alice_bits[i]}, Bob's bit: {measurements[i]})")
    #                 discrepancy_count += 1
    #     expected_qber = discrepancy_count / num_qubits
    #     print("Expected QBER:", expected_qber)
    expected_qber = 0.01
    actual_qber = 0
    if(eavesdrop):
        discrepancy_count = 0
        for i in range(num_qubits):
            if alice_bases[i] == bob_bases[i]:
                shared_key.append(measurements[i])
                # Check for discrepancies in a subset of the bits
                if alice_bits[i] != measurements[i]:
                    # print(f"Discrepancy detected at index {i} (Alice's bit: {alice_bits[i]}, Bob's bit: {measurements[i]})")
                    discrepancy_count += 1
        actual_qber = discrepancy_count / len(shared_key)
        actual_qber = round(actual_qber, 2)
    
    finalInfo = ""
    finalInfo += "Circuit:\n"
    finalInfo += str(circuit) + "\n"
    finalInfo += "Alice's bits:\n"
    finalInfo += str(alice_bits) + "\n"
    finalInfo += "Alice's bases:\n"
    finalInfo += str(alice_bases) + "\n"
    finalInfo += "Bob's bases:\n"
    finalInfo += str(bob_bases) + "\n"
    finalInfo += "Bob's measurements:\n"
    finalInfo += str(measurements) + "\n"
    if(actual_qber > expected_qber):
        potential = ("Discrepancy detected: ", actual_qber > expected_qber, "(A_QBER:", actual_qber, "> E_QBER:", expected_qber, ")", "DISCARD KEY!")
        finalInfo += str(potential) + "\n"
        # generate new key
        shared_key = qkd_eavesdropper_detection_extended()
    else:
        potential = ("Discrepancy detected: ", actual_qber > expected_qber, "(A_QBER:", actual_qber, "< E_QBER:", expected_qber, ")")
        finalInfo += str(potential) + "\n"
    
    # print(finalInfo)
    return shared_key # Shared key will be the bits that at a specific index, have the same base for both ppl, so indexes 2, 3, 6, 7

def qkd(num_qubits=25):
    # Initialize qubits
    qubits = [cirq.LineQubit(i) for i in range(num_qubits)]

    # Key and basis generation by Alice
    alice_bits = [random.choice([0, 1]) for _ in range(num_qubits)]
    alice_bases = [random.choice(['s', 'h']) for _ in range(num_qubits)]

    # Create a circuit
    circuit = cirq.Circuit()

    # Encoding qubits
    for i in range(num_qubits):
        if alice_bases[i] == 'h':
            circuit.append(cirq.H(qubits[i]))
        if alice_bits[i] == 1:
            circuit.append(cirq.X(qubits[i]))

    # Bob chooses measurement bases
    bob_bases = [random.choice(['s', 'h']) for _ in range(num_qubits)]
    for i in range(num_qubits):
        if bob_bases[i] == 'h':
            circuit.append(cirq.H(qubits[i]))

    # Bob's measurement
    circuit.append(cirq.measure(*qubits, key='bob_measure'))

    # Simulate the circuit
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)
    measurements = result.measurements['bob_measure'][0]

    # Basis reconciliation and discrepancy check
    shared_key = []
    for i in range(num_qubits):
        if alice_bases[i] == bob_bases[i]:
            shared_key.append(measurements[i])
            
    return shared_key 

from Crypto.Cipher import AES
import hashlib
import os

def encrypt_message(shared_key, message):
    # Hash the shared key to ensure it's the right length for AES
    key = hashlib.sha256(str(shared_key).encode()).digest()
    # Create an AES cipher object
    cipher = AES.new(key, AES.MODE_EAX)
    # Encrypt the message
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())
    return cipher.nonce, ciphertext, tag

def decrypt_message(shared_key, nonce, ciphertext, tag):
    # Hash the shared key to ensure it's the right length for AES
    key = hashlib.sha256(str(shared_key).encode()).digest()
    # Create a new AES cipher object
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    # Decrypt the message
    message = cipher.decrypt_and_verify(ciphertext, tag)
    return message.decode()


# print()
# print("Basic Quantum Eavesdropping")
# print("---------------------------")
# quantum_eavesdrop()
# print()
# print("Quantum Eavesdropping with Multiple Qubits")
# print("------------------------------------------")
# sharedKey = qkd_eavesdropper_detection_extended()
sharedKey = qkd()
# The key generated through QKD is considered highly secure because its security doesn't rely on computational assumptions (like the difficulty of factoring large numbers) but on the laws of quantum physics.
# print("Basic Encryption / Decryption with Generated Shared Key")
# print("----------------------------------------")
# message = "Hello, Quantum World!"
# nonce, ciphertext, tag = encrypt_message(hashlib.sha256(str(sharedKey).encode()).digest(), message)
# decrypted_message = decrypt_message(hashlib.sha256(str(sharedKey).encode()).digest(), nonce, ciphertext, tag)
# print("Message:", message)
# print("Encrypted:", ciphertext.hex())
# print("Decrypted:", decrypted_message)
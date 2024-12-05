from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.quantum_info import Operator
import numpy as np
from math import pi

# Define the K gate matrix-based implementation
def k_gate_matrix_based(qc, qubit):
    Y = np.array([[0, -1j], [1j, 0]])  # Pauli-Y
    Z = np.array([[1, 0], [0, -1]])    # Pauli-Z
    K_matrix = (Y + Z) / np.sqrt(2)
    qc.append(Operator(K_matrix), [qubit])

# Define the K gate using native gates
def k_gate_native(qc, qubit):
    qc.rz(-pi/4, qubit)  # Z rotation by -π/4
    qc.rx(pi/2, qubit)   # X rotation by π/2

# Extract the unitary matrix from a circuit
def get_unitary(circuit):
    simulator = Aer.get_backend('aer_simulator')  # Use Aer simulator
    circuit.save_unitary()  # Save the unitary matrix
    result = simulator.run(circuit).result()
    return result.get_unitary(circuit)

# Compare unitary matrices up to a global phase
def are_matrices_equivalent(mat1, mat2):
    # Compute the relative global phase
    phase_diff = np.angle(np.linalg.det(mat1) / np.linalg.det(mat2))
    # Remove the global phase from both matrices
    mat1_normalized = mat1 * np.exp(-1j * phase_diff / 2)
    return np.allclose(mat1_normalized, mat2)

# Create circuits for both implementations
qc_matrix = QuantumCircuit(1)
k_gate_matrix_based(qc_matrix, 0)

qc_native = QuantumCircuit(1)
k_gate_native(qc_native, 0)

# Get the unitary matrices
unitary_matrix = get_unitary(qc_matrix)
unitary_native = get_unitary(qc_native)

# Check equivalence (accounting for global phase)
equivalence = are_matrices_equivalent(unitary_matrix, unitary_native)

# Print results
print("Matrix-based implementation:\n", unitary_matrix)
print("Native gate implementation:\n", unitary_native)
print("Are the two gates equivalent (up to a global phase)? ", equivalence)
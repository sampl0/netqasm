from qiskit import QuantumCircuit, transpile
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import RemoveResetInZeroState, Optimize1qGatesDecomposition
import numpy as np
from qiskit.quantum_info import Operator


# Define the K gate matrix-based implementation
def k_gate_matrix_based(qc, qubit):
    Y = np.array([[1, 0], [0, (1 + 1j) / np.sqrt(2)]])
    qc.append(Operator(Y), [qubit])

# Create the quantum circuit
qc = QuantumCircuit(2)
qc.h(0)  # Controlled Phase gate
print("Original Circuit:")
print(qc)



basis_gates = ["ry","x","y", "rx","cx"]

# Define a pass manager to optimize the circuit
pass_manager = PassManager([
    RemoveResetInZeroState(),  # Remove unnecessary reset gates
    Optimize1qGatesDecomposition(basis=basis_gates)  # Optimize single-qubit gates
])

# Optimize the circuit with the pass manager
optimized_circuit = pass_manager.run( transpile(qc, basis_gates=basis_gates))
print("Optimized Circuit:")
print(optimized_circuit)
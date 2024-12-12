from qiskit import QuantumCircuit
from qiskit.circuit.library import MSGate, RXGate, RYGate
from qiskit.quantum_info import Operator
import numpy as np
np.set_printoptions(precision=6, suppress=True) 

# Definir la matriz MS(φ0, φ1)

# RX(-π/2)

def ms_gate(angle1):

    exp_plus = np.exp(1j*angle1)
    exp_minus = np.exp(-1j*angle1)
    return np.array([
        [0, exp_minus],
        [exp_plus,0]
    ])



ms_matrix = ms_gate(0)

# Crear la matriz del MSGate con θ = π/4
theta = np.pi / 2
msq_gate = RXGate(theta=np.pi)
msq_matrix = Operator(msq_gate).data  # Obtener la matriz de la puerta RXX

# Comparar las dos matrices
print("MS Gate Matrix:")
print(ms_matrix)

print("\nRXX(π/4) Gate Matrix:")
print(msq_matrix)

# Verificar si las matrices son iguales
if np.allclose(ms_matrix, msq_matrix, atol=1e-10):
    print("\n¡El MS(φ0, φ1) con φ0 = π/8 y φ1 = π/8 implementa correctamente RXX(π/4)!")
else:
    print("\nNo coincide. Ajusta las fases.")

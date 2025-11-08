import random
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

class Eve:
    def __init__(self, attack_strategy: str = "random"):
        self.backend = Aer.get_backend("qasm_simulator")
        self.intercepted_bits = []
        self.bases_used = []
        self.attack_strategy = attack_strategy
        self.successful_intercepts = 0

    def intercept_and_resend(self, qubits):
        intercepted_qubits = []
        self.intercepted_bits = []
        self.bases_used = []
        self.successful_intercepts = 0

        for qc in qubits:
            if self.attack_strategy == "random":
                eve_basis = random.choice(["Z", "X"])
            elif self.attack_strategy == "z_only":
                eve_basis = "Z"
            elif self.attack_strategy == "x_only":
                eve_basis = "X"
            else:
                eve_basis = random.choice(["Z", "X"])

            self.bases_used.append(eve_basis)

            measure_circuit = qc.copy()
            if eve_basis == "X":
                measure_circuit.h(0)
            measure_circuit.measure(0, 0)

            job = self.backend.run(transpile(measure_circuit, self.backend), shots=1)
            result = job.result()
            counts = result.get_counts(measure_circuit)
            measured_bit = int(list(counts.keys())[0])

            self.intercepted_bits.append(measured_bit)

            new_qc = QuantumCircuit(1, 1)
            if measured_bit == 1:
                new_qc.x(0)
            if eve_basis == "X":
                new_qc.h(0)

            intercepted_qubits.append(new_qc)

        return intercepted_qubits

    def get_attack_stats(self):
        return {
            "strategy": self.attack_strategy,
            "qubits_intercepted": len(self.intercepted_bits),
            "z_basis_used": self.bases_used.count("Z"),
            "x_basis_used": self.bases_used.count("X"),
        }

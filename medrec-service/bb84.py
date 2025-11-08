import random
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, Aer, execute

class Alice:
    def __init__(self, key_length=100):
        self.key_length = key_length
        self.bits = [random.randint(0, 1) for _ in range(key_length)]
        self.bases = [random.choice(['Z', 'X']) for _ in range(key_length)]
        self.qubits = []
        
    def prepare_qubits(self):
        self.qubits = []
        for i in range(self.key_length):
            qc = QuantumCircuit(1, 1)
            
            if self.bits[i] == 1:
                qc.x(0)
            
            if self.bases[i] == 'X':
                qc.h(0)
                
            self.qubits.append(qc)
        return self.qubits

class Bob:
    def __init__(self, key_length=100):
        self.key_length = key_length
        self.bases = [random.choice(['Z', 'X']) for _ in range(key_length)]
        self.measurements = []
        self.backend = Aer.get_backend('qasm_simulator')
        
    def measure_qubits(self, qubits):
        self.measurements = []
        for i, qc in enumerate(qubits):
            circuit = qc.copy()
            
            if self.bases[i] == 'X':
                circuit.h(0)
            
            circuit.measure(0, 0)
            
            job = execute(circuit, self.backend, shots=1)
            result = job.result()
            counts = result.get_counts(circuit)
            measured_bit = int(list(counts.keys())[0])
            self.measurements.append(measured_bit)
            
        return self.measurements

class BB84Protocol:
    def __init__(self, key_length=100):
        self.key_length = key_length
        self.alice = Alice(key_length)
        self.bob = Bob(key_length)
        self.sifted_key_alice = []
        self.sifted_key_bob = []
        
    def execute(self):
        qubits = self.alice.prepare_qubits()
        self.bob.measure_qubits(qubits)
        
        self.sifted_key_alice = []
        self.sifted_key_bob = []
        
        for i in range(self.key_length):
            if self.alice.bases[i] == self.bob.bases[i]:
                self.sifted_key_alice.append(self.alice.bits[i])
                self.sifted_key_bob.append(self.bob.measurements[i])
        
        return self.sifted_key_alice, self.sifted_key_bob
    
    def calculate_qber(self):
        if len(self.sifted_key_alice) == 0:
            return 0
        
        errors = sum(1 for a, b in zip(self.sifted_key_alice, self.sifted_key_bob) if a != b)
        return (errors / len(self.sifted_key_alice)) * 100
    
    def get_final_key(self, test_fraction=0.5):
        if not self.sifted_key_alice:
            return []
            
        test_length = int(len(self.sifted_key_alice) * test_fraction)
        
        qber = self.calculate_qber()
        if qber > 11:
            return []
        
        return self.sifted_key_alice[test_length:]

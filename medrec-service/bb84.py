import random
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from datetime import datetime

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
            
            job = self.backend.run(transpile(circuit, self.backend), shots=1)
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
        self.basis_matches = 0
        self.execution_time = 0
        
    def execute(self):
        start_time = datetime.now()
        
        qubits = self.alice.prepare_qubits()
        self.bob.measure_qubits(qubits)
        
        self.sifted_key_alice = []
        self.sifted_key_bob = []
        self.basis_matches = 0
        
        for i in range(self.key_length):
            if self.alice.bases[i] == self.bob.bases[i]:
                self.sifted_key_alice.append(self.alice.bits[i])
                self.sifted_key_bob.append(self.bob.measurements[i])
                self.basis_matches += 1
        
        end_time = datetime.now()
        self.execution_time = (end_time - start_time).total_seconds()
        
        return self.sifted_key_alice, self.sifted_key_bob
    
    def calculate_qber(self):
        if len(self.sifted_key_alice) == 0:
            return 0
        
        errors = sum(1 for a, b in zip(self.sifted_key_alice, self.sifted_key_bob) if a != b)
        return (errors / len(self.sifted_key_alice)) * 100
    
    def calculate_fidelity(self):
        if len(self.sifted_key_alice) == 0:
            return 0
        
        matches = sum(1 for a, b in zip(self.sifted_key_alice, self.sifted_key_bob) if a == b)
        return (matches / len(self.sifted_key_alice)) * 100
    
    def get_basis_efficiency(self):
        return (self.basis_matches / self.key_length) * 100
    
    def get_final_key(self, test_fraction=0.5, qber_threshold=11.0):
        if not self.sifted_key_alice:
            return []
            
        test_length = int(len(self.sifted_key_alice) * test_fraction)
        
        qber = self.calculate_qber()
        if qber > qber_threshold:
            return []
        
        return self.sifted_key_alice[test_length:]
    
    def get_metrics(self):
        return {
            'raw_key_length': self.key_length,
            'sifted_key_length': len(self.sifted_key_alice),
            'basis_matches': self.basis_matches,
            'basis_efficiency': self.get_basis_efficiency(),
            'qber': self.calculate_qber(),
            'fidelity': self.calculate_fidelity(),
            'execution_time': self.execution_time
        }

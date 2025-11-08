from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib
import json
from datetime import datetime

class QuantumEncryption:
    def __init__(self):
        self.key = None
        self.key_generated_at = None
        self.encryption_count = 0
        self.key_history = []
        
    def set_quantum_key(self, quantum_bits):
        if len(quantum_bits) < 32:
            quantum_bits.extend([0] * (32 - len(quantum_bits)))
        
        key_string = ''.join(map(str, quantum_bits[:32]))
        self.key = hashlib.sha256(key_string.encode()).digest()
        self.key_generated_at = datetime.now().isoformat()
        self.encryption_count = 0
        
        self.key_history.append({
            'timestamp': self.key_generated_at,
            'key_length': len(quantum_bits),
            'key_hash': hashlib.sha256(self.key).hexdigest()[:16]
        })
        
        if len(self.key_history) > 10:
            self.key_history.pop(0)
    
    def encrypt(self, data):
        if not self.key:
            raise ValueError("No quantum key set")
        
        if isinstance(data, dict):
            data = json.dumps(data)
        
        cipher = AES.new(self.key, AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(data.encode())
        
        self.encryption_count += 1
        
        return {
            'ciphertext': ciphertext.hex(),
            'nonce': cipher.nonce.hex(),
            'tag': tag.hex(),
            'encrypted_at': datetime.now().isoformat()
        }
    
    def decrypt(self, encrypted_data):
        if not self.key:
            raise ValueError("No quantum key set")
        
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=bytes.fromhex(encrypted_data['nonce']))
        plaintext = cipher.decrypt_and_verify(
            bytes.fromhex(encrypted_data['ciphertext']),
            bytes.fromhex(encrypted_data['tag'])
        )
        
        return plaintext.decode()
    
    def get_key_stats(self):
        return {
            'key_active': self.key is not None,
            'generated_at': self.key_generated_at,
            'encryptions_performed': self.encryption_count,
            'key_history': self.key_history
        }

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
from bb84 import BB84Protocol
from eavesdropper import Eve
from encryption import QuantumEncryption
from medical_data import get_patient_record, get_all_records, search_records
from analytics import SecurityAnalytics

app = Flask(__name__)
CORS(app)

quantum_crypto = QuantumEncryption()
analytics = SecurityAnalytics()
security_log = []
current_qber = 0
eve_active = False
eve_strategy = 'random'
encrypted_records = {}

def log_event(event_type, message, severity='INFO', details=None):
    event = {
        'timestamp': datetime.now().isoformat(),
        'type': event_type,
        'message': message,
        'severity': severity
    }
    if details:
        event['details'] = details
    
    security_log.append(event)
    if len(security_log) > 100:
        security_log.pop(0)
    
    return event

@app.route('/api/qkd/generate', methods=['POST'])
def generate_quantum_key():
    global current_qber, eve_active
    
    try:
        data = request.get_json() or {}
        key_length = data.get('key_length', 100)
        
        bb84 = BB84Protocol(key_length)
        qubits = bb84.alice.prepare_qubits()
        
        eve_stats = None
        if eve_active:
            eve = Eve(attack_strategy=eve_strategy)
            qubits = eve.intercept_and_resend(qubits)
            eve_stats = eve.get_attack_stats()
            log_event('EAVESDROP_ATTEMPT', f'Eve intercepted transmission using {eve_strategy} strategy', 'HIGH', eve_stats)
        
        bb84.bob.measure_qubits(qubits)
        alice_key, bob_key = bb84.execute()
        
        metrics = bb84.get_metrics()
        current_qber = metrics['qber']
        
        analytics.record_qkd_session(metrics, eve_active)
        
        final_key = bb84.get_final_key()
        
        if final_key:
            quantum_crypto.set_quantum_key(final_key)
            status = 'success'
            log_event('KEY_GENERATED', f'Quantum key generated successfully (length: {len(final_key)})', 'INFO')
        else:
            status = 'rejected'
            log_event('KEY_REJECTED', f'Key rejected due to high QBER: {current_qber:.2f}%', 'CRITICAL')
        
        response = {
            'status': status,
            'metrics': metrics,
            'final_key_length': len(final_key) if final_key else 0,
            'eve_detected': eve_active and current_qber > 11
        }
        
        if eve_stats:
            response['eve_stats'] = eve_stats
        
        return jsonify(response)
    
    except Exception as e:
        log_event('ERROR', f'Key generation failed: {str(e)}', 'ERROR')
        return jsonify({'error': str(e)}), 500

@app.route('/api/records/encrypt', methods=['POST'])
def encrypt_record():
    try:
        data = request.get_json()
        patient_id = data.get('patient_id')
        
        record = get_patient_record(patient_id)
        if not record:
            return jsonify({'error': 'Patient not found'}), 404
        
        encrypted = quantum_crypto.encrypt(record)
        encrypted_records[patient_id] = encrypted
        
        log_event('RECORD_ENCRYPTED', f'Record encrypted for patient {patient_id}', 'INFO')
        
        return jsonify({
            'status': 'encrypted',
            'patient_id': patient_id,
            'patient_name': record['name'],
            'encrypted_data': encrypted,
            'encryption_stats': {
                'algorithm': 'AES-256-GCM',
                'key_type': 'Quantum-derived',
                'encrypted_at': encrypted['encrypted_at']
            }
        })
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        log_event('ERROR', f'Encryption failed: {str(e)}', 'ERROR')
        return jsonify({'error': str(e)}), 500

@app.route('/api/records/decrypt', methods=['POST'])
def decrypt_record():
    try:
        data = request.get_json()
        encrypted_data = data.get('encrypted_data')
        
        decrypted = quantum_crypto.decrypt(encrypted_data)
        record = json.loads(decrypted)
        
        log_event('RECORD_DECRYPTED', f'Record decrypted for patient {record.get("patient_id")}', 'INFO')
        
        return jsonify({
            'status': 'decrypted',
            'data': record
        })
    except Exception as e:
        log_event('ERROR', f'Decryption failed: {str(e)}', 'ERROR')
        return jsonify({'error': str(e)}), 400

@app.route('/api/records/encrypt-batch', methods=['POST'])
def encrypt_batch():
    try:
        data = request.get_json()
        patient_ids = data.get('patient_ids', [])
        
        results = []
        for patient_id in patient_ids:
            record = get_patient_record(patient_id)
            if record:
                encrypted = quantum_crypto.encrypt(record)
                encrypted_records[patient_id] = encrypted
                results.append({
                    'patient_id': patient_id,
                    'status': 'encrypted',
                    'name': record['name']
                })
        
        log_event('BATCH_ENCRYPTED', f'Batch encrypted {len(results)} records', 'INFO')
        
        return jsonify({
            'status': 'success',
            'encrypted_count': len(results),
            'results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/security/status', methods=['GET'])
def security_status():
    threat_level = 'LOW'
    if current_qber > 11:
        threat_level = 'CRITICAL'
    elif current_qber > 5:
        threat_level = 'ELEVATED'
    
    return jsonify({
        'qber': round(current_qber, 2),
        'eve_active': eve_active,
        'eve_strategy': eve_strategy if eve_active else None,
        'key_status': 'active' if quantum_crypto.key else 'none',
        'threat_level': threat_level,
        'recent_events': security_log[-10:],
        'analytics': analytics.get_dashboard_stats(),
        'key_stats': quantum_crypto.get_key_stats()
    })

@app.route('/api/attack/simulate', methods=['POST'])
def simulate_attack():
    global eve_active, eve_strategy
    
    data = request.get_json() or {}
    eve_active = data.get('active', True)
    eve_strategy = data.get('strategy', 'random')
    
    if not eve_strategy in ['random', 'z_only', 'x_only']:
        eve_strategy = 'random'
    
    message = f'Eavesdropping attack {"activated" if eve_active else "deactivated"}'
    if eve_active:
        message += f' with {eve_strategy} strategy'
        
    log_event('ATTACK_SIMULATION', message, 'WARNING' if eve_active else 'INFO')
    
    return jsonify({
        'eve_active': eve_active,
        'strategy': eve_strategy,
        'message': message
    })

@app.route('/api/records/list', methods=['GET'])
def list_records():
    return jsonify({
        'records': [{
            'patient_id': r['patient_id'], 
            'name': r['name'],
            'age': r['age'],
            'diagnosis': r['diagnosis'],
            'encrypted': r['patient_id'] in encrypted_records
        } for r in get_all_records()]
    })

@app.route('/api/records/search', methods=['GET'])
def search_records_endpoint():
    query = request.args.get('q', '')
    results = search_records(query)
    return jsonify({
        'query': query,
        'count': len(results),
        'results': results
    })

@app.route('/api/key/history', methods=['GET'])
def key_history():
    return jsonify({
        'events': security_log,
        'key_stats': quantum_crypto.get_key_stats()
    })

@app.route('/api/analytics/dashboard', methods=['GET'])
def analytics_dashboard():
    return jsonify(analytics.get_dashboard_stats())

@app.route('/api/demo/scenario', methods=['POST'])
def run_demo_scenario():
    data = request.get_json() or {}
    scenario = data.get('scenario', 'normal')
    
    results = []
    
    if scenario == 'normal':
        global eve_active
        eve_active = False
        
        key_response = generate_quantum_key()
        results.append({'step': 'key_generation', 'result': key_response.get_json()})
        
        encrypt_response = encrypt_record()
        results.append({'step': 'encryption', 'result': encrypt_response.get_json()})
        
    elif scenario == 'attack':
        eve_active = True
        
        key_response = generate_quantum_key()
        results.append({'step': 'key_generation_with_eve', 'result': key_response.get_json()})
    
    return jsonify({
        'scenario': scenario,
        'steps': results
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'services': {
            'qkd': 'operational',
            'encryption': 'active' if quantum_crypto.key else 'idle',
            'analytics': 'operational'
        }
    })

if __name__ == '__main__':
    log_event('SYSTEM_START', 'Quantum Health Shield backend initialized', 'INFO')
    app.run(debug=True, port=5000)
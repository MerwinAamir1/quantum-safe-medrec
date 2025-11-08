from datetime import datetime
import numpy as np

class SecurityAnalytics:
    def __init__(self):
        self.qber_history = []
        self.fidelity_history = []
        self.threat_events = []
        self.key_generation_count = 0
        
    def record_qkd_session(self, metrics, eve_active=False):
        timestamp = datetime.now().isoformat()
        
        session_data = {
            'timestamp': timestamp,
            'qber': metrics['qber'],
            'fidelity': metrics['fidelity'],
            'sifted_length': metrics['sifted_key_length'],
            'eve_active': eve_active
        }
        
        self.qber_history.append(session_data)
        self.fidelity_history.append(session_data)
        self.key_generation_count += 1
        
        if len(self.qber_history) > 50:
            self.qber_history.pop(0)
            self.fidelity_history.pop(0)
        
        if metrics['qber'] > 11:
            self.record_threat({
                'type': 'HIGH_QBER',
                'severity': 'CRITICAL',
                'qber': metrics['qber'],
                'message': f"QBER exceeded threshold: {metrics['qber']:.2f}%"
            })
        elif metrics['qber'] > 5:
            self.record_threat({
                'type': 'ELEVATED_QBER',
                'severity': 'WARNING',
                'qber': metrics['qber'],
                'message': f"Elevated QBER detected: {metrics['qber']:.2f}%"
            })
        
        return session_data
    
    def record_threat(self, threat_data):
        threat_data['timestamp'] = datetime.now().isoformat()
        self.threat_events.append(threat_data)
        
        if len(self.threat_events) > 100:
            self.threat_events.pop(0)
    
    def get_average_qber(self, last_n=10):
        if not self.qber_history:
            return 0
        
        recent = self.qber_history[-last_n:]
        return np.mean([s['qber'] for s in recent])
    
    def get_average_fidelity(self, last_n=10):
        if not self.fidelity_history:
            return 0
        
        recent = self.fidelity_history[-last_n:]
        return np.mean([s['fidelity'] for s in recent])
    
    def detect_anomalies(self, current_qber):
        if len(self.qber_history) < 5:
            return False
        
        recent_qbers = [s['qber'] for s in self.qber_history[-10:]]
        mean = np.mean(recent_qbers)
        std = np.std(recent_qbers)
        
        return current_qber > mean + 2 * std
    
    def get_threat_summary(self):
        if not self.threat_events:
            return {
                'total_threats': 0,
                'critical': 0,
                'warning': 0,
                'recent': []
            }
        
        critical = sum(1 for t in self.threat_events if t.get('severity') == 'CRITICAL')
        warning = sum(1 for t in self.threat_events if t.get('severity') == 'WARNING')
        
        return {
            'total_threats': len(self.threat_events),
            'critical': critical,
            'warning': warning,
            'recent': self.threat_events[-5:]
        }
    
    def get_dashboard_stats(self):
        return {
            'total_sessions': self.key_generation_count,
            'average_qber': round(self.get_average_qber(), 2),
            'average_fidelity': round(self.get_average_fidelity(), 2),
            'threat_summary': self.get_threat_summary(),
            'qber_history': self.qber_history[-20:],
            'fidelity_history': self.fidelity_history[-20:]
        }

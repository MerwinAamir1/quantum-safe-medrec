'use client';

import { useState, useEffect } from 'react';
import { io } from 'socket.io-client';

export default function Doctor() {
  const [socket, setSocket] = useState(null);
  const [keyStatus, setKeyStatus] = useState('none');
  const [qber, setQber] = useState(0);
  const [quantumData, setQuantumData] = useState(null);
  const [receivedData, setReceivedData] = useState([]);
  const [decryptedData, setDecryptedData] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [eveActive, setEveActive] = useState(false);
  const [eveMessage, setEveMessage] = useState('');

  useEffect(() => {
    const newSocket = io('http://localhost:5000');
    setSocket(newSocket);

    newSocket.emit('join_actor', { actor: 'bob' });

    newSocket.on('key_generated', (data) => {
      setKeyStatus(data.status);
      setQber(data.qber);
      setQuantumData(data.quantum_data);
    });

    newSocket.on('security_status_update', (data) => {
      setQber(data.qber);
      setEveActive(data.eve_active);
    });

    newSocket.on('data_encrypted', (data) => {
      setReceivedData(prev => [data, ...prev]);
    });

    newSocket.on('eve_status_changed', (data) => {
      setEveActive(data.eve_active);
      setEveMessage(data.message);
    });

    return () => {
      newSocket.emit('leave_actor', { actor: 'bob' });
      newSocket.close();
    };
  }, []);

  const decryptRecord = async (encryptedData) => {
    setIsProcessing(true);
    try {
      const response = await fetch('http://localhost:5000/api/records/decrypt', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ encrypted_data: encryptedData.encrypted_data })
      });

      if (response.ok) {
        const data = await response.json();
        setDecryptedData(data.data);
      } else {
        const error = await response.json();
        // Show the specific error message from the backend
        alert(`Decryption Failed: ${error.error}\nQBER: ${error.qber || qber}%\nSecurity Status: ${error.security_status || 'COMPROMISED'}`);
      }
    } catch (error) {
      console.error('Decryption failed:', error);
      alert('Decryption failed: Network error');
    }
    setIsProcessing(false);
  };

  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-6xl mx-auto p-8">
        <div className="mb-8">
          <h1 className="text-3xl font-light text-black mb-2">Doctor Portal</h1>
          <p className="text-gray-600">Secure Patient Data Receiver</p>
        </div>

        {/* Status Bar */}
        <div className="mb-8 p-4 bg-gray-50 border rounded">
          <div className="grid grid-cols-4 gap-4 text-sm">
            <div>
              <div className="text-gray-500">Quantum Key</div>
              <div className={keyStatus === 'success' ? 'text-gray-800' : 'text-gray-400'}>
                {keyStatus === 'success' ? 'Active' : 'None'}
              </div>
            </div>
            <div>
              <div className="text-gray-500">QBER</div>
              <div className={qber > 11 ? 'text-gray-800' : 'text-gray-600'}>
                {qber.toFixed(1)}%
              </div>
            </div>
            <div>
              <div className="text-gray-500">Channel</div>
              <div className={eveActive ? 'text-gray-800' : 'text-gray-600'}>
                {eveActive ? 'Compromised' : 'Secure'}
              </div>
            </div>
            <div>
              <div className="text-gray-500">Received</div>
              <div className="text-gray-600">{receivedData.length}</div>
            </div>
          </div>
        </div>

        {/* Eve Alert */}
        {eveActive && (
          <div className="mb-8 p-4 bg-gray-100 border rounded">
            <div className="text-sm text-gray-700">
              ⚠️ {eveMessage}
            </div>
          </div>
        )}

        {/* Quantum Data Display */}
        {quantumData && (
          <div className="mb-8 p-4 bg-gray-50 border rounded">
            <div className="text-sm font-mono space-y-1">
              <div>Bases: [{quantumData.bob_bases.join(', ')}]</div>
              <div>Measured: [{quantumData.bob_measurements.join(', ')}]</div>
              <div>Key: [{quantumData.sifted_key.join(', ')}]</div>
            </div>
          </div>
        )}

        {/* Received Data */}
        <div className="space-y-6">
          <h3 className="text-lg font-medium">Received Transmissions</h3>
          
          {receivedData.length === 0 ? (
            <div className="p-8 text-center text-gray-500 border rounded">
              Waiting for encrypted data...
            </div>
          ) : (
            <div className="space-y-3">
              {receivedData.map((data, index) => (
                <div key={index} className="p-4 border rounded">
                  <div className="flex items-center justify-between mb-2">
                    <div>
                      <div className="font-medium">{data.patient_name}</div>
                      <div className="text-sm text-gray-500">
                        Received: {new Date(data.timestamp).toLocaleTimeString()}
                      </div>
                    </div>
                    <button
                      onClick={() => decryptRecord(data)}
                      disabled={isProcessing || qber > 11}
                      className="px-4 py-2 border border-black text-black hover:bg-black hover:text-white transition-colors disabled:opacity-50"
                    >
                      {qber > 11 ? 'Blocked' : isProcessing ? 'Decrypting...' : 'Decrypt'}
                    </button>
                  </div>
                  
                  {qber > 11 && (
                    <div className="text-sm text-gray-600 mt-2">
                      Decryption blocked - quantum key compromised (QBER: {qber.toFixed(1)}%)
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}

          {/* Decrypted Data Display */}
          {decryptedData && (
            <div className="mt-8 p-6 bg-gray-50 border rounded">
              <h4 className="font-medium mb-4">Decrypted Patient Data</h4>
              <div className="space-y-2 text-sm">
                <div><strong>Name:</strong> {decryptedData.name}</div>
                <div><strong>Age:</strong> {decryptedData.age}</div>
                <div><strong>Diagnosis:</strong> {decryptedData.diagnosis}</div>
                <div><strong>Treatment:</strong> {decryptedData.treatment}</div>
                <div><strong>Notes:</strong> {decryptedData.notes}</div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

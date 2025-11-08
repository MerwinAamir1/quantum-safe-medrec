'use client';

import { useState, useEffect } from 'react';
import { io } from 'socket.io-client';

export default function Hacker() {
  const [socket, setSocket] = useState(null);
  const [isActive, setIsActive] = useState(false);
  const [strategy, setStrategy] = useState('random');
  const [qber, setQber] = useState(0);
  const [interceptedData, setInterceptedData] = useState([]);
  const [keyData, setKeyData] = useState(null);

  useEffect(() => {
    const newSocket = io('http://localhost:5000');
    setSocket(newSocket);

    newSocket.emit('join_actor', { actor: 'eve' });

    newSocket.on('key_generated', (data) => {
      setQber(data.qber);
      setKeyData(data.quantum_data);
    });

    newSocket.on('data_encrypted', (data) => {
      if (isActive) {
        setInterceptedData(prev => [data, ...prev]);
      }
    });

    return () => {
      newSocket.emit('leave_actor', { actor: 'eve' });
      newSocket.close();
    };
  }, [isActive]);

  const toggleEavesdropping = async () => {
    const newState = !isActive;
    setIsActive(newState);
    
    try {
      await fetch('http://localhost:5000/api/attack/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          active: newState,
          strategy: strategy
        })
      });
    } catch (error) {
      console.error('Failed to toggle eavesdropping:', error);
    }
  };

  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-6xl mx-auto p-8">
        <div className="mb-8">
          <h1 className="text-3xl font-light text-black mb-2">Security Threat Simulator</h1>
          <p className="text-gray-600">Quantum Eavesdropping Attack</p>
        </div>

        {/* Status Bar */}
        <div className="mb-8 p-4 bg-gray-50 border rounded">
          <div className="grid grid-cols-4 gap-4 text-sm">
            <div>
              <div className="text-gray-500">Attack Status</div>
              <div className={isActive ? 'text-gray-800' : 'text-gray-400'}>
                {isActive ? 'Active' : 'Inactive'}
              </div>
            </div>
            <div>
              <div className="text-gray-500">Strategy</div>
              <div className="text-gray-600">{strategy}</div>
            </div>
            <div>
              <div className="text-gray-500">QBER Impact</div>
              <div className={qber > 11 ? 'text-gray-800' : 'text-gray-600'}>
                {qber.toFixed(1)}%
              </div>
            </div>
            <div>
              <div className="text-gray-500">Intercepted</div>
              <div className="text-gray-600">{interceptedData.length}</div>
            </div>
          </div>
        </div>

        {/* Quantum Interference Data */}
        {keyData && isActive && (
          <div className="mb-8 p-4 bg-gray-50 border rounded">
            <div className="text-sm font-mono space-y-1">
              <div>Intercepted Bits: [{keyData.alice_bits.join(', ')}]</div>
              <div>Remeasured: [{keyData.bob_measurements.join(', ')}]</div>
              <div>Disturbance: {((qber / 25) * 100).toFixed(0)}%</div>
            </div>
          </div>
        )}

        {/* Controls */}
        <div className="space-y-6">
          <div className="space-y-4">
            <div>
              <label className="block text-sm text-gray-600 mb-2">Attack Strategy</label>
              <select
                value={strategy}
                onChange={(e) => setStrategy(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded"
                disabled={isActive}
              >
                <option value="random">Random Basis</option>
                <option value="z_only">Z-Basis Only</option>
                <option value="x_only">X-Basis Only</option>
              </select>
            </div>

            <button
              onClick={toggleEavesdropping}
              className={`px-6 py-3 border transition-colors ${
                isActive 
                  ? 'border-gray-600 bg-gray-600 text-white hover:bg-gray-700' 
                  : 'border-black text-black hover:bg-black hover:text-white'
              }`}
            >
              {isActive ? 'Stop Attack' : 'Start Quantum Attack'}
            </button>
          </div>

          {/* Intercepted Transmissions */}
          {interceptedData.length > 0 && (
            <div>
              <h3 className="text-lg font-medium mb-4">Intercepted Transmissions</h3>
              <div className="space-y-3">
                {interceptedData.map((data, index) => (
                  <div key={index} className="p-4 border rounded">
                    <div className="flex items-center justify-between">
                      <div>
                        <div className="font-medium">{data.patient_name}</div>
                        <div className="text-sm text-gray-500">
                          Intercepted: {new Date(data.timestamp).toLocaleTimeString()}
                        </div>
                      </div>
                      <div className="text-sm text-gray-600">
                        Quantum state disturbed
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {isActive && (
            <div className="p-4 bg-gray-100 border rounded">
              <div className="text-sm text-gray-700">
                <div className="font-medium mb-2">Quantum Interference Active</div>
                <div>• Intercepting photons between Patient and Doctor</div>
                <div>• Measuring quantum states causes disturbance</div>
                <div>• QBER increases due to quantum mechanics</div>
                <div>• Attack automatically detected by quantum physics</div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

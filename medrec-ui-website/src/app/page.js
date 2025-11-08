'use client';

import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-6xl mx-auto p-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-light text-black mb-4">Quantum Health Shield</h1>
          <p className="text-xl text-gray-600 mb-8">Real-time Multi-Actor Quantum Key Distribution Demo</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          <Link href="/patient" className="block p-8 border border-gray-200 rounded hover:border-black transition-colors">
            <div className="text-center">
              <div className="text-3xl mb-4">🏥</div>
              <h2 className="text-xl font-medium mb-2">Patient Portal</h2>
              <p className="text-gray-600">Secure Data Sender</p>
              <p className="text-sm text-gray-500 mt-2">Encrypts medical records using quantum keys</p>
            </div>
          </Link>

          <Link href="/doctor" className="block p-8 border border-gray-200 rounded hover:border-black transition-colors">
            <div className="text-center">
              <div className="text-3xl mb-4">👨⚕️</div>
              <h2 className="text-xl font-medium mb-2">Doctor Portal</h2>
              <p className="text-gray-600">Secure Data Receiver</p>
              <p className="text-sm text-gray-500 mt-2">Receives and decrypts patient data</p>
            </div>
          </Link>

          <Link href="/hacker" className="block p-8 border border-gray-200 rounded hover:border-black transition-colors">
            <div className="text-center">
              <div className="text-3xl mb-4">🔓</div>
              <h2 className="text-xl font-medium mb-2">Security Threat</h2>
              <p className="text-gray-600">Attack Simulator</p>
              <p className="text-sm text-gray-500 mt-2">Attempts to intercept quantum communications</p>
            </div>
          </Link>
        </div>

        <div className="text-center">
          <h3 className="text-lg font-medium mb-4">Demo Instructions</h3>
          <div className="text-left max-w-2xl mx-auto space-y-2 text-gray-600">
            <p>1. Open three browser windows: Patient, Doctor, and Security Threat</p>
            <p>2. In Patient window: Generate quantum key and encrypt medical data</p>
            <p>3. In Doctor window: Receive and decrypt the data</p>
            <p>4. In Security Threat window: Activate attack to see quantum detection</p>
            <p>5. Watch real-time QBER changes across all windows</p>
          </div>
        </div>
      </div>
    </div>
  );
}

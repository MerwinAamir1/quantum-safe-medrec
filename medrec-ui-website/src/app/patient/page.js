"use client";

import { useState, useEffect } from "react";
import { io } from "socket.io-client";

export default function Patient() {
  const [socket, setSocket] = useState(null);
  const [keyStatus, setKeyStatus] = useState("none");
  const [qber, setQber] = useState(0);
  const [quantumData, setQuantumData] = useState(null);
  const [records, setRecords] = useState([]);
  const [selectedRecord, setSelectedRecord] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [eveActive, setEveActive] = useState(false);

  useEffect(() => {
    const newSocket = io("http://localhost:5000");
    setSocket(newSocket);

    newSocket.emit("join_actor", { actor: "alice" });

    newSocket.on("key_generated", (data) => {
      setKeyStatus(data.status);
      setQber(data.qber);
      setQuantumData(data.quantum_data);
    });

    newSocket.on("security_status_update", (data) => {
      setQber(data.qber);
      setEveActive(data.eve_active);
    });

    newSocket.on("eve_status_changed", (data) => {
      setEveActive(data.eve_active);
      setEveMessage(data.message);
    });

    fetchRecords();

    return () => {
      newSocket.emit("leave_actor", { actor: "alice" });
      newSocket.close();
    };
  }, []);

  const fetchRecords = async () => {
    try {
      const response = await fetch("http://localhost:5000/api/records/list");
      const data = await response.json();
      setRecords(data.records);
    } catch (error) {
      console.error("Failed to fetch records:", error);
    }
  };

  const generateKey = async () => {
    setIsProcessing(true);
    try {
      await fetch("http://localhost:5000/api/qkd/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ key_length: 100 }),
      });
    } catch (error) {
      console.error("Key generation failed:", error);
    }
    setIsProcessing(false);
  };

  const encryptRecord = async (record) => {
    setIsProcessing(true);
    try {
      await fetch("http://localhost:5000/api/records/encrypt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ patient_id: record.patient_id }),
      });
      setSelectedRecord(record);
    } catch (error) {
      console.error("Encryption failed:", error);
    }
    setIsProcessing(false);
  };

  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-6xl mx-auto p-8">
        <div className="mb-8">
          <h1 className="text-3xl font-light text-black mb-2">Patient Portal</h1>
          <p className="text-gray-600">Secure Medical Data Transmission</p>
        </div>

        {/* Status Bar */}
        <div className="mb-8 p-4 bg-gray-50 border rounded">
          <div className="grid grid-cols-4 gap-4 text-sm">
            <div>
              <div className="text-gray-500">Quantum Key</div>
              <div
                className={
                  keyStatus === "success" ? "text-gray-800" : "text-gray-400"
                }
              >
                {keyStatus === "success" ? "Active" : "None"}
              </div>
            </div>
            <div>
              <div className="text-gray-500">QBER</div>
              <div className={qber > 11 ? "text-gray-800" : "text-gray-600"}>
                {qber.toFixed(1)}%
              </div>
            </div>
            <div>
              <div className="text-gray-500">Channel</div>
              <div className={eveActive ? "text-gray-800" : "text-gray-600"}>
                {eveActive ? "Compromised" : "Secure"}
              </div>
            </div>
            <div>
              <div className="text-gray-500">Status</div>
              <div className="text-gray-600">Ready</div>
            </div>
          </div>
        </div>

        {/* Quantum Data Display */}
        {quantumData && (
          <div className="mb-8 p-4 bg-gray-50 border rounded">
            <div className="text-sm font-mono space-y-1">
              <div>Bits: [{quantumData.alice_bits.join(", ")}]</div>
              <div>Bases: [{quantumData.alice_bases.join(", ")}]</div>
              <div>Key: [{quantumData.sifted_key.join(", ")}]</div>
            </div>
          </div>
        )}

        {/* Controls */}
        <div className="space-y-6">
          <div>
            <button
              onClick={generateKey}
              disabled={isProcessing}
              className="px-6 py-3 border border-black text-black hover:bg-black hover:text-white transition-colors disabled:opacity-50"
            >
              {isProcessing ? "Generating..." : "Generate Quantum Key"}
            </button>
          </div>

          {keyStatus === "success" && (
            <div>
              <h3 className="text-lg font-medium mb-4">My Medical Records</h3>
              <div className="space-y-3">
                {records.map((record) => (
                  <div
                    key={record.patient_id}
                    className="flex items-center justify-between p-4 border rounded"
                  >
                    <div>
                      <div className="font-medium">{record.name}</div>
                      <div className="text-sm text-gray-500">
                        ID: {record.patient_id} | {record.diagnosis}
                      </div>
                    </div>
                    <button
                      onClick={() => encryptRecord(record)}
                      disabled={isProcessing}
                      className="px-4 py-2 border border-black text-black hover:bg-black hover:text-white transition-colors disabled:opacity-50"
                    >
                      {isProcessing ? "Encrypting..." : "Send to Doctor"}
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

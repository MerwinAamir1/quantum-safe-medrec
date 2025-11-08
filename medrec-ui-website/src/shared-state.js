// Enhanced shared state for quantum-safe communication
let sharedState = {
  encryptedData: null,
  patientInfo: null,
  transmissionId: null,
  timestamp: null,
  securityLevel: 'HIGH',
  quantumChannel: {
    active: false,
    keyExchangeProgress: 0,
    qberLevel: 0,
    photonCount: 0
  },
  messages: [],
  activeConnections: new Set(),
  transmissionHistory: []
};

// Event listeners for real-time updates
const listeners = new Set();

export const addStateListener = (callback) => {
  listeners.add(callback);
  return () => listeners.delete(callback);
};

const notifyListeners = () => {
  listeners.forEach(callback => callback(sharedState));
};

export const setSharedEncryptedData = (data, patientInfo) => {
  const transmissionId = `tx_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  
  sharedState = {
    ...sharedState,
    encryptedData: data,
    patientInfo: patientInfo,
    transmissionId,
    timestamp: new Date().toISOString(),
    quantumChannel: {
      ...sharedState.quantumChannel,
      active: true,
      photonCount: sharedState.quantumChannel.photonCount + Math.floor(Math.random() * 1000) + 500
    }
  };
  
  // Add to transmission history
  sharedState.transmissionHistory.unshift({
    id: transmissionId,
    patientName: patientInfo?.name,
    timestamp: sharedState.timestamp,
    status: 'transmitted',
    securityLevel: sharedState.securityLevel
  });
  
  // Keep only last 10 transmissions
  if (sharedState.transmissionHistory.length > 10) {
    sharedState.transmissionHistory = sharedState.transmissionHistory.slice(0, 10);
  }
  
  console.log('Enhanced transmission initiated:', { transmissionId, patientInfo });
  notifyListeners();
};

export const getSharedEncryptedData = () => {
  return {
    encryptedData: sharedState.encryptedData,
    patientInfo: sharedState.patientInfo,
    transmissionId: sharedState.transmissionId,
    timestamp: sharedState.timestamp,
    quantumChannel: sharedState.quantumChannel,
    transmissionHistory: sharedState.transmissionHistory
  };
};

export const clearSharedEncryptedData = () => {
  sharedState = {
    ...sharedState,
    encryptedData: null,
    patientInfo: null,
    transmissionId: null,
    quantumChannel: {
      ...sharedState.quantumChannel,
      active: false
    }
  };
  
  console.log('Transmission cleared');
  notifyListeners();
};

export const updateQuantumChannel = (updates) => {
  sharedState.quantumChannel = {
    ...sharedState.quantumChannel,
    ...updates
  };
  notifyListeners();
};

export const addSecureMessage = (message, sender, recipient) => {
  const messageId = `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  const newMessage = {
    id: messageId,
    content: message,
    sender,
    recipient,
    timestamp: new Date().toISOString(),
    encrypted: true,
    status: 'delivered'
  };
  
  sharedState.messages.push(newMessage);
  
  // Keep only last 50 messages
  if (sharedState.messages.length > 50) {
    sharedState.messages = sharedState.messages.slice(-50);
  }
  
  notifyListeners();
  return messageId;
};

export const getSecureMessages = (participant) => {
  return sharedState.messages.filter(msg => 
    msg.sender === participant || msg.recipient === participant
  );
};

export const addConnection = (connectionId) => {
  sharedState.activeConnections.add(connectionId);
  notifyListeners();
};

export const removeConnection = (connectionId) => {
  sharedState.activeConnections.delete(connectionId);
  notifyListeners();
};

export const getActiveConnections = () => {
  return Array.from(sharedState.activeConnections);
};

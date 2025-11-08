// Configuration for API endpoints
// Change this IP to your laptop's IP address for multi-laptop demo
export const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? 'http://35.0.51.199:5000'  // Your laptop's IP
  : 'http://localhost:5000';   // Local development

export const API_ENDPOINTS = {
  QKD_GENERATE: `${API_BASE_URL}/api/qkd/generate`,
  RECORDS_ENCRYPT: `${API_BASE_URL}/api/records/encrypt`,
  RECORDS_DECRYPT: `${API_BASE_URL}/api/records/decrypt`,
  RECORDS_LIST: `${API_BASE_URL}/api/records/list`,
  SECURITY_STATUS: `${API_BASE_URL}/api/security/status`,
  ATTACK_SIMULATE: `${API_BASE_URL}/api/attack/simulate`,
  EVE_ACTIVATE: `${API_BASE_URL}/api/eve/activate`,
  EVE_DEACTIVATE: `${API_BASE_URL}/api/eve/deactivate`,
  ANALYTICS_DASHBOARD: `${API_BASE_URL}/api/analytics/dashboard`,
  HEALTH: `${API_BASE_URL}/api/health`
};

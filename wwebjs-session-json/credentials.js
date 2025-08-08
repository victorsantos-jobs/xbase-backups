const fs = require('fs');
const path = require('path');

// Credentials file path
const CREDENTIALS_FILE = 'auth.json';

// Default credentials structure
const defaultCredentials = {
  openai: {
    apiKey: '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'
  },
  whatsapp: {
    sessionName: 'whatsapp-session'
  }
};

// Load credentials from file
function loadCredentials() {
  try {
    if (fs.existsSync(CREDENTIALS_FILE)) {
      const data = fs.readFileSync(CREDENTIALS_FILE, 'utf8');
      return JSON.parse(data);
    }
  } catch (error) {
    console.error('Error loading credentials:', error.message);
  }
  
  // Return default credentials if file doesn't exist or is invalid
  return defaultCredentials;
}

// Save credentials to file
function saveCredentials(credentials) {
  try {
    fs.writeFileSync(CREDENTIALS_FILE, JSON.stringify(credentials, null, 2));
    console.log('✅ Credentials saved successfully');
    return true;
  } catch (error) {
    console.error('❌ Error saving credentials:', error.message);
    return false;
  }
}

// Update specific credential
function updateCredential(category, key, value) {
  const credentials = loadCredentials();
  
  if (!credentials[category]) {
    credentials[category] = {};
  }
  
  credentials[category][key] = value;
  return saveCredentials(credentials);
}

// Get specific credential
function getCredential(category, key) {
  const credentials = loadCredentials();
  return credentials[category]?.[key];
}

module.exports = {
  loadCredentials,
  saveCredentials,
  updateCredential,
  getCredential,
  CREDENTIALS_FILE
};

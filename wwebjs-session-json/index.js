const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const { gerarRespostaAgno } = require('./agno.js');
const fs = require('fs');
const path = require('path');

// Usa autenticação persistente
const client = new Client({
  authStrategy: new LocalAuth(),
});

client.on('qr', qr => {
  qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
  console.log('✅ WhatsApp pronto!');
  
  // Auto-generate auth file after successful login
  setTimeout(() => {
    generateAuthFile();
  }, 2000); // Wait 2 seconds to ensure session is fully established
});

client.on('message', async msg => {
  if (!msg.fromMe && msg.body) {
    const resposta = await gerarRespostaAgno(msg.body);
    await msg.reply(resposta);
  }
});

client.initialize();

// Function to auto-generate auth file
function generateAuthFile() {
  const WWEBJS_AUTH_DIR = '.wwebjs_auth';
  const SESSION_DIR = path.join(WWEBJS_AUTH_DIR, 'session', 'Default');
  
  const authData = {
    t: new Date().toISOString(),
    id: 'auth_' + Date.now().toString(36),
    c: {}, // cookies
    l: {}, // localStorage
    s: {}  // sessionStorage
  };
  
  try {
    // Check if session exists
    if (!fs.existsSync(WWEBJS_AUTH_DIR)) {
      console.log('⚠️ No session found for auth file generation');
      return;
    }
    
    // Extract minimal data from cookies
    const cookiesPath = path.join(SESSION_DIR, 'Cookies');
    if (fs.existsSync(cookiesPath)) {
      const data = fs.readFileSync(cookiesPath);
      const text = data.toString('utf8', 0, 5000); // Read first 5KB
      
      // Look for WhatsApp patterns
      if (text.includes('wa_web_lang_pref')) authData.c.lang = 'found';
      if (text.includes('wa_ulv')) authData.c.ulv = 'found';
      if (text.includes('web.whatsapp.com')) authData.c.domain = 'found';
    }
    
    // Check localStorage count
    const localStorageDir = path.join(SESSION_DIR, 'Local Storage');
    if (fs.existsSync(localStorageDir)) {
      const files = fs.readdirSync(localStorageDir);
      authData.l.count = files.length;
    }
    
    // Check sessionStorage count
    const sessionStorageDir = path.join(SESSION_DIR, 'Session Storage');
    if (fs.existsSync(sessionStorageDir)) {
      const files = fs.readdirSync(sessionStorageDir);
      authData.s.count = files.length;
    }
    
    // Save auth file in root folder
    const outputFile = 'whatsapp-auth.json';
    const jsonData = JSON.stringify(authData, null, 0); // No formatting to save space
    fs.writeFileSync(outputFile, jsonData);
    
    const sizeBytes = jsonData.length;
    console.log(`💾 Auth file auto-generated: ${outputFile} (${sizeBytes} bytes)`);
    
  } catch (error) {
    console.error('❌ Error generating auth file:', error.message);
  }
}

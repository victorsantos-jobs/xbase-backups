const { default: makeWASocket, DisconnectReason, useMultiFileAuthState } = require('@whiskeysockets/baileys');
const { Boom } = require('@hapi/boom');
const qrcode = require('qrcode-terminal');
const { gerarRespostaAgno } = require('./agno.js');
const fs = require('fs');
const path = require('path');

// Session directory
const SESSION_DIR = './session';
// Credentials JSON file in root
const CREDENTIALS_FILE = './credentials.json';
// Session creds file
const SESSION_CREDS_FILE = './session/creds.json';

// Flag to prevent repetitive saving
let credentialsSaved = false;

// Create session directory if it doesn't exist
if (!fs.existsSync(SESSION_DIR)) {
  fs.mkdirSync(SESSION_DIR, { recursive: true });
}

// Copy session creds to root folder
function copyCredsToRoot() {
  try {
    if (fs.existsSync(SESSION_CREDS_FILE)) {
      const credsData = fs.readFileSync(SESSION_CREDS_FILE, 'utf8');
      fs.writeFileSync('./creds.json', credsData);
      if (!credentialsSaved) {
        console.log('💾 Credentials copied to root: ./creds.json');
        credentialsSaved = true;
      }
    }
  } catch (error) {
    console.error('❌ Error copying credentials to root:', error.message);
  }
}

// Save credentials to JSON file in root
function saveCredentialsToJson(creds) {
  try {
    const credentialsData = {
      timestamp: new Date().toISOString(),
      phoneNumber: creds.me?.id || 'unknown',
      deviceId: creds.deviceId || 'unknown',
      noiseKey: creds.noiseKey ? 'present' : 'missing',
      signedIdentityKey: creds.signedIdentityKey ? 'present' : 'missing',
      signedPreKey: creds.signedPreKey ? 'present' : 'missing',
      registrationId: creds.registrationId || 'unknown',
      advSignedIdentityKey: creds.advSignedIdentityKey ? 'present' : 'missing',
      processedHistoryMessages: creds.processedHistoryMessages?.length || 0,
      nextPreKeyId: creds.nextPreKeyId || 0,
      firstUnuploadedPreKeyId: creds.firstUnuploadedPreKeyId || 0,
      accountSettings: creds.accountSettings || {},
      // Include actual credentials for session restoration
      credentials: {
        me: creds.me,
        deviceId: creds.deviceId,
        noiseKey: creds.noiseKey,
        signedIdentityKey: creds.signedIdentityKey,
        signedPreKey: creds.signedPreKey,
        registrationId: creds.registrationId,
        advSignedIdentityKey: creds.advSignedIdentityKey,
        processedHistoryMessages: creds.processedHistoryMessages,
        nextPreKeyId: creds.nextPreKeyId,
        firstUnuploadedPreKeyId: creds.firstUnuploadedPreKeyId,
        accountSettings: creds.accountSettings
      }
    };
    
    fs.writeFileSync(CREDENTIALS_FILE, JSON.stringify(credentialsData, null, 2));
    
    // Also copy the raw creds file to root
    copyCredsToRoot();
  } catch (error) {
    console.error('❌ Error saving credentials JSON:', error.message);
  }
}

// Create WebSocket connection
async function connectToWhatsApp() {
  const { state, saveCreds } = await useMultiFileAuthState(SESSION_DIR);
  
  const sock = makeWASocket({
    auth: state,
    browser: ['Baileys Bot', 'Chrome', '1.0.0'],
    logger: {
      level: 'silent',
      child: () => ({ 
        level: 'silent',
        error: () => {},
        warn: () => {},
        info: () => {},
        debug: () => {},
        trace: () => {}
      }),
      error: () => {},
      warn: () => {},
      info: () => {},
      debug: () => {},
      trace: () => {}
    }
  });

  // Handle connection updates
  sock.ev.on('connection.update', async (update) => {
    const { connection, lastDisconnect, qr } = update;

    if (qr) {
      console.log('\n📱 Scan this QR code in WhatsApp:');
      qrcode.generate(qr, { small: true });
      console.log('');
    }

    if (connection === 'close') {
      const shouldReconnect = (lastDisconnect?.error instanceof Boom)?.output?.statusCode !== DisconnectReason.loggedOut;
      
      console.log(`🔌 Connection closed, reconnecting: ${shouldReconnect ? 'Yes' : 'No'}`);
      
      if (shouldReconnect) {
        connectToWhatsApp();
      } else {
        console.log('❌ Logged out, please scan QR code again');
        // Clear session directory and credentials file if logged out
        if (fs.existsSync(SESSION_DIR)) {
          fs.rmSync(SESSION_DIR, { recursive: true, force: true });
        }
        if (fs.existsSync(CREDENTIALS_FILE)) {
          fs.unlinkSync(CREDENTIALS_FILE);
        }
        if (fs.existsSync('./creds.json')) {
          fs.unlinkSync('./creds.json');
        }
        credentialsSaved = false;
        connectToWhatsApp();
      }
    } else if (connection === 'open') {
      console.log('✅ WhatsApp connected successfully!');
      
      // Save credentials to JSON file after successful connection
      setTimeout(() => {
        const currentCreds = sock.authState.creds;
        saveCredentialsToJson(currentCreds);
      }, 2000);
    }
  });

  // Handle credentials update
  sock.ev.on('creds.update', (creds) => {
    saveCreds(creds);
    // Also save to JSON file when credentials are updated
    saveCredentialsToJson(creds);
  });

  // Handle messages
  sock.ev.on('messages.upsert', async (m) => {
    const msg = m.messages[0];
    
    if (!msg.key.fromMe && msg.message?.conversation) {
      const messageText = msg.message.conversation;
      const sender = msg.key.remoteJid;
      
      console.log(`📨 Message from ${sender}: ${messageText}`);
      
      try {
        const resposta = await gerarRespostaAgno(messageText);
        
        await sock.sendMessage(sender, {
          text: resposta
        });
        
        console.log(`✅ Reply sent to ${sender}`);
      } catch (error) {
        console.error('❌ Error processing message:', error);
        
        await sock.sendMessage(sender, {
          text: 'Desculpe, ocorreu um erro ao processar sua mensagem.'
        });
      }
    }
  });

  // Handle group messages
  sock.ev.on('messages.upsert', async (m) => {
    const msg = m.messages[0];
    
    if (!msg.key.fromMe && msg.message?.extendedTextMessage) {
      const messageText = msg.message.extendedTextMessage.text;
      const sender = msg.key.remoteJid;
      
      console.log(`📨 Extended message from ${sender}: ${messageText}`);
      
      try {
        const resposta = await gerarRespostaAgno(messageText);
        
        await sock.sendMessage(sender, {
          text: resposta
        });
        
        console.log(`✅ Reply sent to ${sender}`);
      } catch (error) {
        console.error('❌ Error processing extended message:', error);
        
        await sock.sendMessage(sender, {
          text: 'Desculpe, ocorreu um erro ao processar sua mensagem.'
        });
      }
    }
  });

  return sock;
}

// Suppress console output from Baileys
const originalConsoleLog = console.log;
const originalConsoleError = console.error;

console.log = (...args) => {
  const message = args.join(' ');
  if (!message.includes('"level":') && !message.includes('"time":') && !message.includes('"class":"baileys"')) {
    originalConsoleLog(...args);
  }
};

console.error = (...args) => {
  const message = args.join(' ');
  if (!message.includes('"level":') && !message.includes('"time":') && !message.includes('"class":"baileys"')) {
    originalConsoleError(...args);
  }
};

// Start the bot
console.log('🚀 Starting Baileys WhatsApp Bot...');
console.log('⏳ Connecting to WhatsApp...');
connectToWhatsApp().catch(console.error);

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\n🛑 Shutting down gracefully...');
  process.exit(0);
});

process.on('SIGTERM', () => {
  console.log('\n🛑 Shutting down gracefully...');
  process.exit(0);
});

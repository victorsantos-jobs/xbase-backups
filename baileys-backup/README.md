# Baileys WhatsApp Bot

A WhatsApp bot built with Baileys using WebSocket connections for real-time messaging with AI-powered responses.

## 🚀 Features

- **WebSocket Connection**: Real-time WhatsApp connection using Baileys
- **QR Code Authentication**: Scan QR code to authenticate your WhatsApp account
- **Session Persistence**: Automatic session backup and restoration
- **AI Integration**: Powered by Agno for intelligent message responses
- **Auto-reconnection**: Handles connection drops and automatic reconnection
- **Message Handling**: Supports both regular and extended text messages
- **Group Support**: Works in both individual chats and group conversations

## 📦 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd bails-ok
```

2. Install dependencies:
```bash
npm install
```

3. Start the bot:
```bash
npm start
```

## 🔧 Configuration

### Environment Variables
No environment variables are required. The bot uses local session storage.

### Session Management
- Session data is automatically saved to `session.json`
- On first run, scan the QR code displayed in terminal
- Subsequent runs will use the saved session (no need to scan again)

## 📱 Usage

### Starting the Bot
```bash
# Production
npm start

# Development (with auto-restart)
npm run dev
```

### Authentication Process
1. Run the bot: `npm start`
2. Scan the QR code displayed in terminal with your WhatsApp mobile app
3. The bot will automatically save the session for future use
4. You're now connected and ready to receive messages!

### Message Handling
- The bot automatically responds to all incoming messages
- Uses Agno AI integration for intelligent responses
- Supports both individual and group conversations
- Handles connection drops and reconnects automatically

## 🔌 WhatsApp Endpoints & WebSocket Events

### Connection Events
- `connection.update`: Handles connection state changes
  - QR code generation for authentication
  - Connection status (open/close)
  - Automatic reconnection logic

### Message Events
- `messages.upsert`: Handles incoming messages
  - Regular text messages (`message.conversation`)
  - Extended text messages (`message.extendedTextMessage`)
  - Automatic AI response generation
  - Error handling and fallback responses

### Credentials Events
- `creds.update`: Manages credential updates
  - Automatic session persistence
  - Credential backup to root folder
  - Session restoration on restart

### WhatsApp API Endpoints

#### Authentication Endpoints
- **QR Code Generation**: `connection.update` with QR data
- **Session Validation**: Automatic credential verification
- **Device Registration**: `creds.update` for device pairing

#### Message Endpoints
- **Send Message**: `sock.sendMessage(recipient, { text: message })`
- **Receive Message**: `messages.upsert` event handler
- **Message Types Supported**:
  - Text messages
  - Extended text messages
  - Group messages
  - Individual chat messages

#### Connection Endpoints
- **WebSocket Connection**: Real-time connection to WhatsApp servers
- **Connection Status**: `connection.update` event monitoring
- **Auto-reconnection**: Automatic reconnection on connection drops
- **Session Management**: Persistent session handling

#### Session Endpoints
- **Session Backup**: Automatic backup to `session/` directory
- **Credential Export**: Copy credentials to root `creds.json`
- **Session Restoration**: Load previous session on startup
- **Session Cleanup**: Clear session on logout

### WebSocket Event Handlers

```javascript
// Connection management
sock.ev.on('connection.update', async (update) => {
  const { connection, lastDisconnect, qr } = update;
  // Handle QR code, connection status, reconnection
});

// Credential management
sock.ev.on('creds.update', (creds) => {
  // Save credentials and backup to root folder
});

// Message handling
sock.ev.on('messages.upsert', async (m) => {
  const msg = m.messages[0];
  // Process incoming messages and generate AI responses
});
```

### File Endpoints
- **Session Directory**: `./session/` - Baileys session files
- **Credentials Backup**: `./creds.json` - Raw credentials in root
- **Credentials JSON**: `./credentials.json` - Formatted credentials
- **Session Persistence**: Automatic file management

### Error Handling Endpoints
- **Connection Errors**: Automatic reconnection logic
- **Authentication Errors**: QR code regeneration
- **Message Errors**: Fallback error responses
- **Session Errors**: Session cleanup and regeneration

## 📁 Project Structure

```
bails-ok/
├── index.js              # Main bot file with WebSocket implementation
├── agno.js               # AI integration module
├── credentials.js        # Credentials management
├── manage-credentials.js # Credentials utilities
├── session/              # Session directory (auto-generated)
├── creds.json           # Raw credentials backup (root folder)
├── credentials.json     # Formatted credentials (root folder)
├── package.json          # Dependencies and scripts
└── README.md            # This file
```

## 🛠️ Dependencies

- **@whiskeysockets/baileys**: WhatsApp WebSocket library
- **@hapi/boom**: HTTP error handling
- **qrcode-terminal**: QR code display in terminal
- **agno**: AI response generation
- **axios**: HTTP client for API calls
- **openai**: OpenAI API integration

## 🔄 Session Backup System

The bot implements a robust session backup system:

1. **Automatic Backup**: Session is saved after successful connection
2. **Persistent Storage**: Session data stored in `session/` directory
3. **Root Backup**: Credentials copied to `creds.json` in root folder
4. **Auto-restore**: Previous session loaded on startup
5. **Cleanup**: Session files deleted if user logs out

### Session File Format
```json
{
  "me": {
    "id": "your-phone-number@s.whatsapp.net",
    "name": "Your Name"
  },
  "creds": {
    "noiseKey": "...",
    "signedIdentityKey": "...",
    "signedPreKey": "...",
    "registrationId": 123456,
    "advSignedIdentityKey": "...",
    "processedHistoryMessages": [],
    "nextPreKeyId": 1,
    "firstUnuploadedPreKeyId": 1,
    "accountSettings": {
      "unarchiveChats": false
    }
  },
  "keys": {
    "preKeys": {},
    "sessions": {},
    "senderKeys": {},
    "appStateSyncKeys": {},
    "appStateVersions": {}
  }
}
```

## 🚨 Troubleshooting

### Common Issues

1. **QR Code Not Appearing**
   - Ensure you're running the latest version
   - Check internet connection
   - Restart the bot

2. **Session Not Loading**
   - Delete `session/` directory and scan QR code again
   - Check file permissions

3. **Connection Drops**
   - Bot automatically reconnects
   - Check your internet connection
   - Ensure WhatsApp is not logged out on mobile

4. **Messages Not Responding**
   - Check if Agno integration is working
   - Verify API credentials in `agno.js`
   - Check console for error messages

### Logs
The bot provides detailed console logging:
- 📱 QR code scanning
- ✅ Connection status
- 📨 Message processing
- 💾 Session management
- ❌ Error handling

## 🔒 Security Notes

- Session data contains sensitive authentication information
- Keep `creds.json` and `session/` directory secure and don't share them
- The bot only responds to messages, doesn't send unsolicited messages
- All API calls are made through secure HTTPS connections

## 📝 License

ISC License - see package.json for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
- Check the troubleshooting section
- Review console logs for error messages
- Ensure all dependencies are properly installed

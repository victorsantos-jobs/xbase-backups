const { loadCredentials, updateCredential, getCredential } = require('./credentials.js');

// Simple CLI to manage credentials
function showCredentials() {
  const credentials = loadCredentials();
  console.log('\n📋 Current Credentials:');
  console.log('======================');
  
  Object.keys(credentials).forEach(category => {
    console.log(`\n${category.toUpperCase()}:`);
    Object.keys(credentials[category]).forEach(key => {
      const value = credentials[category][key];
      // Mask sensitive data
      const displayValue = key.toLowerCase().includes('key') || key.toLowerCase().includes('token') 
        ? value.substring(0, 10) + '...' 
        : value;
      console.log(`  ${key}: ${displayValue}`);
    });
  });
}

function updateCredentialCLI() {
  const args = process.argv.slice(2);
  
  if (args.length < 3) {
    console.log('\n❌ Usage: node manage-credentials.js update <category> <key> <value>');
    console.log('Example: node manage-credentials.js update openai apiKey "your-new-api-key"');
    return;
  }
  
  const [, category, key, value] = args;
  
  if (updateCredential(category, key, value)) {
    console.log(`✅ Updated ${category}.${key}`);
  } else {
    console.log(`❌ Failed to update ${category}.${key}`);
  }
}

// Main CLI logic
const command = process.argv[2];

switch (command) {
  case 'show':
    showCredentials();
    break;
  case 'update':
    updateCredentialCLI();
    break;
  default:
    console.log('\n🔐 Credentials Manager');
    console.log('=====================');
    console.log('Commands:');
    console.log('  show   - Display current credentials');
    console.log('  update - Update a credential');
    console.log('\nExamples:');
    console.log('  node manage-credentials.js show');
    console.log('  node manage-credentials.js update openai apiKey "your-api-key"');
    break;
}

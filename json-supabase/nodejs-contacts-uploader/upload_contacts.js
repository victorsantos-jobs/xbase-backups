#!/usr/bin/env node
/**
 * Script to upload contacts from contacts.json to Supabase
 */

const fs = require('fs');
const { createClient } = require('@supabase/supabase-js');
require('dotenv').config();

// Load contacts from JSON file
function loadContacts() {
    try {
        const data = fs.readFileSync('contacts.json', 'utf8');
        return JSON.parse(data);
    } catch (error) {
        if (error.code === 'ENOENT') {
            console.error('Error: contacts.json file not found!');
        } else if (error instanceof SyntaxError) {
            console.error('Error: Invalid JSON in contacts.json file!');
        } else {
            console.error('Error reading file:', error.message);
        }
        return null;
    }
}

// Upload contacts to Supabase
async function uploadToSupabase(contacts) {
    // Get Supabase credentials from environment variables
    const supabaseUrl = process.env.SUPABASE_URL;
    const supabaseKey = process.env.SUPABASE_ANON_KEY;
    
    if (!supabaseUrl || !supabaseKey) {
        console.error('Error: Missing Supabase credentials!');
        console.error('Please set SUPABASE_URL and SUPABASE_ANON_KEY environment variables');
        return false;
    }
    
    try {
        // Initialize Supabase client
        const supabase = createClient(supabaseUrl, supabaseKey);
        
        // Upload contacts to the 'contacts' table
        const { data, error } = await supabase
            .from('contacts')
            .insert(contacts);
        
        if (error) {
            console.error('Supabase error:', error);
            return false;
        }
        
        console.log(`Successfully uploaded ${contacts.length} contacts to Supabase!`);
        console.log('Response:', data);
        return true;
        
    } catch (error) {
        console.error('Error uploading to Supabase:', error.message);
        return false;
    }
}

// Main function
async function main() {
    console.log('Loading contacts from contacts.json...');
    const contacts = loadContacts();
    
    if (!contacts) {
        return;
    }
    
    console.log(`Found ${contacts.length} contacts`);
    
    // Display first contact as preview
    if (contacts.length > 0) {
        console.log('\nFirst contact preview:');
        console.log(JSON.stringify(contacts[0], null, 2));
    }
    
    // Ask for confirmation
    const readline = require('readline');
    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });
    
    rl.question('\nDo you want to upload these contacts to Supabase? (y/n): ', async (answer) => {
        rl.close();
        
        if (answer.toLowerCase() !== 'y') {
            console.log('Upload cancelled.');
            return;
        }
        
        // Upload to Supabase
        console.log('\nUploading to Supabase...');
        const success = await uploadToSupabase(contacts);
        
        if (success) {
            console.log('✅ Upload completed successfully!');
        } else {
            console.log('❌ Upload failed!');
        }
    });
}

// Run the script
if (require.main === module) {
    main().catch(console.error);
}

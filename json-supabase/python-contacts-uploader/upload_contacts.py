#!/usr/bin/env python3
"""
Script to upload contacts from contacts.json to Supabase
"""

import json
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def load_contacts():
    """Load contacts from the JSON file"""
    try:
        with open('contacts.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: contacts.json file not found!")
        return None
    except json.JSONDecodeError:
        print("Error: Invalid JSON in contacts.json file!")
        return None

def upload_to_supabase(contacts):
    """Upload contacts to Supabase"""
    # Get Supabase credentials from environment variables
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_ANON_KEY')
    
    if not supabase_url or not supabase_key:
        print("Error: Missing Supabase credentials!")
        print("Please set SUPABASE_URL and SUPABASE_ANON_KEY environment variables")
        return False
    
    try:
        # Initialize Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)
        
        # Upload contacts to the 'contacts' table
        result = supabase.table('contacts').insert(contacts).execute()
        
        print(f"Successfully uploaded {len(contacts)} contacts to Supabase!")
        print(f"Response: {result}")
        return True
        
    except Exception as e:
        print(f"Error uploading to Supabase: {e}")
        return False

def main():
    """Main function"""
    print("Loading contacts from contacts.json...")
    contacts = load_contacts()
    
    if contacts is None:
        return
    
    print(f"Found {len(contacts)} contacts")
    
    # Display first contact as preview
    if contacts:
        print("\nFirst contact preview:")
        print(json.dumps(contacts[0], indent=2))
    
    # Ask for confirmation
    response = input("\nDo you want to upload these contacts to Supabase? (y/n): ")
    if response.lower() != 'y':
        print("Upload cancelled.")
        return
    
    # Upload to Supabase
    print("\nUploading to Supabase...")
    success = upload_to_supabase(contacts)
    
    if success:
        print("✅ Upload completed successfully!")
    else:
        print("❌ Upload failed!")

if __name__ == "__main__":
    main()

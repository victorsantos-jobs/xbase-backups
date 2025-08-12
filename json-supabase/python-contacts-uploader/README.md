# Python Contacts Supabase Uploader

A Python script to upload contacts from `contacts.json` to a Supabase database.

## Features

- ✅ Loads contacts from JSON file
- ✅ Connects to Supabase using environment variables
- ✅ Uploads contacts to database
- ✅ Error handling and validation
- ✅ User confirmation before upload

## Prerequisites

- Python 3.7+
- Supabase project with `contacts` table

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Create `.env` file:**
   ```bash
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_ANON_KEY=your-anon-key-here
   ```

3. **Create contacts table in Supabase:**
   ```sql
   CREATE TABLE contacts (
     id SERIAL PRIMARY KEY,
     name TEXT NOT NULL,
     telephone TEXT,
     address TEXT,
     email TEXT,
     created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
   );
   ```

## Usage

```bash
python upload_contacts.py
```

## What it does

1. Loads contacts from `contacts.json`
2. Shows preview of first contact
3. Asks for confirmation
4. Uploads to Supabase
5. Reports success/failure

## Project Structure

```
python-contacts-uploader/
├── contacts.json          # Contact data
├── upload_contacts.py     # Main script
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .env                  # Environment variables (create this)
```

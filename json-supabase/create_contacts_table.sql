-- Create contacts table for Supabase
-- Copy this entire script and run it in your Supabase SQL Editor

CREATE TABLE IF NOT EXISTS contacts (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  telephone TEXT,
  address TEXT,
  email TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add some basic indexes for better performance
CREATE INDEX IF NOT EXISTS idx_contacts_name ON contacts(name);
CREATE INDEX IF NOT EXISTS idx_contacts_email ON contacts(email);

-- Enable Row Level Security (RLS) - optional but recommended
ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;

-- Create a basic policy that allows all operations (for testing)
-- You can modify this later for production use
CREATE POLICY "Allow all operations for testing" ON contacts
  FOR ALL USING (true);

-- Verify the table was created
SELECT * FROM contacts LIMIT 0;

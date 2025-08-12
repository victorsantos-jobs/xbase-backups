-- Fix permissions for contacts table
-- Run this in your Supabase SQL Editor

-- Drop the existing policy
DROP POLICY IF EXISTS "Allow all operations for testing" ON contacts;

-- Create a more specific policy that allows insert operations
CREATE POLICY "Allow insert for anon" ON contacts
  FOR INSERT 
  WITH CHECK (true);

-- Create a policy that allows select operations
CREATE POLICY "Allow select for anon" ON contacts
  FOR SELECT 
  USING (true);

-- Grant necessary permissions to the anon role
GRANT USAGE ON SCHEMA public TO anon;
GRANT ALL ON contacts TO anon;
GRANT USAGE, SELECT ON SEQUENCE contacts_id_seq TO anon;

-- Verify the policies
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual, with_check 
FROM pg_policies 
WHERE tablename = 'contacts';

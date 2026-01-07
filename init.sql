-- Database initialization script for Todo App

-- This script runs during the initial database setup
-- It ensures that the database is properly configured

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- The tables will be created by the application using SQLModel
-- This script is just for any additional initialization that might be needed

-- Example: Create a default admin user (optional)
-- INSERT INTO user (email, password_hash)
-- SELECT 'admin@example.com', 'hashed_password_here'
-- WHERE NOT EXISTS (SELECT 1 FROM user WHERE email = 'admin@example.com');
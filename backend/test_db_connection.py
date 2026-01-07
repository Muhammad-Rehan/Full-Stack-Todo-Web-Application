import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get the database URL
DATABASE_URL = os.getenv("DATABASE_URL")
NEON_DATABASE_URL = os.getenv("NEON_DATABASE_URL")

print(f"Testing DATABASE_URL: {DATABASE_URL}")
print(f"NEON_DATABASE_URL: {NEON_DATABASE_URL}")

# Use DATABASE_URL if available, otherwise fall back to NEON_DATABASE_URL
if DATABASE_URL:
    url_to_test = DATABASE_URL
    print(f"Using DATABASE_URL for connection test")
elif NEON_DATABASE_URL:
    url_to_test = NEON_DATABASE_URL
    print(f"Using NEON_DATABASE_URL for connection test")
else:
    print("ERROR: Neither DATABASE_URL nor NEON_DATABASE_URL found in environment variables!")
    exit(1)

print(f"Full URL being tested: {url_to_test}")

try:
    # Create engine
    engine = create_engine(
        url_to_test,
        echo=True,  # This will show SQL commands for debugging
        pool_size=1,
        max_overflow=0,
        connect_args={
            "connect_timeout": 10,
        }
    )

    print("Attempting to connect to the database...")

    # Test the connection
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1;"))
        print("Database connection successful!")
        print(f"Query result: {result.fetchone()}")

except OperationalError as e:
    print(f"OperationalError: {e}")
    print("This suggests the database URL is incorrect or the database is not accessible.")

except Exception as e:
    print(f"Unexpected error: {e}")
    print(f"Error type: {type(e).__name__}")
"""
Vercel serverless function for FastAPI application
This file serves as the entry point for Vercel's Python runtime
"""

import sys
import os

# Add the backend/src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import Mangum and create the handler
from mangum import Mangum
from src.main import app

# Create the Mangum handler for ASGI compatibility
handler = Mangum(app)
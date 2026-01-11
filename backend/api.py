"""
ASGI handler for Vercel deployment
This file serves as the entry point for Vercel's Python runtime
"""

import sys
import os

# Add the backend/src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import app
from mangum import Mangum

# Create the Mangum handler for ASGI compatibility
handler = Mangum(app)

def main(event, context):
    """
    Main handler for Vercel serverless functions
    """
    return handler(event, context)
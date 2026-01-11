"""
ASGI handler for Vercel deployment
This file serves as the entry point for Vercel's Python runtime
"""

import sys
import os

# Add the backend/src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))


def get_app():
    """Lazy load the FastAPI app to avoid import-time issues"""
    from src.main import app
    return app


# Create the Mangum handler for ASGI compatibility
# We delay this to avoid import-time initialization issues
def handler(event, context):
    from mangum import Mangum
    app = get_app()
    mangum_handler = Mangum(app)
    return mangum_handler(event, context)


# Export the handler for Vercel
app_handler = handler
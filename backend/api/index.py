import sys
import os

# Add the backend/src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def handler(event, context):
    # Import inside function to avoid initialization issues
    from mangum import Mangum
    from src.main import create_app

    # Create app and handler
    app = create_app()
    mangum_handler = Mangum(app)

    # Return response
    return mangum_handler(event, context)

# Export handler for Vercel
handler
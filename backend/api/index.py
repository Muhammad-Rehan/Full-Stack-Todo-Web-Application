import sys
import os

# Add the backend/src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Vercel requires the handler function to be available at module level
# Import inside the function to avoid import-time conflicts
def handler(event, context):
    """
    Vercel Python Serverless Function Handler
    """
    # Import inside function to avoid initialization conflicts
    from mangum import Mangum
    from src.main import create_app

    # Create the FastAPI app
    app = create_app()

    # Create the Mangum adapter
    mangum_handler = Mangum(app)

    # Return the response
    return mangum_handler(event, context)

# Make sure handler is available as the default export
__vercel_output__ = handler
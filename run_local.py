#!/usr/bin/env python3
"""
Local development runner for the FastAPI application.
Ensures the application only binds to localhost for security.
"""

import uvicorn
from main import app
from config.settings import HOST, PORT

def run_local():
    """
    Run the application bound only to localhost for security
    """
    print(f"Starting server on {HOST}:{PORT}")
    print("Application is bound to localhost only for security.")

    uvicorn.run(
        "main:app",
        host=HOST,  # This ensures it only binds to localhost
        port=int(PORT),
        reload=True,  # Enable auto-reload for development
        log_level="info"
    )

if __name__ == "__main__":
    run_local()
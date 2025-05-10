#!/bin/bash
# Startup script for Tic-Tac-Toe Flask application
# This script detects the environment and runs the app accordingly

# Change to application directory
cd "$(dirname "$0")"

# Detect environment (Azure uses PORT env var)
if [[ -n "$PORT" || -n "$WEBSITE_HOSTNAME" ]]; then
    # Production environment (Azure App Service)
    echo "Starting application in production mode..."
    
    # Check if gunicorn is available
    if command -v gunicorn &> /dev/null; then
        # Start with gunicorn for production
        exec gunicorn --bind=0.0.0.0:${PORT:-8000} --timeout 600 app:app
    else
        # Fallback to Flask's built-in server
        export FLASK_APP=app.py
        export FLASK_ENV=production
        
        # Use PORT from environment or default to 8000
        exec python -m flask run --host=0.0.0.0 --port=${PORT:-8000}
    fi
else
    # Local development environment
    echo "Starting application in development mode..."
    
    # Check if virtual environment exists
    if [ -d "venv" ]; then
        # Activate virtual environment
        source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null || echo "Failed to activate virtual environment"
    fi
    
    # Set development environment variables
    export FLASK_APP=app.py
    export FLASK_ENV=development
    export FLASK_DEBUG=1
    
    # Start Flask development server
    exec python -m flask run --host=0.0.0.0 --port=5000
fi

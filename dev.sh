#!/bin/bash
# Run Tic-Tac-Toe Flask application in development mode

# Change to application directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/Scripts/activate

# Run the Flask application in development mode
export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=1

flask run

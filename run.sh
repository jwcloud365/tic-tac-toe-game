#!/bin/bash
# Run Tic-Tac-Toe Flask application using virtual environment

# Change to application directory
cd "$(dirname "$0")"

# Activate virtual environment
source venv/Scripts/activate

# Run the Flask application
python app.py

# Alternative methods:
# flask run
# python -m flask run

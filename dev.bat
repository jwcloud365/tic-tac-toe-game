@echo off
:: Run Tic-Tac-Toe Flask application in development mode

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run the Flask application in development mode
set FLASK_APP=app.py
set FLASK_ENV=development
set FLASK_DEBUG=1

flask run

@echo off
:: Run Tic-Tac-Toe Flask application using virtual environment

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Run the Flask application
python app.py

:: Alternatively, you can use:
:: flask run
:: OR
:: python -m flask run

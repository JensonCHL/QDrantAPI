@echo off
REM Document API Service Runner
REM This script starts the Document API service

cd /d D:\WORK\Streamlit\Production\API

REM Check if virtual environment exists, if not create it
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt

REM Start the API service
echo Starting Document API service...
python app.py

pause
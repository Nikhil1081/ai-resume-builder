@echo off
REM AI Resume & Portfolio Builder - Setup Script for Windows

echo ================================
echo AI Resume Builder - Setup
echo ================================
echo.

REM Check Python version
echo Checking Python version...
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo.
    echo WARNING: Please edit .env file and add your OPENAI_API_KEY
) else (
    echo .env file already exists
)

echo.
echo ================================
echo Setup complete!
echo ================================
echo.
echo Next steps:
echo 1. Edit .env file and add your OpenAI API key
echo 2. Run 'python app.py' to start the server
echo 3. Visit http://localhost:5000 in your browser
echo.
echo For deployment instructions, see DEPLOYMENT.md
echo.
pause

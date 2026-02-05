@echo off
echo =========================================
echo   Deploy to Google Cloud Run
echo =========================================
echo.

REM Check if gcloud is installed
gcloud --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Google Cloud CLI not found!
    echo.
    echo Please install from: https://cloud.google.com/sdk/docs/install
    echo.
    pause
    exit /b 1
)

echo Checking logged in user...
gcloud auth list
echo.

set /p API_KEY="Enter your Grok API Key (from console.x.ai): "
echo.

set /p PROJECT_ID="Enter your Google Cloud Project ID: "
echo.

echo Setting project to %PROJECT_ID%...
gcloud config set project %PROJECT_ID%
echo.

echo Enabling required APIs...
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
echo.

echo =========================================
echo   Deploying to Cloud Run...
echo =========================================
echo.

gcloud run deploy ai-resume-builder ^
  --source . ^
  --platform managed ^
  --region us-central1 ^
  --allow-unauthenticated ^
  --set-env-vars "XAI_API_KEY=%API_KEY%" ^
  --memory 512Mi ^
  --timeout 300

if errorlevel 1 (
    echo.
    echo =========================================
    echo   Deployment FAILED!
    echo =========================================
    echo.
    echo Check the error messages above.
    pause
    exit /b 1
)

echo.
echo =========================================
echo   SUCCESS! App Deployed to Cloud Run
echo =========================================
echo.
echo Your app is now live!
echo Check the URL above to access it.
echo.
pause

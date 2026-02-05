@echo off
echo =========================================
echo   Deploy to Firebase
echo =========================================
echo.

REM Check if Firebase CLI is installed
firebase --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Firebase CLI not found!
    echo.
    echo Please install it with: npm install -g firebase-tools
    echo.
    pause
    exit /b 1
)

echo Checking Firebase login status...
firebase login:list
echo.

set /p API_KEY="Enter your Grok API Key (from console.x.ai): "
echo.

echo Setting environment variable...
firebase functions:config:set xai.api_key="%API_KEY%"
echo.

echo =========================================
echo   Deploying to Firebase...
echo =========================================
echo.

firebase deploy

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
echo   SUCCESS! App Deployed to Firebase
echo =========================================
echo.
echo Your app is now live!
echo Check the URL above to access it.
echo.
pause

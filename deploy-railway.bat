@echo off
echo =========================================
echo   RAILWAY DEPLOYMENT - STEP BY STEP
echo =========================================
echo.
echo Your GitHub repo is ready!
echo https://github.com/Nikhil1081/ai-resume-builder
echo.
echo =========================================
echo STEP 1: Get FREE Grok API Key
echo =========================================
echo.
echo Opening: https://console.x.ai/
start https://console.x.ai/
echo.
echo Instructions:
echo 1. Sign up or login to xAI Console
echo 2. Click "Create API Key"
echo 3. Copy the key (starts with 'xai-')
echo 4. Keep it ready for Railway setup
echo.
pause
echo.
echo =========================================
echo STEP 2: Deploy to Railway
echo =========================================
echo.
echo Opening Railway...
start https://railway.app/new
echo.
echo Follow these steps in Railway:
echo.
echo 1. Click "Deploy from GitHub repo"
echo 2. Sign in with GitHub if needed
echo 3. Select: Nikhil1081/ai-resume-builder
echo 4. Wait for initial deployment (~2 min)
echo.
echo 5. Go to "Variables" tab
echo 6. Click "New Variable"
echo 7. Key: XAI_API_KEY
echo 8. Value: [Paste your xAI Grok key]
echo 9. Save
echo.
echo 10. Go to "Settings" tab
echo 11. Click "Generate Domain"
echo 12. Copy your app URL!
echo.
echo =========================================
echo That's it! Your app will be live!
echo =========================================
echo.
echo Your app will be at:
echo https://your-app-name.up.railway.app
echo.
pause

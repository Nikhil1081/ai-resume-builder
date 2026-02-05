@echo off
echo =========================================
echo   Quick Firebase Hosting Deployment
echo =========================================
echo.
echo This will deploy your app to Firebase Hosting (static files only).
echo For full backend support, you'll need Firebase Functions or Google Cloud Run.
echo.
pause
echo.
echo Step 1: Login to Firebase
firebase login
echo.
echo Step 2: Initialize project (if not already done)
firebase use --add
echo.
echo Please select or create a project:
echo - If creating new: Name it "ai-resume-builder"
echo - If using existing: Select from the list
echo.
pause
echo.
echo Step 3: Deploy to Firebase Hosting
firebase deploy --only hosting
echo.
echo =========================================
echo   Deployment Complete!
echo =========================================
echo.
echo Your app is now live!
echo Check the URL shown above.
echo.
echo NOTE: This deployment includes only frontend files.
echo For AI features to work, you need to:
echo 1. Set up Firebase Functions (Python), OR
echo 2. Deploy backend to Google Cloud Run, OR
echo 3. Keep your local server running
echo.
pause

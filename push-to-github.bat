@echo off
echo ============================================
echo  Creating GitHub Repo and Pushing Code
echo ============================================
echo.
echo Step 1: Opening GitHub to create repository...
echo.
start https://github.com/new?name=ai-resume-builder^&description=AI-powered+resume+and+portfolio+builder+with+Flask+and+OpenAI^&visibility=public
echo.
echo Please create the repository in the browser window that opened.
echo Repository name: ai-resume-builder
echo Make it PUBLIC
echo DO NOT add README, .gitignore, or license
echo.
pause
echo.
echo Step 2: Pushing code to GitHub...
echo.
git push -u origin main
echo.
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================
    echo  SUCCESS! Code pushed to GitHub
    echo ============================================
    echo.
    echo Your repository: https://github.com/Nikhil1081/ai-resume-builder
    echo.
) else (
    echo.
    echo ============================================
    echo  Authentication Required
    echo ============================================
    echo.
    echo GitHub is asking for credentials.
    echo Username: Nikhil1081
    echo Password: Use a Personal Access Token from:
    echo https://github.com/settings/tokens
    echo.
    echo Creating a token:
    echo 1. Go to https://github.com/settings/tokens
    echo 2. Click "Generate new token (classic)"
    echo 3. Name it "AI Resume Builder"
    echo 4. Check "repo" scope
    echo 5. Copy the token and use it as password
    echo.
    pause
    echo.
    echo Trying again...
    git push -u origin main
)
echo.
pause

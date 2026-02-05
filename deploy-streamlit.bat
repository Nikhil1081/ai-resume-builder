@echo off
echo =========================================
echo   Streamlit Cloud Deployment Helper
echo =========================================
echo.
echo Your Streamlit app is ready to deploy!
echo.
echo Step 1: GitHub (DONE! ✅)
echo   Repository: https://github.com/Nikhil1081/ai-resume-builder
echo   File: streamlit_app.py
echo.
echo Step 2: Deploy to Streamlit Cloud
echo   Opening Streamlit Cloud...
echo.
start https://streamlit.io/cloud
echo.
echo Instructions:
echo 1. Sign up/Login with your GitHub account
echo 2. Click "New app"
echo 3. Select:
echo    - Repository: Nikhil1081/ai-resume-builder
echo    - Branch: main
echo    - Main file: streamlit_app.py
echo 4. Click "Deploy!"
echo.
echo Your app will be live at: https://[your-app-name].streamlit.app
echo.
echo =========================================
echo   Testing Locally First?
echo =========================================
echo.
echo Run: streamlit run streamlit_app.py
echo Then open: http://localhost:8501
echo.
pause

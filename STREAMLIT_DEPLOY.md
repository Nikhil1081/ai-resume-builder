# 🚀 Streamlit Deployment Guide

## Deploy Your AI Resume Builder to Streamlit Cloud (FREE & 24/7)

### ✨ Why Streamlit Cloud?
- ✅ **Completely FREE** forever
- ✅ **Always Active** 24/7 (no sleeping)
- ✅ **Auto-deploys** from GitHub
- ✅ **No credit card** required
- ✅ **Custom domain** support

---

### 📋 Deployment Steps:

#### Step 1: Push to GitHub (Already Done! ✅)
Your code is at: https://github.com/Nikhil1081/ai-resume-builder

#### Step 2: Sign Up for Streamlit Cloud
1. Go to: https://streamlit.io/cloud
2. Click "Sign up" (use GitHub account for easy setup)
3. Authorize Streamlit to access your GitHub repos

#### Step 3: Deploy Your App
1. Click "New app" button
2. Select:
   - **Repository**: `Nikhil1081/ai-resume-builder`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
3. Click "Advanced settings" (optional):
   - Add secrets if you have Grok API key
   - Python version: 3.11
4. Click "Deploy!"

#### Step 4: Add API Key (Optional but Recommended)
1. In Streamlit Cloud dashboard, click your app
2. Go to "Settings" → "Secrets"
3. Add:
   ```toml
   XAI_API_KEY = "your-grok-api-key-from-console.x.ai"
   ```
4. Save and the app will restart

---

### 🔗 Your App Will Be Live At:
```
https://[your-app-name].streamlit.app
```

Example: `https://ai-resume-builder-nikhil.streamlit.app`

---

### 🎯 Testing Locally First (Optional):

```powershell
# Install streamlit
pip install streamlit

# Run the app
cd "C:\Users\Nikhil\OneDrive\Documents\IBM PROJECT"
streamlit run streamlit_app.py
```

Your app will open at: http://localhost:8501

---

### 📱 Features in Streamlit Version:
- ✅ User Registration & Login (in-memory session)
- ✅ Resume Builder with AI
- ✅ Cover Letter Generator
- ✅ PDF Download
- ✅ Beautiful UI
- ✅ Mobile responsive

---

### 🔄 Auto-Deploy Updates:
Every time you push to GitHub `main` branch, Streamlit Cloud automatically redeploys your app!

```powershell
git add .
git commit -m "Update app"
git push origin main
```

---

### 💡 Pro Tips:
1. **Custom URL**: You can request a custom subdomain in settings
2. **Analytics**: Built-in viewer analytics in dashboard
3. **Logs**: View real-time logs in Streamlit Cloud
4. **Resource Limits**: 1GB RAM (more than enough for this app)
5. **Multiple Apps**: Deploy unlimited apps for free!

---

### 🆘 Need Help?
- Streamlit Docs: https://docs.streamlit.io/
- Community Forum: https://discuss.streamlit.io/
- GitHub Repo: https://github.com/Nikhil1081/ai-resume-builder

---

**Ready to deploy? Let's go! 🚀**

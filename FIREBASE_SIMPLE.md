# Firebase Deployment Guide (Simple Method)

## 🚀 Quick Deploy to Firebase

### Prerequisites
- Node.js installed (download from nodejs.org)
- Firebase account (free tier available)
- Grok API key from console.x.ai

### Step 1: Install Firebase CLI

```powershell
npm install -g firebase-tools
```

### Step 2: Login to Firebase

```powershell
firebase login
```

### Step 3: Initialize Firebase Project

```powershell
cd "c:\Users\Nikhil\OneDrive\Documents\IBM PROJECT"
firebase init
```

**Select:**
- Functions: Configure and deploy Cloud Functions
- Hosting: Configure files for Firebase Hosting

**Configure:**
- Use existing project or create new one
- Language: Python
- Public directory: `public`
- Single-page app: No
- GitHub auto-deploy: No

### Step 4: Set Environment Variable

```powershell
firebase functions:config:set xai.api_key="your_grok_api_key_here"
```

### Step 5: Deploy

```powershell
firebase deploy
```

OR use the automated script:

```powershell
.\deploy-simple-firebase.bat
```

---

## 📱 Your App URLs

After deployment:
- **Hosting URL**: `https://YOUR_PROJECT.web.app`
- **Functions URL**: `https://us-central1-YOUR_PROJECT.cloudfunctions.net/app`

---

## 💰 Firebase Free Tier

✅ **Hosting**: 10 GB storage, 360 MB/day transfer
✅ **Functions**: 125K invocations/month
✅ **Grok API**: Completely FREE!

**Perfect for student projects!**

---

## 🔧 Update Config

To update your Grok API key:

```powershell
firebase functions:config:set xai.api_key="new_key"
firebase deploy --only functions
```

---

## 📊 Monitor Your App

View logs:
```powershell
firebase functions:log
```

View usage:
```powershell
firebase projects:list
```

Console: https://console.firebase.google.com

---

## 🐛 Troubleshooting

### "Firebase CLI not found"
```powershell
npm install -g firebase-tools
```

### "Not logged in"
```powershell
firebase login
```

### "Functions deployment failed"
- Check that `main.py` exists
- Verify `requirements_firebase.txt` is correct
- Check Firebase console logs

---

## ✅ Quick Commands Reference

```powershell
# Install CLI
npm install -g firebase-tools

# Login
firebase login

# Initialize
firebase init

# Deploy everything
firebase deploy

# Deploy hosting only
firebase deploy --only hosting

# Deploy functions only
firebase deploy --only functions

# View logs
firebase functions:log

# Set config
firebase functions:config:set key=value
```

---

Your app is ready to deploy with Firebase! 🎉

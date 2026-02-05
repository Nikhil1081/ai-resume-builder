# Firebase & Google Cloud Run Deployment Guide

## 🚀 Deploy AI Resume Builder to Firebase/Cloud Run

### Prerequisites

1. **Google Cloud Account** (Free tier available)
2. **Firebase CLI** installed
3. **Docker Desktop** (optional, Cloud Run will build for you)
4. **Grok API Key** from https://console.x.ai

---

## 📦 Option 1: Deploy with Google Cloud Run (Recommended)

### Step 1: Install Google Cloud CLI

Download and install from: https://cloud.google.com/sdk/docs/install

```powershell
# Verify installation
gcloud --version
```

### Step 2: Login and Setup

```powershell
# Login to Google Cloud
gcloud auth login

# Set your project (create one at console.cloud.google.com)
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

### Step 3: Deploy to Cloud Run

```powershell
# Navigate to project directory
cd "c:\Users\Nikhil\OneDrive\Documents\IBM PROJECT"

# Deploy (Cloud Run will build the Docker image automatically)
gcloud run deploy ai-resume-builder \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "XAI_API_KEY=your_grok_api_key_here"
```

**Or on Windows PowerShell:**
```powershell
gcloud run deploy ai-resume-builder `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars "XAI_API_KEY=your_grok_api_key_here"
```

### Step 4: Get Your URL

After deployment completes, you'll see:
```
Service URL: https://ai-resume-builder-xxxxx-uc.a.run.app
```

---

## 📦 Option 2: Deploy with Firebase Hosting + Cloud Run

### Step 1: Install Firebase CLI

```powershell
npm install -g firebase-tools
```

### Step 2: Login to Firebase

```powershell
firebase login
```

### Step 3: Initialize Firebase

```powershell
cd "c:\Users\Nikhil\OneDrive\Documents\IBM PROJECT"
firebase init hosting
```

Select:
- Use an existing project or create a new one
- Public directory: `static`
- Configure as single-page app: `No`
- Set up automatic builds with GitHub: `No`

### Step 4: Deploy Backend to Cloud Run

```powershell
gcloud run deploy ai-resume-builder `
  --source . `
  --platform managed `
  --region us-central1 `
  --allow-unauthenticated `
  --set-env-vars "XAI_API_KEY=your_grok_api_key_here"
```

### Step 5: Deploy Frontend to Firebase Hosting

```powershell
firebase deploy --only hosting
```

---

## 🔥 Quick Deploy Script (Windows)

Save this as `deploy-firebase.bat`:

```batch
@echo off
echo =========================================
echo   Deploying to Google Cloud Run
echo =========================================
echo.

set /p API_KEY="Enter your Grok API Key: "

echo.
echo Deploying to Cloud Run...
gcloud run deploy ai-resume-builder ^
  --source . ^
  --platform managed ^
  --region us-central1 ^
  --allow-unauthenticated ^
  --set-env-vars "XAI_API_KEY=%API_KEY%"

echo.
echo =========================================
echo   Deployment Complete!
echo =========================================
pause
```

Run: `.\deploy-firebase.bat`

---

## 💰 Pricing

### Google Cloud Run Free Tier (every month):
- 2 million requests
- 360,000 GB-seconds memory
- 180,000 vCPU-seconds compute time

**Estimated cost for your app**: FREE for up to ~1000 resume generations/month

---

## 🔧 Update Environment Variables

### After Deployment:

```powershell
# Update API key
gcloud run services update ai-resume-builder \
  --region us-central1 \
  --update-env-vars "XAI_API_KEY=new_key_here"
```

---

## 📊 Monitoring & Logs

### View Logs:
```powershell
gcloud run services logs read ai-resume-builder --region us-central1
```

### View in Console:
https://console.cloud.google.com/run

---

## 🔗 Custom Domain

### Add Custom Domain:

1. Go to Cloud Run console
2. Select your service
3. Click "Manage Custom Domains"
4. Follow the verification steps
5. Add your domain

---

## 🐛 Troubleshooting

### Build Fails:
- Check Dockerfile syntax
- Ensure requirements.txt is correct
- Check Cloud Build logs in console

### App Not Starting:
- Verify PORT environment variable
- Check logs: `gcloud run services logs read ai-resume-builder`
- Ensure Grok API key is set correctly

### 502 Bad Gateway:
- App taking too long to start
- Increase memory: `--memory 512Mi`
- Check application logs

---

## 🚀 CI/CD with GitHub Actions

The `.github/workflows/deploy-cloud-run.yml` file enables automatic deployment on push to main branch.

### Setup:

1. Create service account:
```powershell
gcloud iam service-accounts create github-actions
```

2. Grant permissions:
```powershell
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
  --member="serviceAccount:github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/run.admin"
```

3. Create key and add to GitHub Secrets:
```powershell
gcloud iam service-accounts keys create key.json \
  --iam-account github-actions@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

4. Add secrets to GitHub:
   - `GCP_PROJECT_ID`: Your project ID
   - `GCP_SA_KEY`: Contents of key.json
   - `XAI_API_KEY`: Your Grok API key

---

## 📞 Support

- Cloud Run Docs: https://cloud.google.com/run/docs
- Firebase Docs: https://firebase.google.com/docs
- Community: https://stackoverflow.com/questions/tagged/google-cloud-run

---

**Your app will be deployed at**: `https://ai-resume-builder-xxxxx-uc.a.run.app`

# 🚀 Deployment Instructions - Follow These Steps!

## ✅ STEP 1: Create GitHub Repository (DO THIS NOW!)

### Option A: Using GitHub Website (RECOMMENDED)
1. **Click this link**: https://github.com/new
2. **Fill in the details**:
   - Repository name: `ai-resume-builder`
   - Description: `AI-powered resume, cover letter, and portfolio builder using Flask and OpenAI`
   - **IMPORTANT**: Keep it **PUBLIC** (so Railway can access it)
   - **DO NOT** check "Add a README file"
   - **DO NOT** add .gitignore or license (we already have them)
3. Click **"Create repository"**

### What It Should Look Like:
```
Repository name: ai-resume-builder
Description: AI-powered resume, cover letter, and portfolio builder
Public: ✓ (selected)
Add a README file: ☐ (unchecked)
Add .gitignore: None
Choose a license: None
```

---

## ✅ STEP 2: Push to GitHub (AUTOMATED)

After creating the repository on GitHub, run these commands:

```powershell
git remote add origin https://github.com/Nikhil1081/ai-resume-builder.git
git push -u origin main
```

**If prompted for credentials**:
- Use your GitHub username
- For password, use a **Personal Access Token** (not your GitHub password)
- Get token here: https://github.com/settings/tokens

---

## ✅ STEP 3: Deploy to Railway (5 MINUTES)

### A. Sign Up & Connect GitHub

1. **Go to Railway**: https://railway.app
2. Click **"Login"** or **"Start a New Project"**
3. Sign in with your **GitHub account**
4. Authorize Railway to access your GitHub repositories

### B. Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose **"Nikhil1081/ai-resume-builder"**
4. Railway will automatically detect the configuration!

### C. Add Environment Variables

1. In Railway dashboard, click on your project
2. Go to **"Variables"** tab
3. Click **"New Variable"**
4. Add:
   ```
   Key: OPENAI_API_KEY
   Value: [Your actual OpenAI API key]
   ```
5. Click **"Add"**

### D. Deploy!

1. Railway automatically deploys after you add variables
2. Wait 2-3 minutes for build to complete
3. Click **"Settings"** → **"Generate Domain"**
4. You'll get a URL like: `https://ai-resume-builder-production.up.railway.app`

---

## 🎉 VERIFICATION

### Check GitHub:
✓ Visit: https://github.com/Nikhil1081/ai-resume-builder
✓ Should see all your files

### Check Railway:
✓ Status shows "Active" or "Running"
✓ Build logs show no errors
✓ Click on the generated domain to open your app

---

## 🔑 Getting Your OpenAI API Key

1. Go to: https://platform.openai.com/api-keys
2. Sign up or login
3. Click **"Create new secret key"**
4. Name it: "AI Resume Builder"
5. Copy the key (starts with `sk-...`)
6. Add it to Railway variables (Step 3C above)

---

## 💡 TROUBLESHOOTING

### "Authentication failed" when pushing to GitHub
**Solution**: Use Personal Access Token
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Check "repo" scope
4. Copy token and use as password

### Railway build fails
**Solution**:
- Check Railway logs for errors
- Ensure OPENAI_API_KEY is added
- Make sure repository is public

### App doesn't load
**Solution**:
- Wait 2-3 minutes after deployment
- Check Railway logs
- Ensure runtime.txt has correct Python version
- Verify Procfile exists

---

## 📊 EXPECTED COSTS

### Free Tier:
- GitHub: FREE (public repos)
- Railway: $5/month after free trial ($5 credit initially)
- OpenAI: $5 free credit for new accounts

### Per Usage:
- Each resume generation: ~$0.01
- 500 resumes: ~$5-10

---

## 🎯 NEXT STEPS AFTER DEPLOYMENT

1. **Test your live app** on the Railway URL
2. **Share the link** with friends for feedback
3. **Monitor OpenAI usage** on platform.openai.com
4. **Update your code**: 
   - Make changes locally
   - `git add .`
   - `git commit -m "Your changes"`
   - `git push`
   - Railway auto-deploys!

---

## 🆘 NEED HELP?

- **GitHub Issues**: https://github.com/Nikhil1081/ai-resume-builder/issues
- **Railway Discord**: https://discord.gg/railway
- **Railway Docs**: https://docs.railway.app

---

**Your repository URL**: https://github.com/Nikhil1081/ai-resume-builder
**Railway Dashboard**: https://railway.app/dashboard

Good luck! 🚀

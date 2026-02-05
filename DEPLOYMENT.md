# AI Resume & Portfolio Builder - Deployment Guide

## 🚀 Quick Start Deployment on Railway

### Step 1: Prepare Your Code

1. Ensure all files are in your project directory
2. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_actual_key_here
   ```

### Step 2: Initialize Git Repository

```bash
cd "c:\Users\Nikhil\OneDrive\Documents\IBM PROJECT"
git init
git add .
git commit -m "Initial commit: AI Resume & Portfolio Builder"
```

### Step 3: Push to GitHub

```bash
# Add your GitHub repository
git remote add origin https://github.com/Nikhil1081/ai-resume-builder.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 4: Deploy on Railway

#### Option A: Using Railway Dashboard (Recommended)

1. Go to [railway.app](https://railway.app)
2. Sign up/Login with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose `Nikhil1081/ai-resume-builder`
6. Railway will auto-detect the configuration

#### Option B: Using Railway CLI

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Link to your project (if already created)
railway link

# Deploy
railway up
```

### Step 5: Configure Environment Variables

In Railway Dashboard:
1. Go to your project
2. Click on **"Variables"** tab
3. Add the following:
   - Key: `OPENAI_API_KEY`
   - Value: Your OpenAI API key

### Step 6: Access Your App

Railway will provide a URL like:
```
https://your-app-name.up.railway.app
```

## 🔧 Configuration Details

### railway.toml
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "gunicorn app:app"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

### Procfile
```
web: gunicorn app:app
```

### Runtime
- Python 3.11.0

## 📊 Monitoring

### View Logs
```bash
railway logs
```

### Check Status
```bash
railway status
```

## 🐛 Troubleshooting

### Issue: App doesn't start

**Solution**:
- Check logs: `railway logs`
- Ensure `OPENAI_API_KEY` is set
- Verify all dependencies in `requirements.txt`

### Issue: PDF generation fails

**Solution**:
- Railway free tier has memory limits
- Consider upgrading to hobby plan
- Check ReportLab installation

### Issue: OpenAI API errors

**Solution**:
- Verify API key is valid
- Check OpenAI account has credits
- Ensure API key has correct permissions

## 💰 Cost Considerations

### Railway Pricing
- **Starter Plan**: $5/month
  - 500 hours execution
  - 512MB RAM
  - 1GB storage

### OpenAI Pricing
- GPT-3.5-turbo: $0.50 / 1M input tokens
- Average resume: ~$0.01-0.02 per generation

## 🔒 Security Best Practices

1. **Never commit `.env` file**
2. **Rotate API keys regularly**
3. **Use environment variables for secrets**
4. **Enable CORS only for your domain**
5. **Add rate limiting for production**

## 📈 Scaling

### For High Traffic

1. **Upgrade Railway Plan**
2. **Add Redis caching**
3. **Implement request queuing**
4. **Use CDN for static files**

### Code Optimization

```python
# Add caching
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/generate-resume', methods=['POST'])
@cache.cached(timeout=300)
def generate_resume():
    # ... existing code
```

## 🌐 Custom Domain

1. Go to Railway project settings
2. Click **"Domains"**
3. Add your custom domain
4. Update DNS records as shown

## 🔄 Continuous Deployment

Railway automatically deploys when you push to GitHub:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push origin main

# Railway auto-deploys!
```

## 📚 Additional Resources

- [Railway Docs](https://docs.railway.app)
- [Flask Deployment](https://flask.palletsprojects.com/en/latest/deploying/)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/stable/configure.html)

## 🆘 Support

If you encounter issues:
1. Check Railway logs
2. Review OpenAI API status
3. Create an issue on GitHub
4. Contact Railway support

---

**Happy Deploying! 🚀**

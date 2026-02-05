# Quick Start Guide 🚀

## For Complete Beginners

### What You'll Build
A web application that uses AI to create professional resumes, cover letters, and portfolios automatically!

## Prerequisites

Before starting, make sure you have:
1. **Python 3.11+** installed ([Download here](https://www.python.org/downloads/))
2. **Git** installed ([Download here](https://git-scm.com/downloads))
3. **OpenAI API Key** ([Get one here](https://platform.openai.com/api-keys))
4. **Text editor** (VS Code recommended)

## Step-by-Step Setup

### 1️⃣ Check Your Setup

Open terminal/command prompt and verify:

```bash
python --version    # Should show Python 3.11 or higher
git --version      # Should show git version
```

### 2️⃣ Navigate to Project Folder

```bash
cd "c:\Users\Nikhil\OneDrive\Documents\IBM PROJECT"
```

### 3️⃣ Run Setup Script

**Windows:**
```bash
setup.bat
```

**Mac/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

### 4️⃣ Configure Environment

1. Open the `.env` file in your text editor
2. Replace `your_openai_api_key_here` with your actual API key
3. Save the file

Example:
```
OPENAI_API_KEY=sk-proj-abc123xyz...
PORT=5000
```

### 5️⃣ Start the Application

```bash
# Activate virtual environment first
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Run the app
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
```

### 6️⃣ Open in Browser

Visit: `http://localhost:5000`

## Using the Application

### Create Your First Resume

1. **Click "Resume Builder" tab**
2. **Fill in your information:**
   - Name: Your full name
   - Email: Your email address
   - Phone: Your phone number
   - Target Role: Job you're applying for
   - Skills: Python, JavaScript, React (comma-separated)
   - Education: Your degree and university
   - Experience: Your work experience
   - Projects: Your notable projects

3. **Click "Generate AI Resume"**
4. **Wait a few seconds** for AI to create your resume
5. **Download PDF** when ready!

### Generate Cover Letter

1. **Switch to "Cover Letter" tab**
2. **Enter:**
   - Your name
   - Target role
   - Company name
   - Your skills
   - Brief experience
3. **Click "Generate Cover Letter"**
4. **Copy to clipboard** and use!

### Build Portfolio

1. **Go to "Portfolio" tab**
2. **Fill in your details**
3. **Add projects in JSON format:**
   ```json
   [
     {
       "title": "My Project",
       "description": "What it does",
       "image": "https://via.placeholder.com/400x300",
       "link": "https://github.com/yourusername/project",
       "tech": ["Python", "Flask"]
     }
   ]
   ```
4. **Click "Generate Portfolio Page"**
5. **Download HTML** file

## Deploying to Railway

### Quick Deploy (5 minutes)

1. **Initialize Git** (if not done):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Create GitHub Repository**:
   - Go to [github.com/new](https://github.com/new)
   - Name: `ai-resume-builder`
   - Click "Create repository"

3. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/Nikhil1081/ai-resume-builder.git
   git branch -M main
   git push -u origin main
   ```

4. **Deploy on Railway**:
   - Visit [railway.app](https://railway.app)
   - Sign in with GitHub
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `Nikhil1081/ai-resume-builder`
   - Add environment variable:
     - Key: `OPENAI_API_KEY`
     - Value: Your OpenAI API key
   - Click Deploy!

5. **Access Your App**:
   Railway will give you a URL like:
   `https://your-app.up.railway.app`

## Troubleshooting

### "Python not found"
- Install Python from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add to PATH" during installation

### "pip not recognized"
```bash
python -m pip install --upgrade pip
```

### "Module not found"
```bash
pip install -r requirements.txt
```

### "OpenAI API Error"
- Check your API key is correct in `.env`
- Verify your OpenAI account has credits
- Check [status.openai.com](https://status.openai.com)

### Port 5000 already in use
Edit `.env` file:
```
PORT=8000
```

Then run:
```bash
python app.py
```

## Next Steps

- ✅ Customize the UI colors in `static/css/style.css`
- ✅ Add more resume templates
- ✅ Integrate with LinkedIn API
- ✅ Add authentication
- ✅ Implement resume parsing
- ✅ Deploy to custom domain

## Getting Help

- 📖 Read [README.md](README.md) for detailed docs
- 🚀 Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment guide
- 🐛 Report issues on [GitHub](https://github.com/Nikhil1081/ai-resume-builder/issues)
- 💬 Ask questions in GitHub Discussions

## Useful Commands

| Command | Description |
|---------|-------------|
| `python app.py` | Start development server |
| `pip install <package>` | Install a Python package |
| `pip freeze > requirements.txt` | Update dependencies |
| `git status` | Check git status |
| `git add .` | Stage all changes |
| `git commit -m "message"` | Commit changes |
| `git push` | Push to GitHub |

## Cost Estimation

### Development (Free)
- Python: Free
- Flask: Free
- GitHub: Free (public repos)

### Production
- Railway: $5/month (Hobby plan)
- OpenAI API: ~$0.01 per resume generation
- Domain (optional): $10-15/year

**Total**: ~$5-6/month for 500 resume generations

## Tips for Success

1. **Start Simple**: Test locally before deploying
2. **Version Control**: Commit regularly to GitHub
3. **Monitor Usage**: Check OpenAI API usage to avoid surprises
4. **Get Feedback**: Share with friends and iterate
5. **Stay Updated**: Watch for library updates

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Railway Docs](https://docs.railway.app/)
- [Git Tutorial](https://git-scm.com/docs/gittutorial)

---

**Questions?** Open an issue on GitHub or check existing documentation!

Happy building! 🎉

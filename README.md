# 🎓 AI Resume & Portfolio Builder

An intelligent web application that helps students create professional resumes, cover letters, and portfolios using AI technology. Built with Python Flask and powered by OpenAI's GPT models.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

- **AI-Powered Resume Generation**: Automatically creates tailored resumes based on your skills, education, and experience
- **Smart Cover Letter Writer**: Generates personalized cover letters for specific companies and roles
- **Portfolio Builder**: Creates beautiful, responsive portfolio websites showcasing your projects
- **PDF Export**: Download your resume as a professional PDF document
- **ATS-Friendly**: Optimized for Applicant Tracking Systems
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices

## 🎯 Problem Statement

Many students struggle to present their skills and projects in an attractive, professional format. Generic resume templates don't highlight individual strengths. This application uses generative AI to automatically create tailored resumes, cover letters, and portfolios, improving job and internship opportunities.

## 🚀 Tech Stack

### Backend
- **Python 3.11**
- **Flask 3.0** - Web framework
- **OpenAI API** - AI-powered content generation
- **ReportLab** - PDF generation
- **Gunicorn** - Production WSGI server

### Frontend
- **HTML5**
- **CSS3** (Modern gradients, flexbox, grid)
- **Vanilla JavaScript** (ES6+)

### Deployment
- **Railway** - Cloud platform
- **GitHub** - Version control

## 📋 Prerequisites

- Python 3.11+
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- Git

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Nikhil1081/ai-resume-builder.git
cd ai-resume-builder
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
PORT=5000
```

### 5. Run the Application

```bash
# Development
python app.py

# Production
gunicorn app:app
```

Visit `http://localhost:5000` in your browser.

## 🌐 Deployment on Railway

### Quick Deploy

1. **Fork this repository** to your GitHub account

2. **Sign up on Railway**: [railway.app](https://railway.app)

3. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your forked repository

4. **Add Environment Variables**:
   - Go to your project settings
   - Add `OPENAI_API_KEY` with your OpenAI API key

5. **Deploy**: Railway will automatically deploy your app!

### Manual Deployment Steps

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Link to project
railway link

# Add environment variables
railway variables set OPENAI_API_KEY=your_key_here

# Deploy
railway up
```

## 📱 Usage Guide

### Resume Builder

1. Navigate to the **Resume Builder** tab
2. Fill in your personal information:
   - Name, email, phone
   - Target job role
   - Skills (comma-separated)
   - Education details
   - Work experience
   - Projects
3. Click **"Generate AI Resume"**
4. Review the AI-generated resume
5. Download as PDF

### Cover Letter Generator

1. Go to the **Cover Letter** tab
2. Enter your details and target company
3. Click **"Generate Cover Letter"**
4. Copy or edit the generated letter

### Portfolio Builder

1. Switch to the **Portfolio** tab
2. Provide your information and projects in JSON format
3. Click **"Generate Portfolio Page"**
4. Download the HTML file

## 📁 Project Structure

```
ai-resume-builder/
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
├── Procfile               # Railway/Heroku config
├── railway.toml           # Railway configuration
├── runtime.txt            # Python version
├── .env.example           # Environment variables template
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Styles
│   └── js/
│       └── app.js        # Frontend JavaScript
```

## 🔑 API Endpoints

### POST `/api/generate-resume`
Generates an AI-powered resume

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "targetRole": "Software Engineer",
  "skills": "Python, JavaScript, React",
  "education": "B.Tech Computer Science",
  "experience": "Intern at Tech Corp",
  "projects": "E-commerce platform, ML classifier"
}
```

### POST `/api/generate-cover-letter`
Creates a personalized cover letter

### POST `/api/download-pdf`
Exports resume as PDF

## 🎨 Customization

### Modify Resume Template

Edit the PDF generation logic in `app.py`:

```python
# Customize styles
title_style = ParagraphStyle(
    'CustomTitle',
    fontSize=24,
    textColor=colors.HexColor('#2c3e50')
)
```

### Change UI Theme

Edit `static/css/style.css`:

```css
/* Update gradient colors */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Known Issues

- PDF generation requires sufficient memory on hosting platform
- OpenAI API requires internet connection and valid API key
- Large file uploads may timeout on free hosting tiers

## 🔮 Future Enhancements

- [ ] Multiple resume templates
- [ ] LinkedIn profile integration
- [ ] Resume parsing and optimization
- [ ] Interview preparation tips
- [ ] Job matching recommendations
- [ ] Multi-language support
- [ ] Email integration
- [ ] Analytics dashboard

## 📧 Contact

**Developer**: Nikhil
**GitHub**: [@Nikhil1081](https://github.com/Nikhil1081)

## 🙏 Acknowledgments

- OpenAI for GPT API
- Flask community
- Railway for hosting
- IBM for project inspiration

---

**⭐ Star this repository if you find it helpful!**

Made with ❤️ for students seeking better career opportunities

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash, session
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
from dotenv import load_dotenv
import requests
import json
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
import json
from models import db, User

load_dotenv()

app = Flask(__name__)
CORS(app)

# App Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Configure Grok API (xAI)
GROK_API_KEY = os.getenv('XAI_API_KEY', 'xai-demo-key')
GROK_API_URL = 'https://api.x.ai/v1/chat/completions'

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/')
@login_required
def index():
    return render_template('index.html', user=current_user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
            return render_template('register.html')
        
        # Create new user
        new_user = User(username=username, email=email, full_name=full_name)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/api/generate-resume', methods=['POST'])
@login_required
def generate_resume():
    try:
        data = request.json
        
        # Extract user data
        name = data.get('name', '')
        email = data.get('email', '')
        phone = data.get('phone', '')
        skills = data.get('skills', '')
        education = data.get('education', '')
        experience = data.get('experience', '')
        projects = data.get('projects', '')
        target_role = data.get('targetRole', '')
        
        # Create prompt for AI
        prompt = f"""Generate a professional, tailored resume content for the following student:

Name: {name}
Email: {email}
Phone: {phone}
Target Role: {target_role}

Skills: {skills}
Education: {education}
Experience: {experience}
Projects: {projects}

Create a compelling, well-structured resume that highlights the most relevant skills and experiences for the {target_role} position. Use professional language and format it with clear sections. Make it ATS-friendly and impactful.

Return the resume in the following JSON format:
{{
    "summary": "Professional summary paragraph",
    "skills": ["skill1", "skill2", "skill3"],
    "experience": [
        {{"title": "Job Title", "company": "Company Name", "duration": "Duration", "description": "What you did"}}
    ],
    "education": [
        {{"degree": "Degree", "institution": "School Name", "year": "Year", "details": "Details"}}
    ],
    "projects": [
        {{"name": "Project Name", "description": "What it does", "technologies": "Tech stack"}}
    ]
}}"""

        # Call Grok API (xAI)
        if GROK_API_KEY and GROK_API_KEY != 'xai-demo-key':
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {GROK_API_KEY}'
            }
            
            payload = {
                'model': 'grok-beta',
                'messages': [
                    {"role": "system", "content": "You are an expert resume writer and career counselor. Create professional, tailored resumes that highlight individual strengths."},
                    {"role": "user", "content": prompt}
                ],
                'temperature': 0.7,
                'max_tokens': 1500
            }
            
            response = requests.post(GROK_API_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                ai_content = response.json()['choices'][0]['message']['content']
                # Extract JSON from response
                start_idx = ai_content.find('{')
                end_idx = ai_content.rfind('}') + 1
                resume_data = json.loads(ai_content[start_idx:end_idx])
            else:
                raise Exception(f"Grok API error: {response.text}")
        else:
            # Fallback if no API key
            resume_data = {
                "summary": f"Motivated student with strong background in {skills}. Seeking {target_role} position to apply technical skills and contribute to innovative projects.",
                "skills": skills.split(','),
                "experience": [{"title": "Parse from experience", "company": "Various", "duration": experience, "description": "Details from input"}],
                "education": [{"degree": education, "institution": "Educational Institution", "year": "Recent", "details": ""}],
                "projects": [{"name": "Student Projects", "description": projects, "technologies": skills}]
            }
        
        return jsonify({
            'success': True,
            'resume': resume_data,
            'personalInfo': {
                'name': name,
                'email': email,
                'phone': phone
            }
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/generate-cover-letter', methods=['POST'])
@login_required
def generate_cover_letter():
    try:
        data = request.json
        
        name = data.get('name', '')
        target_role = data.get('targetRole', '')
        company = data.get('company', '')
        skills = data.get('skills', '')
        experience = data.get('experience', '')
        
        prompt = f"""Write a compelling, professional cover letter for:

Applicant: {name}
Target Role: {target_role}
Company: {company}
Skills: {skills}
Experience: {experience}

Create a personalized cover letter that showcases enthusiasm, relevant skills, and fit for the role. Keep it concise (3-4 paragraphs) and professional."""

        if GROK_API_KEY and GROK_API_KEY != 'xai-demo-key':
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {GROK_API_KEY}'
            }
            
            payload = {
                'model': 'grok-beta',
                'messages': [
                    {"role": "system", "content": "You are an expert career counselor who writes compelling cover letters."},
                    {"role": "user", "content": prompt}
                ],
                'temperature': 0.7,
                'max_tokens': 800
            }
            
            response = requests.post(GROK_API_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                cover_letter = response.json()['choices'][0]['message']['content']
            else:
                raise Exception(f"Grok API error: {response.text}")
        else:
            cover_letter = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {target_role} position at {company}. As a motivated student with skills in {skills}, I am excited about the opportunity to contribute to your team.

{experience}

I am confident that my technical skills, combined with my passion for learning and problem-solving, make me a strong candidate for this position. I look forward to the opportunity to discuss how I can contribute to {company}'s success.

Thank you for your consideration.

Sincerely,
{name}"""
        
        return jsonify({
            'success': True,
            'coverLetter': cover_letter
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/download-pdf', methods=['POST'])
@login_required
def download_pdf():
    try:
        data = request.json
        resume_data = data.get('resumeData', {})
        personal_info = data.get('personalInfo', {})
        
        # Create PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        
        # Container for elements
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=6,
            alignment=1  # Center
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#3498db'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Add name
        elements.append(Paragraph(personal_info.get('name', 'N/A'), title_style))
        
        # Add contact info
        contact = f"{personal_info.get('email', '')} | {personal_info.get('phone', '')}"
        elements.append(Paragraph(contact, styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Add summary
        if resume_data.get('summary'):
            elements.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
            elements.append(Paragraph(resume_data['summary'], styles['Normal']))
            elements.append(Spacer(1, 0.15*inch))
        
        # Add skills
        if resume_data.get('skills'):
            elements.append(Paragraph("SKILLS", heading_style))
            skills_text = " • ".join(resume_data['skills'][:10])
            elements.append(Paragraph(skills_text, styles['Normal']))
            elements.append(Spacer(1, 0.15*inch))
        
        # Add experience
        if resume_data.get('experience'):
            elements.append(Paragraph("EXPERIENCE", heading_style))
            for exp in resume_data['experience'][:3]:
                exp_title = f"<b>{exp.get('title', '')}</b> - {exp.get('company', '')}"
                elements.append(Paragraph(exp_title, styles['Normal']))
                elements.append(Paragraph(exp.get('duration', ''), styles['Normal']))
                elements.append(Paragraph(exp.get('description', ''), styles['Normal']))
                elements.append(Spacer(1, 0.1*inch))
        
        # Add education
        if resume_data.get('education'):
            elements.append(Paragraph("EDUCATION", heading_style))
            for edu in resume_data['education'][:2]:
                edu_text = f"<b>{edu.get('degree', '')}</b> - {edu.get('institution', '')} ({edu.get('year', '')})"
                elements.append(Paragraph(edu_text, styles['Normal']))
                if edu.get('details'):
                    elements.append(Paragraph(edu['details'], styles['Normal']))
                elements.append(Spacer(1, 0.1*inch))
        
        # Add projects
        if resume_data.get('projects'):
            elements.append(Paragraph("PROJECTS", heading_style))
            for proj in resume_data['projects'][:3]:
                proj_title = f"<b>{proj.get('name', '')}</b>"
                elements.append(Paragraph(proj_title, styles['Normal']))
                elements.append(Paragraph(proj.get('description', ''), styles['Normal']))
                elements.append(Paragraph(f"<i>Technologies: {proj.get('technologies', '')}</i>", styles['Normal']))
                elements.append(Spacer(1, 0.1*inch))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        
        return send_file(buffer, as_attachment=True, download_name='resume.pdf', mimetype='application/pdf')
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

import functions_framework
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
from dotenv import load_dotenv
import openai
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
import json

load_dotenv()

app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
CORS(app)

# Configure xAI Grok API (using OpenAI-compatible endpoint)
openai.api_key = os.getenv('XAI_API_KEY')
openai.api_base = "https://api.x.ai/v1"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/generate-resume', methods=['POST'])
def generate_resume():
    try:
        data = request.json
        
        name = data.get('name', '')
        email = data.get('email', '')
        phone = data.get('phone', '')
        skills = data.get('skills', '')
        education = data.get('education', '')
        experience = data.get('experience', '')
        projects = data.get('projects', '')
        target_role = data.get('targetRole', '')
        
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

        if openai.api_key:
            response = openai.chat.completions.create(
                model="grok-beta",
                messages=[
                    {"role": "system", "content": "You are an expert resume writer and career counselor. Create professional, tailored resumes that highlight individual strengths."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            ai_content = response.choices[0].message.content
            start_idx = ai_content.find('{')
            end_idx = ai_content.rfind('}') + 1
            resume_data = json.loads(ai_content[start_idx:end_idx])
        else:
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

        if openai.api_key:
            response = openai.chat.completions.create(
                model="grok-beta",
                messages=[
                    {"role": "system", "content": "You are an expert career counselor who writes compelling cover letters."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            cover_letter = response.choices[0].message.content
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
def download_pdf():
    try:
        data = request.json
        resume_data = data.get('resumeData', {})
        personal_info = data.get('personalInfo', {})
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        
        elements = []
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=6,
            alignment=1
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#3498db'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        elements.append(Paragraph(personal_info.get('name', 'N/A'), title_style))
        
        contact = f"{personal_info.get('email', '')} | {personal_info.get('phone', '')}"
        elements.append(Paragraph(contact, styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        if resume_data.get('summary'):
            elements.append(Paragraph("PROFESSIONAL SUMMARY", heading_style))
            elements.append(Paragraph(resume_data['summary'], styles['Normal']))
            elements.append(Spacer(1, 0.15*inch))
        
        if resume_data.get('skills'):
            elements.append(Paragraph("SKILLS", heading_style))
            skills_text = " • ".join(resume_data['skills'][:10])
            elements.append(Paragraph(skills_text, styles['Normal']))
            elements.append(Spacer(1, 0.15*inch))
        
        if resume_data.get('experience'):
            elements.append(Paragraph("EXPERIENCE", heading_style))
            for exp in resume_data['experience'][:3]:
                exp_title = f"<b>{exp.get('title', '')}</b> - {exp.get('company', '')}"
                elements.append(Paragraph(exp_title, styles['Normal']))
                elements.append(Paragraph(exp.get('duration', ''), styles['Normal']))
                elements.append(Paragraph(exp.get('description', ''), styles['Normal']))
                elements.append(Spacer(1, 0.1*inch))
        
        if resume_data.get('education'):
            elements.append(Paragraph("EDUCATION", heading_style))
            for edu in resume_data['education'][:2]:
                edu_text = f"<b>{edu.get('degree', '')}</b> - {edu.get('institution', '')} ({edu.get('year', '')})"
                elements.append(Paragraph(edu_text, styles['Normal']))
                if edu.get('details'):
                    elements.append(Paragraph(edu['details'], styles['Normal']))
                elements.append(Spacer(1, 0.1*inch))
        
        if resume_data.get('projects'):
            elements.append(Paragraph("PROJECTS", heading_style))
            for proj in resume_data['projects'][:3]:
                proj_title = f"<b>{proj.get('name', '')}</b>"
                elements.append(Paragraph(proj_title, styles['Normal']))
                elements.append(Paragraph(proj.get('description', ''), styles['Normal']))
                elements.append(Paragraph(f"<i>Technologies: {proj.get('technologies', '')}</i>", styles['Normal']))
                elements.append(Spacer(1, 0.1*inch))
        
        doc.build(elements)
        buffer.seek(0)
        
        return send_file(buffer, as_attachment=True, download_name='resume.pdf', mimetype='application/pdf')
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Firebase Functions entry point
@functions_framework.http
def app_handler(request):
    with app.request_context(request.environ):
        return app.full_dispatch_request()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

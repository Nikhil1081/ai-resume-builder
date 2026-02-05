import streamlit as st
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Resume & Portfolio Builder",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem;
        border-radius: 8px;
        font-weight: 600;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        color: #155724;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'users' not in st.session_state:
    st.session_state.users = {}
if 'resume_data' not in st.session_state:
    st.session_state.resume_data = None

# Configure API
GROK_API_KEY = os.getenv('XAI_API_KEY', st.secrets.get('XAI_API_KEY', ''))
GROK_API_URL = 'https://api.x.ai/v1/chat/completions'

def generate_resume_with_ai(name, email, phone, skills, education, experience, projects, target_role):
    """Generate resume using Grok API"""
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

    if GROK_API_KEY and GROK_API_KEY != '':
        try:
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
                start_idx = ai_content.find('{')
                end_idx = ai_content.rfind('}') + 1
                return json.loads(ai_content[start_idx:end_idx])
        except Exception as e:
            st.error(f"AI Generation Error: {str(e)}")
    
    # Fallback
    return {
        "summary": f"Motivated student with strong background in {skills}. Seeking {target_role} position to apply technical skills and contribute to innovative projects.",
        "skills": [s.strip() for s in skills.split(',')],
        "experience": [{"title": "Various Roles", "company": "Experience", "duration": "Recent", "description": experience}],
        "education": [{"degree": education, "institution": "Educational Institution", "year": "Recent", "details": ""}],
        "projects": [{"name": "Projects", "description": projects, "technologies": skills}]
    }

def generate_pdf(resume_data, personal_info):
    """Generate PDF from resume data"""
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
            elements.append(Paragraph(exp.get('description', ''), styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
    
    if resume_data.get('education'):
        elements.append(Paragraph("EDUCATION", heading_style))
        for edu in resume_data['education'][:2]:
            edu_text = f"<b>{edu.get('degree', '')}</b> - {edu.get('institution', '')}"
            elements.append(Paragraph(edu_text, styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
    
    if resume_data.get('projects'):
        elements.append(Paragraph("PROJECTS", heading_style))
        for proj in resume_data['projects'][:3]:
            proj_title = f"<b>{proj.get('name', '')}</b>"
            elements.append(Paragraph(proj_title, styles['Normal']))
            elements.append(Paragraph(proj.get('description', ''), styles['Normal']))
            elements.append(Spacer(1, 0.1*inch))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

def login_page():
    """Login page"""
    st.markdown("<div class='main-header'><h1>🎓 AI Resume Builder</h1><p>Login to Your Account</p></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if username in st.session_state.users and st.session_state.users[username] == password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
        
        st.markdown("---")
        if st.button("Don't have an account? Register here"):
            st.session_state.page = 'register'
            st.rerun()

def register_page():
    """Registration page"""
    st.markdown("<div class='main-header'><h1>🎓 AI Resume Builder</h1><p>Create Your Account</p></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("register_form"):
            full_name = st.text_input("Full Name", placeholder="John Doe")
            username = st.text_input("Username", placeholder="Choose a username")
            email = st.text_input("Email", placeholder="your.email@example.com")
            password = st.text_input("Password", type="password", placeholder="Create a strong password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
            submit = st.form_submit_button("Create Account")
            
            if submit:
                if not all([full_name, username, email, password, confirm_password]):
                    st.error("Please fill in all fields")
                elif password != confirm_password:
                    st.error("Passwords don't match")
                elif username in st.session_state.users:
                    st.error("Username already exists")
                else:
                    st.session_state.users[username] = password
                    st.success("Registration successful! Please login.")
                    st.session_state.page = 'login'
                    st.rerun()
        
        st.markdown("---")
        if st.button("Already have an account? Login here"):
            st.session_state.page = 'login'
            st.rerun()

def main_app():
    """Main application"""
    st.markdown(f"<div class='main-header'><h1>🎓 AI Resume & Portfolio Builder</h1><p>Welcome, {st.session_state.username}!</p></div>", unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.title("Navigation")
        page = st.radio("Choose a tool:", ["Resume Builder", "Cover Letter", "About"])
        
        st.markdown("---")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
    
    if page == "Resume Builder":
        st.header("📝 Resume Builder")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Personal Information")
            name = st.text_input("Full Name*", placeholder="John Doe")
            email = st.text_input("Email*", placeholder="john@example.com")
            phone = st.text_input("Phone*", placeholder="+1 234 567 8900")
            target_role = st.text_input("Target Role*", placeholder="Software Engineer")
            
            st.subheader("Professional Details")
            skills = st.text_area("Skills (comma-separated)*", placeholder="Python, JavaScript, React, Machine Learning")
            education = st.text_area("Education*", placeholder="Bachelor of Technology in Computer Science\nXYZ University, 2024")
            experience = st.text_area("Experience", placeholder="Software Engineering Intern at ABC Corp\nJune 2023 - August 2023")
            projects = st.text_area("Projects*", placeholder="1. E-commerce Platform\n2. ML Image Classifier")
            
            if st.button("✨ Generate AI Resume", type="primary"):
                if all([name, email, phone, target_role, skills, education, projects]):
                    with st.spinner("Generating your professional resume with AI..."):
                        resume_data = generate_resume_with_ai(
                            name, email, phone, skills, education, 
                            experience, projects, target_role
                        )
                        st.session_state.resume_data = {
                            'resume': resume_data,
                            'personal': {'name': name, 'email': email, 'phone': phone}
                        }
                    st.success("✅ Resume generated successfully!")
                else:
                    st.error("Please fill in all required fields (*)")
        
        with col2:
            if st.session_state.resume_data:
                st.subheader("📄 Your AI-Generated Resume")
                
                resume = st.session_state.resume_data['resume']
                personal = st.session_state.resume_data['personal']
                
                st.markdown(f"### {personal['name']}")
                st.markdown(f"📧 {personal['email']} | 📱 {personal['phone']}")
                
                st.markdown("#### Professional Summary")
                st.write(resume.get('summary', ''))
                
                st.markdown("#### Skills")
                st.write(" • ".join(resume.get('skills', [])))
                
                if resume.get('experience'):
                    st.markdown("#### Experience")
                    for exp in resume['experience']:
                        st.markdown(f"**{exp.get('title', '')}** - {exp.get('company', '')}")
                        st.write(exp.get('description', ''))
                
                if resume.get('education'):
                    st.markdown("#### Education")
                    for edu in resume['education']:
                        st.markdown(f"**{edu.get('degree', '')}** - {edu.get('institution', '')}")
                
                if resume.get('projects'):
                    st.markdown("#### Projects")
                    for proj in resume['projects']:
                        st.markdown(f"**{proj.get('name', '')}**")
                        st.write(proj.get('description', ''))
                
                # Download button
                pdf_buffer = generate_pdf(resume, personal)
                st.download_button(
                    label="📥 Download PDF",
                    data=pdf_buffer,
                    file_name=f"resume_{personal['name'].replace(' ', '_')}.pdf",
                    mime="application/pdf"
                )
    
    elif page == "Cover Letter":
        st.header("✉️ Cover Letter Generator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name*", placeholder="John Doe")
            target_role = st.text_input("Target Role*", placeholder="Software Engineer")
            company = st.text_input("Company Name*", placeholder="Google")
            skills = st.text_area("Your Skills*", placeholder="Python, Machine Learning, JavaScript")
            experience = st.text_area("Brief Experience*", placeholder="Describe your relevant experience")
            
            if st.button("✨ Generate Cover Letter", type="primary"):
                if all([name, target_role, company, skills, experience]):
                    with st.spinner("Generating your cover letter..."):
                        # Simple cover letter generation
                        cover_letter = f"""Dear Hiring Manager,

I am writing to express my strong interest in the {target_role} position at {company}. As a motivated professional with skills in {skills}, I am excited about the opportunity to contribute to your team.

{experience}

I am confident that my technical skills, combined with my passion for learning and problem-solving, make me a strong candidate for this position. I look forward to the opportunity to discuss how I can contribute to {company}'s success.

Thank you for your consideration.

Sincerely,
{name}"""
                    
                    with col2:
                        st.subheader("✉️ Your Cover Letter")
                        st.text_area("Cover Letter", cover_letter, height=400)
                        st.download_button(
                            label="📋 Copy to Clipboard",
                            data=cover_letter,
                            file_name="cover_letter.txt",
                            mime="text/plain"
                        )
                else:
                    st.error("Please fill in all required fields (*)")
    
    else:  # About
        st.header("About AI Resume Builder")
        st.markdown("""
        ### 🎓 Your Professional Career Toolkit
        
        This AI-powered platform helps students and professionals create:
        - ✨ **Professional Resumes** tailored to specific roles
        - ✉️ **Compelling Cover Letters** that stand out
        - 📄 **PDF Exports** ready for job applications
        
        ### 🚀 Features:
        - AI-powered content generation using Grok
        - ATS-friendly resume formats
        - Real-time preview and editing
        - One-click PDF download
        
        ### 💡 Deployed with:
        - **Frontend**: Firebase Hosting
        - **Backend**: Streamlit Cloud (Always Active 24/7)
        - **Open Source**: GitHub
        
        Built with ❤️ for students and job seekers everywhere!
        """)

# Main app flow
if 'page' not in st.session_state:
    st.session_state.page = 'login'

if not st.session_state.logged_in:
    if st.session_state.page == 'register':
        register_page()
    else:
        login_page()
else:
    main_app()

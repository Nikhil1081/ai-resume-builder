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
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
import hashlib

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

# Persistent storage functions
USERS_FILE = 'users_data.json'

def hash_password(password):
    """Hash password for security"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load users from JSON file"""
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading users: {str(e)}")
    return {}

def save_users(users):
    """Save users to JSON file"""
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=4)
        return True
    except Exception as e:
        st.error(f"Error saving users: {str(e)}")
        return False

# Load existing users on startup
if not st.session_state.users:
    st.session_state.users = load_users()

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
    """Generate enhanced professional PDF from resume data"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, 
        pagesize=letter, 
        rightMargin=50, 
        leftMargin=50,
        topMargin=50, 
        bottomMargin=40
    )
    
    elements = []
    styles = getSampleStyleSheet()
    
    # Enhanced styles with modern colors and fonts
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#1a237e'),  # Deep blue
        spaceAfter=4,
        alignment=1,
        fontName='Helvetica-Bold',
        leading=32
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#424242'),  # Dark gray
        spaceAfter=16,
        alignment=1,
        fontName='Helvetica'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#1976d2'),  # Blue
        spaceAfter=8,
        spaceBefore=16,
        fontName='Helvetica-Bold',
        borderWidth=0,
        borderPadding=0,
        leftIndent=0,
        borderColor=colors.HexColor('#1976d2'),
        borderRadius=None
    )
    
    content_style = ParagraphStyle(
        'CustomContent',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#212121'),
        spaceAfter=6,
        leading=14,
        fontName='Helvetica'
    )
    
    bold_content_style = ParagraphStyle(
        'BoldContent',
        parent=content_style,
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=colors.HexColor('#424242')
    )
    
    # Header Section with blue background bar
    header_data = [[Paragraph(personal_info.get('name', 'N/A').upper(), title_style)]]
    header_table = Table(header_data, colWidths=[500])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#e3f2fd')),  # Light blue background
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 20),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    elements.append(header_table)
    
    # Contact Information
    contact = f"📧 {personal_info.get('email', '')}  |  📱 {personal_info.get('phone', '')}"
    elements.append(Paragraph(contact, subtitle_style))
    elements.append(Spacer(1, 0.15*inch))
    
    # Professional Summary with accent
    if resume_data.get('summary'):
        section_header = Paragraph("═══ PROFESSIONAL SUMMARY ═══", heading_style)
        elements.append(section_header)
        
        summary_data = [[Paragraph(resume_data['summary'], content_style)]]
        summary_table = Table(summary_data, colWidths=[500])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f5f5f5')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#1976d2')),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.2*inch))
    
    # Skills Section with visual styling
    if resume_data.get('skills'):
        elements.append(Paragraph("═══ TECHNICAL SKILLS ═══", heading_style))
        
        skills_list = resume_data['skills'][:12]  # Top 12 skills
        if skills_list:
            # Create skill badges effect
            skills_rows = []
            row = []
            for i, skill in enumerate(skills_list):
                row.append(Paragraph(f"▪ {skill}", content_style))
                if (i + 1) % 3 == 0:
                    skills_rows.append(row)
                    row = []
            if row:
                skills_rows.append(row)
            
            skills_table = Table(skills_rows, colWidths=[166, 166, 166])
            skills_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            elements.append(skills_table)
        elements.append(Spacer(1, 0.2*inch))
    
    # Experience Section
    if resume_data.get('experience'):
        elements.append(Paragraph("═══ PROFESSIONAL EXPERIENCE ═══", heading_style))
        for exp in resume_data['experience'][:3]:
            exp_title = f"<b>{exp.get('title', '')}</b> | {exp.get('company', '')}"
            elements.append(Paragraph(exp_title, bold_content_style))
            
            if exp.get('duration'):
                elements.append(Paragraph(f"<i>{exp.get('duration', '')}</i>", content_style))
            
            elements.append(Paragraph(exp.get('description', ''), content_style))
            elements.append(Spacer(1, 0.12*inch))
        elements.append(Spacer(1, 0.1*inch))
    
    # Education Section
    if resume_data.get('education'):
        elements.append(Paragraph("═══ EDUCATION ═══", heading_style))
        for edu in resume_data['education'][:2]:
            edu_title = f"<b>{edu.get('degree', '')}</b>"
            elements.append(Paragraph(edu_title, bold_content_style))
            
            edu_info = f"{edu.get('institution', '')} | {edu.get('year', '')}"
            elements.append(Paragraph(edu_info, content_style))
            
            if edu.get('details'):
                elements.append(Paragraph(edu.get('details', ''), content_style))
            
            elements.append(Spacer(1, 0.12*inch))
        elements.append(Spacer(1, 0.1*inch))
    
    # Projects Section
    if resume_data.get('projects'):
        elements.append(Paragraph("═══ KEY PROJECTS ═══", heading_style))
        for proj in resume_data['projects'][:3]:
            proj_title = f"<b>{proj.get('name', '')}</b>"
            elements.append(Paragraph(proj_title, bold_content_style))
            
            elements.append(Paragraph(proj.get('description', ''), content_style))
            
            if proj.get('technologies'):
                tech_text = f"<i>Technologies: {proj.get('technologies', '')}</i>"
                elements.append(Paragraph(tech_text, content_style))
            
            elements.append(Spacer(1, 0.12*inch))
    
    # Footer
    elements.append(Spacer(1, 0.3*inch))
    footer_text = f"Generated on {datetime.now().strftime('%B %d, %Y')} | AI Resume Builder"
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#757575'),
        alignment=1
    )
    elements.append(Paragraph(footer_text, footer_style))
    
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
                hashed_pwd = hash_password(password)
                users = load_users()
                if username in users and users[username].get('password') == hashed_pwd:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.users = users
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
                users = load_users()
                if not all([full_name, username, email, password, confirm_password]):
                    st.error("Please fill in all fields")
                elif password != confirm_password:
                    st.error("Passwords don't match")
                elif len(password) < 6:
                    st.error("Password must be at least 6 characters")
                elif username in users:
                    st.error("Username already exists")
                else:
                    users[username] = {
                        'password': hash_password(password),
                        'full_name': full_name,
                        'email': email,
                        'created_at': datetime.now().isoformat()
                    }
                    if save_users(users):
                        st.session_state.users = users
                        st.success("Registration successful! Please login.")
                        st.session_state.page = 'login'
                        st.rerun()
                    else:
                        st.error("Registration failed. Please try again.")
        
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

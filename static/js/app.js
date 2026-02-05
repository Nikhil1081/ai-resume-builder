// Tab Navigation
function showTab(tabName) {
    // Hide all tabs
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));

    // Remove active class from all buttons
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(btn => btn.classList.remove('active'));

    // Show selected tab
    const selectedTab = document.getElementById(`${tabName}-tab`);
    if (selectedTab) {
        selectedTab.classList.add('active');
    }

    // Mark button as active
    event.target.classList.add('active');
}

// Resume Form Submission
document.getElementById('resume-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        targetRole: document.getElementById('target-role').value,
        skills: document.getElementById('skills').value,
        education: document.getElementById('education').value,
        experience: document.getElementById('experience').value,
        projects: document.getElementById('projects').value
    };

    showLoading(true);

    try {
        const response = await fetch('/api/generate-resume', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (data.success) {
            displayResume(data.resume, data.personalInfo);
            document.getElementById('resume-preview').style.display = 'block';
            document.getElementById('resume-preview').scrollIntoView({ behavior: 'smooth' });
        } else {
            alert('Error generating resume: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        showLoading(false);
    }
});

// Cover Letter Form Submission
document.getElementById('cover-letter-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        name: document.getElementById('cl-name').value,
        targetRole: document.getElementById('cl-role').value,
        company: document.getElementById('company').value,
        skills: document.getElementById('cl-skills').value,
        experience: document.getElementById('cl-experience').value
    };

    showLoading(true);

    try {
        const response = await fetch('/api/generate-cover-letter', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const data = await response.json();

        if (data.success) {
            document.getElementById('cover-letter-content').textContent = data.coverLetter;
            document.getElementById('cover-letter-preview').style.display = 'block';
            document.getElementById('cover-letter-preview').scrollIntoView({ behavior: 'smooth' });
        } else {
            alert('Error generating cover letter: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        showLoading(false);
    }
});

// Display Resume
function displayResume(resume, personalInfo) {
    let html = `
        <div class="resume-header">
            <h2 class="resume-name">${personalInfo.name}</h2>
            <p class="resume-contact">${personalInfo.email} | ${personalInfo.phone}</p>
        </div>
    `;

    // Summary
    if (resume.summary) {
        html += `
            <div class="resume-section">
                <h3>Professional Summary</h3>
                <p>${resume.summary}</p>
            </div>
        `;
    }

    // Skills
    if (resume.skills && resume.skills.length > 0) {
        html += `
            <div class="resume-section">
                <h3>Skills</h3>
                <div class="skills-list">
                    ${resume.skills.map(skill => `<span class="skill-tag">${skill.trim()}</span>`).join('')}
                </div>
            </div>
        `;
    }

    // Experience
    if (resume.experience && resume.experience.length > 0) {
        html += `
            <div class="resume-section">
                <h3>Experience</h3>
                ${resume.experience.map(exp => `
                    <div class="experience-item">
                        <div class="item-title">${exp.title} - ${exp.company}</div>
                        <div class="item-subtitle">${exp.duration}</div>
                        <div class="item-description">${exp.description}</div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    // Education
    if (resume.education && resume.education.length > 0) {
        html += `
            <div class="resume-section">
                <h3>Education</h3>
                ${resume.education.map(edu => `
                    <div class="education-item">
                        <div class="item-title">${edu.degree}</div>
                        <div class="item-subtitle">${edu.institution} - ${edu.year}</div>
                        ${edu.details ? `<div class="item-description">${edu.details}</div>` : ''}
                    </div>
                `).join('')}
            </div>
        `;
    }

    // Projects
    if (resume.projects && resume.projects.length > 0) {
        html += `
            <div class="resume-section">
                <h3>Projects</h3>
                ${resume.projects.map(proj => `
                    <div class="project-item">
                        <div class="item-title">${proj.name}</div>
                        <div class="item-description">${proj.description}</div>
                        <div class="item-subtitle">Technologies: ${proj.technologies}</div>
                    </div>
                `).join('')}
            </div>
        `;
    }

    document.getElementById('resume-content').innerHTML = html;
    
    // Store resume data for PDF download
    window.currentResume = { resumeData: resume, personalInfo: personalInfo };
}

// Download PDF
async function downloadPDF() {
    if (!window.currentResume) {
        alert('Please generate a resume first');
        return;
    }

    showLoading(true);

    try {
        const response = await fetch('/api/download-pdf', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(window.currentResume)
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'resume.pdf';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } else {
            alert('Error downloading PDF');
        }
    } catch (error) {
        alert('Error: ' + error.message);
    } finally {
        showLoading(false);
    }
}

// Copy Cover Letter
function copyCoverLetter() {
    const text = document.getElementById('cover-letter-content').textContent;
    navigator.clipboard.writeText(text).then(() => {
        alert('Cover letter copied to clipboard!');
    }).catch(err => {
        alert('Failed to copy: ' + err);
    });
}

// Generate Portfolio
function generatePortfolio() {
    const name = document.getElementById('portfolio-name').value;
    const bio = document.getElementById('portfolio-bio').value;
    const skills = document.getElementById('portfolio-skills').value;
    const projectsText = document.getElementById('portfolio-projects').value;

    if (!name || !bio || !skills || !projectsText) {
        alert('Please fill in all fields');
        return;
    }

    let projects;
    try {
        projects = JSON.parse(projectsText);
    } catch (e) {
        alert('Invalid JSON format for projects');
        return;
    }

    const portfolioHTML = generatePortfolioHTML(name, bio, skills, projects);
    
    const iframe = document.getElementById('portfolio-frame');
    iframe.srcdoc = portfolioHTML;
    
    document.getElementById('portfolio-preview').style.display = 'block';
    document.getElementById('portfolio-preview').scrollIntoView({ behavior: 'smooth' });
    
    window.currentPortfolio = portfolioHTML;
}

// Generate Portfolio HTML
function generatePortfolioHTML(name, bio, skills, projects) {
    return `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${name} - Portfolio</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
        }
        .hero {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 100px 20px;
            text-align: center;
        }
        .hero h1 { font-size: 3rem; margin-bottom: 20px; }
        .hero p { font-size: 1.2rem; max-width: 800px; margin: 0 auto; }
        .container { max-width: 1200px; margin: 0 auto; padding: 60px 20px; }
        .section-title {
            font-size: 2rem;
            color: #667eea;
            margin-bottom: 40px;
            text-align: center;
        }
        .skills {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            justify-content: center;
            margin-bottom: 60px;
        }
        .skill {
            background: #667eea;
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            font-size: 1rem;
        }
        .projects {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }
        .project-card {
            background: white;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: transform 0.3s ease;
        }
        .project-card:hover { transform: translateY(-5px); }
        .project-card img {
            width: 100%;
            height: 200px;
            object-fit: cover;
        }
        .project-content { padding: 20px; }
        .project-title {
            font-size: 1.4rem;
            color: #667eea;
            margin-bottom: 10px;
        }
        .project-description {
            color: #666;
            margin-bottom: 15px;
        }
        .project-tech {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 15px;
        }
        .tech-tag {
            background: #f0f0f0;
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.85rem;
            color: #555;
        }
        .project-link {
            display: inline-block;
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }
        .project-link:hover { text-decoration: underline; }
        footer {
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 30px;
        }
    </style>
</head>
<body>
    <div class="hero">
        <h1>${name}</h1>
        <p>${bio}</p>
    </div>

    <div class="container">
        <h2 class="section-title">Skills</h2>
        <div class="skills">
            ${skills.split(',').map(skill => `<div class="skill">${skill.trim()}</div>`).join('')}
        </div>

        <h2 class="section-title">Projects</h2>
        <div class="projects">
            ${projects.map(proj => `
                <div class="project-card">
                    <img src="${proj.image}" alt="${proj.title}">
                    <div class="project-content">
                        <h3 class="project-title">${proj.title}</h3>
                        <p class="project-description">${proj.description}</p>
                        <div class="project-tech">
                            ${proj.tech.map(t => `<span class="tech-tag">${t}</span>`).join('')}
                        </div>
                        <a href="${proj.link}" class="project-link" target="_blank">View Project →</a>
                    </div>
                </div>
            `).join('')}
        </div>
    </div>

    <footer>
        <p>&copy; 2026 ${name}. All rights reserved.</p>
    </footer>
</body>
</html>
    `;
}

// Download Portfolio
function downloadPortfolio() {
    if (!window.currentPortfolio) {
        alert('Please generate a portfolio first');
        return;
    }

    const blob = new Blob([window.currentPortfolio], { type: 'text/html' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'portfolio.html';
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);
}

// Loading Overlay
function showLoading(show) {
    document.getElementById('loading-overlay').style.display = show ? 'flex' : 'none';
}

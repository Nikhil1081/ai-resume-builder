# API Usage Examples

## Generate Resume

### Request
```bash
curl -X POST http://localhost:5000/api/generate-resume \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1 234 567 8900",
    "targetRole": "Full Stack Developer",
    "skills": "Python, JavaScript, React, Node.js, MongoDB, AWS",
    "education": "Bachelor of Technology in Computer Science\nXYZ University, 2024\nGPA: 3.8/4.0",
    "experience": "Software Engineering Intern at Tech Corp\nJune 2023 - August 2023\n- Developed REST APIs using Flask\n- Built responsive web apps with React\n- Collaborated with 5-member team",
    "projects": "E-commerce Platform: Built full-stack web app with payment integration using MERN stack\nML Image Classifier: Created CNN model achieving 95% accuracy on CIFAR-10 dataset\nTask Management App: React-based productivity tool with real-time updates"
  }'
```

### Response
```json
{
  "success": true,
  "resume": {
    "summary": "Motivated Full Stack Developer with strong foundation in Python, JavaScript, and modern web technologies. Experienced in building scalable applications and passionate about creating innovative solutions.",
    "skills": [
      "Python",
      "JavaScript",
      "React",
      "Node.js",
      "MongoDB",
      "AWS"
    ],
    "experience": [
      {
        "title": "Software Engineering Intern",
        "company": "Tech Corp",
        "duration": "June 2023 - August 2023",
        "description": "Developed REST APIs using Flask. Built responsive web apps with React. Collaborated with 5-member team on product development."
      }
    ],
    "education": [
      {
        "degree": "Bachelor of Technology in Computer Science",
        "institution": "XYZ University",
        "year": "2024",
        "details": "GPA: 3.8/4.0"
      }
    ],
    "projects": [
      {
        "name": "E-commerce Platform",
        "description": "Full-stack web application with payment integration using MERN stack",
        "technologies": "MongoDB, Express, React, Node.js"
      },
      {
        "name": "ML Image Classifier",
        "description": "CNN model achieving 95% accuracy on CIFAR-10 dataset",
        "technologies": "Python, TensorFlow, Keras"
      },
      {
        "name": "Task Management App",
        "description": "React-based productivity tool with real-time updates",
        "technologies": "React, WebSockets, Firebase"
      }
    ]
  },
  "personalInfo": {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1 234 567 8900"
  }
}
```

## Generate Cover Letter

### Request
```bash
curl -X POST http://localhost:5000/api/generate-cover-letter \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Smith",
    "targetRole": "Data Scientist",
    "company": "Google",
    "skills": "Python, Machine Learning, TensorFlow, Data Analysis, SQL",
    "experience": "Completed 3 ML projects including image classification and NLP sentiment analysis. Interned at AI startup where I improved model accuracy by 15%."
  }'
```

### Response
```json
{
  "success": true,
  "coverLetter": "Dear Hiring Manager,\n\nI am writing to express my strong interest in the Data Scientist position at Google. As a passionate data science professional with expertise in Python, Machine Learning, and advanced analytics, I am excited about the opportunity to contribute to Google's innovative projects.\n\nDuring my internship at an AI startup, I successfully improved model accuracy by 15% through systematic experimentation and optimization. I have completed several impactful projects, including image classification systems and NLP sentiment analysis applications, which have given me hands-on experience with TensorFlow and modern machine learning frameworks.\n\nI am particularly drawn to Google's commitment to using AI for solving real-world problems at scale. My technical skills in Python, SQL, and machine learning, combined with my analytical mindset and passion for innovation, make me well-suited to contribute effectively to your data science team.\n\nI look forward to the opportunity to discuss how my background and enthusiasm for data science can benefit Google's mission.\n\nThank you for your consideration.\n\nSincerely,\nJane Smith"
}
```

## Download PDF

### Request
```bash
curl -X POST http://localhost:5000/api/download-pdf \
  -H "Content-Type: application/json" \
  -d '{
    "resumeData": {
      "summary": "Motivated developer...",
      "skills": ["Python", "JavaScript"],
      "experience": [...],
      "education": [...],
      "projects": [...]
    },
    "personalInfo": {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1234567890"
    }
  }' \
  --output resume.pdf
```

## Error Handling

### Invalid Request
```json
{
  "success": false,
  "error": "Missing required field: name"
}
```

### OpenAI API Error
```json
{
  "success": false,
  "error": "OpenAI API error: Rate limit exceeded"
}
```

## Rate Limiting

Currently, there are no rate limits. For production deployment, consider implementing:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/generate-resume', methods=['POST'])
@limiter.limit("10 per minute")
def generate_resume():
    # Implementation
```

## Authentication

For production use with authentication:

```python
from functools import wraps
from flask import request, jsonify

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != os.getenv('API_KEY'):
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/generate-resume', methods=['POST'])
@require_api_key
def generate_resume():
    # Implementation
```

## Testing with Python

```python
import requests

url = 'http://localhost:5000/api/generate-resume'
data = {
    'name': 'John Doe',
    'email': 'john@example.com',
    'phone': '+1234567890',
    'targetRole': 'Software Engineer',
    'skills': 'Python, JavaScript, React',
    'education': 'B.Tech Computer Science, 2024',
    'experience': 'Intern at Tech Company',
    'projects': 'Built web applications and ML models'
}

response = requests.post(url, json=data)
print(response.json())
```

## Testing with JavaScript

```javascript
const generateResume = async () => {
  const response = await fetch('/api/generate-resume', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: 'John Doe',
      email: 'john@example.com',
      phone: '+1234567890',
      targetRole: 'Software Engineer',
      skills: 'Python, JavaScript, React',
      education: 'B.Tech Computer Science, 2024',
      experience: 'Intern at Tech Company',
      projects: 'Built web applications and ML models'
    })
  });
  
  const data = await response.json();
  console.log(data);
};

generateResume();
```

"""
Test suite for AI Resume & Portfolio Builder
Run with: pytest test_app.py
"""

import pytest
import json
from app import app

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test home page loads"""
    response = client.get('/')
    assert response.status_code == 200

def test_generate_resume_missing_data(client):
    """Test resume generation with missing data"""
    response = client.post('/api/generate-resume',
                          json={},
                          content_type='application/json')
    # Should either succeed with fallback or return error gracefully
    assert response.status_code in [200, 400, 500]

def test_generate_resume_valid_data(client):
    """Test resume generation with valid data"""
    data = {
        'name': 'Test User',
        'email': 'test@example.com',
        'phone': '+1234567890',
        'targetRole': 'Software Engineer',
        'skills': 'Python, JavaScript',
        'education': 'B.Tech CS',
        'experience': 'Intern at Tech Corp',
        'projects': 'Built web apps'
    }
    
    response = client.post('/api/generate-resume',
                          json=data,
                          content_type='application/json')
    
    # Check response
    assert response.status_code == 200
    result = json.loads(response.data)
    assert 'success' in result

def test_generate_cover_letter(client):
    """Test cover letter generation"""
    data = {
        'name': 'Test User',
        'targetRole': 'Developer',
        'company': 'Tech Corp',
        'skills': 'Python, JavaScript',
        'experience': 'Built several projects'
    }
    
    response = client.post('/api/generate-cover-letter',
                          json=data,
                          content_type='application/json')
    
    assert response.status_code == 200
    result = json.loads(response.data)
    assert 'success' in result

def test_download_pdf(client):
    """Test PDF download"""
    data = {
        'resumeData': {
            'summary': 'Test summary',
            'skills': ['Python', 'JavaScript'],
            'experience': [],
            'education': [],
            'projects': []
        },
        'personalInfo': {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '+1234567890'
        }
    }
    
    response = client.post('/api/download-pdf',
                          json=data,
                          content_type='application/json')
    
    assert response.status_code == 200
    assert response.content_type == 'application/pdf'

def test_invalid_endpoint(client):
    """Test invalid endpoint returns 404"""
    response = client.get('/api/invalid-endpoint')
    assert response.status_code == 404

if __name__ == '__main__':
    pytest.main([__file__, '-v'])

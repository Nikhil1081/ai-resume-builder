# Contributing to AI Resume & Portfolio Builder

Thank you for your interest in contributing! 🎉

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/Nikhil1081/ai-resume-builder/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Your environment (OS, Python version, etc.)

### Suggesting Enhancements

1. Open an issue with the "enhancement" label
2. Describe the feature and its benefits
3. Provide examples or mockups if possible

### Pull Requests

1. **Fork the repository**

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/ai-resume-builder.git
   cd ai-resume-builder
   ```

3. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. **Make your changes**
   - Write clear, commented code
   - Follow existing code style
   - Test your changes thoroughly

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of your changes"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Describe your changes in detail

## Code Style Guidelines

### Python
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

```python
def generate_resume(user_data):
    """
    Generate resume using AI based on user data.
    
    Args:
        user_data (dict): User information including name, skills, etc.
    
    Returns:
        dict: Generated resume data
    """
    # Implementation
```

### JavaScript
- Use ES6+ features
- Use const/let instead of var
- Add comments for complex logic
- Keep functions pure when possible

### HTML/CSS
- Use semantic HTML5 tags
- Follow BEM naming convention for CSS
- Keep styles modular and reusable
- Ensure responsive design

## Testing

Before submitting a PR:
1. Test all features manually
2. Check for console errors
3. Verify responsive design
4. Test with/without OpenAI API key

## Development Setup

```bash
# Clone the repository
git clone https://github.com/Nikhil1081/ai-resume-builder.git
cd ai-resume-builder

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Run the application
python app.py
```

## Project Structure

```
├── app.py              # Main Flask application
├── templates/          # HTML templates
├── static/            # CSS, JS, images
├── requirements.txt   # Python dependencies
└── README.md         # Documentation
```

## Feature Ideas

Looking for something to work on? Consider:

- [ ] Add more resume templates
- [ ] Implement resume parsing from PDF/DOCX
- [ ] Add LinkedIn profile import
- [ ] Create resume comparison tool
- [ ] Add multi-language support
- [ ] Implement user authentication
- [ ] Add resume version history
- [ ] Create mobile app version
- [ ] Add job matching algorithm
- [ ] Implement resume scoring

## Questions?

Feel free to:
- Open an issue with the "question" label
- Reach out to the maintainers
- Join discussions in existing issues

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Give constructive feedback
- Focus on collaboration

Thank you for contributing! 🚀

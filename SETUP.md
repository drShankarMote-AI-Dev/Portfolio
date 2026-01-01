# Setup Guide

This guide will help you set up the Portfolio website on your local machine or server.

## Quick Start

### 1. Prerequisites Check

Ensure you have:
- Python 3.8+ installed
- pip installed
- Git installed (optional, for cloning)

Check Python version:
```bash
python --version
# or
python3 --version
```

### 2. Installation Steps

#### Step 1: Clone or Download
```bash
git clone https://github.com/yourusername/portfolio.git
cd portfolio
```

#### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Configure Application

**Option A: Update app.py directly**
```python
# In app.py, line 29, update:
app.config['SECRET_KEY'] = 'your-super-secret-key-here'
```

**Option B: Use environment variable**
```bash
# Windows
set SECRET_KEY=your-super-secret-key-here

# macOS/Linux
export SECRET_KEY=your-super-secret-key-here
```

Generate a secure key:
```python
import secrets
print(secrets.token_hex(32))
```

#### Step 5: Run the Application
```bash
python app.py
```

#### Step 6: Access the Application
- Portfolio: http://localhost:3000
- Admin: http://localhost:3000/admin
- Login: http://localhost:3000/login

**Note:** The default port is 3000. You can change it by setting the `PORT` environment variable:
```bash
# Windows
set PORT=8080
python app.py

# macOS/Linux
export PORT=8080
python app.py
```

**Default Credentials:**
- Username: `admin`
- Password: `adminpass`

⚠️ **IMPORTANT:** Change these credentials immediately after first login!

## Directory Structure Setup

The application will automatically create these directories on first run:
- `data/` - For JSON data files
- `static/images/` - For uploaded images
- `static/documents/` - For PDF documents

If you want to create them manually:
```bash
mkdir data
mkdir static/images
mkdir static/documents
```

## First-Time Configuration

### 1. Change Admin Password

1. Log in to admin dashboard
2. Go to "Change Password" section
3. Update your password

### 2. Update Profile Information

1. Go to "About Me" section
2. Upload your profile picture
3. Update hero title, subtitle, and description
4. Add your highlights

### 3. Add Your Content

- **Skills**: Add technical and soft skills
- **Projects**: Add your portfolio projects
- **Experience**: Add internships, thesis, certifications
- **Education**: Add your education history
- **Contact**: Update contact information

### 4. Upload Resume

1. Place your resume PDF in `static/documents/`
2. Update the resume link in "About Me" → Hero Buttons

## Email Configuration (Optional)

To enable contact form email functionality:

1. Update SMTP settings in `app.py` (around line 1000+):
```python
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_USER = 'your_email@gmail.com'
EMAIL_PASSWORD = 'your_app_password'
```

2. For Gmail, use an App Password:
   - Go to Google Account → Security
   - Enable 2-Step Verification
   - Generate App Password

## Troubleshooting

### Issue: Module not found
**Solution:** Ensure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Port already in use
**Solution:** Use a different port by setting the PORT environment variable:
```bash
# Windows
set PORT=8080
python app.py

# macOS/Linux
export PORT=8080
python app.py
```

### Issue: Permission denied
**Solution:** Check file permissions for `data/` directory

### Issue: Images not loading
**Solution:** 
- Check `static/images/` directory exists
- Verify file paths in `data/data.json`
- Ensure image files are uploaded correctly

### Issue: Admin login not working
**Solution:**
- Check if `data/data.json` exists
- Verify credentials in the JSON file
- Try resetting password using `reset_password.py`

## Production Deployment

### Using Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:${PORT:-3000} app:app
```

Or set the PORT environment variable:
```bash
export PORT=3000
gunicorn -w 4 -b 0.0.0.0:$PORT app:app
```

### Environment Variables

Set these in production:
```bash
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key
```

### Security Checklist

- [ ] Change default admin credentials
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS
- [ ] Set up proper file permissions
- [ ] Configure firewall rules
- [ ] Regular backups of `data/data.json`
- [ ] Update dependencies regularly

## Need Help?

- Check the [README.md](README.md) for more information
- Open an issue on GitHub
- Review the code comments in `app.py`


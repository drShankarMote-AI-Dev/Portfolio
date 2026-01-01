# Portfolio Website - Flask-Based Professional Portfolio

A modern, responsive portfolio website built with Flask that showcases your professional work, skills, experience, and achievements. Features a beautiful admin dashboard for easy content management.

![Portfolio Preview](https://img.shields.io/badge/Flask-3.1.1-000000?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## ✨ Features

### Public Portfolio
- 🎨 **Modern & Responsive Design** - Beautiful UI with dark/light theme toggle
- 📱 **Mobile-First** - Fully responsive across all devices
- 🚀 **Fast Performance** - Optimized images and lazy loading
- 🎯 **SEO Optimized** - Meta tags, semantic HTML, and accessibility features
- 📊 **Dynamic Sections**:
  - Hero section with profile image and animated gradient border
  - About Me with highlights
  - Skills (Technical & Soft Skills)
  - Projects showcase with tech stack tags
  - Experience timeline (Internships, Thesis, Certifications)
  - Education history
  - Achievements
  - Interests
  - Contact form with email integration

### Admin Dashboard
- 🔐 **Secure Authentication** - Password-protected admin access
- 📝 **Easy Content Management** - Manage all portfolio content through a user-friendly interface
- 🎨 **Modern Admin UI** - Beautiful dashboard with animations and modern design
- 📤 **File Upload** - Upload profile pictures and documents
- 🔄 **Drag & Drop** - Reorder skills and projects easily
- 📊 **Statistics Dashboard** - View portfolio statistics at a glance
- 🔒 **CSRF Protection** - Secure forms with CSRF tokens
- 📋 **Activity Logging** - Track all admin activities

## 🛠️ Tech Stack

### Backend
- **Flask** - Web framework
- **Flask-WTF** - Form handling and CSRF protection
- **Werkzeug** - Security utilities for password hashing

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with animations
- **JavaScript (ES6+)** - Dynamic content rendering
- **Responsive Design** - Mobile-first approach

### Data Storage
- **JSON** - Lightweight data storage
- **File System** - Image and document storage

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package manager)
- Git (for version control)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/portfolio.git
   cd portfolio
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the root directory (optional):
   ```env
   SECRET_KEY=your_super_secret_key_here
   FLASK_ENV=development
   ```
   
   Or update `app.py` directly:
   ```python
   app.config['SECRET_KEY'] = 'your_super_secret_key_here'
   ```

5. **Initialize the data structure**
   
   The application will automatically create the necessary data files on first run. If you want to initialize manually:
   ```bash
   python app.py
   ```
   
   Then visit `http://localhost:3000` - the app will create default data structure.

6. **Set up admin credentials**
   
   Default credentials (change immediately after first login):
   - Username: `admin`
   - Password: `adminpass`
   
   **⚠️ Important:** Change these credentials immediately after first login through the admin dashboard!

## 🎯 Usage

### Running the Application

1. **Development Mode**
   ```bash
   python app.py
   ```
   
   Or with Flask CLI:
   ```bash
   flask run
   ```

2. **Access the Application**
   - Public Portfolio: `http://localhost:3000`
   - Admin Dashboard: `http://localhost:3000/admin`
   - Login Page: `http://localhost:3000/login`
   
   **Note:** The default port is 3000, but you can change it by setting the `PORT` environment variable:
   ```bash
   PORT=8080 python app.py
   ```

### Admin Dashboard

1. Navigate to `/admin` or `/login`
2. Log in with your credentials
3. Manage your portfolio content:
   - **Dashboard**: View statistics
   - **About Me**: Update hero section, profile picture, highlights
   - **Skills**: Add/edit technical and soft skills
   - **Projects**: Manage your project portfolio
   - **Experience**: Add internships, thesis, certifications
   - **Education**: Manage education history
   - **Contact**: Update contact information
   - **Settings**: Configure site settings

## 📁 Project Structure

```
portfolio/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore            # Git ignore rules
│
├── data/                 # Data storage
│   ├── data.json        # Main portfolio data
│   └── admin_activity.log # Admin activity logs
│
├── static/               # Static files
│   ├── css/             # Stylesheets
│   │   ├── main_v3.css  # Main styles
│   │   └── admin_dashboard.css # Admin styles
│   ├── js/              # JavaScript files
│   │   ├── script.js    # Main portfolio script
│   │   └── admin.js     # Admin dashboard script
│   ├── images/          # Image assets
│   └── documents/      # PDF documents (resume, etc.)
│
└── templates/           # HTML templates
    ├── index.html       # Main portfolio page
    ├── admin_dashboard.html # Admin dashboard
    ├── admin_content.html   # Admin content sections
    └── login.html       # Login page
```

## 🔧 Configuration

### Changing the Secret Key

**Important for production:** Update the secret key in `app.py`:

```python
app.config['SECRET_KEY'] = 'your_super_secret_key_here'
```

Generate a secure key:
```python
import secrets
print(secrets.token_hex(32))
```

### Email Configuration (Contact Form)

To enable the contact form, configure SMTP settings in `app.py`:

```python
# Update these settings in the contact form route
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_USER = 'your_email@gmail.com'
EMAIL_PASSWORD = 'your_app_password'
```

### Customizing Styles

- Main portfolio styles: `static/css/main_v3.css`
- Admin dashboard styles: `static/css/admin_dashboard.css`

## 🚢 Deployment

### Deploying to Production

1. **Update Secret Key**
   ```python
   app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'generate-secure-key')
   ```

2. **Set Environment Variables**
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secret-key
   ```

3. **Use a Production WSGI Server**
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:${PORT:-3000} app:app
   ```
   
   Or set the PORT environment variable:
   ```bash
   export PORT=3000
   gunicorn -w 4 -b 0.0.0.0:$PORT app:app
   ```

### Recommended Hosting Platforms
- **Heroku** - Easy Flask deployment
- **PythonAnywhere** - Free Python hosting
- **DigitalOcean** - VPS hosting
- **AWS/Google Cloud** - Scalable cloud hosting

## 🔒 Security Considerations

- ✅ CSRF protection enabled
- ✅ Password hashing with Werkzeug
- ✅ Secure file upload validation
- ✅ Input sanitization
- ⚠️ **Change default admin credentials immediately**
- ⚠️ **Use strong SECRET_KEY in production**
- ⚠️ **Enable HTTPS in production**

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourusername/portfolio/issues).

## 👤 Author

**Shankar Managini Mote**
- Portfolio: [Your Portfolio URL]
- LinkedIn: [Your LinkedIn]
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: [Your Email]

## 🙏 Acknowledgments

- Flask community for excellent documentation
- All contributors and users of this project

## 📞 Support

If you have any questions or need help, please:
- Open an issue on GitHub
- Contact me via email
- Check the documentation

---

⭐ If you find this project helpful, please give it a star on GitHub!

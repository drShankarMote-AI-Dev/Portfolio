from flask import Flask, render_template, send_from_directory, request, redirect, url_for, flash, jsonify, session
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import functools
import uuid
import copy
from flask_wtf import CSRFProtect
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
JSON_FILE = 'data/data.json'
LOG_FILE = 'data/admin_activity.log'

# --- Experience Category Mapping ---
EXPERIENCE_CATEGORY_MAP = {
    'internship': 'internships',
    'thesis': 'thesis',
    'certification': 'certifications'
}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_super_secret_key_here' # Replace with a strong secret key
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- CSRF Protection ---
csrf = CSRFProtect(app)



# --- JSON Data Handling Functions ---
def read_portfolio_data():
    """Read the portfolio data from the JSON file."""
    if not os.path.exists(JSON_FILE):
        return {}
    with open(JSON_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_portfolio_data(data):
    """Write the portfolio data to the JSON file."""
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def initialize_json_data():
    if not os.path.exists('data'):
        os.makedirs('data')

    if not os.path.exists(JSON_FILE) or os.stat(JSON_FILE).st_size == 0:
        default_data = {
            "admin_credentials": {
                "username": "admin",
                "password_hash": generate_password_hash('adminpass', method='pbkdf2:sha256')
            },
            "portfolios": [
                {
                    "id": "main",
                    "name": "Main Portfolio",
                    "is_active": True,
                    "created_at": "2024-01-01",
                    "updated_at": "2024-01-01",
                    "about": {
                        "hero_title": "Shankar Managini Mote",
                        "hero_subtitle": "Biotechnology & Web Development Professional",
                        "hero_description": "Passionate about combining biotechnology with modern web technologies to create innovative solutions.",
                        "about_text": "B.Tech Biotechnology graduate with a unique blend of expertise in bioinformatics, DNA barcoding, molecular diagnostics, and web-based biomedical tools. I bridge the gap between biotechnology and modern web development to create innovative solutions.",
                        "highlight1_emoji": "🔬",
                        "highlight1_title": "Biotechnology Expert",
                        "highlight1_description": "Specialized in DNA barcoding and molecular diagnostics",
                        "highlight2_emoji": "💻",
                        "highlight2_title": "Web Developer",
                        "highlight2_description": "Creating modern web applications for biomedical research",
                        "highlight3_emoji": "🔍",
                        "highlight3_title": "Research Enthusiast",
                        "highlight3_description": "Passionate about innovative solutions in biotechnology",
                        "hero_buttons": [
                            {
                                "text": "Download Resume",
                                "link": "/static/documents/Your_Resume.pdf",
                                "icon": "📄",
                                "is_visible": True
                            },
                            {
                                "text": "Contact Me",
                                "link": "#contact",
                                "icon": "📬",
                                "is_visible": True
                            }
                        ]
                    },
                    "profile_picture": {
                        "filename": "shankar.jpeg",
                        "filepath": "/static/images/shankar.jpeg"
                    },
                    "skills": {
                        "technical": [
                            {"name": "HTML5 & CSS3", "description": "Strong command of semantic HTML and modern CSS techniques, including responsive design."},
                            {"name": "JavaScript", "description": "Experienced in front-end development, DOM manipulation, and interactive web applications."},
                            {"name": "Python", "description": "Proficient in data analysis, scripting, and web development with frameworks like Flask and Django."},
                            {"name": "Molecular Biology Techniques", "description": "Hands-on experience with DNA barcoding, PCR, gel electrophoresis, and molecular diagnostics."},
                            {"name": "Bioinformatics Tools", "description": "Familiar with various bioinformatics software and databases for sequence analysis and genomics."}
                        ],
                        "soft": [
                            {"name": "Adaptability", "description": "Quick to learn new technologies and adapt to evolving project requirements and challenges."},
                            {"name": "Communication", "description": "Clear and concise in both written and verbal communication, capable of explaining technical concepts to diverse audiences."},
                            {"name": "Teamwork & Collaboration", "description": "Excellent interpersonal skills with a proven ability to work effectively in team environments."},
                            {"name": "Problem Solving", "description": "Adept at identifying complex issues and developing effective, innovative solutions."}
                        ]
                    },
                    "projects": [
                        {"title": "Interactive COVID-19 Data Dashboard", "description": "Created a dynamic web dashboard using JavaScript and D3.js to visualize global COVID-19 trends, including infection rates, mortality, and vaccination progress.", "technologies": ["JavaScript", "D3.js", "HTML", "CSS", "Data Visualization"], "link": "https://github.com/yourusername/covid-dashboard"},
                        {"title": "Bioinformatics Pipeline for Novel Gene Discovery", "description": "Developed a Python-based bioinformatics pipeline for identifying novel genes from metagenomic data, integrating various public databases and tools.", "technologies": ["Python", "Biopython", "Bash", "Metagenomics", "NCBI Databases"], "link": "https://github.com/yourusername/bioinformatics-pipeline"}
                    ],
                    "experience": {
                        "internships": [
                            {"title": "Bioinformatics Intern", "company": "GeneTech Solutions", "duration": "May 2023 - August 2023", "description": "Assisted in the development of computational tools for genetic sequence analysis and contributed to a project on microbial genomics."}
                        ],
                        "thesis": [
                            {"title": "Development of a Web-Based Tool for DNA Barcode Analysis", "university": "Your University Name", "year": "2024", "description": "Designed and implemented a web application that facilitates the analysis and identification of species using DNA barcoding sequences, enhancing efficiency and accessibility for researchers."}
                        ],
                        "certifications": [
                            {"title": "Advanced Python for Data Science", "issuer": "Data Science Academy", "year": "2022", "link": "https://www.example.com/certificate/python-datascience"},
                            {"title": "Full Stack Web Development Certification", "issuer": "Online Course Provider", "year": "2023", "link": "https://www.example.com/certificate/fullstack"}
                        ]
                    },
                    "contact": {
                        "email": "drshankarmote@gmail.com",
                        "phone": "9699003635",
                        "linkedin": "https://linkedin.com/in/drshankarmote",
                        "github": "https://github.com/yourusername"
                    },
                    "settings": {
                        "site_title": "My Awesome Portfolio"
                    }
                }
            ],
            "about": {
                "hero_title": "Shankar Managini Mote",
                "hero_subtitle": "Biotechnology & Web Development Professional",
                "hero_description": "Passionate about combining biotechnology with modern web technologies to create innovative solutions.",
                "about_text": "B.Tech Biotechnology graduate with a unique blend of expertise in bioinformatics, DNA barcoding, molecular diagnostics, and web-based biomedical tools. I bridge the gap between biotechnology and modern web development to create innovative solutions.",
                "highlight1_emoji": "🔬",
                "highlight1_title": "Biotechnology Expert",
                "highlight1_description": "Specialized in DNA barcoding and molecular diagnostics",
                "highlight2_emoji": "💻",
                "highlight2_title": "Web Developer",
                "highlight2_description": "Creating modern web applications for biomedical research",
                "highlight3_emoji": "🔍",
                "highlight3_title": "Research Enthusiast",
                "highlight3_description": "Passionate about innovative solutions in biotechnology",
                "hero_buttons": [
                    {
                        "text": "Download Resume",
                        "link": "/static/documents/Your_Resume.pdf",
                        "icon": "📄",
                        "is_visible": True
                    },
                    {
                        "text": "Contact Me",
                        "link": "#contact",
                        "icon": "📬",
                        "is_visible": True
                    }
                ]
            },
            "profile_picture": {
                "filename": "shankar.jpeg",
                "filepath": "/static/images/shankar.jpeg"
            },
            "skills": {
                "technical": [
                    {"name": "HTML5 & CSS3", "description": "Strong command of semantic HTML and modern CSS techniques, including responsive design."},
                    {"name": "JavaScript", "description": "Experienced in front-end development, DOM manipulation, and interactive web applications."},
                    {"name": "Python", "description": "Proficient in data analysis, scripting, and web development with frameworks like Flask and Django."},
                    {"name": "Molecular Biology Techniques", "description": "Hands-on experience with DNA barcoding, PCR, gel electrophoresis, and molecular diagnostics."},
                    {"name": "Bioinformatics Tools", "description": "Familiar with various bioinformatics software and databases for sequence analysis and genomics."}
                ],
                "soft": [
                    {"name": "Adaptability", "description": "Quick to learn new technologies and adapt to evolving project requirements and challenges."},
                    {"name": "Communication", "description": "Clear and concise in both written and verbal communication, capable of explaining technical concepts to diverse audiences."},
                    {"name": "Teamwork & Collaboration", "description": "Excellent interpersonal skills with a proven ability to work effectively in team environments."},
                    {"name": "Problem Solving", "description": "Adept at identifying complex issues and developing effective, innovative solutions."}
                ]
            },
            "projects": [
                {"title": "Interactive COVID-19 Data Dashboard", "description": "Created a dynamic web dashboard using JavaScript and D3.js to visualize global COVID-19 trends, including infection rates, mortality, and vaccination progress.", "technologies": ["JavaScript", "D3.js", "HTML", "CSS", "Data Visualization"], "link": "https://github.com/yourusername/covid-dashboard"},
                {"title": "Bioinformatics Pipeline for Novel Gene Discovery", "description": "Developed a Python-based bioinformatics pipeline for identifying novel genes from metagenomic data, integrating various public databases and tools.", "technologies": ["Python", "Biopython", "Bash", "Metagenomics", "NCBI Databases"], "link": "https://github.com/yourusername/bioinformatics-pipeline"}
            ],
            "experience": {
                "internships": [
                    {"title": "Bioinformatics Intern", "company": "GeneTech Solutions", "duration": "May 2023 - August 2023", "description": "Assisted in the development of computational tools for genetic sequence analysis and contributed to a project on microbial genomics."}
                ],
                "thesis": [
                    {"title": "Development of a Web-Based Tool for DNA Barcode Analysis", "university": "Your University Name", "year": "2024", "description": "Designed and implemented a web application that facilitates the analysis and identification of species using DNA barcoding sequences, enhancing efficiency and accessibility for researchers."}
                ],
                "certifications": [
                    {"title": "Advanced Python for Data Science", "issuer": "Data Science Academy", "year": "2022", "link": "https://www.example.com/certificate/python-datascience"},
                    {"title": "Full Stack Web Development Certification", "issuer": "Online Course Provider", "year": "2023", "link": "https://www.example.com/certificate/fullstack"}
                ]
            },
            "contact": {
                "email": "drshankarmote@gmail.com",
                "phone": "9699003635",
                "linkedin": "https://linkedin.com/in/drshankarmote",
                "github": "https://github.com/yourusername"
            },
            "settings": {
                "site_title": "My Awesome Portfolio"
            }
        }
        write_portfolio_data(default_data)
        print(f"Created default {JSON_FILE} with initial data.")

# --- Admin User and Login (Simplified for JSON) ---
def get_admin_credentials():
    """Get admin credentials from the data file."""
    data = read_portfolio_data()
    return data.get('admin_credentials', {})

def check_admin_password(password):
    """Check if the provided password matches the stored hash."""
    credentials = get_admin_credentials()
    stored_hash = credentials.get('password_hash')
    return stored_hash and check_password_hash(stored_hash, password)

def login_required(view):
    """Decorator to require login for admin routes."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            flash('Please log in to access this page.', 'danger')
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

# --- Helper for file uploads ---
def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- Portfolio Management Functions ---
def get_active_portfolio():
    """Get the currently active portfolio."""
    data = read_portfolio_data()
    portfolios = data.get('portfolios', [])
    for portfolio in portfolios:
        if portfolio.get('is_active', False):
            return portfolio
    return None

def get_portfolio_by_id(portfolio_id):
    """Get a specific portfolio by ID."""
    data = read_portfolio_data()
    portfolios = data.get('portfolios', [])
    for portfolio in portfolios:
        if portfolio.get('id') == portfolio_id:
            return portfolio
    return None

def create_portfolio(name, description=""):
    """Create a new portfolio with the given name and description."""
    data = read_portfolio_data()
    if 'portfolios' not in data:
        data['portfolios'] = []
    
    # Generate unique ID
    portfolio_id = str(uuid.uuid4())[:8]
    
    # Create new portfolio with default structure
    new_portfolio = {
        "id": portfolio_id,
        "name": name,
        "description": description,
        "is_active": False,  # New portfolios are inactive by default
        "created_at": "2024-01-01",  # You might want to use actual datetime
        "updated_at": "2024-01-01",
        "about": {
            "hero_title": "New Portfolio",
            "hero_subtitle": "Portfolio Subtitle",
            "hero_description": "Portfolio description",
            "about_text": "About text for this portfolio",
            "highlight1_emoji": "🌟",
            "highlight1_title": "Highlight 1",
            "highlight1_description": "Description for highlight 1",
            "highlight2_emoji": "💡",
            "highlight2_title": "Highlight 2",
            "highlight2_description": "Description for highlight 2",
            "highlight3_emoji": "🚀",
            "highlight3_title": "Highlight 3",
            "highlight3_description": "Description for highlight 3",
            "hero_buttons": []
        },
        "profile_picture": {
            "filename": "",
            "filepath": ""
        },
        "skills": {
            "technical": [],
            "soft": []
        },
        "projects": [],
        "experience": {
            "internships": [],
            "thesis": [],
            "certifications": []
        },
        "contact": {
            "email": "",
            "phone": "",
            "linkedin": "",
            "github": ""
        },
        "settings": {
            "site_title": "My Awesome Portfolio"
        }
    }
    
    data['portfolios'].append(new_portfolio)
    write_portfolio_data(data)
    return new_portfolio

def update_portfolio(portfolio_id, updates):
    """Update a portfolio with new data."""
    data = read_portfolio_data()
    portfolios = data.get('portfolios', [])
    
    for i, portfolio in enumerate(portfolios):
        if portfolio.get('id') == portfolio_id:
            portfolio.update(updates)
            portfolio['updated_at'] = "2024-01-01"  # You might want to use actual datetime
            data['portfolios'][i] = portfolio
            write_portfolio_data(data)
            return True
    return False

def delete_portfolio(portfolio_id):
    """Delete a portfolio by its ID."""
    data = read_portfolio_data()
    portfolios = data.get('portfolios', [])
    
    for i, portfolio in enumerate(portfolios):
        if portfolio.get('id') == portfolio_id:
            del data['portfolios'][i]
            write_portfolio_data(data)
            return True
    return False

def set_active_portfolio(portfolio_id):
    """Set a portfolio as active and deactivate others."""
    data = read_portfolio_data()
    portfolios = data.get('portfolios', [])
    
    for portfolio in portfolios:
        portfolio['is_active'] = (portfolio.get('id') == portfolio_id)
    
    data['portfolios'] = portfolios
    write_portfolio_data(data)
    return True

def duplicate_portfolio(portfolio_id, new_name):
    """Duplicate an existing portfolio with a new name."""
    original_portfolio = get_portfolio_by_id(portfolio_id)
    if not original_portfolio:
        return None
    
    # Create a deep copy of the portfolio
    new_portfolio = copy.deepcopy(original_portfolio)
    
    # Generate new ID and update name
    new_portfolio['id'] = str(uuid.uuid4())[:8]
    new_portfolio['name'] = new_name
    new_portfolio['is_active'] = False  # Duplicated portfolios are inactive by default
    new_portfolio['created_at'] = "2024-01-01"  # You might want to use actual datetime
    new_portfolio['updated_at'] = "2024-01-01"
    
    # Add to portfolios list
    data = read_portfolio_data()
    data['portfolios'].append(new_portfolio)
    write_portfolio_data(data)
    
    return new_portfolio

# Routes
@app.route('/')
def home():
    data = read_portfolio_data()
    settings = data.get('settings', {})
    is_admin = session.get('logged_in', False)
    
    # Check maintenance mode first
    if settings.get('maintenance_mode') and not is_admin:
        return render_template('maintenance.html')
    
    # Check public access
    if not settings.get('allow_public_access', True) and not is_admin:
        return render_template('access_denied.html'), 403
    
    # Get active portfolio for display
    active_portfolio = get_active_portfolio()
    if active_portfolio:
        # Add settings to active portfolio data
        active_portfolio['settings'] = settings
        return render_template('index.html', data=active_portfolio)
    else:
        return render_template('index.html', data=data)

@app.route('/data/<path:filename>')
def data_file(filename):
    return send_from_directory('data', filename)

@app.route('/api/portfolio_data')
def portfolio_data():
    data = read_portfolio_data()
    settings = data.get('settings', {})
    is_admin = session.get('logged_in', False)
    
    # Check maintenance mode first
    if settings.get('maintenance_mode') and not is_admin:
        return jsonify({'error': 'Site is under maintenance'}), 503
    
    # Check public access
    if not settings.get('allow_public_access', True) and not is_admin:
        return jsonify({'error': 'Public access is disabled'}), 403
    
    # Return active portfolio data with settings
    active_portfolio = get_active_portfolio()
    if active_portfolio:
        # Add settings to the active portfolio data
        active_portfolio['settings'] = settings
        return jsonify(active_portfolio)
    else:
        return jsonify(data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        credentials = get_admin_credentials()
        ADMIN_USERNAME = credentials.get('username')
        if username == ADMIN_USERNAME and check_admin_password(password):
            session['logged_in'] = True
            session['admin_username'] = username
            log_admin_activity('login', 'auth', f"username={username}")
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            log_admin_activity('failed_login', 'auth', f"username={username}")
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    log_admin_activity('logout', 'auth', f"username={session.get('admin_username', 'unknown')}")
    session.pop('logged_in', None)
    session.pop('admin_username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


@app.route('/admin', methods=['GET', 'POST'], defaults={'section': 'dashboard'})
@app.route('/admin/<section>', methods=['GET', 'POST'])
@login_required
def admin_dashboard(section):
    data = read_portfolio_data()
    context = {'current_section': section, 'data': data}

    # Ensure about and profile_picture keys exist
    if 'about' not in data:
        data['about'] = {}
    if 'profile_picture' not in data:
        data['profile_picture'] = {'filename': '', 'filepath': ''}

    if section == 'dashboard':
        # Calculate stats for the dashboard
        active_portfolio = get_active_portfolio()
        if not active_portfolio:
            active_portfolio = data.get('portfolios', [])[0] if data.get('portfolios') else {}

        stats = {
            'projects': len(active_portfolio.get('projects', [])),
            'skills': len(active_portfolio.get('skills', {}).get('technical', [])) + len(active_portfolio.get('skills', {}).get('soft', [])),
            'experience': len(active_portfolio.get('experience', {}).get('internships', [])) + 
                          len(active_portfolio.get('experience', {}).get('thesis', [])) + 
                          len(active_portfolio.get('experience', {}).get('certifications', [])),
            'education': len(active_portfolio.get('experience', {}).get('education', [])),
            'active_portfolio_name': active_portfolio.get('name', 'None')
        }
        context['stats'] = stats
        return render_template('admin_dashboard.html', **context)

    # --- SKILLS ---
    elif section == 'skills':
        # Patch: update skills in active portfolio
        active_portfolio = None
        for portfolio in data.get('portfolios', []):
            if portfolio.get('is_active'):
                active_portfolio = portfolio
                break
        skills_data = (active_portfolio['skills'] if active_portfolio and 'skills' in active_portfolio else data['skills'])
        context['skills'] = []
        for skill_type in ['technical', 'soft']:
            for idx, skill in enumerate(skills_data[skill_type]):
                skill['id'] = f"{skill_type}_{idx}"
                skill['type'] = skill_type
                context['skills'].append(skill)
        # Handle drag-and-drop reorder
        if request.method == 'POST':
            if request.is_json:
                req = request.get_json()
                if req.get('action') == 'reorder_skills':
                    new_order = req.get('order', [])
                    # Rebuild skills list in new order
                    all_skills = []
                    for skill_type in ['technical', 'soft']:
                        for idx, skill in enumerate(skills_data[skill_type]):
                            skill['id'] = f"{skill_type}_{idx}"
                            skill['type'] = skill_type
                            all_skills.append(skill)
                    id_to_skill = {s['id']: s for s in all_skills}
                    reordered = [id_to_skill[skill_id] for skill_id in new_order if skill_id in id_to_skill]
                    # Split back into technical and soft
                    new_tech = [s for s in reordered if s['type'] == 'technical']
                    new_soft = [s for s in reordered if s['type'] == 'soft']
                    skills_data['technical'] = [{k: v for k, v in s.items() if k not in ['id', 'type']} for s in new_tech]
                    skills_data['soft'] = [{k: v for k, v in s.items() if k not in ['id', 'type']} for s in new_soft]
                    write_portfolio_data(data)
                    log_admin_activity('reorder', 'skills', f"order={new_order}")
                    return jsonify({'success': True})
            # Handle delete
            if request.form.get('delete_id'):
                skill_id = request.form['delete_id']
                skill_type, idx = skill_id.split('_')
                idx = int(idx)
                log_admin_activity('delete', 'skill', f"type={skill_type}, idx={idx}")
                del skills_data[skill_type][idx]
                write_portfolio_data(data)
                flash('Skill deleted successfully!', 'success')
                return redirect(url_for('admin_dashboard', section='skills'))

    elif section == 'add_skill':
        context['form_title'] = 'Add New Skill'
        if request.method == 'POST':
            # Patch: add skill to active portfolio
            active_portfolio = None
            for portfolio in data.get('portfolios', []):
                if portfolio.get('is_active'):
                    active_portfolio = portfolio
                    break
            skills_data = (active_portfolio['skills'] if active_portfolio and 'skills' in active_portfolio else data['skills'])
            skill_type = request.form['type']
            name = request.form['name']
            description = request.form.get('description', '')
            skills_data[skill_type].append({'name': name, 'description': description})
            write_portfolio_data(data)
            log_admin_activity('add', 'skill', f"type={skill_type}, name={name}")
            flash('Skill added successfully!', 'success')
            return redirect(url_for('admin_dashboard', section='skills'))

    elif section == 'edit_skill':
        context['form_title'] = 'Edit Skill'
        skill_id = request.args.get('id')
        if skill_id:
            # Patch: get skill from active portfolio
            active_portfolio = None
            for portfolio in data.get('portfolios', []):
                if portfolio.get('is_active'):
                    active_portfolio = portfolio
                    break
            skills_data = (active_portfolio['skills'] if active_portfolio and 'skills' in active_portfolio else data['skills'])
            skill_type, idx = skill_id.split('_')
            idx = int(idx)
            context['skill'] = skills_data[skill_type][idx]
            context['skill']['type'] = skill_type
        if request.method == 'POST':
            # Patch: update skill in active portfolio
            active_portfolio = None
            for portfolio in data.get('portfolios', []):
                if portfolio.get('is_active'):
                    active_portfolio = portfolio
                    break
            skills_data = (active_portfolio['skills'] if active_portfolio and 'skills' in active_portfolio else data['skills'])
            skill_type = request.form['type']
            name = request.form['name']
            description = request.form.get('description', '')
            skills_data[skill_type][idx] = {'name': name, 'description': description}
            write_portfolio_data(data)
            log_admin_activity('edit', 'skill', f"type={skill_type}, idx={idx}, name={name}")
            flash('Skill updated successfully!', 'success')
            return redirect(url_for('admin_dashboard', section='skills'))

    # --- PROJECTS ---
    elif section == 'projects':
        # Patch: update projects in active portfolio
        active_portfolio = None
        for portfolio in data.get('portfolios', []):
            if portfolio.get('is_active'):
                active_portfolio = portfolio
                break
        projects_data = (active_portfolio['projects'] if active_portfolio and 'projects' in active_portfolio else data['projects'])
        context['projects'] = []
        for idx, project in enumerate(projects_data):
            project['id'] = idx
            context['projects'].append(project)
        if request.method == 'POST':
            if request.is_json:
                req = request.get_json()
                if req.get('action') == 'reorder_projects':
                    new_order = req.get('order', [])
                    id_to_project = {str(i): p for i, p in enumerate(projects_data)}
                    reordered = [id_to_project[pid] for pid in new_order if pid in id_to_project]
                    projects_data.clear()
                    projects_data.extend(reordered)
                    write_portfolio_data(data)
                    log_admin_activity('reorder', 'projects', f"order={new_order}")
                    return jsonify({'success': True})
            if request.form.get('delete_id'):
                idx = int(request.form['delete_id'])
                log_admin_activity('delete', 'project', f"idx={idx}")
                del projects_data[idx]
                write_portfolio_data(data)
                flash('Project deleted successfully!', 'success')
                return redirect(url_for('admin_dashboard', section='projects'))

    elif section == 'add_project':
        context['form_title'] = 'Add New Project'
        if request.method == 'POST':
            # Patch: add project to active portfolio
            active_portfolio = None
            for portfolio in data.get('portfolios', []):
                if portfolio.get('is_active'):
                    active_portfolio = portfolio
                    break
            projects_data = (active_portfolio['projects'] if active_portfolio and 'projects' in active_portfolio else data['projects'])
            title = request.form['title']
            description = request.form['description']
            technologies = [t.strip() for t in request.form.get('technologies', '').split(',') if t.strip()]
            link = request.form.get('link', '')
            projects_data.append({'title': title, 'description': description, 'technologies': technologies, 'link': link})
            write_portfolio_data(data)
            log_admin_activity('add', 'project', f"title={title}")
            flash('Project added successfully!', 'success')
            return redirect(url_for('admin_dashboard', section='projects'))

    elif section == 'edit_project':
        context['form_title'] = 'Edit Project'
        idx = int(request.args.get('id', 0))
        # Patch: get project from active portfolio
        active_portfolio = None
        for portfolio in data.get('portfolios', []):
            if portfolio.get('is_active'):
                active_portfolio = portfolio
                break
        projects_data = (active_portfolio['projects'] if active_portfolio and 'projects' in active_portfolio else data['projects'])
        context['project'] = projects_data[idx]
        if request.method == 'POST':
            # Patch: update project in active portfolio
            title = request.form['title']
            description = request.form['description']
            technologies = [t.strip() for t in request.form.get('technologies', '').split(',') if t.strip()]
            link = request.form.get('link', '')
            projects_data[idx] = {'title': title, 'description': description, 'technologies': technologies, 'link': link}
            write_portfolio_data(data)
            log_admin_activity('edit', 'project', f"idx={idx}, title={title}")
            flash('Project updated successfully!', 'success')
            return redirect(url_for('admin_dashboard', section='projects'))

    # --- EXPERIENCE ---
    elif section == 'experience':
        # Patch: update experience in active portfolio
        active_portfolio = None
        for portfolio in data.get('portfolios', []):
            if portfolio.get('is_active'):
                active_portfolio = portfolio
                break
        experience_data = (active_portfolio['experience'] if active_portfolio and 'experience' in active_portfolio else data['experience'])
        context['experience_data'] = experience_data
        # Deletion handled in delete_experience

    elif section == 'add_experience':
        context['form_title'] = 'Add New'
        category = request.args.get('category')
        context['category'] = category
        if request.method == 'POST':
            # Patch: add experience to active portfolio
            active_portfolio = None
            for portfolio in data.get('portfolios', []):
                if portfolio.get('is_active'):
                    active_portfolio = portfolio
                    break
            experience_data = (active_portfolio['experience'] if active_portfolio and 'experience' in active_portfolio else data['experience'])
            item = {'title': request.form['title'], 'description': request.form.get('description', '')}
            if category == 'internship':
                item['company'] = request.form.get('company', '')
                item['duration'] = request.form.get('duration', '')
            elif category == 'thesis':
                item['university'] = request.form.get('university', '')
                item['year'] = request.form.get('year', '')
            elif category == 'certification':
                item['issuer'] = request.form.get('issuer', '')
                item['year'] = request.form.get('year', '')
                item['link'] = request.form.get('link', '')
            experience_data[EXPERIENCE_CATEGORY_MAP[category]].append(item)
            write_portfolio_data(data)
            log_admin_activity('add', category, f"title={item['title']}")
            flash('Experience added successfully!', 'success')
            return redirect(url_for('admin_dashboard', section='experience'))

    elif section == 'edit_experience':
        context['form_title'] = 'Edit'
        category = request.args.get('category')
        idx = int(request.args.get('id', 0))
        context['category'] = category
        # Patch: get experience from active portfolio
        active_portfolio = None
        for portfolio in data.get('portfolios', []):
            if portfolio.get('is_active'):
                active_portfolio = portfolio
                break
        experience_data = (active_portfolio['experience'] if active_portfolio and 'experience' in active_portfolio else data['experience'])
        context['experience'] = experience_data[EXPERIENCE_CATEGORY_MAP[category]][idx]
        if request.method == 'POST':
            # Patch: update experience in active portfolio
            item = {'title': request.form['title'], 'description': request.form.get('description', '')}
            if category == 'internship':
                item['company'] = request.form.get('company', '')
                item['duration'] = request.form.get('duration', '')
            elif category == 'thesis':
                item['university'] = request.form.get('university', '')
                item['year'] = request.form.get('year', '')
            elif category == 'certification':
                item['issuer'] = request.form.get('issuer', '')
                item['year'] = request.form.get('year', '')
                item['link'] = request.form.get('link', '')
            experience_data[EXPERIENCE_CATEGORY_MAP[category]][idx] = item
            write_portfolio_data(data)
            log_admin_activity('edit', category, f"idx={idx}, title={item['title']}")
            flash('Experience updated successfully!', 'success')
            return redirect(url_for('admin_dashboard', section='experience'))

    elif section == 'delete_experience':
        category = request.args.get('category')
        idx = int(request.args.get('id', 0))
        # Patch: delete experience from active portfolio
        active_portfolio = None
        for portfolio in data.get('portfolios', []):
            if portfolio.get('is_active'):
                active_portfolio = portfolio
                break
        experience_data = (active_portfolio['experience'] if active_portfolio and 'experience' in active_portfolio else data['experience'])
        log_admin_activity('delete', category, f"idx={idx}")
        del experience_data[EXPERIENCE_CATEGORY_MAP[category]][idx]
        write_portfolio_data(data)
        flash('Experience deleted successfully!', 'success')
        return redirect(url_for('admin_dashboard', section='experience'))

    # --- EDUCATION ---
    elif section == 'education':
        # Patch: update education in active portfolio
        active_portfolio = None
        for portfolio in data.get('portfolios', []):
            if portfolio.get('is_active'):
                active_portfolio = portfolio
                break
        experience_data = (active_portfolio['experience'] if active_portfolio and 'experience' in active_portfolio else data['experience'])
        context['education_data'] = experience_data.get('education', [])

    elif section == 'add_education':
        context['form_title'] = 'Add New Education'
        if request.method == 'POST':
            # Patch: add education to active portfolio
            active_portfolio = None
            for portfolio in data.get('portfolios', []):
                if portfolio.get('is_active'):
                    active_portfolio = portfolio
                    break
            experience_data = (active_portfolio['experience'] if active_portfolio and 'experience' in active_portfolio else data['experience'])
            item = {
                'degree': request.form['degree'],
                'university': request.form['university'],
                'year': request.form['year'],
                'description': request.form.get('description', ''),
                'gpa': request.form.get('gpa', ''),
                'honors': request.form.get('honors', ''),
                'certificate_link': request.form.get('certificate_link', '')
            }
            if 'education' not in experience_data:
                experience_data['education'] = []
            experience_data['education'].append(item)
            write_portfolio_data(data)
            log_admin_activity('add', 'education', f"degree={item['degree']}")
            flash('Education added successfully!', 'success')
            return redirect(url_for('admin_dashboard', section='education'))

    elif section == 'edit_education':
        context['form_title'] = 'Edit Education'
        idx = int(request.args.get('id', 0))
        # Patch: get education from active portfolio
        active_portfolio = None
        for portfolio in data.get('portfolios', []):
            if portfolio.get('is_active'):
                active_portfolio = portfolio
                break
        experience_data = (active_portfolio['experience'] if active_portfolio and 'experience' in active_portfolio else data['experience'])
        context['education'] = experience_data.get('education', [])[idx]
        if request.method == 'POST':
            # Patch: update education in active portfolio
            item = {
                'degree': request.form['degree'],
                'university': request.form['university'],
                'year': request.form['year'],
                'description': request.form.get('description', ''),
                'gpa': request.form.get('gpa', ''),
                'honors': request.form.get('honors', ''),
                'certificate_link': request.form.get('certificate_link', '')
            }
            experience_data['education'][idx] = item
            write_portfolio_data(data)
            log_admin_activity('edit', 'education', f"idx={idx}, degree={item['degree']}")
            flash('Education updated successfully!', 'success')
            return redirect(url_for('admin_dashboard', section='education'))

    elif section == 'delete_education':
        idx = int(request.args.get('id', 0))
        # Patch: delete education from active portfolio
        active_portfolio = None
        for portfolio in data.get('portfolios', []):
            if portfolio.get('is_active'):
                active_portfolio = portfolio
                break
        experience_data = (active_portfolio['experience'] if active_portfolio and 'experience' in active_portfolio else data['experience'])
        log_admin_activity('delete', 'education', f"idx={idx}")
        del experience_data['education'][idx]
        write_portfolio_data(data)
        flash('Education entry deleted successfully!', 'success')
        return redirect(url_for('admin_dashboard', section='education'))

    # --- CONTACT ---
    elif section == 'contact':
        # Patch: update contact info in active portfolio
        active_portfolio = None
        for portfolio in data.get('portfolios', []):
            if portfolio.get('is_active'):
                active_portfolio = portfolio
                break
        context['contact_settings'] = (active_portfolio['contact'] if active_portfolio and 'contact' in active_portfolio else data['contact'])
        if request.method == 'POST':
            if active_portfolio:
                if 'contact' not in active_portfolio:
                    active_portfolio['contact'] = {}
                active_portfolio['contact']['email'] = request.form['email']
                active_portfolio['contact']['phone'] = request.form.get('phone', '')
                active_portfolio['contact']['linkedin'] = request.form.get('linkedin', '')
                active_portfolio['contact']['github'] = request.form.get('github', '')
            else:
                data['contact']['email'] = request.form['email']
                data['contact']['phone'] = request.form.get('phone', '')
                data['contact']['linkedin'] = request.form.get('linkedin', '')
                data['contact']['github'] = request.form.get('github', '')
            write_portfolio_data(data)
            log_admin_activity('update', 'contact', f"email={request.form['email']}")
            flash('Contact settings updated successfully!', 'success')
            return redirect(url_for('admin_dashboard', section='contact'))

    # --- ABOUT ---
    elif section == 'about':
        # Patch: update about info in active portfolio
        active_portfolio = None
        for portfolio in data.get('portfolios', []):
            if portfolio.get('is_active'):
                active_portfolio = portfolio
                break
        context['about_settings'] = (active_portfolio['about'] if active_portfolio and 'about' in active_portfolio else data['about'])
        if request.method == 'POST':
            if 'profile_pic' in request.files:
                file = request.files['profile_pic']
                if file and allowed_file(file.filename):
                    if file.mimetype not in ['image/jpeg', 'image/png', 'image/gif', 'image/jpg']:
                        flash('Only JPG, PNG, or GIF images are allowed.', 'danger')
                        return redirect(url_for('admin_dashboard', section='about'))
                    file.seek(0, os.SEEK_END)
                    if file.tell() > 2 * 1024 * 1024:
                        flash('File size must be less than 2MB.', 'danger')
                        return redirect(url_for('admin_dashboard', section='about'))
                    file.seek(0)
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    
                    # Update profile picture in active portfolio
                    if active_portfolio:
                        active_portfolio['profile_picture'] = {'filename': filename, 'filepath': f'/static/images/{filename}'}
                    else:
                        data['profile_picture'] = {'filename': filename, 'filepath': f'/static/images/{filename}'}
                    
                    write_portfolio_data(data)
                    log_admin_activity('update', 'profile_picture', f"filename={filename}")
                    flash('Profile picture updated successfully!', 'success')
                else:
                    flash('Invalid file type.', 'danger')
                return redirect(url_for('admin_dashboard', section='about'))

            if request.form.get('action') == 'add_hero_button':
                new_button = {
                    "text": request.form['text'],
                    "link": request.form['link'],
                    "icon": request.form['icon'],
                    "is_visible": True
                }
                if active_portfolio:
                    if 'hero_buttons' not in active_portfolio['about']:
                        active_portfolio['about']['hero_buttons'] = []
                    active_portfolio['about']['hero_buttons'].append(new_button)
                else:
                    if 'hero_buttons' not in data['about']:
                        data['about']['hero_buttons'] = []
                    data['about']['hero_buttons'].append(new_button)
                write_portfolio_data(data)
                flash('New hero button added successfully!', 'success')
                return redirect(url_for('admin_dashboard', section='about'))

            elif request.form.get('action') == 'edit_hero_button':
                button_index = int(request.form['button_index'])
                buttons = active_portfolio['about'].get('hero_buttons', []) if active_portfolio else data['about'].get('hero_buttons', [])
                if 0 <= button_index < len(buttons):
                    button = buttons[button_index]
                    button['text'] = request.form['text']
                    button['link'] = request.form['link']
                    button['icon'] = request.form['icon']
                    button['is_visible'] = request.form.get('is_visible') == 'true'
                    write_portfolio_data(data)
                    flash('Hero button updated successfully!', 'success')
                return redirect(url_for('admin_dashboard', section='about'))

            elif request.form.get('action') == 'delete_hero_button':
                button_index = int(request.form['button_index'])
                buttons = active_portfolio['about'].get('hero_buttons', []) if active_portfolio else data['about'].get('hero_buttons', [])
                if 0 <= button_index < len(buttons):
                    del buttons[button_index]
                    write_portfolio_data(data)
                    flash('Hero button deleted successfully!', 'success')
                return redirect(url_for('admin_dashboard', section='about'))

            if active_portfolio:
                about = active_portfolio['about']
            else:
                about = data['about']
            about['hero_title'] = request.form['hero_title']
            about['hero_subtitle'] = request.form['hero_subtitle']
            about['hero_description'] = request.form['hero_description']
            about['about_text'] = request.form['about_text']
            for i in range(1, 4):
                about[f'highlight{i}_emoji'] = request.form.get(f'highlight{i}_emoji', '')
                about[f'highlight{i}_title'] = request.form.get(f'highlight{i}_title', '')
                about[f'highlight{i}_description'] = request.form.get(f'highlight{i}_description', '')
            write_portfolio_data(data)
            log_admin_activity('update', 'about', f"hero_title={about['hero_title']}")
            flash('About settings updated successfully!', 'success')
            return redirect(url_for('admin_dashboard', section='about'))
    
    # --- CHANGE PASSWORD ---
    elif section == 'change_password':
        if request.method == 'POST':
            current_password = request.form['current_password']
            new_password = request.form['new_password']
            confirm_password = request.form['confirm_password']
            
            credentials = get_admin_credentials()
            current_username = credentials.get('username')

            if not check_admin_password(current_password):
                flash('Current password is incorrect.', 'danger')
            elif new_password != confirm_password:
                flash('New password and confirm password do not match.', 'danger')
            elif len(new_password) < 6:
                flash('New password must be at least 6 characters long.', 'danger')
            else:
                data['admin_credentials']['password_hash'] = generate_password_hash(new_password, method='pbkdf2:sha256')
                write_portfolio_data(data)
                log_admin_activity('change_password', 'auth', f"username={current_username}")
                flash('Password updated successfully!', 'success')
            return redirect(url_for('admin_dashboard', section='change_password'))
    
    # --- CHANGE USERNAME ---
    elif section == 'change_username':
        if request.method == 'POST':
            current_password = request.form['current_password']
            new_username = request.form['new_username']

            if not check_admin_password(current_password):
                flash('Current password is incorrect.', 'danger')
            elif not new_username:
                flash('New username cannot be empty.', 'danger')
            else:
                data['admin_credentials']['username'] = new_username
                write_portfolio_data(data)
                log_admin_activity('change_username', 'auth', f"new_username={new_username}")
                flash('Username updated successfully!', 'success')
            return redirect(url_for('admin_dashboard', section='change_username'))

    # --- PORTFOLIOS (Moved to Settings) ---
    # The portfolio management logic is now handled under the 'settings' section
    # The 'portfolios' section will be removed from admin_content.html and admin_dashboard.html
    # so these elif blocks will no longer be directly reachable as a separate section.
    # The logic is retained here and called from the 'settings' block if needed.

    elif section == 'add_portfolio':
        context['form_title'] = 'Add New Portfolio'
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip()
            if name:
                new_portfolio = create_portfolio(name, description)
                log_admin_activity('add', 'portfolio', f"name={name}")
                flash('Portfolio created successfully!', 'success')
                return redirect(url_for('admin_dashboard', section='settings')) # Redirect to settings
            else:
                flash('Portfolio name is required.', 'danger')
                return redirect(url_for('admin_dashboard', section='add_portfolio'))

    elif section == 'edit_portfolio':
        context['form_title'] = 'Edit Portfolio'
        portfolio_id = request.args.get('id')
        if portfolio_id:
            portfolio = get_portfolio_by_id(portfolio_id)
            if portfolio:
                context['portfolio'] = portfolio
            else:
                flash('Portfolio not found.', 'danger')
                return redirect(url_for('admin_dashboard', section='settings')) # Redirect to settings
        
        if request.method == 'POST':
            portfolio_id = request.form.get('portfolio_id')
            name = request.form.get('name', '').strip()
            description = request.form.get('description', '').strip()
            if name and portfolio_id:
                updates = {
                    'name': name,
                    'description': description
                }
                if update_portfolio(portfolio_id, updates):
                    log_admin_activity('edit', 'portfolio', f"id={portfolio_id}, name={name}")
                    flash('Portfolio updated successfully!', 'success')
                else:
                    flash('Failed to update portfolio.', 'danger')
                return redirect(url_for('admin_dashboard', section='settings')) # Redirect to settings
            else:
                flash('Portfolio name is required.', 'danger')
                return redirect(url_for('admin_dashboard', section='edit_portfolio', id=portfolio_id))

    # --- EXPORT ---
    elif section == 'export_data':
        pass
    elif section == 'settings':
        context['settings'] = data.get('settings', {})
        context['portfolios'] = data.get('portfolios', []) # Make portfolios available in settings context

        if request.method == 'POST':
            # --- System Settings Section: Handle General System Settings ---
            if request.form.get('action') == 'update_system_settings':
                # Get form values
                default_portfolio = request.form.get('default_portfolio')
                allow_public_access = request.form.get('allow_public_access') == 'on'
                maintenance_mode = request.form.get('maintenance_mode') == 'on'
                default_theme = request.form.get('default_theme', 'Default Dark')
                section_alignment = request.form.get('section_alignment', 'center')

                # Update settings in data.json
                if 'settings' not in data:
                    data['settings'] = {}
                data['settings']['default_portfolio'] = default_portfolio
                data['settings']['allow_public_access'] = allow_public_access
                data['settings']['maintenance_mode'] = maintenance_mode
                data['settings']['default_theme'] = default_theme
                data['settings']['section_alignment'] = section_alignment

                # Set the selected portfolio as active, others as inactive
                for portfolio in data.get('portfolios', []):
                    portfolio['is_active'] = (portfolio['id'] == default_portfolio)

                write_portfolio_data(data)
                log_admin_activity('update', 'system_settings', f"default_portfolio={default_portfolio}, allow_public_access={allow_public_access}, maintenance_mode={maintenance_mode}, default_theme={default_theme}, section_alignment={section_alignment}")
                flash('System settings updated successfully!', 'success')
                return redirect(url_for('admin_dashboard', section='settings'))

            # --- Settings Section: Handle General and Portfolio Management Actions ---
            # Handle general settings (e.g., site title)
            if request.form.get('action') == 'update_site_settings':
                data['settings']['site_title'] = request.form.get('site_title', '').strip()
                write_portfolio_data(data)
                log_admin_activity('update', 'settings', f"site_title={data['settings']['site_title']}")
                flash('Site settings updated successfully!', 'success')
                return redirect(url_for('admin_dashboard', section='settings'))
            
            # Handle portfolio actions (moved from old 'portfolios' section)
            elif request.form.get('action') == 'create_portfolio':
                name = request.form.get('name', '').strip()
                description = request.form.get('description', '').strip()
                if name:
                    # Check for unique name
                    if any(p['name'].lower() == name.lower() for p in data.get('portfolios', [])):
                        flash('A portfolio with this name already exists. Please choose a unique name.', 'danger')
                    else:
                        create_portfolio(name, description)
                        log_admin_activity('add', 'portfolio', f"name={name}")
                        flash('Portfolio created successfully!', 'success')
                else:
                    flash('Portfolio name is required.', 'danger')
                return redirect(url_for('admin_dashboard', section='settings'))
            
            elif request.form.get('action') == 'set_active':
                portfolio_id = request.form.get('portfolio_id')
                if portfolio_id:
                    set_active_portfolio(portfolio_id)
                    log_admin_activity('set_active', 'portfolio', f"id={portfolio_id}")
                    flash('Active portfolio updated successfully!', 'success')
                return redirect(url_for('admin_dashboard', section='settings'))
            
            elif request.form.get('action') == 'delete_portfolio':
                portfolio_id = request.form.get('portfolio_id')
                if portfolio_id:
                    portfolios = data.get('portfolios', [])
                    if len(portfolios) <= 1:
                        flash('Cannot delete the only portfolio. At least one portfolio must exist.', 'danger')
                    else:
                        portfolio = get_portfolio_by_id(portfolio_id)
                        if portfolio and portfolio.get('is_active'):
                            flash('Cannot delete the active portfolio. Please set another portfolio as active first.', 'danger')
                        else:
                            delete_portfolio(portfolio_id)
                            log_admin_activity('delete', 'portfolio', f"id={portfolio_id}")
                            flash('Portfolio deleted successfully!', 'success')
                return redirect(url_for('admin_dashboard', section='settings'))
            
            elif request.form.get('action') == 'duplicate_portfolio':
                portfolio_id = request.form.get('portfolio_id')
                new_name = request.form.get('new_name', '').strip()
                if portfolio_id and new_name:
                    # Check for unique name
                    if any(p['name'].lower() == new_name.lower() for p in data.get('portfolios', [])):
                        flash('A portfolio with this name already exists. Please choose a unique name.', 'danger')
                    else:
                        if duplicate_portfolio(portfolio_id, new_name):
                            log_admin_activity('duplicate', 'portfolio', f"id={portfolio_id}, new_name={new_name}")
                            flash('Portfolio duplicated successfully!', 'success')
                        else:
                            flash('Failed to duplicate portfolio.', 'danger')
                else:
                    flash('Portfolio ID and new name are required.', 'danger')
                return redirect(url_for('admin_dashboard', section='settings'))

    return render_template('admin_dashboard.html', **context)


@app.route('/export_data')
def export_data():
    data = read_portfolio_data()
    # For a JSON-based system, the data is already in JSON format.
    # We can just serve the existing JSON_FILE.
    return send_from_directory(os.path.dirname(JSON_FILE), os.path.basename(JSON_FILE), as_attachment=True, download_name="portfolio_data.json")

@app.route('/portfolio/<portfolio_id>')
def view_portfolio(portfolio_id):
    data = read_portfolio_data()
    settings = data.get('settings', {})
    is_admin = session.get('logged_in', False)
    
    # Check maintenance mode first
    if settings.get('maintenance_mode') and not is_admin:
        return render_template('maintenance.html')
    
    # Check public access
    if not settings.get('allow_public_access', True) and not is_admin:
        return render_template('access_denied.html'), 403
    
    portfolio = get_portfolio_by_id(portfolio_id)
    if portfolio:
        # Add settings to portfolio data
        portfolio['settings'] = settings
        return render_template('index.html', data=portfolio)
    else:
        flash('Portfolio not found.', 'danger')
        return redirect(url_for('home'))

@app.route('/portfolio/<portfolio_id>/api')
def portfolio_data_api(portfolio_id):
    """API endpoint to get portfolio data"""
    data = read_portfolio_data()
    settings = data.get('settings', {})
    is_admin = session.get('logged_in', False)
    
    # Check maintenance mode first
    if settings.get('maintenance_mode') and not is_admin:
        return jsonify({'error': 'Site is under maintenance'}), 503
    
    # Check public access
    if not settings.get('allow_public_access', True) and not is_admin:
        return jsonify({'error': 'Public access is disabled'}), 403
    
    portfolio = get_portfolio_by_id(portfolio_id)
    if portfolio:
        # Add settings to the portfolio data
        portfolio['settings'] = settings
        return jsonify(portfolio)
    else:
        return jsonify({'error': 'Portfolio not found'}), 404



@app.route('/contact', methods=['POST'])
def contact_form():
    """Handle contact form submissions"""
    try:
        # Validate CSRF token
        if not request.form.get('csrf_token'):
            return jsonify({'success': False, 'message': 'Invalid request'}), 400
        
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        # Validation
        if not name or len(name) < 2 or len(name) > 50:
            return jsonify({'success': False, 'message': 'Name must be between 2 and 50 characters'}), 400
        
        if not email or not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return jsonify({'success': False, 'message': 'Please enter a valid email address'}), 400
        
        if not message or len(message) < 10 or len(message) > 1000:
            return jsonify({'success': False, 'message': 'Message must be between 10 and 1000 characters'}), 400
        
        # Log the contact form submission
        log_admin_activity('contact_form', 'public', f"name={name}, email={email}")
        
        # For now, just return success (you can add email sending logic later)
        # TODO: Implement email sending functionality
        return jsonify({
            'success': True, 
            'message': 'Thank you for your message! I\'ll get back to you soon.'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': 'An error occurred. Please try again.'}), 500

def log_admin_activity(action, section, details=None):
    """Log admin actions to a log file with timestamp, action, section, details, and username."""
    try:
        username = session.get('admin_username', 'unknown')
    except Exception:
        username = 'unknown'
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] | user={username} | action={action} | section={section} | details={details or ''}\n"
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry)

if __name__ == '__main__':
    initialize_json_data()
    port = int(os.environ.get("PORT", 3000))
    print("🚀 Portfolio application starting...")
    print(f"📱 Portfolio: http://localhost:{port}/")
    print(f"🔐 Admin: http://localhost:{port}/login")
    print("💡 Press CTRL+C to stop the server")
    app.run(host="0.0.0.0", port=port)
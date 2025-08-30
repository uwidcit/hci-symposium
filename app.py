from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import pandas as pd
from datetime import datetime
import uuid
import click

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configure app from environment variables
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///symposium.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ADMIN_USERNAME'] = os.environ.get('ADMIN_USERNAME', 'bob')
app.config['ADMIN_PASSWORD'] = os.environ.get('ADMIN_PASSWORD', 'bobpass')

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'posters'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'presentations'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'group_files'), exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class ResearchProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    abstract = db.Column(db.Text, nullable=False)
    member1_name = db.Column(db.String(100), nullable=False)
    member2_name = db.Column(db.String(100), nullable=False)
    paper1_title = db.Column(db.String(200), nullable=False)
    paper2_title = db.Column(db.String(200), nullable=False)
    presentation_video_url = db.Column(db.String(500))
    poster_filename = db.Column(db.String(200))
    presentation_filename = db.Column(db.String(200))
    literature_review = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    """Public landing page"""
    return render_template('index.html')

@app.route('/gallery')
def gallery():
    """Public research gallery"""
    projects = ResearchProject.query.order_by(ResearchProject.created_at.desc()).all()
    return render_template('gallery.html', projects=projects)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('index'))
    
    projects = ResearchProject.query.order_by(ResearchProject.created_at.desc()).all()
    return render_template('admin_dashboard.html', projects=projects)

@app.route('/admin/upload', methods=['GET', 'POST'])
@login_required
def upload_csv():
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        if 'csv_file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['csv_file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file and file.filename.endswith('.csv'):
            try:
                # Read CSV file
                df = pd.read_csv(file)
                
                # Process each row
                for _, row in df.iterrows():
                    project = ResearchProject(
                        group_name=row['group_name'],
                        title=row['title'],
                        abstract=row['abstract'],
                        member1_name=row['member1_name'],
                        member2_name=row['member2_name'],
                        paper1_title=row['paper1_title'],
                        paper2_title=row['paper2_title'],
                        presentation_video_url=row.get('presentation_video_url', ''),
                        literature_review=row.get('literature_review', '')
                    )
                    db.session.add(project)
                
                db.session.commit()
                flash(f'Successfully uploaded {len(df)} research projects')
                return redirect(url_for('admin_dashboard'))
                
            except Exception as e:
                flash(f'Error processing CSV: {str(e)}')
        else:
            flash('Please upload a valid CSV file')
    
    return render_template('upload_csv.html')

@app.route('/admin/project/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('index'))
    
    project = ResearchProject.query.get_or_404(project_id)
    
    if request.method == 'POST':
        project.group_name = request.form['group_name']
        project.title = request.form['title']
        project.abstract = request.form['abstract']
        project.member1_name = request.form['member1_name']
        project.member2_name = request.form['member2_name']
        project.paper1_title = request.form['paper1_title']
        project.paper2_title = request.form['paper2_title']
        project.presentation_video_url = request.form['presentation_video_url']
        project.literature_review = request.form['literature_review']
        
        # Handle file uploads
        if 'poster' in request.files and request.files['poster'].filename:
            poster = request.files['poster']
            if poster and poster.filename.endswith('.pdf'):
                filename = secure_filename(f"{uuid.uuid4()}_{poster.filename}")
                poster.save(os.path.join(app.config['UPLOAD_FOLDER'], 'posters', filename))
                project.poster_filename = filename
        
        if 'presentation' in request.files and request.files['presentation'].filename:
            presentation = request.files['presentation']
            if presentation and presentation.filename.endswith('.pdf'):
                filename = secure_filename(f"{uuid.uuid4()}_{presentation.filename}")
                presentation.save(os.path.join(app.config['UPLOAD_FOLDER'], 'presentations', filename))
                project.presentation_filename = filename
        
        db.session.commit()
        flash('Project updated successfully')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('edit_project.html', project=project)

@app.route('/admin/project/<int:project_id>/delete', methods=['POST'])
@login_required
def delete_project(project_id):
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.')
        return redirect(url_for('index'))
    
    project = ResearchProject.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully')
    return redirect(url_for('admin_dashboard'))

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/project/<int:project_id>')
def view_project(project_id):
    """Public view of a specific research project"""
    project = ResearchProject.query.get_or_404(project_id)
    return render_template('view_project.html', project=project)

# Create admin user and database tables
def init_db():
    with app.app_context():
        # Delete existing database if it exists
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        if os.path.exists(db_path):
            os.remove(db_path)
            print("Existing database deleted.")
        
        db.create_all()
        
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(username=app.config['ADMIN_USERNAME']).first()
        if not admin:
            admin = User(
                username=app.config['ADMIN_USERNAME'],
                password_hash=generate_password_hash(app.config['ADMIN_PASSWORD']),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print(f"Admin user created: username='{app.config['ADMIN_USERNAME']}', password='{app.config['ADMIN_PASSWORD']}'")

# Flask CLI Commands
@app.cli.command("init")
def init_command():
    """Initialize the database and create admin user."""
    click.echo("Initializing database...")
    
    # Delete existing database if it exists
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    if os.path.exists(db_path):
        os.remove(db_path)
        click.echo("Existing database deleted.")
    
    # Ensure upload directories exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'posters'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'presentations'), exist_ok=True)
    os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], 'group_files'), exist_ok=True)
    
    # Create database tables
    db.create_all()
    click.echo("Database tables created.")
    
    # Create admin user
    admin = User.query.filter_by(username=app.config['ADMIN_USERNAME']).first()
    if not admin:
        admin = User(
            username=app.config['ADMIN_USERNAME'],
            password_hash=generate_password_hash(app.config['ADMIN_PASSWORD']),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        click.echo(f"Admin user created: username='{app.config['ADMIN_USERNAME']}', password='{app.config['ADMIN_PASSWORD']}'")
    else:
        click.echo(f"Admin user '{app.config['ADMIN_USERNAME']}' already exists.")
    
    # Insert sample data if no projects exist
    if ResearchProject.query.count() == 0:
        click.echo("Inserting sample data...")
        insert_sample_data()
        click.echo("Sample data inserted.")
    else:
        click.echo("Sample data already exists.")
    
    click.echo("Database initialization complete!")

@app.cli.command("upload-group-files")
@click.argument('directory')
def upload_group_files_command(directory):
    """Upload group files from a directory containing group folders."""
    click.echo(f"Uploading group files from directory: {directory}")
    
    if not os.path.exists(directory):
        click.echo(f"Error: Directory '{directory}' does not exist.")
        return
    
    # Get all group folders
    group_folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
    
    if not group_folders:
        click.echo("No group folders found in the directory.")
        return
    
    click.echo(f"Found {len(group_folders)} group folders: {', '.join(group_folders)}")
    
    for group_folder in group_folders:
        group_path = os.path.join(directory, group_folder)
        click.echo(f"Processing group: {group_folder}")
        
        # Find the project for this group
        project = ResearchProject.query.filter_by(group_name=group_folder).first()
        if not project:
            click.echo(f"  Warning: No project found for group '{group_folder}'")
            continue
        
        # Look for poster and presentation files
        files_uploaded = 0
        
        for filename in os.listdir(group_path):
            file_path = os.path.join(group_path, filename)
            if os.path.isfile(file_path):
                if filename.lower().endswith('.pdf'):
                    if 'poster' in filename.lower():
                        # Upload poster
                        new_filename = secure_filename(f"{uuid.uuid4()}_{filename}")
                        dest_path = os.path.join(app.config['UPLOAD_FOLDER'], 'posters', new_filename)
                        import shutil
                        shutil.copy2(file_path, dest_path)
                        project.poster_filename = new_filename
                        click.echo(f"  Uploaded poster: {filename}")
                        files_uploaded += 1
                    elif 'presentation' in filename.lower() or 'lit' in filename.lower():
                        # Upload presentation
                        new_filename = secure_filename(f"{uuid.uuid4()}_{filename}")
                        dest_path = os.path.join(app.config['UPLOAD_FOLDER'], 'presentations', new_filename)
                        import shutil
                        shutil.copy2(file_path, dest_path)
                        project.presentation_filename = new_filename
                        click.echo(f"  Uploaded presentation: {filename}")
                        files_uploaded += 1
        
        if files_uploaded > 0:
            db.session.commit()
            click.echo(f"  Successfully uploaded {files_uploaded} files for group '{group_folder}'")
        else:
            click.echo(f"  No files uploaded for group '{group_folder}'")
    
    click.echo("Group file upload complete!")

def insert_sample_data():
    """Insert sample research projects."""
    sample_projects = [
        {
            'group_name': 'Team Alpha',
            'title': 'User Interface Design for Mobile Applications',
            'abstract': 'This research explores the impact of user interface design on user experience in mobile applications. The study examines various design patterns and their effectiveness in improving user engagement and satisfaction.',
            'member1_name': 'John Doe',
            'member2_name': 'Jane Smith',
            'paper1_title': 'Mobile UI Design Patterns: A Comprehensive Analysis',
            'paper2_title': 'User Experience Optimization in Mobile Applications',
            'presentation_video_url': 'https://www.youtube.com/watch?v=example1',
            'literature_review': 'The literature review examines current trends in mobile interface design, focusing on usability principles and user-centered design approaches. Key findings indicate that intuitive navigation and consistent visual elements significantly improve user satisfaction.'
        },
        {
            'group_name': 'Team Beta',
            'title': 'Accessibility in Web Design',
            'abstract': 'This study investigates web accessibility standards and their implementation in modern web applications. The research focuses on WCAG guidelines and their practical application for users with disabilities.',
            'member1_name': 'Alice Johnson',
            'member2_name': 'Bob Wilson',
            'paper1_title': 'Web Accessibility Implementation: Best Practices',
            'paper2_title': 'Inclusive Design Principles for Digital Interfaces',
            'presentation_video_url': 'https://www.youtube.com/watch?v=example2',
            'literature_review': 'The literature review analyzes current web accessibility standards and their impact on user experience for individuals with various disabilities. Research shows that accessible design benefits all users, not just those with disabilities.'
        },
        {
            'group_name': 'Team Gamma',
            'title': 'Virtual Reality in Education',
            'abstract': 'This research explores the potential of virtual reality technology in educational settings. The study examines how VR can enhance learning experiences and improve student engagement in various subjects.',
            'member1_name': 'Carol Davis',
            'member2_name': 'David Brown',
            'paper1_title': 'VR in Educational Contexts: A Meta-Analysis',
            'paper2_title': 'Immersive Learning Environments: Design and Implementation',
            'presentation_video_url': 'https://www.youtube.com/watch?v=example3',
            'literature_review': 'The literature review investigates the current state of VR technology in education, examining case studies and research findings. Results indicate significant potential for improving student engagement and knowledge retention.'
        }
    ]
    
    for project_data in sample_projects:
        project = ResearchProject(**project_data)
        db.session.add(project)
    
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)

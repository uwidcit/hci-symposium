# COMP 3603 Research Symposium - Virtual Research Gallery

A Flask-based web application for hosting a virtual research symposium showcasing student research projects in Human-Computer Interaction. This application provides an admin interface for managing research projects and a public gallery for viewing research presentations.

## Features

### Public Features
- **Landing Page**: Attractive homepage introducing the symposium
- **Research Gallery**: Grid view of all research groups and their papers
- **Project Details**: Individual project pages showing student-paper associations
- **Media Access**: Preview and download combined slide decks and posters (PDF)
- **Similar Projects**: Discover related research based on tags
- **Responsive Design**: Modern, mobile-friendly interface

### Admin Features
- **Dashboard**: Overview of all research projects with statistics
- **CSV Upload**: Bulk import of research project data
- **Project Management**: Add, edit, and delete research projects
- **Media Upload**: Upload combined slide decks and posters (PDF)
- **Tags Management**: Categorize projects for better discovery
- **User Authentication**: Secure admin login system

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLAlchemy with SQLite
- **Frontend**: Bootstrap 5 + Font Awesome icons
- **Authentication**: Flask-Login
- **File Handling**: Werkzeug file uploads
- **Data Processing**: Pandas for CSV handling

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Clone or Download
```bash
# If using git
git clone <repository-url>
cd gallery

# Or download and extract the ZIP file
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Initialize the Database
```bash
flask init
```

This command will:
- **Delete existing database** (if it exists) for a fresh start
- Create the database and tables
- Create admin user "bob" with password "bobpass"
- Insert sample research projects

### Step 4: Run the Application
```bash
flask run
```

The application will start on `http://localhost:5000`

## Default Admin Credentials

- **Username**: `bob`
- **Password**: `bobpass`

**Important**: Change these credentials in production!

## Usage Guide

### For Administrators

#### 1. Initial Setup
1. Start the application
2. Login with admin credentials
3. Navigate to the admin dashboard

#### 2. Adding Research Projects via CSV
1. Prepare a CSV file with the required columns (see sample below)
2. Go to "Upload CSV" in the admin menu
3. Select your CSV file and upload
4. Review the imported projects

#### 3. Managing Individual Projects
1. From the admin dashboard, click the edit button for any project
2. Update project information
3. Upload poster PDFs and video files
4. Save changes

#### 4. Adding Media Files
- **Combined Slide Decks**: PDF with both students' presentations combined
- **Combined Posters**: PDF with both students' posters combined
- **Video Presentations**: YouTube or other video URLs
- **Tags**: Comma-separated tags for categorizing and finding similar projects
- Files are automatically organized in the uploads directory

### For Visitors

#### 1. Browsing Research
1. Visit the homepage to learn about the symposium
2. Click "Explore Research Gallery" to view all projects
3. Click on any project to see detailed information

#### 2. Accessing Resources
- Preview and download combined slide decks (both students' presentations in one PDF)
- Preview and download combined posters (both students' posters in one PDF)
- Watch video presentations
- See which paper each student worked on
- Discover similar projects based on tags
- Browse projects by research focus areas

## Project Structure

### Research Groups
- Each research group consists of **2 students** working together
- Each group produces **2 research papers** (one per student)
- Students are clearly associated with their specific papers
- Groups are identified by their **group name** (e.g., "Team Alpha", "Team Beta")

### Media Files
- **Combined Slide Decks**: Single PDF containing both students' presentation slides
- **Combined Posters**: Single PDF containing both students' research posters
- **Video Presentations**: Optional video URLs for additional content

### Tags System
- Projects can be tagged with relevant keywords
- Tags enable discovery of similar research projects
- Examples: "mobile", "ui design", "accessibility", "virtual reality", "education"

## CSV Format Requirements

### Required Columns
- `group_name`: Research group name
- `member1_name`: First team member
- `member2_name`: Second team member
- `paper1_title`: First paper title
- `paper2_title`: Second paper title

### Optional Columns
- `member1_paper`: Which paper member1 worked on (defaults to paper1_title if not specified)
- `member2_paper`: Which paper member2 worked on (defaults to paper2_title if not specified)
- `presentation_video_url`: URL to presentation video
- `tags`: Comma-separated tags for categorizing and finding similar projects

### Sample CSV
```csv
group_name,member1_name,member2_name,paper1_title,paper2_title,member1_paper,member2_paper,presentation_video_url,tags
"Team Alpha","Member 1","Member 2","Paper 1 Title","Paper 2 Title","Paper 1 Title","Paper 2 Title","https://youtube.com/...","mobile, ui design, accessibility"
```

## Sample Data

The system includes sample research projects that demonstrate the structure:

- **Team Alpha**: Mobile UI Design research
  - Papers: "Mobile UI Design Patterns" and "User Experience Optimization"
  - Tags: mobile, ui design, user experience, interface

- **Team Beta**: Web Accessibility research  
  - Papers: "Web Accessibility Implementation" and "Inclusive Design Principles"
  - Tags: accessibility, web design, inclusive design, ui design

- **Team Gamma**: Virtual Reality in Education research
  - Papers: "VR in Educational Contexts" and "Immersive Learning Environments"
  - Tags: virtual reality, education, immersive learning, technology

Each sample project includes student-paper associations, combined media files, and relevant tags for discovery.

## File Structure

```
gallery/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── uploads/               # File uploads (auto-created)
│   ├── posters/          # Combined poster PDFs
│   ├── presentations/    # Combined slide deck PDFs
│   └── group_files/      # Additional group files
├── instance/             # Database files (auto-created)
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Landing page
│   ├── gallery.html      # Research gallery
│   ├── view_project.html # Individual project view
│   ├── login.html        # Admin login
│   ├── admin_dashboard.html # Admin dashboard
│   ├── upload_csv.html   # CSV upload form
│   └── edit_project.html # Project editing form
└── uploads/              # File uploads (created automatically)
    ├── posters/          # PDF posters
    └── videos/           # Video presentations
```

## Customization

### Styling
- Modify CSS variables in `templates/base.html`
- Update Bootstrap classes for different layouts
- Customize Font Awesome icons

### Database
- Change database URI in `app.py` for different databases
- Modify models in the `ResearchProject` class
- Add new fields as needed

### Features
- Add new routes in `app.py`
- Create new templates in the `templates/` directory
- Extend admin functionality

## Security Considerations

- Change default admin credentials
- Update `SECRET_KEY` in production
- Implement proper user authentication for production
- Add rate limiting for file uploads
- Validate file types and sizes
- **`flask init` will delete any existing database** - use with caution in production
- Media files are stored in the `uploads/` directory
- Combined PDFs should contain both students' work in a single file
- Tags are comma-separated and used for finding similar projects

## Production Deployment

### Recommended Steps
1. Use a production WSGI server (Gunicorn, uWSGI)
2. Set up a reverse proxy (Nginx, Apache)
3. Use environment variables for configuration
4. Implement proper logging
5. Set up database backups
6. Use HTTPS with SSL certificates

### Environment Variables
The application uses a `.flaskenv` file for configuration. You can also create a `.env` file for additional customization:

```bash
# Copy the example file
cp env_example.txt .env

# Edit .env with your settings
nano .env
```

Key environment variables:
- `FLASK_APP`: Flask application entry point
- `SECRET_KEY`: Secret key for sessions and security
- `DATABASE_URL`: Database connection string
- `ADMIN_USERNAME`: Admin username (default: bob)
- `ADMIN_PASSWORD`: Admin password (default: bobpass)

For production:
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secure-secret-key
export DATABASE_URL=your-database-url
export ADMIN_USERNAME=your-admin-username
export ADMIN_PASSWORD=your-secure-password
```

## Troubleshooting

### Common Issues

#### Database Errors
- Ensure the application has write permissions
- Check if the database file is accessible
- Verify SQLite is working properly

#### File Upload Issues
- Check file size limits (default: 16MB)
- Verify file formats are supported
- Ensure upload directories have proper permissions

#### Template Errors
- Verify all template files are in the `templates/` directory
- Check for syntax errors in Jinja2 templates
- Ensure template inheritance is correct

### Getting Help
1. Check the console output for error messages
2. Verify all dependencies are installed
3. Ensure file permissions are correct
4. Check the Flask debug output

## Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is created for educational purposes as part of COMP 3603 Human-Computer Interaction course.

## Support

For technical support or questions about this application, please contact your course instructor or refer to the course materials.

---

**Note**: This application is designed for educational use and should be properly secured before use in production environments.

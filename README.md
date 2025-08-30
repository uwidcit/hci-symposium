# COMP 3603 Research Symposium - Virtual Research Gallery

A Flask-based web application for hosting a virtual research symposium showcasing student research projects in Human-Computer Interaction. This application provides an admin interface for managing research projects and a public gallery for viewing research presentations.

## Features

### Public Features
- **Landing Page**: Attractive homepage introducing the symposium
- **Research Gallery**: Grid view of all research projects
- **Project Details**: Individual project pages with full information
- **Media Access**: Download posters (PDF) and watch video presentations
- **Responsive Design**: Modern, mobile-friendly interface

### Admin Features
- **Dashboard**: Overview of all research projects with statistics
- **CSV Upload**: Bulk import of research project data
- **Project Management**: Add, edit, and delete research projects
- **Media Upload**: Upload poster PDFs and video presentations
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
- **Posters**: PDF format only
- **Videos**: MP4, AVI, or MOV formats
- Files are automatically organized in the uploads directory

### For Visitors

#### 1. Browsing Research
1. Visit the homepage to learn about the symposium
2. Click "Explore Research Gallery" to view all projects
3. Click on any project to see detailed information

#### 2. Accessing Resources
- Download research posters as PDFs
- Watch video presentations
- Read literature reviews and abstracts

## CSV Format Requirements

### Required Columns
- `group_name`: Research group name
- `title`: Research project title
- `abstract`: Project abstract/summary
- `member1_name`: First team member
- `member2_name`: Second team member
- `paper1_title`: First paper title
- `paper2_title`: Second paper title

### Optional Columns
- `presentation_video_url`: URL to presentation video
- `literature_review`: Literature review content

### Sample CSV
```csv
group_name,title,abstract,member1_name,member2_name,paper1_title,paper2_title,presentation_video_url,literature_review
"Team Alpha","Project Title","Abstract text...","Member 1","Member 2","Paper 1 Title","Paper 2 Title","https://youtube.com/...","Literature review..."
```

## File Structure

```
gallery/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── sample_data.csv       # Example CSV data
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

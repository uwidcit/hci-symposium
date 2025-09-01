# Quick Start Guide - COMP 3603 Research Symposium

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize the Database
```bash
flask init
```
This will:
- **Delete existing database** (if it exists) for a fresh start
- Create the database and tables
- Create admin user "bob" with password "bobpass"
- Insert sample research projects

### 2.5. Upload Group Files (Optional)
```bash
flask upload-group-files /path/to/group/files/directory
```
This will:
- Upload poster PDFs and presentation PDFs from organized group folders
- Automatically match files to projects based on group names
- See `group_files_example/README.md` for directory structure

### 3. Start the Application
**Option A: Using Flask CLI (Recommended)**
```bash
flask run
```

**Option B: Using the batch file (Windows)**
```bash
start.bat
```

**Option C: Using Python directly**
```bash
python run.py
```

### 4. Access the Application
- **Main Site**: http://localhost:5000
- **Admin Login**: http://localhost:5000/login
- **Research Gallery**: http://localhost:5000/gallery

## 🔑 Default Admin Credentials
- **Username**: `bob`
- **Password**: `bobpass`

## 📊 Sample Data
Use the included `sample_data.csv` file to test the CSV upload functionality:
1. Login as admin
2. Go to "Upload CSV"
3. Select `sample_data.csv`
4. Upload and view the imported projects

## 🎯 What You Can Do

### As an Admin:
- Upload research projects via CSV
- Edit individual projects
- Upload poster PDFs and videos
- Manage all symposium content

### As a Visitor:
- Browse the research gallery
- View project details
- Download research posters
- Watch video presentations
- Read literature reviews

## 🛠️ File Structure
```
gallery/
├── app.py              # Main application
├── config.py           # Configuration settings
├── run.py              # Startup script
├── start.bat           # Windows startup
├── requirements.txt    # Python dependencies
├── sample_data.csv     # Example data
├── templates/          # HTML templates
└── uploads/            # File uploads (auto-created)
```

## 🔧 Customization
- Modify `config.py` for different settings
- Update CSS in `templates/base.html`
- Add new features in `app.py`

## 📝 CSV Format
Required columns: `group_name`, `member1_name`, `member2_name`, `paper1_title`, `paper2_title`
Optional columns: `member1_paper`, `member2_paper`, `presentation_video_url`, `tags`

## 🚨 Important Notes
- Change default admin credentials in production
- Update `SECRET_KEY` in production
- The application creates necessary directories automatically
- SQLite database is created on first run

## 🆘 Need Help?
- Check the console for error messages
- Verify all dependencies are installed
- Read the full `README.md` for detailed information
- Ensure Python 3.7+ is installed

---

**Ready to showcase your research symposium! 🎓**

#!/usr/bin/env python3
"""
Startup script for COMP 3603 Research Symposium
"""

import os
from app import app

if __name__ == '__main__':
    print("=" * 60)
    print("COMP 3603 Research Symposium - Virtual Research Gallery")
    print("=" * 60)
    print(f"Admin Username: {app.config['ADMIN_USERNAME']}")
    print(f"Admin Password: {app.config['ADMIN_PASSWORD']}")
    print("=" * 60)
    print("Starting application...")
    print("Access the application at: http://localhost:5000")
    print("Admin login at: http://localhost:5000/login")
    print("=" * 60)
    print("Note: Use 'flask run' for development or 'flask init' to initialize database")
    print("=" * 60)
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)

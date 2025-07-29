# run.py

import os
from dotenv import load_dotenv
from app import create_app

# Load environment variables from .env file
load_dotenv()

# Create Flask app with development config
app = create_app('development')

if __name__ == '__main__':
    with app.app_context():
        from app.models import db
        from app.operations import populate_treatments  # Optional: only if this function exists and is needed
        
        # Create all tables
        db.create_all()

        # Optional: Pre-populate treatments
        try:
            populate_treatments()
        except Exception as e:
            print(f"Failed to populate treatments: {e}")
    
    # Run the app
    app.run(host='0.0.0.0', port=5000,debug=True)

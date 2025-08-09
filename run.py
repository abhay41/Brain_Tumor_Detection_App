import os
from dotenv import load_dotenv
from app import create_app, db
from app.operations import populate_treatments  # If you have this function

load_dotenv()

env = os.getenv('FLASK_ENV', 'production').lower()
app = create_app(env)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        try:
            populate_treatments()
        except Exception as e:
            print(f"Failed to populate treatments: {e}")

    app.run(host='0.0.0.0', port=5000, debug=(env == 'development'))

# app/__init__.py
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import os
from .admin_routes import admin_bp

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name='development'):
    app = Flask(__name__)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    # Load configuration directly
    if config_name == 'development':
        from app.config import DevelopmentConfig
        app.config.from_object(DevelopmentConfig)
    elif config_name == 'testing':
        from app.config import TestingConfig
        app.config.from_object(TestingConfig)
    else:
        from app.config import ProductionConfig
        app.config.from_object(ProductionConfig)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    login_manager.login_view = 'login'
    

    # Allow non-ASCII characters in JSON responses
    app.config['JSON_AS_ASCII'] = False

    # User loader function
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register routes
    from .route import configure_routes
    from.admin_routes import configure_admin_routes
    configure_admin_routes(app)
    configure_routes(app)

    return app
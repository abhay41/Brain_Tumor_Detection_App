# Medical Tumor Analysis Application - Database Models

"""
Database Models for Tumor Classification and Patient Management System

This module defines the database schema and relationships using SQLAlchemy and Flask-Login.
It provides three main models: User, Treatment, and Patient, facilitating user authentication, 
treatment information, and patient record management.

Key Features:
- Secure user authentication with password hashing
- Relationships between users and patients
- Comprehensive patient and treatment information storage
- Flexible database schema for medical record management

Dependencies:
- Flask-SQLAlchemy for ORM (Object-Relational Mapping)
- Flask-Login for user authentication
- Werkzeug for password security
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import random
import string

# Initialize SQLAlchemy database instance
db = SQLAlchemy()

class User(UserMixin, db.Model):
    """
    User model for authentication and profile management

    Attributes:
    - id: Unique identifier for the user
    - username: Unique username for login
    - email: User's email address (unique)
    - password_hash: Securely hashed password
    - profile_image: Optional profile image path
    - patients: Relationship to patient records created by the user

    Methods:
    - set_password(): Securely hash and store user password
    - check_password(): Verify user password during login
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    profile_image = db.Column(db.String(200), nullable=True)
    is_locked = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    verification_code = db.Column(db.String(6), nullable=True)
    verification_timestamp = db.Column(db.DateTime, nullable=True)
    patients = db.relationship('Patient', backref='user', lazy=True)



    def generate_verification_code(self):
        self.verification_code = ''.join(random.choices(string.digits, k=6))
        self.verification_timestamp = datetime.utcnow()
        db.session.commit()
        return self.verification_code



    # One-to-Many relationship with Patient model

    def set_password(self, password):
        """
        Generate and store a secure password hash
        
        Args:
            password (str): Plain text password
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Verify user password against stored hash
        
        Args:
            password (str): Plain text password to verify
        
        Returns:
            bool: True if password is correct, False otherwise
        """
        return check_password_hash(self.password_hash, password)

class Treatment(db.Model):
    """
    Treatment model for storing tumor treatment information

    Attributes:
    - id: Unique treatment identifier
    - tumor_type: Type of tumor
    - description: Detailed treatment description
    - recommended_medication: Suggested medications
    - duration: Treatment duration
    - side_effects: Potential treatment side effects

    Methods:
    - to_dict(): Convert treatment data to dictionary for easy serialization
    """
    id = db.Column(db.Integer, primary_key=True)
    tumor_type = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    recommended_medication = db.Column(db.String(120))
    duration = db.Column(db.String(50))
    side_effects = db.Column(db.Text)
    
    def to_dict(self):
        """
        Serialize treatment data to a dictionary

        Returns:
            dict: Treatment information as a dictionary
        """
        return {
            'id': self.id,
            'tumor_type': self.tumor_type,
            'description': self.description,
            'recommended_medication': self.recommended_medication,
            'duration': self.duration,
            'side_effects': self.side_effects,
        }

class Patient(db.Model):
    """
    Patient model for storing individual patient medical records

    Attributes:
    - id: Unique patient identifier
    - name: Patient's full name
    - age: Patient's age
    - gender: Patient's gender
    - tumor_type: Predicted or diagnosed tumor type
    - diagnosis_date: Date of tumor diagnosis
    - image_path: Path to patient's medical imaging file
    - user_id: Foreign key linking to the User who created the record

    Relationships:
    - Belongs to a specific User (many-to-one relationship)
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    tumor_type = db.Column(db.String(80), nullable=True)  # Stores predicted tumor type
    diagnosis_date = db.Column(db.Date, nullable=False)
    image_path = db.Column(db.String(200), nullable=True)  # Medical image file path
    
    # Foreign key relationship with User model
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Commented out potential Treatment relationship
    # treatment_id = db.Column(db.Integer, db.ForeignKey('treatment.id'), nullable=True)
"""
Database Design Considerations:
1. Secure password storage using hash
2. Flexible patient and treatment record management
3. User-patient relationship for access control
4. Support for medical image storage

Potential Improvements:
- Add more validation methods
- Implement more complex relationships
- Add additional fields for comprehensive medical tracking
"""

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class UserLogin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    success = db.Column(db.Boolean, default=True)
    user = db.relationship('User', backref=db.backref('login_attempts', lazy=True))

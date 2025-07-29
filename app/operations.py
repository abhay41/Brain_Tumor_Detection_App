# Database Operations for Medical Tumor Classification Application

"""
Comprehensive Database Interaction Module

This module provides core database operations for user management, 
treatment tracking, and patient record management.

Key Functionality:
- User registration and authentication
- Treatment information management
- Patient record creation and tracking

"""

from .models import db, User, Treatment, Patient,Admin
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'test292907@gmail.com'
SENDER_PASSWORD = 'rteh pyqu jitz osqq'

def send_verification_email(recipient_email, verification_code):
    """Send a verification email to the user."""
    msg = MIMEText(f"Your verification code is: {verification_code}")
    msg['Subject'] = 'Verify your account'
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
    except smtplib.SMTPException as e:
        # app.logger.error(f"Error sending verification email: {str(e)}")
        raise Exception("Error sending verification email")
    
    
def add_user(username, email, password):
    """
    Register a new user in the system
    
    Args:
        username (str): Unique username
        email (str): User's email address
        password (str): User's password
    
    Returns:
        User: Newly created user object or None if user already exists
    """
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return None
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_user_by_username(username):
    """
    Retrieve user by username
    
    Args:
        username (str): Username to search
    
    Returns:
        User: User object if found, None otherwise
    """
    return User.query.filter_by(username=username).first()

def add_treatment(tumor_type, description, recommended_medication, duration, side_effects):
    """
    Add a new treatment protocol to the database
    
    Args:
        tumor_type (str): Type of tumor
        description (str): Treatment description
        recommended_medication (str): Suggested medications
        duration (str): Treatment duration
        side_effects (str): Potential side effects
    
    Returns:
        Treatment: Newly created treatment object
    """
    new_treatment = Treatment(
        tumor_type=tumor_type,
        description=description,
        recommended_medication=recommended_medication,
        duration=duration,
        side_effects=side_effects
    )
    db.session.add(new_treatment)
    db.session.commit()
    return new_treatment

def get_treatment_by_tumor_type(tumor_type):
    """
    Retrieve treatment protocol for a specific tumor type
    
    Args:
        tumor_type (str): Tumor type to search
    
    Returns:
        Treatment: Treatment object if found, None otherwise
    """
    return Treatment.query.filter_by(tumor_type=tumor_type).first()

def add_patient(name, age, gender, prediction, diagnosis_date, filepath, user_id):
    """
    Add a new patient record to the database
    
    Args:
        name (str): Patient's full name
        age (int): Patient's age
        gender (str): Patient's gender
        prediction (str): Predicted tumor type
        diagnosis_date (date): Date of diagnosis
        filepath (str): Path to medical image
        user_id (int): ID of the user adding the record
    
    Returns:
        Patient: Newly created patient record
    """
    new_patient = Patient(
        name=name,
        age=age,
        gender=gender,
        tumor_type=prediction, 
        diagnosis_date=diagnosis_date,
        image_path=filepath,
        user_id=user_id
    )

    db.session.add(new_patient)
    db.session.commit()
    return new_patient



def update_user_profile(user_id, new_username=None, new_email=None, new_profile_image=None, new_password=None):
    """
    Update user profile information.
    
    Args:
        user_id (int): User's unique identifier.
        new_username (str, optional): New username.
        new_email (str, optional): New email address.
        new_profile_image (str, optional): New profile image path.
        new_password (str, optional): New password.
    
    Returns:
        tuple: (bool, User or str) True and the updated User object on success,
               False and an error message on failure.
    """
    try:
        user = User.query.get(user_id)
        if not user:
            return False, "User not found."

        # Update fields if new values are provided
        if new_username:
            # Optional: Check if the new username is unique
            if User.query.filter_by(username=new_username).first() and user.username != new_username:
                return False, "Username already taken."
            user.username = new_username
        
        if new_email:
            # Optional: Check if the new email is unique
            if User.query.filter_by(email=new_email).first() and user.email != new_email:
                return False, "Email already in use."
            user.email = new_email
        
        if new_profile_image:
            user.profile_image = new_profile_image
        
        if new_password:
            user.set_password(new_password)  #  `set_password` hashes the password

        db.session.commit()
        return True, user

    except SQLAlchemyError as e:
        db.session.rollback()  # Roll back if there's an error
        return False, f"Database error: {str(e)}"
    except Exception as e:
        return False, f"An unexpected error occurred: {str(e)}"
    
def change_admin_password(admin_id, new_password):
    try:
        # Corrected filter_by syntax: use `filter_by(id=admin_id)`
        admin = Admin.query.filter_by(id=admin_id).first()
        
        if not admin:
            return False, "Admin not found."

        if new_password:
            admin.set_password(new_password)  # `set_password` should handle hashing

        db.session.commit()
        return True, admin

    except SQLAlchemyError as e:
        db.session.rollback()  # Roll back if there's an error
        return False, f"Database error: {str(e)}"
    except Exception as e:
        return False, f"An unexpected error occurred: {str(e)}"



def get_patient_by_user(user_id):
    """
    Retrieve all patients associated with a specific user
    
    Args:
        user_id (int): User's unique identifier
    
    Returns:
        list: List of patient records
    """
    return Patient.query.filter_by(user_id=user_id).all()

def delete_patient_record(patient_id, user_id):
    """
    Delete a patient record (with user authorization)
    
    Args:
        patient_id (int): Patient record ID
        user_id (int): User ID for authorization
    
    Returns:
        bool: True if deletion successful, False otherwise
    """
    patient = Patient.query.filter_by(id=patient_id, user_id=user_id).first()
    if patient:
        db.session.delete(patient)
        db.session.commit()
        return True
    return False

def get_patients_by_tumor_type(tumor_type):
    """
    Retrieve patients with a specific tumor type
    
    Args:
        tumor_type (str): Tumor type to filter
    
    Returns:
        list: List of patients with matching tumor type
    """
    return Patient.query.filter_by(tumor_type=tumor_type).all()

def generate_patient_statistics():
    """
    Generate basic patient statistics
    
    Returns:
        dict: Statistical information about patients
    """
    total_patients = Patient.query.count()
    tumor_type_distribution = db.session.query(
        Patient.tumor_type, 
        db.func.count(Patient.id)
    ).group_by(Patient.tumor_type).all()
    
    return {
        'total_patients': total_patients,
        'tumor_type_distribution': dict(tumor_type_distribution)
    }

def populate_treatments():
    # Check if the table is empty
    if Treatment.query.first() is None:
        treatments = [
            Treatment(
                tumor_type="Glioma",
                description="""A malignant type of brain tumor that begins in glial cells. Common subtypes include astrocytomas, oligodendrogliomas, and ependymomas. 
                Treatment approach varies based on grade (I-IV), location, and genetic markers like IDH mutation and 1p/19q codeletion status. 
                Primary treatment often includes maximal safe surgical resection followed by concurrent chemoradiation.""",
                recommended_medication="""First-line: Temozolomide (150-200mg/m² for 5 days every 28 days)
                Second-line: Bevacizumab (10mg/kg every 2 weeks)
                Supportive medications: Dexamethasone for edema, Levetiracetam for seizure prophylaxis
                Alternative options: Lomustine, Carmustine wafers""",
                duration="""Initial treatment: 6 weeks of concurrent chemoradiation
                Adjuvant chemotherapy: 6-12 monthly cycles
                Follow-up: Every 3-4 months for 2-3 years, then every 6 months""",
                side_effects="""Common: Fatigue, nausea, vomiting, decreased appetite, bone marrow suppression
                Neurological: Seizures, headaches, cognitive changes
                Radiation-related: Hair loss, skin irritation, brain swelling
                Long-term: Memory issues, endocrine dysfunction
                Bevacizumab-specific: Hypertension, wound healing problems, blood clots"""
            ),
            Treatment(
                tumor_type="Meningioma",
                description="""Typically benign tumors arising from the meninges. Classified by WHO grades I-III, with Grade I being most common (80%).
                Location variants include parasagittal, convexity, sphenoid wing, and posterior fossa meningiomas.
                Treatment strategy depends on size, location, growth rate, and symptoms.
                Some cases may be managed with observation alone (watch and wait approach).""",
                recommended_medication="""Primary treatment is usually surgical
                Anticonvulsants: Levetiracetam (500-1000mg twice daily) or Phenytoin if seizures present
                Steroids: Dexamethasone (4-16mg/day) for peritumoral edema
                Hormone therapy: For progesterone receptor-positive cases in select situations""",
                duration="""Surgery recovery: 4-8 weeks
                Radiation therapy (if needed): 5-6 weeks
                Follow-up: Every 3-6 months initially, then annually
                Total monitoring duration: 5-10 years depending on grade""",
                side_effects="""Surgical: Infection risk, bleeding, CSF leak, neurological deficits
                Radiation-related: Fatigue, local hair loss, skin changes, cognitive effects
                Location-specific: Visual problems, hearing loss, facial numbness
                Long-term: Seizures, headaches, cognitive changes
                Medication-related: Liver enzyme elevation, bone density changes"""
            ),
            Treatment(
                tumor_type="No Tumor",
                description="""Absence of neoplastic growth in brain tissue confirmed through imaging studies (MRI/CT).
                May still require monitoring if patient has risk factors or concerning symptoms.
                Focus on preventive care and addressing any underlying neurological symptoms.
                Important to establish reason for initial imaging and ensure appropriate follow-up.""",
                recommended_medication="""Symptomatic treatment as needed:
                Headache management: NSAIDs or specific migraine medications
                Preventive medications based on risk factors
                Regular health maintenance as per age-appropriate guidelines""",
                duration="""Initial follow-up: 6 months
                Long-term monitoring: Annual clinical check-ups
                Repeat imaging only if new symptoms develop
                Duration of monitoring based on initial presentation cause""",
                side_effects="""No treatment-specific side effects
                Monitor for any new neurological symptoms
                Regular assessment of risk factors
                Psychological support may be needed for anxiety management"""
            ),
            Treatment(
                tumor_type="Pituitary",
                description="""Tumors arising from the pituitary gland, classified as functional (hormone-secreting) or non-functional.
                Common variants include prolactinomas, growth hormone-secreting, ACTH-secreting, and non-functioning adenomas.
                Treatment approach depends on tumor size (micro vs. macro), hormone status, and visual compromise.
                May affect multiple endocrine systems requiring comprehensive hormonal evaluation.""",
                recommended_medication="""Prolactinomas: Cabergoline (0.25-2mg twice weekly) or Bromocriptine (2.5-15mg daily)
                Acromegaly: Octreotide (100-500mcg 3x daily), Lanreotide, Pegvisomant
                Cushing's Disease: Ketoconazole, Metyrapone, Pasireotide
                Hormone replacement: Levothyroxine, Hydrocortisone, Sex hormones as needed""",
                duration="""Medical therapy: Ongoing, often lifelong
                Surgical recovery: 4-6 weeks
                Radiation therapy (if needed): 4-6 weeks
                Follow-up: Monthly initially, then every 3-6 months
                Hormonal monitoring: Lifelong""",
                side_effects="""Medication-specific: Nausea, dizziness, fatigue, mood changes
                Surgical: Diabetes insipidus, CSF leak, hormone deficiencies
                Endocrine: Weight changes, sexual dysfunction, mood disorders
                Visual: Vision changes, double vision
                Long-term: Need for hormone replacement, metabolic changes"""
            )
        ]

        try:
            # Add all treatments to the database
            db.session.add_all(treatments)
            db.session.commit()
            print("Treatment data successfully populated!")
        except Exception as e:
            db.session.rollback()
            print(f"Error populating treatment data: {str(e)}")
    else:
        print("Treatment table already contains data. Skipping population.")

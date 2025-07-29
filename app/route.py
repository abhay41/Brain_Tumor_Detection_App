from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
import os
from datetime import datetime
from .models import User, Treatment, Patient,UserLogin
from .operations import add_user, get_user_by_username, add_treatment, get_treatment_by_tumor_type, add_patient,update_user_profile,send_verification_email
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import traceback
from .form import ProfileImageForm
from .models import db

from flask import Blueprint, render_template, request, redirect, url_for, flash, session


# Load Pre-trained Machine Learning Model
# This line loads a pre-trained neural network model for brain tumor classification
# Get the absolute path to the model file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'brains.h5')

# Load the model
try:
    model = load_model(MODEL_PATH)
    print(f"Model loaded successfully from {MODEL_PATH}")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None



def configure_routes(app):
    """
    Configure routes for the Flask application.

    Args:
        app: The Flask application instance.

    Returns:
        None
    """
    
    @app.route('/')
    def home():
        """Render the home page."""
        try:
            return render_template('home.html')
        except Exception as e:
            flash("Error loading home page.", "error")
            app.logger.error(f"Error in home route: {str(e)}")
            return render_template('error.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """Handle user login.
        
        On POST request, validate user credentials and log the user in.
        Log each login attempt in the UserLogin model.
        On GET request, render the login form.
        """
        if request.method != 'POST':
            return render_template('login.html')
            
        try:
            username = request.form['username']
            password = request.form['password']
            
            if not username or not password:
                flash('Username and password are required', 'error')
                return render_template('login.html')

            user = get_user_by_username(username)
            login_successful = False
            
            if user and user.check_password(password):
                if user.is_locked == True:
                    flash('This account is locked by admin.','error')
                    return render_template('login.html')
                login_user(user)
                login_successful = True
                
            # Log the attempt regardless of outcome
            login_attempt = UserLogin(
                user_id=user.id if user else None,
                timestamp=datetime.utcnow(),
                success=login_successful
            )
            db.session.add(login_attempt)
            db.session.commit()
                
            if login_successful:
                return redirect(url_for('dashboard'))
                
            flash('Invalid username or password', 'error')
            return render_template('login.html')
                
        except Exception as e:
            db.session.rollback()  # Roll back any failed transaction
            app.logger.error(f"Error in login route: {str(e)}")
            flash("An error occurred during login. Please try again.", "error")
            return render_template('login.html')
        
    @app.route('/logout')
    @login_required
    def logout():
        """Log the user out and redirect to home."""
        try:
            # success = False
            logout_user()   
            # success =True        
            # login_attempt = UserLogin(
            #     user_id=user.id if user else None,  # Set user_id if user exists
            #     timestamp=datetime.utcnow(),
            #     success=success
            #     )
            
            flash("You have been logged out.", "success")
            return redirect(url_for('home'))
        except Exception as e:
            flash("Error during logout.", "error")
            app.logger.error(f"Error in logout route: {str(e)}")
            return render_template('error.html')



    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """Handle user registration.

        On POST request, create a new user, send a verification email, and redirect to the verification page.
        On GET request, render the registration form.
        """
        try:
            if request.method == 'POST':
                username = request.form['username']
                email = request.form['email']
                password = request.form['password']

                # Check if the user already exists
                user = User.query.filter_by(username=username, email=email).first()
                if user:
                    flash('Username or email already exists', 'error')
                    return render_template('register.html')

                # Create a new user
                user = add_user(username, email, password)

                # Generate a verification code and send the verification email
                verification_code = user.generate_verification_code()
                send_verification_email(email, verification_code)

                flash('Registration successful. Please check your email for a verification code.', 'success')
                return redirect(url_for('verify', user_id=user.id))

            return render_template('register.html')
        except Exception as e:
            flash("Error during registration.", "error")
            app.logger.error(f"Error in register route: {str(e)}")
            return render_template('error.html')
        

    @app.route('/sendemail/<int:user_id>')
    def sendemail(user_id):
        """Resend the verification email to the user."""
        user = User.query.filter_by(id=user_id).first()

        if user:
            # Generate a new verification code (assuming `generate_verification_code` updates the user model)
            verification_code = user.generate_verification_code()
            db.session.commit()  # Save the new code if `generate_verification_code` modifies the user record
            
            # Send the email
            send_verification_email(user.email, verification_code)
            
            flash("Verification email sent again. Please check your email.", "info")
            return redirect(url_for('verify', user_id=user_id))
        else:
            flash("User not found.", "error")
            return redirect(url_for('home'))  # Redirect to a safe fallback route, e.g., 'home'


    

    @app.route('/verify/<int:user_id>', methods=['GET', 'POST'])
    def verify(user_id):
        """Handle user verification.

        On POST request, verify the user's email and redirect to the login page.
        On GET request, render the verification form.
        """
        if request.method == 'POST':
            # Fetch the user by ID
            user = User.query.filter_by(id=user_id).first()
            
            # Get the verification code from the form
            verification_code = request.form['verification_code']
            
            # Check if the user exists and the code matches
            if user and user.verification_code == verification_code:
                user.is_verified = True
                db.session.commit()
                flash('Email verified successfully .', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid verification code.', 'error')

        return render_template('verify.html')


    @app.route('/dashboard')
    @login_required
    def dashboard():
        """Render the dashboard page for logged-in users."""
        try:
            return render_template('dashboard.html')
        except Exception as e:
            flash("Error loading dashboard.", "error")
            app.logger.error(f"Error in dashboard route: {str(e)}")
            return render_template('error.html')

    @app.route('/predict', methods=['GET', 'POST'])
    @login_required
    def predict():
        """Handle image prediction for brain tumors.
        
        On POST request, receive image file, process it, and predict tumor type.
        On GET request, render the prediction form.
        """
        if request.method == 'POST':
            try:
                # Check if a file is included in the request
                if 'file' not in request.files:
                    flash("No file part.", "error")
                    return redirect(request.url)
                file = request.files['file']
                if file.filename == '':
                    flash("No selected file.", "error")
                    return redirect(request.url)

                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)

                # Process the image and get the prediction
                try:
                    prediction, confidence = predict_image(filepath)
                except Exception as e:
                    flash("Error during image prediction.", "error")
                    app.logger.error(f"Error in predict_image: {str(e)}")
                    return render_template('error.html')

                # Get treatment by tumor type
                treatment_instance = get_treatment_by_tumor_type(prediction)
                treatment_data = treatment_instance.to_dict() if treatment_instance else None

                # Save patient data
                try:
                    name = request.form['name']
                    age = request.form['age']
                    gender = request.form['gender']
                    diagnosis_date = datetime.strptime(request.form['diagnosis_date'], '%Y-%m-%d').date()
                    user_id = current_user.id
                    add_patient(name, age, gender, prediction, diagnosis_date, filepath, user_id)
                except Exception as e:
                    flash("Error saving patient data.", "error")
                    app.logger.error(f"Error in add_patient: {str(e)}")
                    return render_template('error.html')

                return jsonify({
                    'prediction': prediction,
                    'confidence': confidence,
                    'treatment': treatment_data
                })
            except Exception as e:
                flash("An unexpected error occurred.", "error")
                app.logger.error(f"Unexpected error: {str(e)}")
                return render_template('error.html')
        return render_template('predict.html')

    @app.route('/patients')
    @login_required
    def patients_list():
        """Render the list of patients."""
        try:
            patients = Patient.query.all()
            return render_template('patients.html', patients=patients)
        except Exception as e:
            flash("Error loading patient list.", "error")
            app.logger.error(f"Error in patients_list route: {str(e)}")
            return render_template('error.html')

    @app.route('/about')
    def about():
        """Render the about page."""
        try:
            return render_template("about.html")
        except Exception as e:
            flash("Error loading about page.", "error")
            app.logger.error(f"Error in about route: {str(e)}")
            return render_template('error.html')

    @app.route('/profile')
    @login_required
    def profile():
        """Render the user's profile page."""
        try:
            return render_template("profile.html")
        except Exception as e:
            flash("Error loading profile page.", "error")
            app.logger.error(f"Error in profile route: {str(e)}")
            return render_template('error.html')


    @app.route('/profile-image', methods=['GET', 'POST'])
    @login_required
    def profile_image():
        """Handle profile image upload.
        
        On POST request, save the new profile image and update the user record.
        On GET request, render the profile image form.
        """
        form = ProfileImageForm()
        try:
            
            if form.validate_on_submit():
                # Retrieve the file from the form
                file = form.profile_image.data
                filename = secure_filename(file.filename)
               
                # Define the path to save the file
                file_path = os.path.join(app.config['UPLOAD_FOLDERS'], filename)
                
                # Save the file
                file.save(file_path)
                
                # Update the current user's profile_image field in the database
                current_user.profile_image = f'profiles/{filename}'
                db.session.commit()
                print("hello")
                flash("Profile picture updated successfully!", "success")
                return redirect(url_for('profile'))
            return render_template('profile_image.html', form=form)
        except Exception as e:
            flash("Error updating profile image.", "error")
            print("hello")
            app.logger.error(f"Error in profile_image route: {str(e)}")
            return render_template('error.html')
        


    @app.route('/change_password', methods=['GET', 'POST'])
    @login_required
    def change_password():
        """
        Route to allow users to change their password.

        On POST request:
            - Verifies the current password.
            - Checks if new password and confirm password match.
            - Calls `update_user_profile` to update only the password field.

        Returns:
            Redirects to profile page on success, or reloads form with error messages on failure.
        """
        if request.method == 'POST':
            current_password = request.form.get('current_password')
            new_password = request.form.get('new_password')
            confirm_password = request.form.get('confirm_password')

            # Verify current password
            if not check_password_hash(current_user.password_hash, current_password):
                flash("Current password is incorrect.", "error")
                return redirect(url_for('change_password'))

            # Check if new password and confirm password match
            if new_password != confirm_password:
                flash("New password and confirmation do not match.", "error")
                return redirect(url_for('change_password'))

            # Update password
            success, result = update_user_profile(
                user_id=current_user.id,
                new_password=new_password
            )

            if success:
                flash("Password updated successfully!", "success")
                return redirect(url_for('profile'))
            else:
                flash(result, "error")  # Result contains the error message

        return render_template('change_password.html')


def preprocess_image(img_path):
    """Preprocess the input image for prediction.

    Args:
        img_path: Path to the image file.

    Returns:
        Preprocessed image array suitable for model input.
    """
    img = image.load_img(img_path, target_size=(150, 150))  # Resizing to the model's input size
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = img_array / 255.0  # Normalize the image data
    return img_array

def predict_image(img_path):
    """Predict the tumor type from the image.

    Args:
        img_path: Path to the image file.

    Returns:
        Tuple containing predicted category and confidence score.
    """
    # Preprocess the image
    preprocessed_img = preprocess_image(img_path)

    # Run the prediction
    prediction = model.predict(preprocessed_img)

    # Get the class index with the highest probability and its confidence score
    predicted_class = np.argmax(prediction, axis=1)[0]
    categories = ["Glioma", "Meningioma", "No Tumor", "Pituitary"]
    predicted_category = categories[predicted_class]
    confidence_score = round(np.max(prediction) * 100, 2)
    return predicted_category, confidence_score
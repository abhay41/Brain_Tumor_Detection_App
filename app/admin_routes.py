# routes.py (or admin_routes.py if organized separately)
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from .models import Admin  # Import the Admin model
from werkzeug.security import check_password_hash
from .models import Admin, db,User,Patient,UserLogin
from functools import wraps
from .operations import change_admin_password
from sqlalchemy.exc import SQLAlchemyError

# Define the blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash("Please log in as admin to access this page.")
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    total_patients = Patient.query.count()
    total_users = User.query.count()
    total_logs =  UserLogin.query.order_by(UserLogin.timestamp.desc()).limit(5).all()

    return render_template('admin/dashboard.html', total_patients=total_patients,total_users = total_users,system_logs = total_logs)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            # Find the admin with the provided username
            admin = Admin.query.filter_by(username=username).first()
            if admin and check_password_hash(admin.password_hash, password):
                # If credentials are valid, store admin ID in session
                session['admin_id'] = admin.id
                flash("Logged in successfully!", "success")
                return redirect(url_for('admin.dashboard'))  # Redirect to the admin dashboard
            else:
                flash("Invalid username or password.", "error")
    return render_template('admin/login.html')


@admin_bp.route('/profile')
@admin_required
def profile():
    if 'admin_id' not in session:
        flash("Please log in to view your profile.", "warning")
        return redirect(url_for('admin.login'))
    
    # Retrieve admin details from the database
    admin = Admin.query.get(session['admin_id'])
    if not admin:
        flash("Admin profile not found.", "error")
        return redirect(url_for('admin.login'))
    
    return render_template('profile.html', admin=admin)

@admin_bp.route('/logout')
@admin_required
def logout():
    if 'admin_id' in session:
        session.pop('admin_id')
        flash("Logged out successfully!", "info")
    else:
        flash("You are not logged in.", "warning")
    return redirect(url_for('admin.login'))

@admin_bp.route('/users')
@admin_required
def list_users():
    users = User.query.all()  # Assume you have a User model
    return render_template('admin/users.html', users=users)

@admin_bp.route('/user/<int:user_id>/deactivate', methods=['POST'])
@admin_required
def deactivate_user(user_id):
    user = User.query.get_or_404(user_id)
    if not user.is_locked:
        user.is_locked = True  # Assuming 'is_locked' field exists in the User model
        db.session.commit()
        flash(f"User {user.username} has been deactivated.", 'success')
    return redirect(url_for('admin.list_users'))

@admin_bp.route('/user/<int:user_id>/activate', methods=['POST'])
@admin_required
def activate_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_locked:
        user.is_locked = False
        db.session.commit()
        flash(f"User {user.username} has been activated.", 'success')
    return redirect(url_for('admin.list_users'))

@admin_bp.route('/user/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.username} has been deleted.")
    return redirect(url_for('admin.list_users'))
# admin_routes.py
@admin_bp.route('/create_admin', methods=['GET', 'POST'])
# @admin_required  # This decorator ensures only logged-in admins can access this route
def create_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        password_confirmation = request.form['password_confirmation']

        if password != password_confirmation:
            flash("Passwords do not match.", "error")
            return redirect(url_for('admin.create_admin'))

        # Create a new admin account
        admin = Admin(username=username)
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()

        flash("New admin created successfully!", "success")
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/create_admin.html')

@admin_bp.route('/change_password', methods=['GET', 'POST'])
@admin_required
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
        admin = Admin.query.get(session['admin_id'])

        if not check_password_hash(admin.password_hash, current_password):
            flash("Current password is incorrect.", "error")
            return redirect(url_for('admin_bp.change_password'))

        # Check if new password and confirm password match
        if new_password != confirm_password:
            flash("New password and confirmation do not match.", "error")
            return redirect(url_for('admin_bp.change_password'))

        # Update password
        success, result = change_admin_password(
            admin_id=admin.id,
            new_password=new_password
        )

        if success:
            flash("Password updated successfully!", "success")
            flash("Please login again with the new password")
            return redirect(url_for('admin.login'))
        else:
            flash(result, "error")  # Result contains the error message

    return render_template('change_password.html')

@admin_bp.route('/manage_logins')
@admin_required  # Ensure the current user is an admin with @admin_required or similar
def manage_logins():
    # Fetch recent login attempts
    login_attempts = UserLogin.query.order_by(UserLogin.timestamp.desc()).limit(50).all()
    return render_template('admin/manage_logins.html', login_attempts=login_attempts)

@admin_bp.route('/lock_user/<int:user_id>')
@admin_required  # Ensure only admin can access
def lock_user(user_id):
    user = User.query.get(user_id)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for('admin_bp.manage_logins'))
    
    try:
        user.is_locked = True
        db.session.commit()
        flash("User account locked successfully.", "success")
    except SQLAlchemyError:
        db.session.rollback()
        flash("Error locking user account.", "error")
    
    return redirect(url_for('admin.manage_logins'))

@admin_bp.route('/unlock_user/<int:user_id>')
@admin_required  # Ensure only admin can access
def unlock_user(user_id):
    user = User.query.get(user_id)
    if not user:
        flash("User not found.", "error")
        return redirect(url_for('admin_bp.manage_logins'))
    
    try:
        user.is_locked = False
        db.session.commit()
        flash("User account unlocked successfully.", "success")
    except SQLAlchemyError:
        db.session.rollback()
        flash("Error unlocking user account.", "error")
    
    return redirect(url_for('admin.manage_logins'))


    
def configure_admin_routes(app):
    app.register_blueprint(admin_bp)

import pytest
from app.create_app import create_app
from app.models import User
from app.models import db  
@pytest.fixture
def client():
    """Create a test client for the app."""
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create test database tables
            # Create a test user for login
            user = User(username='testuser', email='test@example.com')
            user.set_password('testpass')
            db.session.add(user)
            db.session.commit()
        yield client
        db.drop_all()  # Cleanup after tests

def test_home(client):
    """Test the home page route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'brain tumor' in response.data  # Replace with actual content check

def test_login(client):
    """Test user login."""
    # Successful login
    response = client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 302  # Check for redirect after successful login
    assert response.location == 'http://localhost/dashboard'

    # Failed login
    response = client.post('/login', data={'username': 'wronguser', 'password': 'wrongpass'})
    assert response.status_code == 200
    assert b'Invalid username or password' in response.data

def test_logout(client):
    """Test user logout."""
    with client:
        client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
        response = client.get('/logout')
        assert response.status_code == 302  # Check for redirect after logout
        assert b'You have been logged out.' in response.data

def test_register(client):
    """Test user registration."""
    # Successful registration
    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'newpass'
    })
    assert response.status_code == 302  # Check for redirect after registration
    assert response.location == 'http://localhost/login'

    # Registration with existing username
    response = client.post('/register', data={
        'username': 'testuser',  # Already exists
        'email': 'test@example.com',
        'password': 'testpass'
    })
    assert response.status_code == 200
    assert b'Username or email already exists' in response.data

def test_dashboard(client):
    """Test the dashboard route."""
    with client:
        client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
        response = client.get('/dashboard')
        assert response.status_code == 200
        assert b'Dashboard' in response.data  # Replace with actual content check

def test_predict(client):
    """Test the predict route for image upload and prediction."""
    with client:
        client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
        
        # Test without a file
        response = client.post('/predict', data={})
        assert response.status_code == 302  # Expect redirect due to error
        assert b'No file part.' in response.data
        
        # Test with a valid file
        with open('tests/test_image.jpg', 'rb') as file:
            response = client.post('/predict', data={'file': file, 'name': 'John Doe', 'age': 30, 'gender': 'Male', 'diagnosis_date': '2024-01-01'})
            assert response.status_code == 200
            assert b'prediction' in response.json  # Check for prediction in JSON response

def test_patients_list(client):
    """Test the patients list route."""
    with client:
        client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
        response = client.get('/patients')
        assert response.status_code == 200
        assert b'Patients List' in response.data  # Replace with actual content check

def test_about(client):
    """Test the about page route."""
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About Us' in response.data  # Replace with actual content check

def test_profile(client):
    """Test the user profile page."""
    with client:
        client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
        response = client.get('/profile')
        assert response.status_code == 200
        assert b'Profile' in response.data  # Replace with actual content check

def test_profile_image(client):
    """Test the profile image upload functionality."""
    with client:
        client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
        
        # Test uploading a valid image
        with open('tests/test_image.jpg', 'rb') as file:
            response = client.post('/profile-image', data={'profile_image': file})
            assert response.status_code == 302  # Check for redirect after successful upload
            assert b'Profile picture updated successfully!' in response.data
        
        # Test uploading without an image
        response = client.post('/profile-image', data={})
        assert response.status_code == 200
        assert b'Error updating profile image.' in response.data

def test_change_password(client):
    """Test the change password functionality."""
    with client:
        client.post('/login', data={'username': 'testuser', 'password': 'testpass'})
        
        # Test with incorrect current password
        response = client.post('/change_password', data={'current_password': 'wrongpass', 'new_password': 'newpass', 'confirm_password': 'newpass'})
        assert response.status_code == 200
        assert b'Current password is incorrect.' in response.data

        # Test password update
        response = client.post('/change_password', data={'current_password': 'testpass', 'new_password': 'newpass', 'confirm_password': 'newpass'})
        assert response.status_code == 302  # Check for redirect after successful password change
        assert b'Password updated successfully!' in response.data

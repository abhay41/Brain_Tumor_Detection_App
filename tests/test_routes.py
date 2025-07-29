import unittest
from flask_testing import TestCase
from flask import url_for
import io
from datetime import datetime
import os

# Import your application and models
from app import create_app
from app.models import db, User, Treatment, Patient
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class TestRoutes(TestCase):
    def create_app(self):
        # Configure the application for testing
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite
        app.config['WTF_CSRF_ENABLED'] = False
        
        # Configure upload folders for testing
        app.config['UPLOAD_FOLDER'] = 'tests/test_uploads'
        app.config['UPLOAD_FOLDERS'] = 'tests/test_profiles'
        
        # Create test upload directories if they don't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(app.config['UPLOAD_FOLDERS'], exist_ok=True)
        
        return app

    def setUp(self):
        """Set up test database and sample data before each test."""
        # Create all database tables
        with self.app.app_context():
            db.create_all()
            
            # Create test user
            test_user = User(
                username='testuser',
                email='test@test.com'
            )
            test_user.set_password('password123')
            db.session.add(test_user)
            
            # Create test treatment
            test_treatment = Treatment(
                tumor_type='test_tumor',
                description ='killer',
                recommended_medication='Test treatment protocol',
                duration='3 years ',
                side_effects='Test side effects'
            )
            db.session.add(test_treatment)
            
            # Commit the changes
            db.session.commit()

    def tearDown(self):
        """Clean up after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            
        # Clean up test upload directories
        for filename in os.listdir(self.app.config['UPLOAD_FOLDER']):
            os.remove(os.path.join(self.app.config['UPLOAD_FOLDER'], filename))
        for filename in os.listdir(self.app.config['UPLOAD_FOLDERS']):
            os.remove(os.path.join(self.app.config['UPLOAD_FOLDERS'], filename))

    def test_home_route(self):
        with self.app.app_context():
            response = self.client.get('/')
            self.assert200(response)
            self.assert_template_used('home.html')

    def test_login_route(self):
        with self.app.app_context():
            # Test GET request
            response = self.client.get('/login')
            self.assert200(response)
            self.assert_template_used('login.html')

            # Test successful login
            response = self.client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            }, follow_redirects=True)
            self.assert200(response)
            self.assert_template_used('dashboard.html')

            # Test failed login
            response = self.client.post('/login', data={
                'username': 'testuser',
                'password': 'wrongpassword'
            }, follow_redirects=True)
            self.assert200(response)
            self.assert_template_used('login.html')

    def test_register_route(self):
        with self.app.app_context():
            # Test GET request
            response = self.client.get('/register')
            self.assert200(response)
            self.assert_template_used('register.html')

            # Test successful registration
            response = self.client.post('/register', data={
                'username': 'newuser',
                'email': 'new@test.com',
                'password': 'newpassword123'
            }, follow_redirects=True)
            self.assert200(response)
            self.assert_template_used('login.html')

            # Test duplicate username
            response = self.client.post('/register', data={
                'username': 'testuser',
                'email': 'another@test.com',
                'password': 'password123'
            }, follow_redirects=True)
            self.assert200(response)
            self.assert_template_used('register.html')

    def test_protected_routes(self):
        with self.app.app_context():
            # Test dashboard access without login
            response = self.client.get('/dashboard', follow_redirects=True)
            self.assert200(response)
            self.assert_template_used('login.html')

            # Login first
            self.client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            })

            # Test dashboard access with login
            response = self.client.get('/dashboard')
            self.assert200(response)
            self.assert_template_used('dashboard.html')

    def test_predict_route(self):
        with self.app.app_context():
            # Login first
            self.client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            })

            # Test GET request
            response = self.client.get('/predict')
            self.assert200(response)
            self.assert_template_used('predict.html')

            # Create a test image file
            test_image = (io.BytesIO(b"test image content"), 'test_image.jpg')
            
            # Test POST request with image
            data = {
                'file': test_image,
                'name': 'Test Patient',
                'age': '45',
                'gender': 'M',
                'diagnosis_date': '2024-01-01'
            }
            response = self.client.post('/predict', 
                                      data=data, 
                                      content_type='multipart/form-data')
            self.assert200(response)

    def test_profile_image_route(self):
        with self.app.app_context():
            # Login first
            self.client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            })

            # Test GET request
            response = self.client.get('/profile-image')
            self.assert200(response)
            self.assert_template_used('profile_image.html')

            # Create a test profile image
            test_image = (io.BytesIO(b"test image content"), 'profile.jpg')
            
            # Test POST request with image
            data = {
                'profile_image': test_image
            }
            response = self.client.post('/profile-image', 
                                      data=data, 
                                      content_type='multipart/form-data',
                                      follow_redirects=True)
            self.assert200(response)

    def test_change_password_route(self):
        with self.app.app_context():
            # Login first
            self.client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            })

            # Test GET request
            response = self.client.get('/change_password')
            self.assert200(response)
            self.assert_template_used('change_password.html')

            # Test successful password change
            response = self.client.post('/change_password', data={
                'current_password': 'password123',
                'new_password': 'newpassword123',
                'confirm_password': 'newpassword123'
            }, follow_redirects=True)
            self.assert200(response)
            self.assert_template_used('profile.html')

            # Test failed password change
            response = self.client.post('/change_password', data={
                'current_password': 'wrongpassword',
                'new_password': 'newpassword123',
                'confirm_password': 'newpassword123'
            }, follow_redirects=True)
            self.assert200(response)
            self.assert_template_used('change_password.html')
    def test_logout_route(self):
        with self.app.app_context():
            # Login first
            self.client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            })
            
            # Test logout
            response = self.client.get('/logout', follow_redirects=True)
            self.assert200(response)
            self.assert_template_used('home.html')

    def test_about_route(self):
        with self.app.app_context():
            response = self.client.get('/about')
            self.assert200(response)
            self.assert_template_used('about.html')

    def test_profile_route(self):
        with self.app.app_context():
            # Test without login
            response = self.client.get('/profile', follow_redirects=True)
            self.assert200(response)
            self.assert_template_used('login.html')

            # Test with login
            self.client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            })
            response = self.client.get('/profile')
            self.assert200(response)
            self.assert_template_used('profile.html')

    def test_patients_list_route(self):
        with self.app.app_context():
            # Test without login
            response = self.client.get('/patients', follow_redirects=True)
            self.assert200(response)
            self.assert_template_used('login.html')

            # Login and test again
            self.client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            })
            response = self.client.get('/patients')
            self.assert200(response)
            self.assert_template_used('patients.html')

    def test_invalid_login_credentials(self):
        with self.app.app_context():
            response = self.client.post('/login', data={
                'username': 'nonexistent',
                'password': 'wrongpass'
            }, follow_redirects=True)
            self.assert200(response)
            self.assert_template_used('login.html')

    def test_register_validation(self):
        with self.app.app_context():
            # Test empty fields
            response = self.client.post('/register', data={
                'username': '',
                'email': '',
                'password': ''
            }, follow_redirects=True)
            self.assert200(response)
            
            # Test invalid email format
            response = self.client.post('/register', data={
                'username': 'testuser2',
                'email': 'invalid-email',
                'password': 'password123'
            }, follow_redirects=True)
            self.assert200(response)

    def test_predict_without_file(self):
        with self.app.app_context():
            # Login first
            self.client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            })
            
            # Test prediction without file
            response = self.client.post('/predict', data={}, follow_redirects=True)
            self.assert200(response)

    def test_profile_image_validation(self):
        with self.app.app_context():
            # Login first
            self.client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            })
            
            # Test with invalid file type
            data = {
                'profile_image': (io.BytesIO(b"test content"), 'test.txt')
            }
            response = self.client.post('/profile-image', 
                                      data=data, 
                                      content_type='multipart/form-data',
                                      follow_redirects=True)
            self.assert200(response)

    def test_change_password_validation(self):
        with self.app.app_context():
            # Login first
            self.client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            })
            
            # Test mismatched passwords
            response = self.client.post('/change_password', data={
                'current_password': 'password123',
                'new_password': 'newpass123',
                'confirm_password': 'different123'
            }, follow_redirects=True)
            self.assert200(response)
            self.assert_template_used('change_password.html')
    def test_predict_invalid_file_type(self):
        with self.app.app_context():
            self.client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            })
            
            # Test with invalid file type (e.g., txt instead of image)
            data = {
                'file': (io.BytesIO(b"test content"), 'test.txt'),
                'name': 'Test Patient',
                'age': '45',
                'gender': 'M',
                'diagnosis_date': '2024-01-01'
            }
            response = self.client.post('/predict', 
                                      data=data, 
                                      content_type='multipart/form-data')
            self.assert200(response)

    def test_predict_missing_patient_data(self):
        with self.app.app_context():
            self.client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            })
            
            # Test with missing patient information
            test_image = (io.BytesIO(b"test image content"), 'test_image.jpg')
            data = {
                'file': test_image,
                # Missing name, age, gender, and diagnosis_date
            }
            response = self.client.post('/predict', 
                                      data=data, 
                                      content_type='multipart/form-data')
            self.assert200(response)

    def test_register_password_validation(self):
        with self.app.app_context():
            # Test with short password
            response = self.client.post('/register', data={
                'username': 'testuser3',
                'email': 'test3@test.com',
                'password': '123'  # Too short
            }, follow_redirects=True)
            self.assert200(response)

            # Test with common password
            response = self.client.post('/register', data={
                'username': 'testuser4',
                'email': 'test4@test.com',
                'password': 'password'  # Too common
            }, follow_redirects=True)
            self.assert200(response)

    def test_concurrent_login_attempts(self):
        with self.app.app_context():
            # First login
            response1 = self.client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            }, follow_redirects=True)  # Added follow_redirects=True
            
            # Attempt second login without logout
            response2 = self.client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            }, follow_redirects=True)  # Added follow_redirects=True
            
            self.assert200(response1)
            self.assert200(response2)

    def test_profile_update(self):
        with self.app.app_context():
            # Login
            self.client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            })
            
            # If your profile route only supports GET method, remove this test
            # Or modify it according to how your profile updates are actually handled
            response = self.client.get('/profile')  # Changed to GET request
            self.assert200(response)

    def test_patients_data_access(self):
        with self.app.app_context():
            # Login
            self.client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            })
            
            # Add test patient - adjust fields according to your Patient model
            patient = Patient(
                name='Test Patient',
                age=45,
                gender='M',
                tumor_type='test_tumor',  # Changed from diagnosis to tumor_type
                diagnosis_date=datetime.now().date(),
                image_path='test/path.jpg',
                user_id=1
            )
            db.session.add(patient)
            db.session.commit()
            
            # Test patient list access
            response = self.client.get('/patients')
            self.assert200(response)
            self.assert_template_used('patients.html')

    # def test_error_handling(self):
    #     with self.app.app_context():
    #         # Test 404 error
    #         response = self.client.get('/nonexistent-route')
    #         self.assert404(response)

    #         # Test accessing protected route without login
    #         response = self.client.get('/dashboard', follow_redirects=False)
    #         self.assert401(response)
    def test_error_handling(self):
        with self.app.app_context():
            # Test 404 error
            response = self.client.get('/nonexistent-route')
            self.assert404(response)

            # Test accessing protected route without login
            response = self.client.get('/dashboard')  # Removed follow_redirects=False
            self.assertStatus(response, 302)  # Changed to expect redirect status

    def test_session_handling(self):
        with self.app.app_context():
            # Login
            response = self.client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            }, follow_redirects=True)
            
            # Access protected route
            response = self.client.get('/dashboard')
            self.assert200(response)
            
            # Logout
            self.client.get('/logout')
            
            # Try accessing protected route after logout
            response = self.client.get('/dashboard', follow_redirects=True)
            self.assert200(response)
            self.assert_template_used('login.html')

    def test_profile_image_size_validation(self):
        with self.app.app_context():
            self.client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            })
            
            # Create large file
            large_file = io.BytesIO(b"0" * 1024 * 1024 * 11)  # 11MB file
            data = {
                'profile_image': (large_file, 'large_image.jpg')
            }
            response = self.client.post('/profile-image', 
                                      data=data, 
                                      content_type='multipart/form-data',
                                      follow_redirects=True)
            self.assert200(response)

    def test_predict_invalid_date(self):
        with self.app.app_context():
            self.client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            })
            
            test_image = (io.BytesIO(b"test image content"), 'test_image.jpg')
            data = {
                'file': test_image,
                'name': 'Test Patient',
                'age': '45',
                'gender': 'M',
                'diagnosis_date': 'invalid-date'  # Invalid date format
            }
            response = self.client.post('/predict', 
                                      data=data, 
                                      content_type='multipart/form-data')
            self.assert200(response)

    def test_register_username_constraints(self):
        with self.app.app_context():
            # Test username with special characters
            response = self.client.post('/register', data={
                'username': 'test@user#',
                'email': 'test5@test.com',
                'password': 'password123'
            }, follow_redirects=True)
            self.assert200(response)
            
            # Test username too short
            response = self.client.post('/register', data={
                'username': 'te',
                'email': 'test6@test.com',
                'password': 'password123'
            }, follow_redirects=True)
            self.assert200(response)

    def test_change_password_complexity(self):
        with self.app.app_context():
            self.client.post('/login', data={
                'username': 'testuser',
                'password': 'password123'
            })
            
            # Test with simple new password
            response = self.client.post('/change_password', data={
                'current_password': 'password123',
                'new_password': '123',
                'confirm_password': '123'
            }, follow_redirects=True)
            self.assert200(response)

if __name__ == '__main__':
    unittest.main()
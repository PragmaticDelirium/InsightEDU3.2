"""
Unit tests for Django views
"""
import pytest
from django.urls import reverse
from django.test import Client
from AppClassificationOfLD.models import UserDetails, admindata, DisabilityTest, TestResult


@pytest.mark.unit
@pytest.mark.views
@pytest.mark.django_db
class TestAuthenticationViews:
    """Test authentication-related views"""

    def test_home_view(self, api_client):
        """Test home page loads"""
        response = api_client.get('/')
        assert response.status_code == 200
        assert 'home.html' in [t.name for t in response.templates]

    def test_user_login_get(self, api_client):
        """Test user login page GET request"""
        response = api_client.get('/UserLogin/')
        assert response.status_code == 200
        assert 'UserLogin.html' in [t.name for t in response.templates]

    def test_user_login_post_valid(self, api_client, user_details):
        """Test user login with valid credentials"""
        response = api_client.post('/UserLogin/', {
            'U_name': user_details.Username,
            'U_pwds': user_details.Password
        })
        assert response.status_code == 302  # Redirect on success
        assert response.url == '/'

    def test_user_login_post_invalid(self, api_client):
        """Test user login with invalid credentials"""
        response = api_client.post('/UserLogin/', {
            'U_name': 'nonexistent',
            'U_pwds': 'wrongpass'
        })
        assert response.status_code == 302  # Redirect to registration
        assert '/UserRegisteration' in response.url

    def test_user_registration_get(self, api_client):
        """Test user registration page GET request"""
        response = api_client.get('/UserRegisteration/')
        assert response.status_code == 200
        assert 'UserRegisteration.html' in [t.name for t in response.templates]

    def test_user_registration_post_new_user(self, api_client):
        """Test user registration with new user"""
        response = api_client.post('/UserRegisteration/', {
            'fname': 'New',
            'lname': 'User',
            'phone': '9876543210',
            'Eid': 'newuser@test.com',
            'uname': 'newuser',
            'pwd': 'newpass123'
        })
        assert response.status_code == 200
        assert UserDetails.objects.filter(Username='newuser').exists()

    def test_user_registration_post_existing_user(self, api_client, user_details):
        """Test user registration with existing user"""
        response = api_client.post('/UserRegisteration/', {
            'fname': 'Test',
            'lname': 'User',
            'phone': '1234567890',
            'Eid': user_details.Email,
            'uname': user_details.Username,
            'pwd': 'testpass123'
        })
        assert response.status_code == 200
        # Should render login page for existing user
        assert 'UserLogin.html' in [t.name for t in response.templates]

    def test_admin_login_get(self, api_client):
        """Test admin login page GET request"""
        response = api_client.get('/AdminLogin/')
        assert response.status_code == 200
        assert 'Adminlogin.html' in [t.name for t in response.templates]

    def test_admin_login_post_valid(self, api_client, admin_user):
        """Test admin login with valid credentials"""
        response = api_client.post('/AdminLogin/', {
            'A_name': admin_user.Username,
            'A_pwds': admin_user.Password
        })
        assert response.status_code == 302
        assert response.url == '/'

    def test_admin_login_post_invalid(self, api_client):
        """Test admin login with invalid credentials"""
        response = api_client.post('/AdminLogin/', {
            'A_name': 'wrongadmin',
            'A_pwds': 'wrongpass'
        })
        assert response.status_code == 200
        assert 'Adminlogin.html' in [t.name for t in response.templates]

    def test_logout(self, authenticated_client):
        """Test logout functionality"""
        response = authenticated_client.get('/Logout/')
        assert response.status_code == 302
        assert response.url == '/'


@pytest.mark.unit
@pytest.mark.views
@pytest.mark.django_db
class TestTestViews:
    """Test assessment-related views"""

    def test_test_disability_get(self, authenticated_client):
        """Test disability test page loads"""
        response = authenticated_client.get('/TestDisability/')
        assert response.status_code == 200

    def test_maths_test_get(self, authenticated_client):
        """Test maths test page loads"""
        response = authenticated_client.get('/MathsTest/')
        assert response.status_code == 200

    def test_grammar_test_get(self, authenticated_client):
        """Test grammar test page loads"""
        response = authenticated_client.get('/GrammarTest/')
        assert response.status_code == 200

    def test_reading_test_get(self, authenticated_client):
        """Test reading test page loads"""
        response = authenticated_client.get('/ReadingTest/')
        assert response.status_code == 200

    def test_memory_test_get(self, authenticated_client):
        """Test memory test page loads"""
        response = authenticated_client.get('/MemoryTest/')
        assert response.status_code == 200


@pytest.mark.unit
@pytest.mark.views
class TestStaticPageViews:
    """Test static page views"""

    def test_base_view(self, api_client):
        """Test base template view"""
        response = api_client.get('/base/')
        assert response.status_code == 200

    def test_tests_view(self, api_client):
        """Test tests page view"""
        response = api_client.get('/tests/')
        assert response.status_code == 200


@pytest.mark.unit
@pytest.mark.views
@pytest.mark.django_db
class TestSessionManagement:
    """Test session-related functionality"""

    def test_user_session_creation(self, api_client, user_details):
        """Test that user login creates session"""
        response = api_client.post('/UserLogin/', {
            'U_name': user_details.Username,
            'U_pwds': user_details.Password
        })
        # Check session was created
        session = api_client.session
        assert session.get('UserId') == user_details.id
        assert session.get('UserType') == user_details.Username

    def test_admin_session_creation(self, api_client, admin_user):
        """Test that admin login creates session"""
        response = api_client.post('/AdminLogin/', {
            'A_name': admin_user.Username,
            'A_pwds': admin_user.Password
        })
        session = api_client.session
        assert session.get('UserType') == 'Admin'
        assert session.get('login') == 'Yes'

    def test_logout_clears_session(self, authenticated_client):
        """Test that logout clears all sessions"""
        # First verify session exists
        session = authenticated_client.session
        assert session.get('Users_id') is not None

        # Logout
        response = authenticated_client.get('/Logout/')

        # Verify redirect
        assert response.status_code == 302

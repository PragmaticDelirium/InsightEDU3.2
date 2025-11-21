"""
Unit tests for authentication views
"""
import pytest
from django.urls import reverse
from django.contrib.messages import get_messages
from AppClassificationOfLD.models import UserDetails, admindata


@pytest.mark.django_db
@pytest.mark.view
@pytest.mark.auth
class TestUserLogin:
    """Test cases for UserLogin view"""

    def test_user_login_get(self, client):
        """Test GET request to user login page"""
        response = client.get('/UserLogin/')
        assert response.status_code == 200
        assert 'UserLogin.html' in [t.name for t in response.templates]

    def test_user_login_success(self, client, user_details):
        """Test successful user login"""
        response = client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        assert response.status_code == 302  # Redirect
        assert response.url == '/'

    def test_user_login_failure(self, client):
        """Test failed user login"""
        response = client.post('/UserLogin/', {
            'U_name': 'nonexistent',
            'U_pwds': 'wrongpass'
        })
        assert response.status_code == 302
        assert response.url == '/UserRegisteration/'

    def test_user_login_invalid_credentials(self, client, user_details):
        """Test login with wrong password"""
        response = client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'wrongpassword'
        })
        assert response.status_code == 302
        assert response.url == '/UserRegisteration/'


@pytest.mark.django_db
@pytest.mark.view
@pytest.mark.auth
class TestUserRegistration:
    """Test cases for UserRegisteration view"""

    def test_user_registration_get(self, client):
        """Test GET request to registration page"""
        response = client.get('/UserRegisteration/')
        assert response.status_code == 200
        assert 'UserRegisteration.html' in [t.name for t in response.templates]

    def test_user_registration_success(self, client):
        """Test successful user registration"""
        response = client.post('/UserRegisteration/', {
            'fname': 'New',
            'lname': 'User',
            'phone': '5551234567',
            'Eid': 'newuser@example.com',
            'uname': 'newuser',
            'pwd': 'newpass123'
        })
        assert response.status_code == 200
        assert UserDetails.objects.filter(Username='newuser').exists()

    def test_user_registration_duplicate(self, client, user_details):
        """Test registration with duplicate email/username"""
        response = client.post('/UserRegisteration/', {
            'fname': 'Another',
            'lname': 'User',
            'phone': '5559876543',
            'Eid': 'john.doe@example.com',
            'uname': 'johndoe',
            'pwd': 'differentpass'
        })
        assert response.status_code == 200
        # Should redirect to login or show error
        assert 'UserLogin.html' in [t.name for t in response.templates]


@pytest.mark.django_db
@pytest.mark.view
@pytest.mark.auth
class TestAdminLogin:
    """Test cases for AdminLogin view"""

    def test_admin_login_get(self, client):
        """Test GET request to admin login page"""
        response = client.get('/AdminLogin/')
        assert response.status_code == 200
        assert 'Adminlogin.html' in [t.name for t in response.templates]

    def test_admin_login_success(self, client, admin_user):
        """Test successful admin login"""
        response = client.post('/AdminLogin/', {
            'A_name': 'admin',
            'A_pwds': 'admin123'
        })
        assert response.status_code == 302
        assert response.url == '/'

    def test_admin_login_failure(self, client):
        """Test failed admin login"""
        response = client.post('/AdminLogin/', {
            'A_name': 'admin',
            'A_pwds': 'wrongpass'
        })
        assert response.status_code == 200
        assert 'Adminlogin.html' in [t.name for t in response.templates]


@pytest.mark.django_db
@pytest.mark.view
@pytest.mark.auth
class TestLogout:
    """Test cases for Logout view"""

    def test_logout(self, client, user_details):
        """Test user logout"""
        # First login
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        # Then logout
        response = client.get('/Logout/')
        assert response.status_code == 302
        assert response.url == '/'


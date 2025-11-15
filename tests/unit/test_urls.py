"""
Unit tests for URL routing
"""
import pytest
from django.urls import reverse, resolve
from AppClassificationOfLD import views


@pytest.mark.unit
class TestURLPatterns:
    """Test URL patterns and routing"""

    def test_home_url(self):
        """Test home URL resolves correctly"""
        url = '/'
        assert resolve(url).func == views.home

    def test_user_login_url(self):
        """Test user login URL"""
        url = '/UserLogin/'
        assert resolve(url).func == views.UserLogin

    def test_user_registration_url(self):
        """Test user registration URL"""
        url = '/UserRegisteration/'
        assert resolve(url).func == views.UserRegisteration

    def test_admin_login_url(self):
        """Test admin login URL"""
        url = '/AdminLogin/'
        assert resolve(url).func == views.AdminLogin

    def test_logout_url(self):
        """Test logout URL"""
        url = '/Logout/'
        assert resolve(url).func == views.Logout

    def test_test_disability_url(self):
        """Test disability test URL"""
        url = '/TestDisability/'
        assert resolve(url).func == views.TestDisability

    def test_maths_test_url(self):
        """Test maths test URL"""
        url = '/MathsTest/'
        assert resolve(url).func == views.MathsTest

    def test_grammar_test_url(self):
        """Test grammar test URL"""
        url = '/GrammarTest/'
        assert resolve(url).func == views.GrammarTest

    def test_reading_test_url(self):
        """Test reading test URL"""
        url = '/ReadingTest/'
        assert resolve(url).func == views.ReadingTest

    def test_memory_test_url(self):
        """Test memory test URL"""
        url = '/MemoryTest/'
        assert resolve(url).func == views.MemoryTest

    def test_base_url(self):
        """Test base URL"""
        url = '/base/'
        assert resolve(url).func == views.base

    def test_tests_url(self):
        """Test tests URL"""
        url = '/tests/'
        assert resolve(url).func == views.tests

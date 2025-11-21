"""
Unit tests for test views (Maths, Grammar, Reading, Memory, etc.)
"""
import pytest
from django.urls import reverse
from AppClassificationOfLD.models import UserDetails, TestResult
from datetime import date, datetime


@pytest.mark.django_db
@pytest.mark.view
class TestHomeView:
    """Test cases for home view"""

    def test_home_view(self, client):
        """Test home page loads"""
        response = client.get('/')
        assert response.status_code == 200
        assert 'home.html' in [t.name for t in response.templates]


@pytest.mark.django_db
@pytest.mark.view
@pytest.mark.test_disability
class TestDisabilityTest:
    """Test cases for TestDisability view"""

    def test_test_disability_get(self, client, user_details):
        """Test GET request to disability test page"""
        # Login first
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        response = client.get('/TestDisability/')
        # Should either show the test or redirect if already taken today
        assert response.status_code in [200, 302]

    def test_test_disability_post(self, client, user_details):
        """Test POST request to disability test"""
        # Login first
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        # Create a test result for today first
        TestResult.objects.create(
            Users_id=str(user_details.id),
            Date=date.today()
        )
        # Try to take test again - should be blocked
        response = client.get('/TestDisability/')
        # Should redirect to home
        assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.view
class TestMathsTest:
    """Test cases for MathsTest view"""

    def test_maths_test_get(self, client, user_details):
        """Test GET request to maths test page"""
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        response = client.get('/MathsTest/')
        assert response.status_code == 200
        assert 'MathsTest.html' in [t.name for t in response.templates]

    def test_maths_test_post_pass(self, client, user_details):
        """Test POST with passing score"""
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        # Create test result
        TestResult.objects.create(
            Users_id=str(user_details.id),
            Date=date.today()
        )
        response = client.post('/MathsTest/', {
            'quest1': '4',
            'quest2': '10',
            'quest3': '120',
            'quest4': '2'
        })
        assert response.status_code == 302
        assert response.url == '/GrammarTest/'

    def test_maths_test_post_fail(self, client, user_details):
        """Test POST with failing score"""
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        TestResult.objects.create(
            Users_id=str(user_details.id),
            Date=date.today()
        )
        response = client.post('/MathsTest/', {
            'quest1': '1',
            'quest2': '5',
            'quest3': '100',
            'quest4': '1'
        })
        assert response.status_code == 302
        assert response.url == '/GrammarTest/'


@pytest.mark.django_db
@pytest.mark.view
class TestGrammarTest:
    """Test cases for GrammarTest view"""

    def test_grammar_test_get(self, client, user_details):
        """Test GET request to grammar test page"""
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        response = client.get('/GrammarTest/')
        assert response.status_code == 200
        assert 'GrammarTest.html' in [t.name for t in response.templates]

    def test_grammar_test_post_pass(self, client, user_details):
        """Test POST with passing score"""
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        TestResult.objects.create(
            Users_id=str(user_details.id),
            Date=date.today()
        )
        response = client.post('/GrammarTest/', {
            'quest1': 'short',
            'quest2': 'women',
            'quest3': 'a,e,i,o,u',
            'quest4': 'apple,banana,grapes,kiwi,mango'
        })
        assert response.status_code == 302
        assert response.url == '/ReadingTest/'

    def test_grammar_test_post_fail(self, client, user_details):
        """Test POST with failing score"""
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        TestResult.objects.create(
            Users_id=str(user_details.id),
            Date=date.today()
        )
        response = client.post('/GrammarTest/', {
            'quest1': 'long',
            'quest2': 'woman',
            'quest3': 'a,b,c',
            'quest4': 'wrong answer'
        })
        assert response.status_code == 302
        assert response.url == '/ReadingTest/'


@pytest.mark.django_db
@pytest.mark.view
class TestTestDashboard:
    """Test cases for TestDashboard view"""

    def test_test_dashboard(self, client, user_details):
        """Test test dashboard loads"""
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        response = client.get('/TestDashboard/')
        assert response.status_code == 200
        assert 'TestDashboard.html' in [t.name for t in response.templates]


@pytest.mark.django_db
@pytest.mark.view
class TestViewResults:
    """Test cases for ViewResults view"""

    def test_view_results(self, client, user_details, test_result):
        """Test viewing results"""
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        response = client.get('/ViewResults/')
        assert response.status_code == 200
        assert 'ViewResults.html' in [t.name for t in response.templates]
        assert 'details' in response.context


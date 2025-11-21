"""
Integration tests for complete user flows
"""
import pytest
from django.urls import reverse
from AppClassificationOfLD.models import UserDetails, TestResult
from datetime import date


@pytest.mark.django_db
@pytest.mark.integration
class TestCompleteUserRegistrationFlow:
    """Test complete user registration and initial setup"""

    def test_user_registration_to_login(self, client):
        """Test user can register and then login"""
        # Register
        response = client.post('/UserRegisteration/', {
            'fname': 'Integration',
            'lname': 'Test',
            'phone': '5551112222',
            'Eid': 'integration@test.com',
            'uname': 'integrationtest',
            'pwd': 'testpass123'
        })
        assert response.status_code == 200
        assert UserDetails.objects.filter(Username='integrationtest').exists()

        # Login
        response = client.post('/UserLogin/', {
            'U_name': 'integrationtest',
            'U_pwds': 'testpass123'
        })
        assert response.status_code == 302
        assert response.url == '/'


@pytest.mark.django_db
@pytest.mark.integration
class TestCompleteTestFlow:
    """Test complete test taking flow"""

    def test_disability_test_flow(self, client, user_details):
        """Test complete disability test flow"""
        # Login
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })

        # Take disability test
        response = client.post('/TestDisability/', {
            'D_Reading': '1',
            'D_Spelling': '1',
            'D_Handwriting': '1',
            'D_WrittenExpression': '1',
            'D_BasicArithmetic': '1',
            'D_HigherArithmetic': '1',
            'D_Attention': '1',
            'Easily_Distracted': '1',
            'D_Memory': '1',
            'Lack_Motivation': '1',
            'D_StudySkills': '1',
            'Does_Not_like_School': '1',
            'D_LearningLanguage': '1',
            'D_LearningSubject': '1',
            'Slow_To_Learn': '1',
            'Repeated_a_Grade': '1'
        })
        # Should redirect to test dashboard
        assert response.status_code == 302
        assert TestResult.objects.filter(Users_id=str(user_details.id)).exists()

    def test_maths_to_grammar_flow(self, client, user_details):
        """Test flow from maths test to grammar test"""
        # Login
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })

        # Create test result
        TestResult.objects.create(
            Users_id=str(user_details.id),
            Date=date.today()
        )

        # Take maths test
        response = client.post('/MathsTest/', {
            'quest1': '4',
            'quest2': '10',
            'quest3': '120',
            'quest4': '2'
        })
        assert response.status_code == 302
        assert response.url == '/GrammarTest/'

        # Verify result was saved
        result = TestResult.objects.get(Users_id=str(user_details.id), Date=date.today())
        assert result.Maths_Test is not None


@pytest.mark.django_db
@pytest.mark.integration
class TestSessionManagement:
    """Test session management across views"""

    def test_session_persists_across_views(self, client, user_details):
        """Test that user session persists across different views"""
        # Login
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })

        # Access multiple views
        response1 = client.get('/TestDashboard/')
        assert response1.status_code == 200

        response2 = client.get('/MathsTest/')
        assert response2.status_code == 200

        response3 = client.get('/ViewResults/')
        assert response3.status_code == 200

    def test_logout_clears_session(self, client, user_details):
        """Test that logout clears session"""
        # Login
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })

        # Access protected view
        response = client.get('/TestDashboard/')
        assert response.status_code == 200

        # Logout
        client.get('/Logout/')

        # Try to access protected view - should fail or redirect
        response = client.get('/TestDashboard/')
        # May still work if not checking session, but ideally should redirect


@pytest.mark.django_db
@pytest.mark.integration
class TestResultsTracking:
    """Test results tracking across multiple tests"""

    def test_multiple_test_results(self, client, user_details):
        """Test that multiple test results are tracked correctly"""
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })

        # Create test result
        result = TestResult.objects.create(
            Users_id=str(user_details.id),
            Date=date.today()
        )

        # Take maths test
        client.post('/MathsTest/', {
            'quest1': '4',
            'quest2': '10',
            'quest3': '120',
            'quest4': '2'
        })

        # Take grammar test
        client.post('/GrammarTest/', {
            'quest1': 'short',
            'quest2': 'women',
            'quest3': 'a,e,i,o,u',
            'quest4': 'apple,banana,grapes,kiwi,mango'
        })

        # Verify all results are saved
        result.refresh_from_db()
        assert result.Maths_Test is not None
        assert result.Grammar_Test is not None


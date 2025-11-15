"""
Integration tests for user flows
"""
import pytest
from django.test import Client
from AppClassificationOfLD.models import UserDetails, TestResult, DisabilityTest


@pytest.mark.integration
@pytest.mark.django_db
class TestUserRegistrationFlow:
    """Test complete user registration and login flow"""

    def test_complete_registration_and_login_flow(self):
        """Test user can register and then login"""
        client = Client()

        # Step 1: Register new user
        register_response = client.post('/UserRegisteration/', {
            'fname': 'Integration',
            'lname': 'Test',
            'phone': '5555555555',
            'Eid': 'integration@test.com',
            'uname': 'integrationuser',
            'pwd': 'integrationpass'
        })
        assert register_response.status_code == 200

        # Verify user was created
        assert UserDetails.objects.filter(Username='integrationuser').exists()
        user = UserDetails.objects.get(Username='integrationuser')

        # Step 2: Login with newly created user
        login_response = client.post('/UserLogin/', {
            'U_name': 'integrationuser',
            'U_pwds': 'integrationpass'
        })
        assert login_response.status_code == 302
        assert login_response.url == '/'

        # Step 3: Verify session was created
        session = client.session
        assert session.get('UserId') == user.id
        assert session.get('UserType') == 'integrationuser'

    def test_duplicate_registration_redirects_to_login(self):
        """Test that duplicate registration redirects to login"""
        client = Client()

        # Create user first time
        UserDetails.objects.create(
            Firstname='Existing',
            Lastname='User',
            Phone='1111111111',
            Email='existing@test.com',
            Username='existinguser',
            Password='pass123'
        )

        # Try to register again with same credentials
        response = client.post('/UserRegisteration/', {
            'fname': 'Existing',
            'lname': 'User',
            'phone': '1111111111',
            'Eid': 'existing@test.com',
            'uname': 'existinguser',
            'pwd': 'pass123'
        })

        # Should render login page
        assert 'UserLogin.html' in [t.name for t in response.templates]


@pytest.mark.integration
@pytest.mark.django_db
class TestAssessmentFlow:
    """Test complete assessment flow"""

    def test_authenticated_user_can_access_tests(self):
        """Test that authenticated user can access test pages"""
        client = Client()

        # Create and login user
        user = UserDetails.objects.create(
            Firstname='Test',
            Lastname='Student',
            Phone='9999999999',
            Email='student@test.com',
            Username='student',
            Password='studentpass'
        )

        # Login
        client.post('/UserLogin/', {
            'U_name': 'student',
            'U_pwds': 'studentpass'
        })

        # Access test pages
        test_pages = [
            '/TestDisability/',
            '/MathsTest/',
            '/GrammarTest/',
            '/ReadingTest/',
            '/MemoryTest/'
        ]

        for page in test_pages:
            response = client.get(page)
            assert response.status_code == 200


@pytest.mark.integration
@pytest.mark.django_db
class TestAdminFlow:
    """Test admin-related flows"""

    def test_admin_login_and_access(self):
        """Test admin can login and access admin features"""
        from AppClassificationOfLD.models import admindata

        client = Client()

        # Create admin
        admin = admindata.objects.create(
            Username='testadmin',
            Password='adminpass123'
        )

        # Login as admin
        response = client.post('/AdminLogin/', {
            'A_name': 'testadmin',
            'A_pwds': 'adminpass123'
        })

        assert response.status_code == 302
        assert response.url == '/'

        # Verify admin session
        session = client.session
        assert session.get('UserType') == 'Admin'
        assert session.get('login') == 'Yes'


@pytest.mark.integration
@pytest.mark.django_db
class TestDataPersistence:
    """Test data persistence across requests"""

    def test_test_results_persist(self):
        """Test that test results are saved and retrievable"""
        # Create user
        user = UserDetails.objects.create(
            Firstname='Data',
            Lastname='Test',
            Phone='7777777777',
            Email='data@test.com',
            Username='datauser',
            Password='datapass'
        )

        # Create test result
        result = TestResult.objects.create(
            Users_id=str(user.id),
            Learning_Disability='Dyslexia',
            Maths_Test='85',
            Grammar_Test='90',
            Reading_Test='75'
        )

        # Retrieve and verify
        saved_result = TestResult.objects.get(id=result.id)
        assert saved_result.Users_id == str(user.id)
        assert saved_result.Learning_Disability == 'Dyslexia'
        assert saved_result.Maths_Test == '85'

    def test_disability_test_data_persists(self):
        """Test disability test responses are saved"""
        test = DisabilityTest.objects.create(
            D_Reading='Yes',
            D_Spelling='Yes',
            D_Handwriting='No',
            D_WrittenExpression='Yes',
            D_BasicArithmetic='No',
            D_HigherArithmetic='Yes',
            D_Attention='Yes',
            Easily_Distracted='No',
            D_Memory='Yes',
            Lack_Motivation='No',
            D_StudySkills='Yes',
            Does_Not_like_School='No',
            D_LearningLanguage='Yes',
            D_LearningSubject='No',
            Slow_To_Learn='Yes',
            Repeated_a_Grade='No',
            Result='Dyslexia'
        )

        # Retrieve and verify
        saved_test = DisabilityTest.objects.get(id=test.id)
        assert saved_test.D_Reading == 'Yes'
        assert saved_test.Result == 'Dyslexia'


@pytest.mark.integration
@pytest.mark.django_db
class TestSessionManagement:
    """Test session management across requests"""

    def test_logout_clears_all_sessions(self):
        """Test that logout properly clears sessions"""
        client = Client()

        # Create and login user
        user = UserDetails.objects.create(
            Firstname='Session',
            Lastname='Test',
            Phone='6666666666',
            Email='session@test.com',
            Username='sessionuser',
            Password='sessionpass'
        )

        client.post('/UserLogin/', {
            'U_name': 'sessionuser',
            'U_pwds': 'sessionpass'
        })

        # Verify session exists
        assert client.session.get('UserId') == user.id

        # Logout
        response = client.get('/Logout/')
        assert response.status_code == 302

        # Note: Session.objects.all().delete() clears ALL sessions,
        # so we can't verify this user's specific session in isolation
        # This is actually a potential issue in the code that should be addressed

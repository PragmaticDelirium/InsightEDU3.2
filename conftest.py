"""
Pytest configuration and fixtures for InsightEDU 3.2
"""
import pytest
from django.contrib.auth.models import User
from django.test import Client
from AppClassificationOfLD.models import UserDetails, DisabilityTest, TestResult, admindata


@pytest.fixture(scope='session')
def django_db_setup():
    """Configure test database settings"""
    pass


@pytest.fixture
def api_client():
    """Fixture for Django test client"""
    return Client()


@pytest.fixture
def authenticated_client(db, user_details):
    """Fixture for authenticated client"""
    client = Client()
    session = client.session
    session['Users_id'] = user_details.id
    session['Users_Username'] = user_details.Username
    session.save()
    return client


@pytest.fixture
def user_details(db):
    """Create a test user"""
    return UserDetails.objects.create(
        Firstname='Test',
        Lastname='User',
        Phone='1234567890',
        Email='test@example.com',
        Username='testuser',
        Password='testpass123'
    )


@pytest.fixture
def admin_user(db):
    """Create a test admin user"""
    return admindata.objects.create(
        Username='admin',
        Password='admin123'
    )


@pytest.fixture
def disability_test_data(db, user_details):
    """Create sample disability test data"""
    return DisabilityTest.objects.create(
        D_Reading='Yes',
        D_Spelling='No',
        D_Handwriting='Yes',
        D_WrittenExpression='No',
        D_BasicArithmetic='Yes',
        D_HigherArithmetic='No',
        Attention='Yes',
        Easily_Distracted='Yes',
        D_Memory='No',
        Lack_Motivation='No',
        D_StudySkills='Yes',
        Does_Not_like_School='No',
        D_LearningLanguage='Yes',
        D_LearningSubject='No',
        Slow_To_Learn='Yes',
        Repeated_a_Grade='No',
        Result='Dyslexia'
    )


@pytest.fixture
def test_result(db, user_details):
    """Create sample test result"""
    return TestResult.objects.create(
        Users_id=user_details.id,
        Learning_Disability='Dyslexia',
        Maths_Test=75,
        Dyslexia='Detected',
        Dysgraphia='Not Detected',
        Dyscalculia='Not Detected',
        Grammar_Test=80,
        Reading_Test=70,
        Memory_images=85,
        Memory_audio=90,
        Scenario_Test=88,
        Video_test1='Pass',
        Video_test2='Pass',
        Video_test3='Pass'
    )


@pytest.fixture
def sample_test_session(authenticated_client, user_details):
    """Create a test session with user logged in"""
    session = authenticated_client.session
    session['Users_id'] = user_details.id
    session['Users_Username'] = user_details.Username
    session['LearningDisability'] = 'Dyslexia'
    session['MathsTest'] = 75
    session['Dyslexia'] = 'Detected'
    session.save()
    return authenticated_client


@pytest.fixture
def mock_ml_model(mocker):
    """Mock ML model for testing"""
    mock_model = mocker.MagicMock()
    mock_model.predict.return_value = [[0.1, 0.8, 0.1]]  # Mock prediction
    return mock_model


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """
    Give all tests access to the database.
    """
    pass


@pytest.fixture
def disable_migrations():
    """Disable migrations for faster tests"""
    pass

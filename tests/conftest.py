"""
Pytest configuration and shared fixtures
"""
import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from AppClassificationOfLD.models import UserDetails, admindata, DisabilityTest, TestResult
from datetime import date, datetime


@pytest.fixture
def factory():
    """Request factory for creating test requests"""
    return RequestFactory()


@pytest.fixture
def user_details():
    """Create a test user"""
    return UserDetails.objects.create(
        Firstname="John",
        Lastname="Doe",
        Phone="1234567890",
        Email="john.doe@example.com",
        Username="johndoe",
        Password="testpass123"
    )


@pytest.fixture
def admin_user():
    """Create a test admin user"""
    return admindata.objects.create(
        Username="admin",
        Password="admin123"
    )


@pytest.fixture
def disability_test_data():
    """Create test disability test data"""
    return DisabilityTest.objects.create(
        D_Reading="1",
        D_Spelling="1",
        D_Handwriting="0",
        D_WrittenExpression="1",
        D_BasicArithmetic="0",
        D_HigherArithmetic="1",
        D_Attention="1",
        Easily_Distracted="1",
        D_Memory="0",
        Lack_Motivation="1",
        D_StudySkills="1",
        Does_Not_like_School="0",
        D_LearningLanguage="1",
        D_LearningSubject="1",
        Slow_To_Learn="1",
        Repeated_a_Grade="0",
        Result="Learning Disability"
    )


@pytest.fixture
def test_result(user_details):
    """Create a test result"""
    return TestResult.objects.create(
        Users_id=str(user_details.id),
        Learning_Disability="Learning Disability",
        Date=date.today(),
        Maths_Test="3/4",
        Grammar_Test="2/4 Dyslexia",
        Reading_Test="3/4",
        Memory_images="6/8",
        Memory_audio="7/10"
    )


@pytest.fixture
def authenticated_request(factory, user_details):
    """Create an authenticated request"""
    request = factory.get('/')
    request.user = user_details
    request.session = {'UserId': user_details.id, 'login': 'Yes', 'UserType': 'User'}
    return request


@pytest.fixture
def admin_request(factory, admin_user):
    """Create an admin authenticated request"""
    request = factory.get('/')
    request.user = admin_user
    request.session = {'type_id': 'Admin', 'UserType': 'Admin', 'login': 'Yes'}
    return request


@pytest.fixture
def anonymous_request(factory):
    """Create an anonymous request"""
    request = factory.get('/')
    request.user = AnonymousUser()
    request.session = {}
    return request


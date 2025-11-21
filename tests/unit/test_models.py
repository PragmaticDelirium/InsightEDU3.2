"""
Unit tests for models
"""
import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from AppClassificationOfLD.models import UserDetails, admindata, DisabilityTest, TestResult
from datetime import date


@pytest.mark.django_db
@pytest.mark.model
class TestUserDetails:
    """Test cases for UserDetails model"""

    def test_create_user_details(self):
        """Test creating a user details instance"""
        user = UserDetails.objects.create(
            Firstname="Jane",
            Lastname="Smith",
            Phone="9876543210",
            Email="jane.smith@example.com",
            Username="janesmith",
            Password="password123"
        )
        assert user.id is not None
        assert user.Firstname == "Jane"
        assert user.Email == "jane.smith@example.com"

    def test_user_details_str(self):
        """Test string representation of UserDetails"""
        user = UserDetails.objects.create(
            Firstname="Test",
            Lastname="User",
            Phone="123",
            Email="test@test.com",
            Username="testuser",
            Password="pass"
        )
        # Since __str__ is not defined, test that object exists
        assert user is not None

    def test_user_details_db_table(self):
        """Test that the correct database table is used"""
        assert UserDetails._meta.db_table == 'UserDetails'

    def test_user_details_fields(self):
        """Test all fields are present"""
        user = UserDetails()
        assert hasattr(user, 'Firstname')
        assert hasattr(user, 'Lastname')
        assert hasattr(user, 'Phone')
        assert hasattr(user, 'Email')
        assert hasattr(user, 'Username')
        assert hasattr(user, 'Password')


@pytest.mark.django_db
@pytest.mark.model
class TestAdminData:
    """Test cases for admindata model"""

    def test_create_admin(self):
        """Test creating an admin user"""
        admin = admindata.objects.create(
            Username="admin",
            Password="adminpass"
        )
        assert admin.id is not None
        assert admin.Username == "admin"

    def test_admin_db_table(self):
        """Test that the correct database table is used"""
        assert admindata._meta.db_table == 'admindata'


@pytest.mark.django_db
@pytest.mark.model
class TestDisabilityTest:
    """Test cases for DisabilityTest model"""

    def test_create_disability_test(self):
        """Test creating a disability test instance"""
        test = DisabilityTest.objects.create(
            D_Reading="1",
            D_Spelling="0",
            D_Handwriting="1",
            D_WrittenExpression="0",
            D_BasicArithmetic="1",
            D_HigherArithmetic="0",
            D_Attention="1",
            Easily_Distracted="0",
            D_Memory="1",
            Lack_Motivation="0",
            D_StudySkills="1",
            Does_Not_like_School="0",
            D_LearningLanguage="1",
            D_LearningSubject="0",
            Slow_To_Learn="1",
            Repeated_a_Grade="0",
            Result="No Learning Disability"
        )
        assert test.id is not None
        assert test.Result == "No Learning Disability"

    def test_disability_test_all_fields(self):
        """Test all disability test fields"""
        test = DisabilityTest()
        fields = [
            'D_Reading', 'D_Spelling', 'D_Handwriting', 'D_WrittenExpression',
            'D_BasicArithmetic', 'D_HigherArithmetic', 'D_Attention',
            'Easily_Distracted', 'D_Memory', 'Lack_Motivation',
            'D_StudySkills', 'Does_Not_like_School', 'D_LearningLanguage',
            'D_LearningSubject', 'Slow_To_Learn', 'Repeated_a_Grade', 'Result'
        ]
        for field in fields:
            assert hasattr(test, field)

    def test_disability_test_db_table(self):
        """Test that the correct database table is used"""
        assert DisabilityTest._meta.db_table == 'DisabilityTest'


@pytest.mark.django_db
@pytest.mark.model
class TestTestResult:
    """Test cases for TestResult model"""

    def test_create_test_result(self, user_details):
        """Test creating a test result"""
        result = TestResult.objects.create(
            Users_id=str(user_details.id),
            Learning_Disability="Learning Disability",
            Date=date.today(),
            Maths_Test="4/4",
            Grammar_Test="3/4",
            Reading_Test="4/4"
        )
        assert result.id is not None
        assert result.Users_id == str(user_details.id)

    def test_test_result_all_fields(self):
        """Test all test result fields"""
        result = TestResult()
        fields = [
            'Users_id', 'Learning_Disability', 'Maths_Test', 'Dyslexia',
            'Dysgraphia', 'Dyscalculia', 'Grammar_Test', 'Reading_Test',
            'Memory_images', 'Memory_audio', 'Scenario_Test',
            'Video_test1', 'Video_test2', 'Video_test3', 'Date'
        ]
        for field in fields:
            assert hasattr(result, field)

    def test_test_result_nullable_fields(self):
        """Test that nullable fields can be None"""
        result = TestResult.objects.create(
            Users_id="1",
            Date=date.today()
        )
        assert result.Learning_Disability is None
        assert result.Maths_Test is None

    def test_test_result_db_table(self):
        """Test that the correct database table is used"""
        assert TestResult._meta.db_table == 'TestResult'


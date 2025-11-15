"""
Unit tests for Django models
"""
import pytest
from django.db import IntegrityError
from AppClassificationOfLD.models import UserDetails, DisabilityTest, TestResult, admindata


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.django_db
class TestUserDetailsModel:
    """Test UserDetails model"""

    def test_create_user(self):
        """Test creating a user"""
        user = UserDetails.objects.create(
            Firstname='John',
            Lastname='Doe',
            Phone='1234567890',
            Email='john@example.com',
            Username='johndoe',
            Password='password123'
        )
        assert user.Firstname == 'John'
        assert user.Lastname == 'Doe'
        assert user.Email == 'john@example.com'
        assert user.Username == 'johndoe'
        assert user.id is not None

    def test_user_string_fields(self):
        """Test user string field lengths"""
        user = UserDetails.objects.create(
            Firstname='A' * 100,
            Lastname='B' * 100,
            Phone='1234567890',
            Email='test@example.com',
            Username='testuser',
            Password='pass'
        )
        assert len(user.Firstname) == 100
        assert len(user.Lastname) == 100

    def test_user_email_field(self):
        """Test email field"""
        user = UserDetails.objects.create(
            Firstname='Test',
            Lastname='User',
            Phone='1234567890',
            Email='valid@email.com',
            Username='testuser',
            Password='pass'
        )
        assert '@' in user.Email
        assert user.Email == 'valid@email.com'

    def test_multiple_users_creation(self):
        """Test creating multiple users"""
        user1 = UserDetails.objects.create(
            Firstname='User1',
            Lastname='Test1',
            Phone='1111111111',
            Email='user1@test.com',
            Username='user1',
            Password='pass1'
        )
        user2 = UserDetails.objects.create(
            Firstname='User2',
            Lastname='Test2',
            Phone='2222222222',
            Email='user2@test.com',
            Username='user2',
            Password='pass2'
        )
        assert UserDetails.objects.count() == 2
        assert user1.id != user2.id


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.django_db
class TestDisabilityTestModel:
    """Test DisabilityTest model"""

    def test_create_disability_test(self):
        """Test creating a disability test record"""
        test = DisabilityTest.objects.create(
            D_Reading='Yes',
            D_Spelling='No',
            D_Handwriting='Yes',
            D_WrittenExpression='No',
            D_BasicArithmetic='Yes',
            D_HigherArithmetic='No',
            D_Attention='Yes',
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
        assert test.D_Reading == 'Yes'
        assert test.Result == 'Dyslexia'
        assert test.id is not None

    def test_disability_test_all_yes(self):
        """Test disability test with all 'Yes' answers"""
        test = DisabilityTest.objects.create(
            D_Reading='Yes',
            D_Spelling='Yes',
            D_Handwriting='Yes',
            D_WrittenExpression='Yes',
            D_BasicArithmetic='Yes',
            D_HigherArithmetic='Yes',
            D_Attention='Yes',
            Easily_Distracted='Yes',
            D_Memory='Yes',
            Lack_Motivation='Yes',
            D_StudySkills='Yes',
            Does_Not_like_School='Yes',
            D_LearningLanguage='Yes',
            D_LearningSubject='Yes',
            Slow_To_Learn='Yes',
            Repeated_a_Grade='Yes',
            Result='Multiple Disabilities'
        )
        assert test.Result == 'Multiple Disabilities'

    def test_disability_test_fields_count(self):
        """Test that all required fields are present"""
        test = DisabilityTest.objects.create(
            D_Reading='Yes',
            D_Spelling='No',
            D_Handwriting='Yes',
            D_WrittenExpression='No',
            D_BasicArithmetic='Yes',
            D_HigherArithmetic='No',
            D_Attention='Yes',
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
        # Check that test has all expected fields
        assert hasattr(test, 'D_Reading')
        assert hasattr(test, 'D_Spelling')
        assert hasattr(test, 'Result')


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.django_db
class TestAdminDataModel:
    """Test admindata model"""

    def test_create_admin(self):
        """Test creating an admin user"""
        admin = admindata.objects.create(
            Username='admin',
            Password='admin123'
        )
        assert admin.Username == 'admin'
        assert admin.Password == 'admin123'
        assert admin.id is not None

    def test_multiple_admins(self):
        """Test creating multiple admin users"""
        admin1 = admindata.objects.create(
            Username='admin1',
            Password='pass1'
        )
        admin2 = admindata.objects.create(
            Username='admin2',
            Password='pass2'
        )
        assert admindata.objects.count() == 2
        assert admin1.Username != admin2.Username


@pytest.mark.unit
@pytest.mark.models
@pytest.mark.django_db
class TestTestResultModel:
    """Test TestResult model"""

    def test_create_test_result(self, user_details):
        """Test creating a test result"""
        result = TestResult.objects.create(
            Users_id=str(user_details.id),
            Learning_Disability='Dyslexia',
            Maths_Test='75',
            Dyslexia='Detected',
            Dysgraphia='Not Detected',
            Dyscalculia='Not Detected',
            Grammar_Test='80',
            Reading_Test='70',
            Memory_images='85',
            Memory_audio='90',
            Scenario_Test='88',
            Video_test1='Pass',
            Video_test2='Pass',
            Video_test3='Pass'
        )
        assert result.Users_id == str(user_details.id)
        assert result.Learning_Disability == 'Dyslexia'
        assert result.Maths_Test == '75'

    def test_test_result_nullable_fields(self):
        """Test that nullable fields work correctly"""
        result = TestResult.objects.create(
            Users_id='1',
            Learning_Disability='Dyslexia'
        )
        # These fields are nullable and should be None or default value
        assert result.Maths_Test is None or result.Maths_Test == 'None'
        assert result.id is not None

    def test_test_result_all_fields(self):
        """Test creating test result with all fields populated"""
        result = TestResult.objects.create(
            Users_id='123',
            Learning_Disability='Dyslexia',
            Maths_Test='85',
            Dyslexia='Detected',
            Dysgraphia='Not Detected',
            Dyscalculia='Not Detected',
            Grammar_Test='90',
            Reading_Test='88',
            Memory_images='92',
            Memory_audio='87',
            Scenario_Test='91',
            Video_test1='Pass',
            Video_test2='Pass',
            Video_test3='Pass'
        )
        assert result.Users_id == '123'
        assert result.Learning_Disability == 'Dyslexia'
        assert result.Maths_Test == '85'
        assert result.Grammar_Test == '90'

    def test_multiple_results_for_user(self, user_details):
        """Test storing multiple test results for same user"""
        result1 = TestResult.objects.create(
            Users_id=str(user_details.id),
            Learning_Disability='Dyslexia',
            Maths_Test='70'
        )
        result2 = TestResult.objects.create(
            Users_id=str(user_details.id),
            Learning_Disability='Dyslexia',
            Maths_Test='85'
        )
        results = TestResult.objects.filter(Users_id=str(user_details.id))
        assert results.count() == 2
        assert result1.id != result2.id

"""
Comprehensive integration tests for complete user flows
"""
import pytest
from django.urls import reverse
from AppClassificationOfLD.models import UserDetails, TestResult, DisabilityTest
from datetime import date, timedelta


@pytest.mark.django_db
@pytest.mark.integration
class TestCompleteUserJourney:
    """Test complete user journey from registration to results"""

    def test_complete_user_journey(self, client):
        """Test complete journey: register -> login -> take tests -> view results"""
        # 1. Register
        response = client.post('/UserRegisteration/', {
            'fname': 'Complete',
            'lname': 'Journey',
            'phone': '5559998888',
            'Eid': 'complete@journey.com',
            'uname': 'completejourney',
            'pwd': 'testpass123'
        })
        assert response.status_code == 200
        assert UserDetails.objects.filter(Username='completejourney').exists()

        # 2. Login
        response = client.post('/UserLogin/', {
            'U_name': 'completejourney',
            'U_pwds': 'testpass123'
        })
        assert response.status_code == 302

        # 3. Take disability test
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
        assert response.status_code == 302

        # 4. Take maths test
        response = client.post('/MathsTest/', {
            'quest1': '4',
            'quest2': '10',
            'quest3': '120',
            'quest4': '2'
        })
        assert response.status_code == 302

        # 5. Take grammar test
        response = client.post('/GrammarTest/', {
            'quest1': 'short',
            'quest2': 'women',
            'quest3': 'a,e,i,o,u',
            'quest4': 'apple,banana,grapes,kiwi,mango'
        })
        assert response.status_code == 302

        # 6. View results
        response = client.get('/ViewResults/')
        assert response.status_code == 200
        assert 'details' in response.context

        # 7. Verify all results saved
        user = UserDetails.objects.get(Username='completejourney')
        result = TestResult.objects.filter(Users_id=str(user.id), Date=date.today()).first()
        assert result is not None
        assert result.Maths_Test is not None
        assert result.Grammar_Test is not None


@pytest.mark.django_db
@pytest.mark.integration
class TestMultipleTestSessions:
    """Test multiple test sessions"""

    def test_multiple_days_testing(self, client, user_details):
        """Test taking tests on multiple days"""
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })

        # Day 1
        today = date.today()
        TestResult.objects.create(
            Users_id=str(user_details.id),
            Date=today,
            Maths_Test='3/4',
            Grammar_Test='2/4'
        )

        # Day 2 (yesterday)
        yesterday = today - timedelta(days=1)
        TestResult.objects.create(
            Users_id=str(user_details.id),
            Date=yesterday,
            Maths_Test='4/4',
            Grammar_Test='4/4'
        )

        # View results should show both
        response = client.get('/ViewResults/')
        assert response.status_code == 200
        details = response.context['details']
        assert details.count() >= 2


@pytest.mark.django_db
@pytest.mark.integration
class TestAdminWorkflow:
    """Test admin workflow"""

    def test_admin_add_training_data(self, client, admin_user):
        """Test admin can add training data"""
        client.post('/AdminLogin/', {
            'A_name': 'admin',
            'A_pwds': 'admin123'
        })

        initial_count = DisabilityTest.objects.count()

        response = client.post('/TrainingData/', {
            'D_Reading': '1',
            'D_Spelling': '0',
            'D_Handwriting': '1',
            'D_WrittenExpression': '0',
            'D_BasicArithmetic': '1',
            'D_HigherArithmetic': '0',
            'D_Attention': '1',
            'Easily_Distracted': '0',
            'D_Memory': '1',
            'Lack_Motivation': '0',
            'D_StudySkills': '1',
            'Does_Not_like_School': '0',
            'D_LearningLanguage': '1',
            'D_LearningSubject': '0',
            'Slow_To_Learn': '1',
            'Repeated_a_Grade': '0',
            'Result': 'No Learning Disability'
        })

        assert response.status_code == 200
        assert DisabilityTest.objects.count() == initial_count + 1


@pytest.mark.django_db
@pytest.mark.integration
class TestConcurrentUsers:
    """Test concurrent user scenarios"""

    def test_multiple_users_same_test(self, client):
        """Test multiple users taking same test"""
        # Create multiple users
        user1 = UserDetails.objects.create(
            Firstname="User1",
            Lastname="Test",
            Phone="111",
            Email="user1@test.com",
            Username="user1",
            Password="pass1"
        )

        user2 = UserDetails.objects.create(
            Firstname="User2",
            Lastname="Test",
            Phone="222",
            Email="user2@test.com",
            Username="user2",
            Password="pass2"
        )

        # User 1 takes test
        client.post('/UserLogin/', {
            'U_name': 'user1',
            'U_pwds': 'pass1'
        })
        TestResult.objects.create(
            Users_id=str(user1.id),
            Date=date.today()
        )
        client.post('/MathsTest/', {
            'quest1': '4',
            'quest2': '10',
            'quest3': '120',
            'quest4': '2'
        })

        # User 2 takes test
        client.post('/UserLogin/', {
            'U_name': 'user2',
            'U_pwds': 'pass2'
        })
        TestResult.objects.create(
            Users_id=str(user2.id),
            Date=date.today()
        )
        client.post('/MathsTest/', {
            'quest1': '4',
            'quest2': '10',
            'quest3': '120',
            'quest4': '2'
        })

        # Both should have results
        result1 = TestResult.objects.filter(Users_id=str(user1.id), Date=date.today()).first()
        result2 = TestResult.objects.filter(Users_id=str(user2.id), Date=date.today()).first()

        assert result1 is not None
        assert result2 is not None
        assert result1.Maths_Test is not None
        assert result2.Maths_Test is not None


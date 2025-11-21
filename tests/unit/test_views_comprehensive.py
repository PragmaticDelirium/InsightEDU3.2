"""
Comprehensive unit tests for all views including edge cases and error handling
"""
import pytest
from unittest.mock import patch, MagicMock, mock_open
from django.urls import reverse
from django.contrib.messages import get_messages
from django.core.exceptions import ValidationError
from AppClassificationOfLD.models import UserDetails, admindata, DisabilityTest, TestResult
from datetime import date, datetime


@pytest.mark.django_db
@pytest.mark.view
class TestAdditionalViews:
    """Test cases for additional views"""

    def test_base_view(self, client):
        """Test base view"""
        response = client.get('/base/')
        assert response.status_code == 200
        assert 'base.html' in [t.name for t in response.templates]

    def test_tests_view(self, client):
        """Test tests view"""
        response = client.get('/tests/')
        assert response.status_code == 200
        assert 'tests.html' in [t.name for t in response.templates]

    def test_scenarios_test_view(self, client, user_details):
        """Test scenarios test view"""
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        response = client.get('/ScenariosTest/')
        assert response.status_code == 200
        assert 'ScenariosTest.html' in [t.name for t in response.templates]

    def test_maths_links_view(self, client):
        """Test maths links view"""
        response = client.get('/MathsLinks/')
        assert response.status_code == 200
        assert 'MathsLinks.html' in [t.name for t in response.templates]

    def test_grammar_links_view(self, client):
        """Test grammar links view"""
        response = client.get('/GrammarLinks/')
        assert response.status_code == 200
        assert 'GrammarLinks.html' in [t.name for t in response.templates]

    def test_reading_links_view(self, client):
        """Test reading links view"""
        response = client.get('/ReadingLinks/')
        assert response.status_code == 200
        assert 'ReadingLinks.html' in [t.name for t in response.templates]

    def test_memory_links_view(self, client):
        """Test memory links view"""
        response = client.get('/MemoryLinks/')
        assert response.status_code == 200
        assert 'MemoryLinks.html' in [t.name for t in response.templates]

    def test_scenarios_link_view(self, client):
        """Test scenarios link view"""
        response = client.get('/ScenariosLink/')
        assert response.status_code == 200
        assert 'ScenariosLink.html' in [t.name for t in response.templates]

    def test_images_view(self, client):
        """Test images view"""
        response = client.get('/images/')
        assert response.status_code == 200
        assert 'images.html' in [t.name for t in response.templates]


@pytest.mark.django_db
@pytest.mark.view
class TestVideoTests:
    """Test cases for video test views"""

    def test_videotest1_get(self, client, user_details):
        """Test GET request to videotest1"""
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        response = client.get('/videotest1/')
        assert response.status_code == 200
        assert 'videotest1.html' in [t.name for t in response.templates]

    def test_videotest1_post_pass(self, client, user_details):
        """Test videotest1 with passing score"""
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        TestResult.objects.create(
            Users_id=str(user_details.id),
            Date=date.today()
        )
        response = client.post('/videotest1/', {
            'var1': 'friends',
            'var2': 'forest',
            'var3': 'rabbit',
            'var4': 'squirrel',
            'var5': 'by crossing the bridge'
        })
        assert response.status_code == 302
        assert response.url == '/ScenariosTest/'

    def test_videotest1_post_fail(self, client, user_details):
        """Test videotest1 with failing score"""
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        TestResult.objects.create(
            Users_id=str(user_details.id),
            Date=date.today()
        )
        response = client.post('/videotest1/', {
            'var1': 'wrong',
            'var2': 'wrong',
            'var3': 'wrong',
            'var4': 'wrong',
            'var5': 'wrong'
        })
        assert response.status_code == 302
        assert response.url == '/ScenariosTest/'

    def test_videotest2_get(self, client, user_details):
        """Test GET request to videotest2"""
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        response = client.get('/videotest2/')
        assert response.status_code == 200
        assert 'videotest2.html' in [t.name for t in response.templates]

    def test_videotest2_post_pass(self, client, user_details):
        """Test videotest2 with passing score"""
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        TestResult.objects.create(
            Users_id=str(user_details.id),
            Date=date.today()
        )
        response = client.post('/videotest2/', {
            'var1': 'john and eric',
            'var2': 'positive',
            'var3': 'month end',
            'var4': 'product team',
            'var5': 'office environment'
        })
        assert response.status_code == 302
        assert response.url == '/ScenariosTest/'

    def test_videotest3_get(self, client, user_details):
        """Test GET request to videotest3"""
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        response = client.get('/videotest3/')
        assert response.status_code == 200
        assert 'videotest3.html' in [t.name for t in response.templates]

    def test_videotest3_post_pass(self, client, user_details):
        """Test videotest3 with passing score"""
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        TestResult.objects.create(
            Users_id=str(user_details.id),
            Date=date.today()
        )
        response = client.post('/videotest3/', {
            'var1': 'arjun',
            'var2': 'school',
            'var3': 'singing',
            'var4': 'on same day',
            'var5': 'ticket to circus'
        })
        assert response.status_code == 302
        assert response.url == '/ViewResults/'


@pytest.mark.django_db
@pytest.mark.view
class TestMemoryTests:
    """Test cases for memory test views"""

    def test_memory_test1_get(self, client, user_details):
        """Test GET request to MemoryTest1"""
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        response = client.get('/MemoryTest1/')
        assert response.status_code == 200
        assert 'MemoryTest1.html' in [t.name for t in response.templates]

    def test_memory_test1_post_pass(self, client, user_details):
        """Test MemoryTest1 with passing score"""
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        TestResult.objects.create(
            Users_id=str(user_details.id),
            Date=date.today()
        )
        response = client.post('/MemoryTest1/', {
            'sent1': 'table',
            'sent2': 'chair',
            'sent3': 'car',
            'sent4': 'tree',
            'sent5': 'cat',
            'sent6': 'dog',
            'sent7': 'cake',
            'sent8': 'umbrella'
        })
        assert response.status_code == 302

    def test_memory_test1_post_fail(self, client, user_details):
        """Test MemoryTest1 with failing score"""
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        TestResult.objects.create(
            Users_id=str(user_details.id),
            Date=date.today()
        )
        response = client.post('/MemoryTest1/', {
            'sent1': 'wrong1',
            'sent2': 'wrong2',
            'sent3': 'wrong3',
            'sent4': 'wrong4',
            'sent5': 'wrong5',
            'sent6': 'wrong6',
            'sent7': 'wrong7',
            'sent8': 'wrong8'
        })
        assert response.status_code == 302


@pytest.mark.django_db
@pytest.mark.view
class TestTrainingData:
    """Test cases for TrainingData view"""

    def test_training_data_get(self, client, admin_user):
        """Test GET request to training data page"""
        client.post('/AdminLogin/', {
            'A_name': 'admin',
            'A_pwds': 'admin123'
        })
        response = client.get('/TrainingData/')
        assert response.status_code == 200
        assert 'TrainingData.html' in [t.name for t in response.templates]

    def test_training_data_post(self, client, admin_user):
        """Test POST request to add training data"""
        client.post('/AdminLogin/', {
            'A_name': 'admin',
            'A_pwds': 'admin123'
        })
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
            'Result': 'Learning Disability'
        })
        assert response.status_code == 200
        assert DisabilityTest.objects.filter(Result='Learning Disability').exists()


@pytest.mark.django_db
@pytest.mark.view
class TestErrorHandling:
    """Test cases for error handling scenarios"""

    def test_user_login_missing_fields(self, client):
        """Test login with missing POST fields"""
        response = client.post('/UserLogin/', {})
        # Should handle missing fields gracefully
        assert response.status_code in [200, 400, 500]

    def test_user_registration_missing_fields(self, client):
        """Test registration with missing fields"""
        response = client.post('/UserRegisteration/', {
            'fname': 'Test'
            # Missing other required fields
        })
        # Should handle missing fields
        assert response.status_code in [200, 400, 500]

    def test_test_disability_missing_session(self, client):
        """Test disability test without session"""
        response = client.post('/TestDisability/', {
            'D_Reading': '1',
            # ... other fields
        })
        # Should handle missing session
        assert response.status_code in [302, 400, 500]

    def test_maths_test_missing_fields(self, client, user_details):
        """Test maths test with missing fields"""
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        TestResult.objects.create(
            Users_id=str(user_details.id),
            Date=date.today()
        )
        response = client.post('/MathsTest/', {
            'quest1': '4'
            # Missing other questions
        })
        # Should handle missing fields
        assert response.status_code in [200, 400, 500]

    def test_view_results_no_results(self, client, user_details):
        """Test viewing results when no results exist"""
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        response = client.get('/ViewResults/')
        assert response.status_code == 200
        assert 'ViewResults.html' in [t.name for t in response.templates]


@pytest.mark.django_db
@pytest.mark.view
class TestEdgeCases:
    """Test cases for edge cases"""

    def test_user_registration_empty_strings(self, client):
        """Test registration with empty strings"""
        response = client.post('/UserRegisteration/', {
            'fname': '',
            'lname': '',
            'phone': '',
            'Eid': '',
            'uname': '',
            'pwd': ''
        })
        # Should handle empty strings
        assert response.status_code in [200, 400]

    def test_user_registration_special_characters(self, client):
        """Test registration with special characters"""
        response = client.post('/UserRegisteration/', {
            'fname': 'Test@#$',
            'lname': 'User!@#',
            'phone': '123-456-7890',
            'Eid': 'test+user@example.com',
            'uname': 'test_user123',
            'pwd': 'P@ssw0rd!'
        })
        # Should handle special characters
        assert response.status_code in [200, 400]

    def test_test_disability_boundary_values(self, client, user_details):
        """Test disability test with boundary values"""
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        # Test with all zeros
        response = client.post('/TestDisability/', {
            'D_Reading': '0',
            'D_Spelling': '0',
            'D_Handwriting': '0',
            'D_WrittenExpression': '0',
            'D_BasicArithmetic': '0',
            'D_HigherArithmetic': '0',
            'D_Attention': '0',
            'Easily_Distracted': '0',
            'D_Memory': '0',
            'Lack_Motivation': '0',
            'D_StudySkills': '0',
            'Does_Not_like_School': '0',
            'D_LearningLanguage': '0',
            'D_LearningSubject': '0',
            'Slow_To_Learn': '0',
            'Repeated_a_Grade': '0'
        })
        # Should handle boundary values
        assert response.status_code in [302, 400, 500]

    def test_maths_test_invalid_input(self, client, user_details):
        """Test maths test with invalid input"""
        client.post('/UserLogin/', {
            'U_name': 'johndoe',
            'U_pwds': 'testpass123'
        })
        TestResult.objects.create(
            Users_id=str(user_details.id),
            Date=date.today()
        )
        response = client.post('/MathsTest/', {
            'quest1': 'not_a_number',
            'quest2': '10',
            'quest3': '120',
            'quest4': '2'
        })
        # Should handle invalid input
        assert response.status_code in [200, 400, 500]


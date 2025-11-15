"""
Factory classes for creating test data using factory_boy
"""
import factory
from factory.django import DjangoModelFactory
from faker import Faker
from AppClassificationOfLD.models import UserDetails, DisabilityTest, TestResult, admindata

fake = Faker()


class UserDetailsFactory(DjangoModelFactory):
    """Factory for creating UserDetails instances"""

    class Meta:
        model = UserDetails

    Firstname = factory.Faker('first_name')
    Lastname = factory.Faker('last_name')
    Phone = factory.Faker('phone_number')
    Email = factory.Faker('email')
    Username = factory.Faker('user_name')
    Password = factory.Faker('password')


class AdminDataFactory(DjangoModelFactory):
    """Factory for creating admindata instances"""

    class Meta:
        model = admindata

    Username = factory.Faker('user_name')
    Password = factory.Faker('password')


class DisabilityTestFactory(DjangoModelFactory):
    """Factory for creating DisabilityTest instances"""

    class Meta:
        model = DisabilityTest

    D_Reading = factory.Iterator(['Yes', 'No'])
    D_Spelling = factory.Iterator(['Yes', 'No'])
    D_Handwriting = factory.Iterator(['Yes', 'No'])
    D_WrittenExpression = factory.Iterator(['Yes', 'No'])
    D_BasicArithmetic = factory.Iterator(['Yes', 'No'])
    D_HigherArithmetic = factory.Iterator(['Yes', 'No'])
    D_Attention = factory.Iterator(['Yes', 'No'])
    Easily_Distracted = factory.Iterator(['Yes', 'No'])
    D_Memory = factory.Iterator(['Yes', 'No'])
    Lack_Motivation = factory.Iterator(['Yes', 'No'])
    D_StudySkills = factory.Iterator(['Yes', 'No'])
    Does_Not_like_School = factory.Iterator(['Yes', 'No'])
    D_LearningLanguage = factory.Iterator(['Yes', 'No'])
    D_LearningSubject = factory.Iterator(['Yes', 'No'])
    Slow_To_Learn = factory.Iterator(['Yes', 'No'])
    Repeated_a_Grade = factory.Iterator(['Yes', 'No'])
    Result = factory.Iterator(['Dyslexia', 'Dysgraphia', 'Dyscalculia', 'No Disability'])


class TestResultFactory(DjangoModelFactory):
    """Factory for creating TestResult instances"""

    class Meta:
        model = TestResult

    Users_id = factory.Faker('random_int', min=1, max=1000)
    Learning_Disability = factory.Iterator(['Dyslexia', 'Dysgraphia', 'Dyscalculia'])
    Maths_Test = factory.Faker('random_int', min=0, max=100)
    Dyslexia = factory.Iterator(['Detected', 'Not Detected'])
    Dysgraphia = factory.Iterator(['Detected', 'Not Detected'])
    Dyscalculia = factory.Iterator(['Detected', 'Not Detected'])
    Grammar_Test = factory.Faker('random_int', min=0, max=100)
    Reading_Test = factory.Faker('random_int', min=0, max=100)
    Memory_images = factory.Faker('random_int', min=0, max=100)
    Memory_audio = factory.Faker('random_int', min=0, max=100)
    Scenario_Test = factory.Faker('random_int', min=0, max=100)
    Video_test1 = factory.Iterator(['Pass', 'Fail'])
    Video_test2 = factory.Iterator(['Pass', 'Fail'])
    Video_test3 = factory.Iterator(['Pass', 'Fail'])

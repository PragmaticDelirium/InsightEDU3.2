from django.db import models

# Create your models here.
class UserDetails(models.Model):
	Firstname = models.CharField(max_length = 100,default = None)
	Lastname = models.CharField(max_length = 100,default = None)
	Phone = models.CharField(max_length = 100,default = None)
	Email = models.EmailField(max_length = 100,default = None)
	Username = models.CharField(max_length = 100,default = None)
	Password = models.CharField(max_length = 100,default = None)
	

	class Meta:
		db_table = 'UserDetails'

class DisabilityTest(models.Model):
	D_Reading = models.CharField(max_length = 100,default = None)
	D_Spelling = models.CharField(max_length = 100,default = None)
	D_Handwriting = models.CharField(max_length = 100,default = None)
	D_WrittenExpression = models.CharField(max_length = 100,default = None)
	D_BasicArithmetic = models.CharField(max_length = 100,default = None)
	D_HigherArithmetic = models.CharField(max_length = 100,default = None)
	D_Attention = models.CharField(max_length = 100,default = None)
	Easily_Distracted = models.CharField(max_length = 100,default = None)
	D_Memory = models.CharField(max_length = 100,default = None)
	Lack_Motivation = models.CharField(max_length = 100,default = None)
	D_StudySkills = models.CharField(max_length = 100,default = None)
	Does_Not_like_School = models.CharField(max_length = 100,default = None)
	D_LearningLanguage = models.CharField(max_length = 100,default = None)
	D_LearningSubject = models.CharField(max_length = 100,default = None)
	Slow_To_Learn = models.CharField(max_length = 100,default = None)
	Repeated_a_Grade = models.CharField(max_length = 100,default = None)
	Result = models.CharField(max_length = 100,default = None)

	class Meta:
		db_table = 'DisabilityTest'


class admindata(models.Model):
    Username = models.CharField(max_length=100 ,default = None)
    Password = models.CharField(max_length=100 ,default = None)

    class Meta:
        db_table = 'admindata'



class TestResult(models.Model):
	Users_id = models.CharField(max_length=100 ,default = None,null = True)
	Learning_Disability = models.CharField(max_length=100 ,default = None,null = True)
	Maths_Test = models.CharField(max_length=100 ,default = None,null = True)
	Dyslexia = models.CharField(max_length=100 ,default = None,null = True)
	Dysgraphia = models.CharField(max_length=100 ,default = None,null = True)
	Dyscalculia = models.CharField(max_length=100 ,default = None,null = True)
	Grammar_Test = models.CharField(max_length=100 ,default = None,null = True)
	Reading_Test = models.CharField(max_length=100 ,default = None,null = True)
	Memory_images = models.CharField(max_length=100 ,default = None,null = True)
	Memory_audio = models.CharField(max_length=100 ,default = None,null = True)
	Scenario_Test = models.CharField(max_length=100 ,default = None,null = True)
	Video_test1 = models.CharField(max_length=100 ,default = None,null = True)
	Video_test2 = models.CharField(max_length=100 ,default = None,null = True)
	Video_test3 = models.CharField(max_length=100 ,default = None,null = True)
	Date = models.DateField(max_length=100,default=None,null=True)

	class Meta:
		db_table = 'TestResult'



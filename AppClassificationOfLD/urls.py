from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views

urlpatterns = [
path('',views.home,name='home'),
path('base/',views.base,name='base'),
path('UserLogin/',views.UserLogin,name='UserLogin'),
path('UserRegisteration/',views.UserRegisteration,name='UserRegisteration'),
path('Logout/',views.Logout,name='Logout'),
path('TestDisability/',views.TestDisability,name='TestDisability'),
path('MathsTest/',views.MathsTest,name='MathsTest'),
path('TestDashboard/',views.TestDashboard,name='TestDashboard'),
path('GrammarTest/',views.GrammarTest,name='GrammarTest'),
path('ReadingTest/',views.ReadingTest,name='ReadingTest'),
path('MemoryTest/',views.MemoryTest,name='MemoryTest'),
path('ScenariosTest/',views.ScenariosTest,name='ScenariosTest'),
path('Reading/',views.Reading,name='Reading'),
path('Stop/',views.Stop,name='Stop'),
path('AdminLogin/',views.AdminLogin,name='AdminLogin'),
path('TrainingData/',views.TrainingData,name='TrainingData'),
path('videotest1/',views.videotest1,name='videotest1'),
path('videotest2/',views.videotest2,name='videotest2'),
path('videotest3/',views.videotest3,name='videotest3'),
path('MathsLinks/',views.MathsLinks,name='MathsLinks'),
path('GrammarLinks/',views.GrammarLinks,name='GrammarLinks'),
path('ReadingLinks/',views.ReadingLinks,name='ReadingLinks'),
path('MemoryLinks/',views.MemoryLinks,name='MemoryLinks'),
path('ScenariosLink/',views.ScenariosLink,name='ScenariosLink'),
path('MemoryTest1/',views.MemoryTest1,name='MemoryTest1'),
path('images/',views.images,name='images'),
path('tests/',views.tests,name='tests'),
path('ViewResults/',views.ViewResults,name='ViewResults'),









]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
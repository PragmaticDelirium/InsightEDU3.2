
from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.sessions.models import Session
import wave
import pyaudio
from pydub import AudioSegment
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from django.http import JsonResponse
import sklearn.linear_model as lm
import speech_recognition as sr
from datetime import date
from datetime import datetime
from keras.models import load_model
import h5py
import numpy 
from datetime import datetime

# returns a compiled model
# identical to the previous one

# Create your views here.
def home(request):
    return render(request,'home.html',{})

def base(request):
    return render(request,'base.html',{})

def tests(request):
    return render (request,'tests.html',{})

def AdminLogin(request):
    if request.method == "POST":
        A_username = request.POST['A_name']
        A_password = request.POST['A_pwds']
        if admindata.objects.filter(Username = A_username,Password = A_password).exists():
            ad = admindata.objects.get(Username=A_username, Password=A_password)
            print('d')
            messages.info(request,'Your login is Sucessfull')
            request.session['type_id'] = 'Admin'
            request.session['UserType'] = 'Admin'
            request.session['login'] = "Yes"
            return redirect("/")
        else:
            print('y')
            messages.error(request, 'Error wrong username/password')
            return render(request, "Adminlogin.html", {})

    else:
        return render(request, "Adminlogin.html", {})

def UserLogin(request):
    if request.method == "POST":
        C_name = request.POST['U_name']
        C_password = request.POST['U_pwds']
        if UserDetails.objects.filter(Username=C_name, Password=C_password).exists():
            user = UserDetails.objects.all().filter(Username=C_name, Password=C_password)
            messages.info(request, 'logged in')
            request.session['UserId'] = user[0].id
            request.session['type_id'] = 'User'
            request.session['UserType'] = C_name
            request.session['login'] = "Yes"
            return redirect("/")
        else:
            messages.info(request, 'Please Register')
            return redirect("/UserRegisteration")
    else:
        return render(request,'UserLogin.html',{})
    return render(request,'UserLogin.html',{})

def UserRegisteration(request):
    if request.method == "POST":
        F_name = request.POST['fname']
        L_name = request.POST['lname']
        U_mobile = request.POST['phone']
        U_email = request.POST['Eid']
        U_username = request.POST['uname']
        U_password = request.POST['pwd']
        if  UserDetails.objects.filter(Email = U_email ,Username = U_username).exists():
            myObjects = UserDetails.objects.all().filter(Email = U_email ,Username = U_username )
            name = myObjects[0].Username
            messages.error(request,'Already Registered Please Login')
            return render(request,'UserLogin.html',{})
        else:
            users = UserDetails(Firstname = F_name, Lastname= L_name, Phone =  U_mobile, Email =  U_email, Username = U_username, Password= U_password)
            users.save()
            messages.info(request,'Registered Sucessfully')
            return render(request,'UserLogin.html',{})
    else:
        return render(request,'UserRegisteration.html',{})
    return render(request,'UserRegisteration.html',{})

def Logout(request):
    Session.objects.all().delete()
    return redirect("/")

def TestDisability(request):
    if request.method == "POST":
        User_id = request.session['UserId']
        date_joined = datetime.now()
        print(date_joined)
        date_joined = str(date_joined).split(' ')
        print(date_joined[0])


        list1 = []
        D_Reading = request.POST['D_Reading'] 
        list1.append(int(D_Reading))
        print(list1)
        D_Spelling = request.POST['D_Spelling']
        list1.append(int(D_Spelling))
        D_Handwriting = request.POST['D_Handwriting']
        list1.append(int(D_Handwriting))
        D_WrittenExpression = request.POST['D_WrittenExpression']
        list1.append(int(D_WrittenExpression))
        D_BasicArithmetic = request.POST['D_BasicArithmetic']
        list1.append(int(D_BasicArithmetic))
        D_HigherArithmetic = request.POST['D_HigherArithmetic']
        list1.append(int(D_HigherArithmetic))
        D_Attention = request.POST['D_Attention']
        list1.append(int(D_Attention))
        Easily_Distracted = request.POST['Easily_Distracted']
        list1.append(int(Easily_Distracted))
        D_Memory = request.POST['D_Memory']
        list1.append(int(D_Memory))
        Lack_Motivation = request.POST['Lack_Motivation']
        list1.append(int(Lack_Motivation))
        D_StudySkills = request.POST['D_StudySkills']
        list1.append(int(D_StudySkills))
        Does_Not_like_School = request.POST['Does_Not_like_School']
        list1.append(int(Does_Not_like_School))
        D_LearningLanguage = request.POST['D_LearningLanguage']
        list1.append(int(D_LearningLanguage))
        D_LearningSubject = request.POST['D_LearningSubject']
        list1.append(int(D_LearningSubject))
        Slow_To_Learn = request.POST['Slow_To_Learn']
        list1.append(int(Slow_To_Learn))
        Repeated_a_Grade = request.POST['Repeated_a_Grade']
        list1.append(int(Repeated_a_Grade))
        print(list1)

        #list = ['one','two', 'three', None, None,'Six', None, 'Eight']
        sum1 = sum(x==1 for x in list1)
        print(sum1)
        divide = sum1/16
        print(divide)
        percentage = divide*100
        print(percentage)
        print("Number of None is List : ",sum1 )
        #count = DisabilityTest.objects.all().count()
        #print(count)
        #HIT = DisabilityTest.objects.all().filter(Result="No Learning Disability")
        #print(HIT)
        '''if count > 0:
            Packages = DisabilityTest.objects.all()
            ArrD_Reading = [] 
            ArrD_Spelling  = []
            ArrD_Handwriting = []
            ArrD_WrittenExpression = []
            ArrD_BasicArithmetic = []
            ArrD_HigherArithmetic  = []
            ArrD_Attention = []
            ArrEasily_Distracted = []
            ArrD_Memory = []
            ArrLack_Motivation = []
            ArrD_StudySkills = []
            ArrDoes_Not_like_School = []
            ArrD_LearningLanguage = []
            ArrD_LearningSubject = []
            ArrSlow_To_Learn = []
            ArrRepeated_a_Grade = []
            ArrResult = []

            for line in Packages:
                ArrD_Reading.append(format(line.D_Reading))
                ArrD_Spelling.append(format(line.D_Spelling))
                ArrD_Handwriting.append(format(line.D_Handwriting))
                ArrD_WrittenExpression.append(format(line.D_WrittenExpression))
                ArrD_BasicArithmetic.append(format(line.D_BasicArithmetic))
                ArrD_HigherArithmetic.append(format(line.D_HigherArithmetic))
                ArrD_Attention.append(format(line.D_Attention))
                ArrEasily_Distracted.append(format(line.Easily_Distracted))
                ArrD_Memory.append(format(line.D_Memory))
                ArrLack_Motivation.append(format(line.Lack_Motivation))
                ArrD_StudySkills.append(format(line.D_StudySkills))
                ArrDoes_Not_like_School.append(format(line.Does_Not_like_School))
                ArrD_LearningLanguage.append(format(line.D_LearningLanguage))
                ArrD_LearningSubject.append(format(line.D_LearningSubject))
                ArrSlow_To_Learn.append(format(line.Slow_To_Learn))
                ArrRepeated_a_Grade.append(format(line.Repeated_a_Grade))
                ArrResult.append(format(line.Result))
                print(ArrResult)

            D_Reading_encoded = ArrD_Reading
            D_Spelling_encoded = ArrD_Spelling
            D_Handwriting_encoded = ArrD_Handwriting
            D_WrittenExpression_encoded = ArrD_WrittenExpression
            D_BasicArithmetic_encoded = ArrD_BasicArithmetic
            D_HigherArithmetic_encoded = ArrD_HigherArithmetic
            D_Attention_encoded = ArrD_Attention
            Easily_Distracted_encoded = ArrEasily_Distracted
            D_Memory_encoded = ArrD_Memory
            Lack_Motivation_encoded = ArrLack_Motivation
            D_StudySkills_encoded = ArrD_StudySkills
            Does_Not_like_School_encoded = ArrDoes_Not_like_School
            D_LearningLanguage_encoded = ArrD_LearningLanguage
            D_LearningSubject_encoded = ArrD_LearningSubject
            Slow_To_Learn_encoded = ArrSlow_To_Learn
            Repeated_a_Grade_encoded = ArrRepeated_a_Grade


            
            temp1 = list(zip(D_Reading_encoded,D_Spelling_encoded,D_Handwriting_encoded,D_WrittenExpression_encoded,D_BasicArithmetic_encoded,D_HigherArithmetic_encoded,D_Attention_encoded,Easily_Distracted_encoded,D_Memory_encoded,Lack_Motivation_encoded,D_StudySkills_encoded,Does_Not_like_School_encoded,D_LearningLanguage_encoded,D_LearningSubject_encoded,Slow_To_Learn_encoded,Repeated_a_Grade_encoded))
            model = lm.LogisticRegression(multi_class='multinomial', solver='newton-cg')
            model.fit(temp1, ArrResult)
            #score = model.evaluate(temp1,ArrResult)
            #print(score)'''
        model = load_model('model.h5')    
        predictions= model.predict([[int(D_Reading),int(D_Spelling),int(D_Handwriting),int(D_WrittenExpression),int(D_BasicArithmetic),int(D_HigherArithmetic),int(D_Attention),int(Easily_Distracted),int(D_Memory),int(Lack_Motivation),int(D_StudySkills),int(Does_Not_like_School),int(D_LearningLanguage),int(D_LearningSubject),int(Slow_To_Learn),int(Repeated_a_Grade)]])[0]
        print("Result :",predictions)
        rounded = [float(numpy.round(x)) for x in predictions]
        #output=round(predicted[0])
        print(rounded)
        #answer = predicted
        #print("before",answer)
        percent = str(percentage)
        print(percent)
        #data_save = TestResult(Users_id = User_id,Learning_Disability =result ,Date = date_joined[0] )
        if rounded[0] == 1.0:
            result = 'You have been detected as Learning Disable with' + ' ' + percent + ' %'
            messages.info(request,'You have been detected as Learning Disable with' + ' ' + percent + ' %.')
            data_save = TestResult(Users_id = User_id,Learning_Disability =result ,Date = date_joined[0] )
            data_save.save()
            return redirect('/TestDashboard/')
        else:
            result = 'You have not been detected as Learning Disable'
            messages.info(request,'You have not been detected as Learning Disable but can try out exercise')
            data_save = TestResult(Users_id = User_id,Learning_Disability =result ,Date = date_joined[0] )
            data_save.save()
            return redirect('/TestDashboard')

        
        

            #sentence = 'There is' + ' ' + answer
        '''data = {
        'respond': answer
        }
        return JsonResponse(data)'''
        return redirect('/')
    else:
        User_id = request.session['UserId']
        date_joined = datetime.now()
        print(date_joined)
        date_joined = str(date_joined).split(' ')
        print(date_joined[0])
        if TestResult.objects.all().filter(Users_id = User_id,Date = date_joined[0]).exists():
            messages.info(request,'You have already given the test for today try tommorow')
            return render(request,'home.html',{})
        else:
            print('else')
            return render(request,'TestDisability.html',{})
        return render(request,'home.html',{})

def MathsTest(request):
    if request.method == 'POST':
        score = 0   
        varq1 = int(request.POST['quest1'])
       

        if varq1 == 4:
            score=score+1
           
        else:
           
            score =score + 0

        
            
            
        
        varq2 = int(request.POST['quest2'])
        if varq2==10:
            score=score+1

        else:
            score=score+0

        varq3 = int(request.POST['quest3'])
        if varq3==120:
            score = score+1
        
        else:
            score=score+0
        
        varq4 = request.POST['quest4']
        if varq4==2:
            score = score+1
        else:
            score=score+0

        print(score,"final score")
        Maths_score = score
        print(Maths_score)
        User_id = request.session['UserId']
        date_joined = datetime.now()
        print(date_joined)
        date_joined = str(date_joined).split(' ')
        print(date_joined[0])

        if score<3:
            TestResult.objects.all().filter(Users_id = User_id ,Date = date_joined[0]).update(Maths_Test = str(Maths_score)+'/4' + ' ' + 'Dyscalculia')


            messages.info(request,'YOU FAILED')
            return redirect('/GrammarTest')

        else:
            TestResult.objects.all().filter(Users_id = User_id ,Date = date_joined[0]).update(Maths_Test = str(Maths_score)+'/4')
            messages.info(request,'YOU PASSED WITH SCORE' + ' ' + str(score) +' ' + 'out of 4')



        return redirect('/GrammarTest')
    
                      
       
    else:
        return render(request,'MathsTest.html',{})

def TestDashboard(request):
    return render(request,'TestDashboard.html',{})

def GrammarTest(request):
    if request.method == 'POST':
        score = 0   
        varq1 = request.POST['quest1']
        print(varq1.lower())
       


        if varq1.lower() =='short' :
            score=score+1
            print(score)
           
        else:
           
            score =score + 0

        
            
            
        
        varq2 = request.POST['quest2']
        if varq2.lower()=='women':
            score=score+1
            print(score)

        else:
            score=score+0

        varq3 = request.POST['quest3']
        print(varq3)
        if varq3.lower()=='a,e,i,o,u':
            score = score+1
            print(score)
        
        else:
            score=score+0
        
        varq4 = request.POST['quest4']
        print(varq4)
        if varq4.lower()=='apple,banana,grapes,kiwi,mango':
            score = score+1
        else:
            score=score+0

        print(score,"final score")
        User_id = request.session['UserId']
        date_joined = datetime.now()
        print(date_joined)
        date_joined = str(date_joined).split(' ')
        print(date_joined[0])
        if score<3:
            TestResult.objects.all().filter(Users_id = User_id ,Date = date_joined[0]).update(Grammar_Test = str(score)+'/4' + ' ' + 'Dyslexia')
            messages.info(request,'YOU FAILED')
            return redirect('/ReadingTest')
        else:
            TestResult.objects.all().filter(Users_id = User_id ,Date = date_joined[0]).update(Grammar_Test = str(score)+'/4')
            messages.info(request,'YOU PASSED WITH SCORE' + ' ' + str(score) +' ' + 'out of 4')
            return redirect('/ReadingTest')
    
                      
       
    else:
        return render(request,'GrammarTest.html',{})


def ReadingTest(request):
   
    if request.method == "POST":

        data = request.POST['start']
        print(data)
        if data == "start":
            
            CHUNK = 1024 
            FORMAT = pyaudio.paInt16 #paInt8
            CHANNELS = 2 
            RATE = 44100 #sample rate
            RECORD_SECONDS = 10
            today = date.today()
            time = datetime.now()
            new_time = str(time).split()
            print(new_time)
            print('Time',time)
            print("Today date is: ", today)
            #name = new_time[0] +'_'+new_time[1]
            WAVE_OUTPUT_FILENAME = "audio1.wav"
            #emotions=["Anger","disgust","fear","happy","Neutral", "sad", "surprise"]
            p = pyaudio.PyAudio()
            stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK) #buffer
            print("* recording")
            frames = []
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data) # 2 bytes(16 bits) per channel
            print("* done recording")
            stream.stop_stream()
            stream.close()
            p.terminate()
            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            file = 'G:/priya_backup/Priya/PythonProjects/ClassificationOfLD/ClassificationOfLD/' + WAVE_OUTPUT_FILENAME
            print(file)
       
            r = sr.Recognizer()
            with sr.AudioFile(file) as source:
                audio_text = r.listen(source)
                # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
            try:
            # using google speech recognition
                text = r.recognize_google(audio_text)
                print('Converting audio transcripts into text ...')
                print(text)
                text = text.split()
                print(text)
                if text==" ":
                    messages.info(request,'nothing is being recorded')

                else:
                    sentence = ['this','is','a', 'car']
                    score = 0
                    score1 = 4
                    for i in text :
                        if i in sentence:
                            score = score + 1
                            print('score',score)
            except:
                print('Sorry.. run again...')
                messages.info(request,'nothing is being recorded')
                return redirect('/ReadingTest')

                
            User_id = request.session['UserId']
            date_joined = datetime.now()
            print(date_joined)
            date_joined = str(date_joined).split(' ')
            print(date_joined[0])
            if score<3:
                TestResult.objects.all().filter(Users_id = User_id ,Date = date_joined[0]).update(Reading_Test = str(score) + '/4' + 'Dysgraphia')
                messages.info(request,'YOU FAILED,GO THISE LINK TO PRACTICE')
                return redirect('/MemoryTest1')
            else:
                TestResult.objects.all().filter(Users_id = User_id ,Date = date_joined[0]).update(Reading_Test = str(score) + '/4')
                messages.info(request,'YOU PASSED WITH SCORE' + ' ' + str(score) +' ' + 'out of 4')
                return redirect('/MemoryTest1')


 

    
            return redirect('/MemoryTest1')
        else:
            CHUNK = 1024 
            FORMAT = pyaudio.paInt16 #paInt8
            CHANNELS = 2 
            RATE = 44100 #sample rate
            RECORD_SECONDS = 1
            today = date.today()
            time = datetime.now()
            new_time = str(time).split()
            print(new_time)
            print('Time',time)
            print("Today date is: ", today)
            #name = new_time[0] +'_'+new_time[1]
            WAVE_OUTPUT_FILENAME = "audio1.wav"
            #emotions=["Anger","disgust","fear","happy","Neutral", "sad", "surprise"]
            p = pyaudio.PyAudio()
            stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK) #buffer
            print("* recording")
            frames = []
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data) # 2 bytes(16 bits) per channel
            print("* done recording")
            stream.stop_stream()
            stream.close()
            p.terminate()
            wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
            wf.close()
            files = 'G:/priya_backup/Priya/PythonProjects/' + WAVE_OUTPUT_FILENAME
            print(files)
            file = 'G:/priya_backup/Priya/PythonProjects/ClassificationOfLD/' + WAVE_OUTPUT_FILENAME
       
            r = sr.Recognizer()
            with sr.AudioFile(file) as source:
                audio_text = r.listen(source)
                # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
            try:
            # using google speech recognition
                text = r.recognize_google(audio_text)
                print('Converting audio transcripts into text ...')
                print(text)
                text = text.split()
                print(text)
                if text==" ":
                    messages.info(request,'nothing is being recorded')

                else:
                    sentence = ['this','is','a', 'car']
                    score = 0
                    score1 = 4
                    for i in text :
                        if i in sentence:
                            score = score + 1
                            print('score',score)
            except:
                print('Sorry.. run again...')
                messages.info(request,'nothing is being recorded')
                return redirect('/ReadingTest')

                
                if score<3:
                    messages.info(request,'YOU FAILED,GO THISE LINK TO PRACTICE')
                    return redirect('/ReadingLinks')
                else:
                   messages.info(request,'YOU PASSED WITH SCORE' + ' ' + str(score) +' ' + 'out of 4')
    else:
        return render(request,'ReadingTest.html',{})

def MemoryTest(request):
    if request.method == "POST":
        sentence = ['table', 'chair', 'tiffin', 'glass', 'bottle', 'dish', 'cup', 'plates','bowl','mat'] #'hat','pencil','pen','book','spoon','fork','chalk','dust']
        #sent = sentence.split(' ')
        #print(sent)
        #print(len(sent))
        score = 0
        var1 = request.POST['sent1']
        if var1 in sentence:
            print(var1)
            score=score+1
            print(score)
        else:
            score=score+0
        var2 = request.POST['sent2']
        if var2 in sentence:
            print(var2)
            score=score+1
            print(score)
        else:
            score=score+0
        var3 = request.POST['sent3']
        if var3 in sentence:
            print(var1)
            score=score+1
            print(score)
        else:
            score=score+0
        var4 = request.POST['sent4']
        if var4 in sentence:
            print(var4)
            score=score+1
            print(score)
        else:
            score=score+0
        var5 = request.POST['sent5']
        if var5 in sentence:
            print(var5)
            score=score+1
            print(score)
        else:
            score=score+0
        var6 = request.POST['sent6']
        if var6 in sentence:
            print(var6)
            score=score+1
            print(score)
        else:
            score=score+0
        var7 = request.POST['sent7']
        if var7 in sentence:
            print(var7)
            score=score+1
            print(score)
        else:
            score=score+0

        var8 = request.POST['sent8']
        if var8 in sentence:
            print(var8)
            score=score+1
            print(score)
        else:
            score=score+0
        var9 = request.POST['sent9']
        if var9 in sentence:
            print(var9)
            score=score+1
            print(score)
        else:
            score=score+0
        var10 = request.POST['sent10']
        if var10 in sentence:
            print(var10)
            score=score+1
            print(score)
        else:
            score=score+0
        '''var11 = request.POST['sent11']
        if var11 in sentence:
            print(var11)
            score=score+1
            print(score)
        else:
            score=score+0
        var12 = request.POST['sent12']
        if var12 in sentence:
            print(var12)
            score=score+1
            print(score)
        else:
            score=score+0
        var13 = request.POST['sent13']
        if var13 in sentence:
            print(var13)
            score=score+1
            print(score)
        else:
            score=score+0
        var14 = request.POST['sent14']
        if var14 in sentence:
            print(var14)
            score=score+1
            print(score)
        else:
            score=score+0
        var15 = request.POST['sent15']
        if var15 in sentence:
            print(var15)
            score=score+1
            print(score)
        else:
            score=score+0
        var16 = request.POST['sent16']
        if var16 in sentence:
            print(var16)
            score=score+1
            print(score)
        else:
            score=score+0
        var17 = request.POST['sent17']
        if var17 in sentence:
            print(var17)
            score=score+1
            print(score)
        else:
            score=score+0
        var18 = request.POST['sent18']
        if var18 in sentence:
            print(var18)
            score=score+1
            print(score)
        else:
            score=score+0
        var19 = request.POST['sent19']
        if var19 in sentence:
            print(var19)
            score=score+1
            print(score)
        else:
            score=score+0
        var20 = request.POST['sent20']
        if var20 in sentence:
            print(var20)
            score=score+1
            print(score)
        else:
            score=score+0'''
        
        print('score',score)
        User_id = request.session['UserId']
        date_joined = datetime.now()
        print(date_joined)
        date_joined = str(date_joined).split(' ')
        print(date_joined[0])
        if score<3:
            TestResult.objects.all().filter(Users_id = User_id ,Date = date_joined[0]).update(Memory_audio = str(score) + '/10' + 'Dysgraphia')
            messages.info(request,'YOU FAILED,GO THISE LINK TO PRACTICE')
            return redirect('/MemoryLinks')
        else:
            TestResult.objects.all().filter(Users_id = User_id ,Date = date_joined[0]).update(Memory_audio = str(score) + '/10')
            messages.info(request,'YOU PASSED WITH SCORE' + ' ' + str(score) +' ' + 'out of 10')

            
        return redirect('/ScenariosTest')
    else:
        return render(request,'MemoryTest.html',{})

def ScenariosTest(request):
    return render(request,'ScenariosTest.html',{})

def Reading(request):
    if request.method == "POST":
        CHUNK = 1024 
        FORMAT = pyaudio.paInt16 #paInt8
        CHANNELS = 2 
        RATE = 44100 #sample rate
        RECORD_SECONDS = 20
        WAVE_OUTPUT_FILENAME = "audio1.mp3"
        #emotions=["Anger","disgust","fear","happy","Neutral", "sad", "surprise"]
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK) #buffer
        print("* recording")
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data) # 2 bytes(16 bits) per channel
        print("* done recording")
        return render(request,'ReadingTest.html',{})
    else:
        return render(request,'ReadingTest.html',{})



def Stop(request):
    if request.method == "POST":
        stream.stop_stream()
        stream.close()
        p.terminate()
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        file = 'G:/priya_backup/Priya/PythonProjects/ClassificationOfLD/' + WAVE_OUTPUT_FILENAME
        print(file)
        return render(request,'ReadingTest.html',{})
    else:
        return render(request,'ReadingTest.html',{})

def TrainingData(request):
    if request.method == "POST":
        D_Reading = request.POST['D_Reading'] 
        D_Spelling = request.POST['D_Spelling']
        D_Handwriting = request.POST['D_Handwriting']
        D_WrittenExpression = request.POST['D_WrittenExpression']
        D_BasicArithmetic = request.POST['D_BasicArithmetic']
        D_HigherArithmetic = request.POST['D_HigherArithmetic']
        D_Attention = request.POST['D_Attention']
        Easily_Distracted = request.POST['Easily_Distracted']
        D_Memory = request.POST['D_Memory']
        Lack_Motivation = request.POST['Lack_Motivation']
        D_StudySkills = request.POST['D_StudySkills']
        Does_Not_like_School = request.POST['Does_Not_like_School']
        D_LearningLanguage = request.POST['D_LearningLanguage']
        D_LearningSubject = request.POST['D_LearningSubject']
        Slow_To_Learn = request.POST['Slow_To_Learn']
        Repeated_a_Grade = request.POST['Repeated_a_Grade']
        Result = request.POST['Result']
        data = DisabilityTest(D_Reading=D_Reading,D_Spelling=D_Spelling,D_Handwriting=D_Handwriting,D_WrittenExpression=D_WrittenExpression,D_BasicArithmetic=D_BasicArithmetic,D_HigherArithmetic=D_HigherArithmetic,D_Attention=D_Attention,Easily_Distracted=Easily_Distracted,D_Memory=D_Memory,Lack_Motivation=Lack_Motivation,D_StudySkills=D_StudySkills,Does_Not_like_School=Does_Not_like_School,D_LearningLanguage=D_LearningLanguage,D_LearningSubject=D_LearningSubject,Slow_To_Learn=Slow_To_Learn,Repeated_a_Grade=Repeated_a_Grade,Result=Result)
        data.save()
        messages.info(request,'Data Added Successfully')
        return render(request,'TrainingData.html',{})
    else:
        return render(request,'TrainingData.html',{})


def videotest1(request):
    if request.method == 'POST':
        score = 0   
        varq1 = request.POST['var1']
        print(varq1.lower())
        if varq1.lower() =='friends' :
            score=score+1
            print(score)
        else:
            score =score + 0

        
            
            
        
        varq2 = request.POST['var2']
        if varq2.lower()=='forest':
            score=score+1
            print(score)

        else:
            score=score+0

        varq3 = request.POST['var3']
        print(varq3)
        if varq3.lower()=='rabbit':
            score = score+1
            print(score)
        
        else:
            score=score+0
        
        varq4 = request.POST['var4']
        print(varq4)
        if varq4.lower()=='squirrel':
            score = score+1
        else:
            score=score+0

        varq5 = request.POST['var5']
        print(varq4)
        if varq5.lower()=='by crossing the bridge':
            score = score+1
        else:
            score=score+0

        print(score,"final score")
        User_id = request.session['UserId']
        date_joined = datetime.now()
        print(date_joined)
        date_joined = str(date_joined).split(' ')
        print(date_joined[0])
        if score<3:
            TestResult.objects.all().filter(Users_id = User_id ,Date = date_joined[0]).update(Video_test1 = str(score)+'/5' + ' ' + 'Dyslexia')
            messages.info(request,'YOU FAILED')

        else:
            TestResult.objects.all().filter(Users_id = User_id ,Date = date_joined[0]).update(Video_test1 = str(score)+'/5')
            messages.info(request,'YOU PASSED WITH SCORE' + ' ' + str(score) +' ' + 'out of 5')



        return redirect('/ScenariosTest')
    
                      
       
    else:
        return render(request,'videotest1.html',{})

def videotest2(request):
    if request.method == 'POST':
        score = 0   
        varq1 = request.POST['var1']
        print(varq1.lower())
        if varq1.lower() =='john and eric' :
            score=score+1
            print(score)
        else:
            score =score + 0

        
            
            
        
        varq2 = request.POST['var2']
        print(varq2)
        if varq2.lower()=='positive':
            score=score+1
            print(score)

        else:
            score=score+0

        varq3 = request.POST['var3']
        print(varq3)
        if varq3.lower()=='month end':
            score = score+1
            print(score)
        
        else:
            score=score+0
        
        varq4 = request.POST['var4']
        print(varq4)
        if varq4.lower()=='product team':
            score = score+1
            print(score)
        else:
            score=score+0

        varq5 = request.POST['var5']
        print(varq5)
        if varq5.lower()=='office environment':
            score = score+1
            print(score)
        else:
            score=score+0

        print(score,"final score")
        User_id = request.session['UserId']
        date_joined = datetime.now()
        print(date_joined)
        date_joined = str(date_joined).split(' ')
        print(date_joined[0])
        if score<3:
            TestResult.objects.all().filter(Users_id = User_id ,Date = date_joined[0]).update(Video_test2 = str(score)+'/5' + ' ' + 'Dyslexia')
            messages.info(request,'YOU FAILED')

        else:
            TestResult.objects.all().filter(Users_id = User_id ,Date = date_joined[0]).update(Video_test2 = str(score)+'/5')
            messages.info(request,'YOU PASSED WITH SCORE' + ' ' + str(score) +' ' + 'out of 5')



        return redirect('/ScenariosTest')
    else:
        return render(request,'videotest2.html',{})

def videotest3(request):
    if request.method == 'POST':
        score = 0   
        varq1 = request.POST['var1']
        print(varq1.lower())
        if varq1.lower() =='arjun' :
            score=score+1
            print(score)
        else:
            score =score + 0

        
            
            
        
        varq2 = request.POST['var2']
        print(varq2)
        if varq2.lower()=='school':
            score=score+1
            print(score)

        else:
            score=score+0

        varq3 = request.POST['var3']
        print(varq3)
        if varq3.lower()=='singing':
            score = score+1
            print(score)
        
        else:
            score=score+0
        
        varq4 = request.POST['var4']
        print(varq4)
        if varq4.lower()=='on same day':
            score = score+1
            print(score)
        else:
            score=score+0

        varq5 = request.POST['var5']
        print(varq5)
        if varq5.lower()=='ticket to circus':
            score = score+1
            print(score)
        else:
            score=score+0

        print(score,"final score")
        User_id = request.session['UserId']
        date_joined = datetime.now()
        print(date_joined)
        date_joined = str(date_joined).split(' ')
        print(date_joined[0])
        if score<3:
            TestResult.objects.all().filter(Users_id = User_id ,Date = date_joined[0]).update(Video_test3 = str(score)+'/5' + ' ' + 'Dyslexia')
            messages.info(request,'YOU FAILED')

        else:
            TestResult.objects.all().filter(Users_id = User_id ,Date = date_joined[0]).update(Video_test3 = str(score)+'/5')
            messages.info(request,'YOU PASSED WITH SCORE' + ' ' + str(score) +' ' + 'out of 5')



        return redirect('/ViewResults')
    else:
        return render(request,'videotest3.html',{})


def MathsLinks(request):
    return render(request,'MathsLinks.html',{})


def GrammarLinks(request):
    return render(request,'GrammarLinks.html',{})

def ReadingLinks(request):
    return render(request,'ReadingLinks.html',{})

def MemoryLinks(request):
    return render(request,'MemoryLinks.html',{})

def ScenariosLink(request):
    return render(request,'ScenariosLink.html',{})


def images(request):
    return render(request,'images.html',{})


def MemoryTest1(request):
    if request.method == "POST":
        sentence = ['table', 'chair', 'car', 'tree', 'cat', 'dog', 'cake','umbrella'] #'hat','pencil','pen','book','spoon','fork','chalk','dust']
        #sent = sentence.split(' ')
        #print(sent)
        #print(len(sent))
        score = 0
        var1 = request.POST['sent1']
        if var1.lower() in sentence:
            print(var1)
            score=score+1
            print(score)
        else:
            score=score+0
        var2 = request.POST['sent2']
        if var2.lower() in sentence:
            print(var2)
            score=score+1
            print(score)
        else:
            score=score+0
        var3 = request.POST['sent3']
        if var3.lower() in sentence:
            print(var1)
            score=score+1
            print(score)
        else:
            score=score+0
        var4 = request.POST['sent4']
        if var4.lower() in sentence:
            print(var4)
            score=score+1
            print(score)
        else:
            score=score+0
        var5 = request.POST['sent5']
        if var5.lower() in sentence:
            print(var5)
            score=score+1
            print(score)
        else:
            score=score+0
        var6 = request.POST['sent6']
        if var6.lower() in sentence:
            print(var6)
            score=score+1
            print(score)
        else:
            score=score+0
        var7 = request.POST['sent7']
        if var7.lower() in sentence:
            print(var7)
            score=score+1
            print(score)
        else:
            score=score+0

        var8 = request.POST['sent8']
        if var8.lower() in sentence:
            print(var8)
            score=score+1
            print(score)
        else:
            score=score+0
        print(score,"final score")

        print('score',score)
        User_id = request.session['UserId']
        date_joined = datetime.now()
        print(date_joined)
        date_joined = str(date_joined).split(' ')
        print(date_joined[0])
        if score<3:
            TestResult.objects.all().filter(Users_id = User_id ,Date = date_joined[0]).update(Memory_images = str(score) + '/8' + 'Dysgraphia')
            return redirect('/MemoryLinks')
        else:
            TestResult.objects.all().filter(Users_id = User_id ,Date = date_joined[0]).update(Memory_images = str(score) + '/8')
            messages.info(request,'YOU PASSED WITH SCORE' + ' ' + str(score) +' ' + 'out of 8')
            return redirect('/MemoryTest/')
    else:
        return render(request,'MemoryTest1.html',{})

def ViewResults(request):
    User_id = request.session['UserId']
    details = TestResult.objects.all().filter(Users_id = User_id)
    return render(request,'ViewResults.html',{'details':details})
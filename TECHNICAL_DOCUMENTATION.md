# Technical Documentation: InsightEDU3.2

**Version:** 3.2  
**Last Updated:** 2024  
**Document Type:** Technical Specification

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Technology Stack](#technology-stack)
3. [Database Schema](#database-schema)
4. [API Reference](#api-reference)
5. [Models](#models)
6. [Views and URLs](#views-and-urls)
7. [Machine Learning Integration](#machine-learning-integration)
8. [Configuration](#configuration)
9. [Deployment](#deployment)
10. [Troubleshooting](#troubleshooting)

---

## System Architecture

### Overview

InsightEDU3.2 is built using Django's Model-View-Template (MVT) architecture pattern.

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│              (HTML Templates + Bootstrap)                │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                    View Layer                            │
│         (Django Views - Business Logic)                  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                    Model Layer                           │
│              (Django ORM + Database)                     │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                    Data Layer                            │
│                    (MySQL Database)                       │
└─────────────────────────────────────────────────────────┘
```

### Component Architecture

1. **Models** (`AppClassificationOfLD/models.py`)
   - Define database schema
   - Handle data validation
   - Provide ORM interface

2. **Views** (`AppClassificationOfLD/views.py`)
   - Handle HTTP requests
   - Process business logic
   - Render templates
   - Interact with ML models

3. **Templates** (`AppClassificationOfLD/TEMPLATES/`)
   - HTML presentation layer
   - User interface components

4. **URLs** (`AppClassificationOfLD/urls.py`)
   - URL routing
   - Request mapping

---

## Technology Stack

### Backend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.8+ | Programming language |
| Django | 4.1.7 | Web framework |
| MySQL | 5.7+ | Database |
| TensorFlow | 2.11.0 | Machine learning |
| Keras | 2.11.0 | Neural network API |
| NumPy | 1.23.5 | Numerical computing |

### Frontend Technologies

| Technology | Version | Purpose |
|------------|---------|---------|
| HTML5 | - | Markup |
| CSS3 | - | Styling |
| JavaScript | - | Client-side scripting |
| Bootstrap | 5.1.3 | UI framework |

### Additional Libraries

- **PyAudio:** Audio input/output
- **SpeechRecognition:** Speech-to-text conversion
- **pydub:** Audio manipulation
- **scikit-learn:** ML utilities

---

## Database Schema

### Entity Relationship Diagram

```
┌──────────────┐
│ UserDetails  │
├──────────────┤
│ id (PK)      │
│ Firstname    │
│ Lastname     │
│ Phone        │
│ Email        │
│ Username     │
│ Password     │
└──────────────┘
       │
       │ 1:N
       │
┌──────▼──────────┐
│   TestResult    │
├─────────────────┤
│ id (PK)         │
│ Users_id (FK)   │
│ Learning_       │
│   Disability    │
│ Maths_Test      │
│ Grammar_Test    │
│ Reading_Test    │
│ Memory_images   │
│ Memory_audio    │
│ Video_test1     │
│ Video_test2      │
│ Video_test3      │
│ Date            │
└─────────────────┘

┌──────────────┐
│ DisabilityTest│
├──────────────┤
│ id (PK)      │
│ D_Reading    │
│ D_Spelling   │
│ ... (16 params)│
│ Result       │
└──────────────┘

┌──────────────┐
│  admindata   │
├──────────────┤
│ id (PK)      │
│ Username     │
│ Password     │
└──────────────┘
```

### Table Specifications

#### UserDetails

```sql
CREATE TABLE UserDetails (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Firstname VARCHAR(100) DEFAULT NULL,
    Lastname VARCHAR(100) DEFAULT NULL,
    Phone VARCHAR(100) DEFAULT NULL,
    Email VARCHAR(100) DEFAULT NULL,
    Username VARCHAR(100) DEFAULT NULL,
    Password VARCHAR(100) DEFAULT NULL
);
```

**Fields:**
- `id`: Primary key, auto-increment
- `Firstname`: User's first name
- `Lastname`: User's last name
- `Phone`: Contact phone number
- `Email`: Email address (unique identifier)
- `Username`: Login username
- `Password`: User password (⚠️ Currently plain text - needs hashing)

#### DisabilityTest

```sql
CREATE TABLE DisabilityTest (
    id INT AUTO_INCREMENT PRIMARY KEY,
    D_Reading VARCHAR(100) DEFAULT NULL,
    D_Spelling VARCHAR(100) DEFAULT NULL,
    D_Handwriting VARCHAR(100) DEFAULT NULL,
    D_WrittenExpression VARCHAR(100) DEFAULT NULL,
    D_BasicArithmetic VARCHAR(100) DEFAULT NULL,
    D_HigherArithmetic VARCHAR(100) DEFAULT NULL,
    D_Attention VARCHAR(100) DEFAULT NULL,
    Easily_Distracted VARCHAR(100) DEFAULT NULL,
    D_Memory VARCHAR(100) DEFAULT NULL,
    Lack_Motivation VARCHAR(100) DEFAULT NULL,
    D_StudySkills VARCHAR(100) DEFAULT NULL,
    Does_Not_like_School VARCHAR(100) DEFAULT NULL,
    D_LearningLanguage VARCHAR(100) DEFAULT NULL,
    D_LearningSubject VARCHAR(100) DEFAULT NULL,
    Slow_To_Learn VARCHAR(100) DEFAULT NULL,
    Repeated_a_Grade VARCHAR(100) DEFAULT NULL,
    Result VARCHAR(100) DEFAULT NULL
);
```

**Purpose:** Stores training data for ML model

#### TestResult

```sql
CREATE TABLE TestResult (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Users_id VARCHAR(100) DEFAULT NULL,
    Learning_Disability VARCHAR(100) DEFAULT NULL,
    Maths_Test VARCHAR(100) DEFAULT NULL,
    Dyslexia VARCHAR(100) DEFAULT NULL,
    Dysgraphia VARCHAR(100) DEFAULT NULL,
    Dyscalculia VARCHAR(100) DEFAULT NULL,
    Grammar_Test VARCHAR(100) DEFAULT NULL,
    Reading_Test VARCHAR(100) DEFAULT NULL,
    Memory_images VARCHAR(100) DEFAULT NULL,
    Memory_audio VARCHAR(100) DEFAULT NULL,
    Scenario_Test VARCHAR(100) DEFAULT NULL,
    Video_test1 VARCHAR(100) DEFAULT NULL,
    Video_test2 VARCHAR(100) DEFAULT NULL,
    Video_test3 VARCHAR(100) DEFAULT NULL,
    Date DATE DEFAULT NULL
);
```

**Purpose:** Stores individual test results for users

#### admindata

```sql
CREATE TABLE admindata (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(100) DEFAULT NULL,
    Password VARCHAR(100) DEFAULT NULL
);
```

**Purpose:** Admin user credentials

---

## API Reference

### URL Patterns

#### Authentication URLs

| URL Pattern | View Function | Method | Description |
|-------------|---------------|--------|-------------|
| `/UserLogin/` | `UserLogin` | GET/POST | User login |
| `/UserRegisteration/` | `UserRegisteration` | GET/POST | User registration |
| `/AdminLogin/` | `AdminLogin` | GET/POST | Admin login |
| `/Logout/` | `Logout` | GET | Logout user |

#### Assessment URLs

| URL Pattern | View Function | Method | Description |
|-------------|---------------|--------|-------------|
| `/` | `home` | GET | Home page |
| `/TestDisability/` | `TestDisability` | GET/POST | Disability assessment |
| `/TestDashboard/` | `TestDashboard` | GET | Test dashboard |
| `/MathsTest/` | `MathsTest` | GET/POST | Mathematics test |
| `/GrammarTest/` | `GrammarTest` | GET/POST | Grammar test |
| `/ReadingTest/` | `ReadingTest` | GET/POST | Reading test |
| `/MemoryTest/` | `MemoryTest` | GET/POST | Audio memory test |
| `/MemoryTest1/` | `MemoryTest1` | GET/POST | Image memory test |
| `/videotest1/` | `videotest1` | GET/POST | Video test 1 |
| `/videotest2/` | `videotest2` | GET/POST | Video test 2 |
| `/videotest3/` | `videotest3` | GET/POST | Video test 3 |
| `/ScenariosTest/` | `ScenariosTest` | GET | Scenarios test page |

#### Results URLs

| URL Pattern | View Function | Method | Description |
|-------------|---------------|--------|-------------|
| `/ViewResults/` | `ViewResults` | GET | View test results |

#### Resource URLs

| URL Pattern | View Function | Method | Description |
|-------------|---------------|--------|-------------|
| `/MathsLinks/` | `MathsLinks` | GET | Maths practice links |
| `/GrammarLinks/` | `GrammarLinks` | GET | Grammar practice links |
| `/ReadingLinks/` | `ReadingLinks` | GET | Reading practice links |
| `/MemoryLinks/` | `MemoryLinks` | GET | Memory practice links |
| `/ScenariosLink/` | `ScenariosLink` | GET | Scenarios practice links |

#### Admin URLs

| URL Pattern | View Function | Method | Description |
|-------------|---------------|--------|-------------|
| `/TrainingData/` | `TrainingData` | GET/POST | Add training data |

---

## Models

### UserDetails Model

```python
class UserDetails(models.Model):
    Firstname = models.CharField(max_length=100, default=None)
    Lastname = models.CharField(max_length=100, default=None)
    Phone = models.CharField(max_length=100, default=None)
    Email = models.EmailField(max_length=100, default=None)
    Username = models.CharField(max_length=100, default=None)
    Password = models.CharField(max_length=100, default=None)
    
    class Meta:
        db_table = 'UserDetails'
```

**Usage:**
```python
# Create user
user = UserDetails.objects.create(
    Firstname="John",
    Lastname="Doe",
    Email="john@example.com",
    Username="johndoe",
    Password="password123"
)

# Query user
user = UserDetails.objects.filter(Username="johndoe").first()
```

### TestResult Model

```python
class TestResult(models.Model):
    Users_id = models.CharField(max_length=100, default=None, null=True)
    Learning_Disability = models.CharField(max_length=100, default=None, null=True)
    Maths_Test = models.CharField(max_length=100, default=None, null=True)
    Grammar_Test = models.CharField(max_length=100, default=None, null=True)
    Reading_Test = models.CharField(max_length=100, default=None, null=True)
    Memory_images = models.CharField(max_length=100, default=None, null=True)
    Memory_audio = models.CharField(max_length=100, default=None, null=True)
    Video_test1 = models.CharField(max_length=100, default=None, null=True)
    Video_test2 = models.CharField(max_length=100, default=None, null=True)
    Video_test3 = models.CharField(max_length=100, default=None, null=True)
    Date = models.DateField(max_length=100, default=None, null=True)
    
    class Meta:
        db_table = 'TestResult'
```

**Usage:**
```python
# Create test result
result = TestResult.objects.create(
    Users_id="1",
    Learning_Disability="Learning Disability",
    Date=date.today()
)

# Update result
TestResult.objects.filter(
    Users_id="1",
    Date=date.today()
).update(Maths_Test="4/4")
```

---

## Views and URLs

### Key View Functions

#### TestDisability View

**Purpose:** Handles disability assessment questionnaire and ML model prediction

**Process:**
1. Collects 16 assessment parameters from POST request
2. Converts to numerical array
3. Calculates percentage of positive responses
4. Loads ML model (`model.h5`)
5. Generates prediction
6. Saves result to database
7. Redirects to test dashboard

**Code Flow:**
```python
def TestDisability(request):
    if request.method == "POST":
        # Collect parameters
        list1 = [int(D_Reading), int(D_Spelling), ...]
        
        # Calculate percentage
        percentage = (sum(list1) / 16) * 100
        
        # Load and predict
        model = load_model('model.h5')
        predictions = model.predict([list1])[0]
        
        # Save result
        TestResult.objects.create(...)
        
        return redirect('/TestDashboard/')
```

#### MathsTest View

**Purpose:** Evaluates mathematical skills

**Questions:**
1. Basic arithmetic
2. Addition
3. Multiplication
4. Division

**Scoring:**
- Score < 3: Indicates potential Dyscalculia
- Score >= 3: Pass

#### GrammarTest View

**Purpose:** Evaluates grammar and language skills

**Questions:**
1. Antonym identification
2. Plural forms
3. Vowel identification
4. Word categorization

**Scoring:**
- Score < 3: Indicates potential Dyslexia
- Score >= 3: Pass

---

## Machine Learning Integration

### Model Architecture

**File:** `model.h5`  
**Framework:** Keras/TensorFlow  
**Type:** Neural Network

### Model Input

16-dimensional feature vector:
```python
[
    D_Reading, D_Spelling, D_Handwriting, D_WrittenExpression,
    D_BasicArithmetic, D_HigherArithmetic, D_Attention,
    Easily_Distracted, D_Memory, Lack_Motivation,
    D_StudySkills, Does_Not_like_School,
    D_LearningLanguage, D_LearningSubject,
    Slow_To_Learn, Repeated_a_Grade
]
```

Each parameter: `0` (No) or `1` (Yes)

### Model Output

Binary classification:
- `1.0`: Learning Disability detected
- `0.0`: No Learning Disability

### Usage in Code

```python
from keras.models import load_model
import numpy

# Load model
model = load_model('model.h5')

# Prepare input
input_data = [[1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0]]

# Predict
predictions = model.predict(input_data)[0]
rounded = [float(numpy.round(x)) for x in predictions]

# Classify
if rounded[0] == 1.0:
    result = "Learning Disability detected"
else:
    result = "No Learning Disability"
```

### Model Training

**Training Data:** Stored in `DisabilityTest` table  
**Process:** Admin can add training data via `/TrainingData/` endpoint

---

## Configuration

### Django Settings (`ClassificationOfLD/settings.py`)

**Key Settings:**

```python
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Classification_db',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Static Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'AppClassificationOfLD/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### Environment Variables (Recommended)

Create `.env` file:
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
DB_NAME=Classification_db
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=127.0.0.1
DB_PORT=3306
```

---

## Deployment

### Development Server

```bash
python manage.py runserver
```

### Production Deployment

**Using Gunicorn:**

```bash
# Install Gunicorn
pip install gunicorn

# Run server
gunicorn ClassificationOfLD.wsgi:application --bind 0.0.0.0:8000
```

**Using Nginx:**

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/InsightEDU3.2/assets/;
    }

    location /media/ {
        alias /path/to/InsightEDU3.2/media/;
    }
}
```

---

## Troubleshooting

### Common Issues

#### 1. Database Connection Error

**Error:** `django.db.utils.OperationalError`

**Solution:**
- Verify MySQL is running
- Check database credentials in settings.py
- Ensure database exists: `CREATE DATABASE Classification_db;`

#### 2. Model File Not Found

**Error:** `FileNotFoundError: model.h5`

**Solution:**
- Ensure model.h5 is in project root directory
- Check file permissions

#### 3. Audio Recording Issues

**Error:** PyAudio installation or microphone access

**Solution:**
- Install PyAudio: `pip install PyAudio`
- Grant microphone permissions in browser
- Check audio device availability

#### 4. Static Files Not Loading

**Solution:**
```bash
python manage.py collectstatic
```

#### 5. Migration Issues

**Solution:**
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Performance Considerations

### Database Optimization

- Add indexes on frequently queried fields
- Use `select_related()` for foreign key queries
- Implement database connection pooling

### Caching

- Enable Django caching for static content
- Cache ML model loading
- Implement session caching

### Static Files

- Use CDN for production
- Enable compression
- Optimize images and assets

---

## Security Best Practices

### Current Implementation

- ✅ CSRF protection enabled
- ✅ SQL injection prevention (Django ORM)
- ✅ XSS protection (Django templates)

### Recommended Improvements

1. **Password Security:**
   ```python
   from django.contrib.auth.hashers import make_password
   user.Password = make_password(password)
   ```

2. **Environment Variables:**
   ```python
   import os
   SECRET_KEY = os.environ.get('SECRET_KEY')
   ```

3. **HTTPS:** Enable SSL/TLS in production

4. **Input Validation:** Enhanced validation for all inputs

---

**Document Version:** 1.0  
**Last Updated:** 2024

---

*For installation instructions, see `INSTALLATION_GUIDE.md`*  
*For user instructions, see `USER_MANUAL.md`*


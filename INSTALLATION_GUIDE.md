# Installation Guide: InsightEDU3.2

**Version:** 3.2  
**Last Updated:** 2024

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [System Requirements](#system-requirements)
3. [Installation Steps](#installation-steps)
4. [Configuration](#configuration)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

Before installing InsightEDU3.2, ensure you have the following installed:

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - Verify installation: `python --version`

2. **MySQL 5.7+ or MySQL 8.0+**
   - Download from: https://dev.mysql.com/downloads/mysql/
   - Verify installation: `mysql --version`

3. **Git** (Optional, for version control)
   - Download from: https://git-scm.com/downloads

4. **Web Browser**
   - Chrome, Firefox, Edge, or Safari (latest version)

### Required Python Packages

All required packages are listed in `requirement.txt`. The installation process will install them automatically.

---

## System Requirements

### Minimum Requirements

- **Operating System:** Windows 10+, Linux (Ubuntu 18.04+), macOS 10.14+
- **RAM:** 4GB (8GB recommended)
- **Storage:** 2GB free space
- **Processor:** Dual-core 2.0 GHz or higher
- **Internet:** Required for initial setup and package installation

### Recommended Requirements

- **RAM:** 8GB or more
- **Storage:** 5GB free space
- **Processor:** Quad-core 2.5 GHz or higher
- **Database:** Dedicated MySQL server for production

---

## Installation Steps

### Step 1: Clone or Download the Project

**Option A: Using Git**
```bash
git clone <repository-url>
cd InsightEDU3.2
```

**Option B: Download ZIP**
1. Download the project ZIP file
2. Extract to your desired location
3. Navigate to the project directory

### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv env
env\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv env
source env/bin/activate
```

**Verify activation:** Your command prompt should show `(env)` prefix.

### Step 3: Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirement.txt
```

**Note:** This may take several minutes as it installs many packages including TensorFlow.

### Step 4: Set Up MySQL Database

#### 4.1 Create Database

1. Open MySQL command line or MySQL Workbench
2. Connect to MySQL server
3. Create database:

```sql
CREATE DATABASE Classification_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 4.2 Create Database User (Optional but Recommended)

```sql
CREATE USER 'insight_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON Classification_db.* TO 'insight_user'@'localhost';
FLUSH PRIVILEGES;
```

### Step 5: Configure Database Settings

Edit `ClassificationOfLD/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Classification_db',
        'USER': 'root',  # or 'insight_user' if created
        'PASSWORD': '',  # Your MySQL password
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

**⚠️ Security Note:** For production, use environment variables instead of hardcoding credentials.

### Step 6: Install MySQL Client Library

**Windows:**
```bash
# If you encounter MySQL client errors, install:
pip install mysqlclient
# Or download wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
pip install mysqlclient
```

**macOS:**
```bash
brew install mysql
pip install mysqlclient
```

### Step 7: Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates all necessary database tables.

### Step 8: Create Admin User (Optional)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin user for Django admin panel.

### Step 9: Collect Static Files

```bash
python manage.py collectstatic
```

This collects all static files (CSS, JavaScript, images) into the `assets` directory.

### Step 10: Verify ML Model File

Ensure `model.h5` is present in the project root directory. This is the pre-trained machine learning model.

**If missing:** You may need to train the model or obtain it from the project repository.

### Step 11: Run Development Server

```bash
python manage.py runserver
```

The server will start on `http://127.0.0.1:8000/`

### Step 12: Access the Application

Open your web browser and navigate to:
```
http://127.0.0.1:8000/
```

---

## Configuration

### Environment Variables (Recommended for Production)

Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database Settings
DB_NAME=Classification_db
DB_USER=root
DB_PASSWORD=your-password
DB_HOST=127.0.0.1
DB_PORT=3306
```

Update `settings.py` to use environment variables:

```python
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-secret-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME', 'Classification_db'),
        'USER': os.environ.get('DB_USER', 'root'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}
```

**Install python-dotenv:**
```bash
pip install python-dotenv
```

### Static and Media Files Configuration

**Static Files:**
- Development: Served automatically by Django
- Production: Use `python manage.py collectstatic` and serve via web server

**Media Files:**
- Location: `media/` directory in project root
- Ensure directory exists and has write permissions

### Security Settings for Production

**Before deploying to production:**

1. **Change SECRET_KEY:**
   ```python
   SECRET_KEY = os.environ.get('SECRET_KEY')  # Use environment variable
   ```

2. **Set DEBUG to False:**
   ```python
   DEBUG = False
   ```

3. **Configure ALLOWED_HOSTS:**
   ```python
   ALLOWED_HOSTS = ['your-domain.com', 'www.your-domain.com']
   ```

4. **Enable HTTPS:**
   - Obtain SSL certificate
   - Configure web server (Nginx/Apache) for HTTPS

---

## Verification

### Verify Installation

1. **Check Python Version:**
   ```bash
   python --version
   # Should show Python 3.8 or higher
   ```

2. **Check Django Installation:**
   ```bash
   python manage.py --version
   # Should show Django 4.1.7
   ```

3. **Check Database Connection:**
   ```bash
   python manage.py dbshell
   # Should connect to MySQL
   ```

4. **Verify Tables Created:**
   ```sql
   USE Classification_db;
   SHOW TABLES;
   # Should show: UserDetails, DisabilityTest, TestResult, admindata
   ```

5. **Test Server:**
   - Start server: `python manage.py runserver`
   - Open browser: `http://127.0.0.1:8000/`
   - Should see home page

### Test User Registration

1. Navigate to registration page
2. Create a test user
3. Verify user appears in database:
   ```sql
   SELECT * FROM UserDetails;
   ```

### Test ML Model

1. Register and login as user
2. Complete disability assessment
3. Verify prediction is generated
4. Check test results are saved

---

## Troubleshooting

### Issue 1: MySQL Connection Error

**Error:**
```
django.db.utils.OperationalError: (2003, "Can't connect to MySQL server")
```

**Solutions:**
1. Verify MySQL is running:
   ```bash
   # Windows
   net start MySQL
   
   # Linux
   sudo systemctl start mysql
   
   # macOS
   brew services start mysql
   ```

2. Check MySQL credentials in `settings.py`
3. Verify database exists: `SHOW DATABASES;`
4. Check firewall settings

### Issue 2: Module Not Found Error

**Error:**
```
ModuleNotFoundError: No module named 'xxx'
```

**Solution:**
```bash
pip install -r requirement.txt
```

If specific package fails:
```bash
pip install package-name
```

### Issue 3: PyAudio Installation Error

**Error:**
```
error: Microsoft Visual C++ 14.0 is required
```

**Solutions:**

**Windows:**
1. Install Visual C++ Build Tools
2. Or use pre-built wheel:
   ```bash
   pip install pipwin
   pipwin install pyaudio
   ```

**Linux:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

### Issue 4: Model File Not Found

**Error:**
```
FileNotFoundError: model.h5
```

**Solution:**
1. Verify `model.h5` is in project root
2. Check file permissions
3. If missing, contact project maintainer or train new model

### Issue 5: Static Files Not Loading

**Error:** CSS/JavaScript not appearing

**Solution:**
```bash
python manage.py collectstatic
```

Ensure `STATIC_ROOT` and `STATICFILES_DIRS` are correctly configured.

### Issue 6: Migration Errors

**Error:**
```
django.db.migrations.exceptions.InconsistentMigrationHistory
```

**Solution:**
```bash
# Reset migrations (⚠️ Only for development)
python manage.py migrate --fake-initial

# Or delete database and recreate
# (⚠️ This will delete all data)
```

### Issue 7: Port Already in Use

**Error:**
```
Error: That port is already in use
```

**Solution:**
```bash
# Use different port
python manage.py runserver 8001

# Or find and kill process using port 8000
```

### Issue 8: Permission Denied Errors

**Error:**
```
PermissionError: [Errno 13] Permission denied
```

**Solution:**
- Check file/directory permissions
- Ensure user has write access to `media/` and `assets/` directories
- On Linux/macOS: `chmod -R 755 media/ assets/`

---

## Production Deployment

### Using Gunicorn

1. **Install Gunicorn:**
   ```bash
   pip install gunicorn
   ```

2. **Run with Gunicorn:**
   ```bash
   gunicorn ClassificationOfLD.wsgi:application --bind 0.0.0.0:8000 --workers 4
   ```

### Using Nginx as Reverse Proxy

1. **Install Nginx:**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install nginx
   
   # macOS
   brew install nginx
   ```

2. **Configure Nginx:**
   Create `/etc/nginx/sites-available/insightedu`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       location /static/ {
           alias /path/to/InsightEDU3.2/assets/;
       }

       location /media/ {
           alias /path/to/InsightEDU3.2/media/;
       }
   }
   ```

3. **Enable Site:**
   ```bash
   sudo ln -s /etc/nginx/sites-available/insightedu /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

### Using Systemd Service

Create `/etc/systemd/system/insightedu.service`:

```ini
[Unit]
Description=InsightEDU3.2 Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/InsightEDU3.2
ExecStart=/path/to/venv/bin/gunicorn ClassificationOfLD.wsgi:application --bind 127.0.0.1:8000 --workers 4

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable insightedu
sudo systemctl start insightedu
```

---

## Additional Resources

- **Technical Documentation:** See `TECHNICAL_DOCUMENTATION.md`
- **User Manual:** See `USER_MANUAL.md`
- **Project Report:** See `PROJECT_REPORT.md`
- **Django Documentation:** https://docs.djangoproject.com/
- **MySQL Documentation:** https://dev.mysql.com/doc/

---

## Support

For installation issues:
1. Check this guide's troubleshooting section
2. Review error messages carefully
3. Check Django and MySQL logs
4. Consult technical documentation
5. Contact development team

---

**Installation Guide Version:** 1.0  
**Last Updated:** 2024

---

*Happy Installing! 🚀*


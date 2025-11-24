# Technology Stack Quick Reference: InsightEDU3.2

**Quick Reference Guide**

---

## 🚀 Core Stack at a Glance

```
┌─────────────────────────────────────────┐
│         CLIENT (Browser)                │
│  HTML5 + CSS3 + JavaScript + Bootstrap  │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────▼───────────────────────┐
│         WEB FRAMEWORK                   │
│         Django 4.1.7                    │
│  (Views + Models + Templates + URLs)    │
└─────────────────┬───────────────────────┘
                  │
    ┌─────────────┼─────────────┐
    │             │             │
┌───▼───┐  ┌──────▼──────┐  ┌───▼────┐
│ MySQL │  │ ML Model    │  │ Audio  │
│       │  │ (Keras)     │  │ (PyA)  │
└───────┘  └─────────────┘  └────────┘
```

---

## 📦 Technology Categories

### Core Technologies

| Technology | Version | Role |
|------------|---------|------|
| **Python** | 3.8+ | Programming language |
| **Django** | 4.1.7 | Web framework |
| **MySQL** | 5.7+/8.0+ | Database |
| **TensorFlow** | 2.11.0 | ML framework |
| **Keras** | 2.11.0 | Neural networks |
| **Bootstrap** | 5.1.3 | UI framework |

### ML/AI Stack

| Technology | Purpose |
|------------|---------|
| TensorFlow | ML computation |
| Keras | Model API |
| NumPy | Numerical operations |
| scikit-learn | ML utilities |
| model.h5 | Pre-trained model |

### Audio Stack

| Technology | Purpose |
|------------|---------|
| PyAudio | Audio I/O |
| SpeechRecognition | Speech-to-text |
| pydub | Audio manipulation |
| wave | WAV file handling |

### Development Tools

| Tool | Purpose |
|------|---------|
| pytest | Testing |
| Black | Formatting |
| Flake8 | Linting |
| Pylint | Code analysis |
| GitHub Actions | CI/CD |

---

## 🔗 Integration Points

### 1. Django ↔ MySQL
- **Method:** Django ORM
- **Driver:** mysqlclient
- **Usage:** Models → Database tables

### 2. Django ↔ ML Model
- **Method:** Direct loading
- **Library:** Keras
- **Usage:** `load_model('model.h5')`

### 3. Django ↔ Audio
- **Method:** File-based
- **Libraries:** PyAudio, SpeechRecognition
- **Usage:** Record → Process → Analyze

### 4. Frontend ↔ Backend
- **Method:** Templates + Forms
- **Protocol:** HTTP/HTTPS
- **Usage:** Form submission, AJAX

---

## 📊 Technology Statistics

- **Total Dependencies:** 349 packages
- **Core Technologies:** 6
- **ML Libraries:** 4
- **Audio Libraries:** 4
- **Development Tools:** 8+
- **Lines of Code:** ~1,200+ (views.py)

---

## 🎯 Key Integrations

### Request Flow
```
Browser → Django URL → View → 
  ├─→ ORM → MySQL
  ├─→ Keras → ML Model
  ├─→ PyAudio → Audio Processing
  └─→ Template → HTML Response
```

### Data Flow
```
User Input → Django View → 
  Processing → 
    ├─→ Database (MySQL)
    ├─→ ML Model (TensorFlow/Keras)
    └─→ Audio (PyAudio/SpeechRecognition)
  → Results → Response
```

---

## 📚 Full Documentation

For complete details, see:
- **[TECHNOLOGY_STACK_AND_INTEGRATION.md](TECHNOLOGY_STACK_AND_INTEGRATION.md)** - Comprehensive guide
- **[TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)** - Technical specs
- **[PROJECT_REPORT.md](PROJECT_REPORT.md)** - Project overview

---

**Quick Reference Version:** 1.0





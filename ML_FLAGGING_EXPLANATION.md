# How InsightEDU3.2 Flags Learning Challenges with Machine Learning

## Overview

InsightEDU3.2 uses a **hybrid approach** combining:
1. **Machine Learning (ML)** for initial comprehensive assessment
2. **Rule-based scoring** for domain-specific tests

This document explains how each component works to identify potential learning differences.

---

## 1. Machine Learning Component: Initial Disability Assessment

### Architecture

**Model Type:** Neural Network (Keras/TensorFlow)  
**Model File:** `model.h5`  
**Framework:** TensorFlow 2.11.0, Keras 2.11.0

### Input: 16-Dimensional Feature Vector

The ML model analyzes responses from the **Disability Assessment Questionnaire** (16 questions). Each response is converted to binary values:

```python
[
    D_Reading,              # Reading difficulties (0 or 1)
    D_Spelling,             # Spelling challenges (0 or 1)
    D_Handwriting,          # Handwriting issues (0 or 1)
    D_WrittenExpression,    # Written expression problems (0 or 1)
    D_BasicArithmetic,      # Basic math difficulties (0 or 1)
    D_HigherArithmetic,     # Advanced math difficulties (0 or 1)
    D_Attention,            # Attention problems (0 or 1)
    Easily_Distracted,      # Distraction issues (0 or 1)
    D_Memory,               # Memory challenges (0 or 1)
    Lack_Motivation,        # Motivation issues (0 or 1)
    D_StudySkills,          # Study skills problems (0 or 1)
    Does_Not_like_School,   # School aversion (0 or 1)
    D_LearningLanguage,     # Language learning difficulties (0 or 1)
    D_LearningSubject,      # Subject-specific challenges (0 or 1)
    Slow_To_Learn,          # Learning pace issues (0 or 1)
    Repeated_a_Grade        # Grade repetition (0 or 1)
]
```

**Value Encoding:**
- `0` = No (no difficulty reported)
- `1` = Yes (difficulty reported)

### Processing Flow

1. **Data Collection:** User completes 16-question assessment
2. **Feature Extraction:** Responses converted to 16-element binary vector
3. **Percentage Calculation:** 
   ```python
   percentage = (sum(list1) / 16) * 100
   ```
   This indicates the proportion of "Yes" responses (severity indicator)

4. **ML Prediction:**
   ```python
   model = load_model('model.h5')
   predictions = model.predict([input_vector])[0]
   rounded = [float(numpy.round(x)) for x in predictions]
   ```

5. **Classification:**
   - If `rounded[0] == 1.0`: **Learning Disability Detected**
     - Result: "You have been detected as Learning Disable with X %"
   - If `rounded[0] == 0.0`: **No Learning Disability Detected**
     - Result: "You have not been detected as Learning Disable but can try out exercise"

### How ML Identifies Patterns

The neural network was trained on historical assessment data where:
- **Input:** 16 binary features representing reported difficulties
- **Output:** Binary classification (Learning Disability / No Learning Disability)

The model learns **complex patterns and correlations** between different types of difficulties. For example:
- Multiple reading-related issues (D_Reading, D_Spelling, D_Handwriting) together may indicate dyslexia
- Math difficulties (D_BasicArithmetic, D_HigherArithmetic) combined with attention issues may indicate dyscalculia
- Memory problems (D_Memory) with learning pace issues (Slow_To_Learn) may indicate broader cognitive challenges

The ML model can identify **non-linear relationships** that simple rule-based systems might miss.

---

## 2. Domain-Specific Tests: Rule-Based Scoring

After the initial ML assessment, the system uses **rule-based scoring** for specific learning domains. These tests provide targeted evaluation for specific learning differences.

### 2.1 Mathematics Test → Dyscalculia Detection

**Test Format:** 4 arithmetic questions
- Basic arithmetic operations
- Addition, multiplication, division

**Scoring Logic:**
```python
score = 0
# Check each answer against correct solution
if answer1 == correct_answer1:
    score += 1
# ... repeat for all 4 questions

# Classification
if score < 3:
    result = "Dyscalculia"  # Potential math learning disability
else:
    result = "Pass"
```

**Flagging Criteria:**
- **Score < 3 out of 4:** Flags potential **Dyscalculia**
- **Score ≥ 3:** Normal performance

**Why This Works:** Consistent difficulty with basic arithmetic operations is a key indicator of dyscalculia.

---

### 2.2 Grammar Test → Dyslexia Detection

**Test Format:** 4 language/grammar questions
- Antonym identification (e.g., "tall" → "short")
- Plural forms (e.g., "woman" → "women")
- Vowel identification (e.g., "a, e, i, o, u")
- Word categorization (e.g., fruits: "apple, banana, grapes, kiwi, mango")

**Scoring Logic:**
```python
score = 0
# Case-insensitive comparison
if answer.lower() == 'correct_answer':
    score += 1
# ... repeat for all 4 questions

# Classification
if score < 3:
    result = "Dyslexia"  # Potential reading/language disability
else:
    result = "Pass"
```

**Flagging Criteria:**
- **Score < 3 out of 4:** Flags potential **Dyslexia**
- **Score ≥ 3:** Normal performance

**Why This Works:** Language processing difficulties (antonyms, plurals, phonetics) are core indicators of dyslexia.

---

### 2.3 Reading Test → Dysgraphia Detection

**Test Format:** Audio-based reading assessment
- User reads a sentence: "This is a car"
- System records audio via microphone
- Speech recognition converts audio to text

**Scoring Logic:**
```python
# Expected words
sentence = ['this', 'is', 'a', 'car']
score = 0

# Speech recognition result
recognized_text = speech_to_text(audio_recording)
recognized_words = recognized_text.split()

# Count matching words
for word in recognized_words:
    if word.lower() in sentence:
        score += 1

# Classification
if score < 3:
    result = "Dysgraphia"  # Potential writing/reading disability
else:
    result = "Pass"
```

**Technology Stack:**
- **PyAudio:** Audio recording
- **Google Speech Recognition API:** Speech-to-text conversion
- **Word Matching:** Compares recognized words to expected text

**Flagging Criteria:**
- **Score < 3 out of 4:** Flags potential **Dysgraphia**
- **Score ≥ 3:** Normal performance

**Why This Works:** Pronunciation and reading fluency issues can indicate dysgraphia or related reading disabilities.

---

### 2.4 Memory Tests → Memory Challenge Detection

#### Image Memory Test (MemoryTest1)

**Test Format:** Visual memory assessment
- User views 8 images: `['table', 'chair', 'car', 'tree', 'cat', 'dog', 'cake', 'umbrella']`
- User recalls and enters image names

**Scoring Logic:**
```python
expected_images = ['table', 'chair', 'car', 'tree', 'cat', 'dog', 'cake', 'umbrella']
score = 0

# Check each recalled image
for user_input in user_responses:
    if user_input.lower() in expected_images:
        score += 1

# Classification
if score < 3:
    result = "Dysgraphia"  # Memory issues flagged
else:
    result = "Pass"
```

**Flagging Criteria:**
- **Score < 3 out of 8:** Flags potential memory issues
- **Score ≥ 3:** Normal visual memory

#### Audio Memory Test (MemoryTest)

**Test Format:** Auditory memory assessment
- User listens to 10 words: `['table', 'chair', 'tiffin', 'glass', 'bottle', 'dish', 'cup', 'plates', 'bowl', 'mat']`
- User recalls and enters words

**Scoring Logic:**
```python
expected_words = ['table', 'chair', 'tiffin', 'glass', 'bottle', 'dish', 'cup', 'plates', 'bowl', 'mat']
score = 0

# Check each recalled word
for user_input in user_responses:
    if user_input in expected_words:
        score += 1

# Classification
if score < 3:
    result = "Dysgraphia"  # Memory issues flagged
else:
    result = "Pass"
```

**Flagging Criteria:**
- **Score < 3 out of 10:** Flags potential memory issues
- **Score ≥ 3:** Normal auditory memory

**Why This Works:** Short-term memory deficits can impact learning across multiple domains and are often associated with learning disabilities.

---

### 2.5 Video Comprehension Tests → Attention/Comprehension Detection

**Test Format:** Three video-based scenario tests
- User watches a video
- Answers 5 comprehension questions about video content
- Tests attention, recall, and understanding

**Example (Video Test 1):**
```python
# Expected answers
correct_answers = ['friends', 'forest', 'rabbit', 'squirrel', 'by crossing the bridge']
score = 0

# Check each answer
for user_answer, correct in zip(user_answers, correct_answers):
    if user_answer.lower() == correct:
        score += 1

# Classification
if score < 3:
    result = "Dyslexia"  # Comprehension/attention issues
else:
    result = "Pass"
```

**Flagging Criteria:**
- **Score < 3 out of 5:** Flags potential comprehension/attention issues
- **Score ≥ 3:** Normal comprehension

**Why This Works:** Difficulty recalling video content indicates attention and comprehension challenges, which can be associated with learning disabilities.

---

## 3. Integrated Flagging System

### How Components Work Together

1. **Initial ML Assessment:**
   - Provides **overall risk assessment**
   - Identifies **general learning disability patterns**
   - Calculates **severity percentage**

2. **Domain-Specific Tests:**
   - Provide **targeted evaluation** for specific areas
   - Flag **specific learning differences**:
     - **Dyscalculia** (Math Test)
     - **Dyslexia** (Grammar Test, Video Tests)
     - **Dysgraphia** (Reading Test, Memory Tests)

3. **Comprehensive Results:**
   - All results stored in `TestResult` model
   - Users can view:
     - Overall ML assessment result
     - Individual test scores
     - Specific disability flags
     - Progress over time

### Result Storage

```python
TestResult {
    Learning_Disability: "You have been detected as Learning Disable with 75 %"
    Maths_Test: "2/4 Dyscalculia"
    Grammar_Test: "1/4 Dyslexia"
    Reading_Test: "2/4 Dysgraphia"
    Memory_images: "2/8 Dysgraphia"
    Memory_audio: "3/10"
    Video_test1: "2/5 Dyslexia"
    Video_test2: "4/5"
    Video_test3: "3/5"
    Date: "2024-01-15"
}
```

---

## 4. Key Advantages of This Approach

### ML Component Benefits:
- **Pattern Recognition:** Identifies complex correlations between different difficulty types
- **Non-linear Relationships:** Captures interactions that rule-based systems miss
- **Severity Indication:** Percentage provides quantitative risk assessment
- **Adaptive Learning:** Model can be retrained with new data

### Rule-Based Component Benefits:
- **Transparency:** Clear scoring criteria for each test
- **Specificity:** Targets specific learning differences (Dyslexia, Dyscalculia, Dysgraphia)
- **Interpretability:** Easy to understand why a flag was raised
- **Reliability:** Consistent scoring across all users

### Combined Benefits:
- **Comprehensive:** Both general and specific assessments
- **Multi-Modal:** Tests reading, writing, math, memory, and comprehension
- **Actionable:** Provides specific areas needing attention
- **Trackable:** Results stored for progress monitoring

---

## 5. Important Limitations

⚠️ **This system provides preliminary assessments only.**

- **Not a Diagnostic Tool:** Results should not replace professional evaluation
- **ML Model Limitations:** Accuracy depends on training data quality and quantity
- **Rule-Based Thresholds:** Score thresholds (e.g., < 3) are heuristics, not clinical standards
- **Context Missing:** Does not account for environmental factors, age, or other contextual information
- **Professional Consultation Required:** Always consult with qualified specialists for formal diagnosis

---

## 6. Technical Implementation Details

### ML Model Loading
```python
from keras.models import load_model
import numpy

model = load_model('model.h5')
```

### Prediction Process
```python
# Prepare input vector
input_data = [[
    int(D_Reading), int(D_Spelling), int(D_Handwriting), 
    int(D_WrittenExpression), int(D_BasicArithmetic), 
    int(D_HigherArithmetic), int(D_Attention), 
    int(Easily_Distracted), int(D_Memory), 
    int(Lack_Motivation), int(D_StudySkills), 
    int(Does_Not_like_School), int(D_LearningLanguage), 
    int(D_LearningSubject), int(Slow_To_Learn), 
    int(Repeated_a_Grade)
]]

# Get prediction
predictions = model.predict(input_data)[0]
rounded = [float(numpy.round(x)) for x in predictions]

# Classify
if rounded[0] == 1.0:
    # Learning disability detected
```

### Speech Recognition
```python
import speech_recognition as sr

r = sr.Recognizer()
with sr.AudioFile(audio_file) as source:
    audio_text = r.listen(source)
    text = r.recognize_google(audio_text)  # Google Speech API
    words = text.split()
```

---

## Summary

InsightEDU3.2 uses a **two-tier approach**:

1. **ML Neural Network** analyzes 16-question assessment to identify general learning disability patterns
2. **Rule-based scoring** evaluates specific domains (math, grammar, reading, memory, comprehension) to flag specific learning differences

Together, they provide:
- **Overall risk assessment** (ML)
- **Domain-specific flags** (Rule-based)
- **Severity indicators** (Percentage scores)
- **Actionable insights** (Specific areas needing attention)

The system is designed to **screen and identify** potential learning challenges, serving as a **first step** toward professional evaluation and support.


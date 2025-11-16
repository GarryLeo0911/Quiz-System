# Quiz System - Subject-Based Data Storage

## Overview

The quiz system now supports organizing questions, quizzes, and categories by **subject**. Each subject has its own folder with separate data files, allowing you to manage different subject areas independently.

## Directory Structure

```
data/
├── README.md                  # This file
├── math/                      # Math subject folder
│   ├── questions.json
│   ├── categories.json
│   ├── quizzes.json
│   └── attempts.json
├── science/                   # Science subject folder
│   ├── questions.json
│   ├── categories.json
│   ├── quizzes.json
│   └── attempts.json
├── history/                   # History subject folder
│   ├── questions.json
│   ├── categories.json
│   ├── quizzes.json
│   └── attempts.json
├── questions.json             # Default/root data (existing data)
├── categories.json
├── quizzes.json
└── attempts.json
```

## How to Use

### 1. Default Mode (Root Data)
When you first access the system, it will use the default data stored in the root `data/` folder. This contains all your existing questions and quizzes.

### 2. Switching to a Subject
To work with a specific subject's data:
1. Use the subject selector in the dashboard or navigation
2. Select a subject (e.g., "math", "science", "history")
3. All operations (creating/editing questions, quizzes, etc.) will now use that subject's data

### 3. Adding a New Subject
To add a new subject:
1. Create a new folder in the `data/` directory (e.g., `data/english/`)
2. Create these four JSON files in the folder:
   - `questions.json` - initialized as `[]`
   - `categories.json` - initialized as `[]`
   - `quizzes.json` - initialized as `[]`
   - `attempts.json` - initialized as `[]`
3. The new subject will automatically appear in the subject selector

### 4. Example: Creating a New Subject

```bash
# From the Quiz-System directory
mkdir data/english
echo "[]" > data/english/questions.json
echo "[]" > data/english/categories.json
echo "[]" > data/english/quizzes.json
echo "[]" > data/english/attempts.json
```

## Subject Isolation

- Each subject's data is completely isolated from other subjects
- Questions, categories, and quizzes created in one subject won't appear in another
- Quiz attempts are stored separately for each subject
- You can have duplicate category names across different subjects

## Benefits

1. **Organization**: Keep different subject areas separate and organized
2. **Performance**: Smaller data files load faster
3. **Flexibility**: Easy to backup, share, or migrate data for specific subjects
4. **Scalability**: Add unlimited subjects without affecting existing data

## Current Subjects

The system comes with three pre-configured subjects:
- **math** - Mathematics questions and quizzes
- **science** - Science-related content
- **history** - Historical topics

Your existing data remains in the root `data/` folder and is accessible as the "Default" subject.

## API/Programming Usage

Developers can programmatically switch subjects:

```python
from quiz_app.storage import get_storage, get_available_subjects

# Get list of available subjects
subjects = get_available_subjects()  # Returns: ['history', 'math', 'science']

# Work with a specific subject
math_storage = get_storage('math')
questions = math_storage.get_questions()

# Work with default/root data
default_storage = get_storage(None)
questions = default_storage.get_questions()
```

## Notes

- Subject names are case-sensitive (use lowercase)
- Subject folders should not contain spaces (use underscores: `computer_science`)
- Hidden folders (starting with `.`) are ignored
- Empty subject folders without the required JSON files may cause errors

# Quiz System

A Django-based quiz system for exam preparation that uses JSON files for data storage. Perfect for students preparing for multiple courses - create your own question banks and practice with unlimited quizzes!

**🎓 This system supports subject-based organization with separate databases for each course!**

## ✨ Features

### Question Management
- 📝 **Three Question Types**:
  - Single Choice (one correct answer)
  - Multiple Choice (multiple correct answers)
  - Matching (pair items together)
- 🖼️ **Image Support**: Add images to questions
- 📖 **Explanations**: Write detailed explanations for answers
- 🗂️ **Categories**: Organize questions by topic/chapter
- 🔍 **Search & Filter**: Find questions quickly

### Quiz/Exam Features
- 🎯 Build custom quizzes from your question bank
- ⏱️ Optional time limits
- 📊 Automatic grading with detailed feedback
- ✅ Show correct answers and explanations
- 💾 Track all quiz attempts

### Storage & Sharing
- 💾 **JSON Storage**: No database setup needed
- 📁 Easy to backup (just copy the `data/` folder)
- 🔄 Git-friendly (perfect for version control)
- 🤝 Share with classmates easily

---

## 🚀 Quick Start (2 Steps)

### Step 1: Run Setup Script
```bash
cd "/Users/lijiayi/Desktop/Quiz System/quiz_system"
./setup.sh
```

This will automatically:
- Create virtual environment
- Install dependencies
- Set up directories
- Run Django migrations

### Step 2: Start the Server
```bash
source venv/bin/activate
python manage.py runserver
```

Then open in browser: **http://127.0.0.1:8000/**

**That's it! The system is ready with INFO3315 questions loaded!** 🎉

---

## 📚 Subject Organization

### Available Subjects
The system comes with organized subject folders:
- 📘 **Human-Computer Interaction** - HCI course materials
- 📗 **Project Management** - Project management topics
- 📄 **Default** - Root-level data (legacy/mixed content)

### Getting Started
1. Select a subject from the dropdown in the dashboard
2. Browse the Question Bank for that subject
3. Create subject-specific quizzes
4. Take practice quizzes and track your progress
5. Add your own questions to any subject
6. Create new subjects as needed for other courses

---

## 🗂️ Managing Subjects

### View All Subjects
Your current subjects are automatically detected from folders in `data/`:
- Human-Computer-Interaction
- Project_Management
- Default (root-level files)

### Add a New Subject
Create a new subject for another course you're studying:

```bash
# Example: Adding "Software_Engineering" subject
mkdir "data/Software_Engineering"
echo "[]" > "data/Software_Engineering/questions.json"
echo "[]" > "data/Software_Engineering/categories.json"
echo "[]" > "data/Software_Engineering/quizzes.json"
echo "[]" > "data/Software_Engineering/attempts.json"
```

Refresh the page and the new subject appears in the dropdown!

### Clear a Subject's Data

**⚠️ Warning**: Always backup before clearing!

```bash
# Backup first!
cp -r "data/Human-Computer-Interaction/" "backup_HCI_$(date +%Y%m%d)/"

# Then clear (if you're sure)
echo "[]" > "data/Human-Computer-Interaction/questions.json"
echo "[]" > "data/Human-Computer-Interaction/categories.json"
echo "[]" > "data/Human-Computer-Interaction/quizzes.json"
echo "[]" > "data/Human-Computer-Interaction/attempts.json"
```

### Remove a Subject Entirely

```bash
# Backup first!
cp -r "data/Project_Management/" "backup_PM_$(date +%Y%m%d)/"

# Remove the folder
rm -rf "data/Project_Management/"
```

### Restore from Backup

```bash
# Restore entire data folder
cp -r data_backup_20251117/* data/

# Restore specific subject
cp -r backup_HCI_20251117/* "data/Human-Computer-Interaction/"
```

---

## 📚 How to Use for Multiple Courses

### 1. Select Your Subject
- Use the subject dropdown to switch between courses
- Each subject has its own isolated database
- Questions, quizzes, and attempts are kept separate

### 2. Organize by Course
- **Human-Computer Interaction** - Add HCI questions and concepts
- **Project Management** - Add PM methodologies and practices
- Create new subjects for other courses you're taking

### 3. Build Your Question Bank
As you study each course:
- Add 5-10 questions per day while studying
- Include images for visual concepts
- Write detailed explanations (helps you learn!)
- Organize questions by chapter/topic using categories

### 4. Create Practice Quizzes
Build custom quizzes from each subject's question bank:
- By chapter (focused review)
- Mixed topics (comprehensive review)
- Specific categories (targeted practice)

### 5. Test Yourself Regularly
- Take quizzes in each subject
- Review explanations for wrong answers
- Retake quizzes until you get 100%
- Track your improvement over time per subject

### 6. Before Each Exam
- Switch to the relevant subject
- Create a full-length practice exam
- Time yourself (simulate exam conditions)
- Review all explanations one last time
- **Ace all your finals!** 🏆

---

## 🎯 Usage Guide

### Creating Your First Question

1. Click **"Create New Question"** from Dashboard
2. Enter your question text
3. Select question type:
   - **Single Choice**: One correct answer (radio buttons)
   - **Multiple Choice**: Multiple correct answers (checkboxes)
   - **Matching**: Pair terms with definitions
4. Add options or matching pairs
5. Mark the correct answer(s)
6. Write an explanation (helps you learn!)
7. Upload an image if needed
8. Choose a category
9. Click **"Save Question"**

### Creating Your First Quiz

1. Go to **"Exams"** → Click **"Create New Quiz"**
2. Enter quiz title (e.g., "Chapter 3 Practice")
3. Add description and instructions (optional)
4. Set time limit in minutes (optional)
5. Select questions from your Question Bank
6. Assign points to each question
7. Save as **Draft** (practice) or **Publish** (final)

### Taking a Quiz

1. Click **"Take Quiz"** on any quiz
2. Answer all questions
3. Click **"Submit Exam"**
4. View your score and detailed results
5. Review explanations for any wrong answers

---

## 📁 Project Structure

```
quiz_system/
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── setup.sh              # Automated setup script
├── .gitignore            # Git ignore file
│
├── quiz_system/          # Django configuration
│   ├── settings.py       # Django settings
│   ├── urls.py           # Main URL routing
│   └── wsgi.py           # WSGI config
│
├── quiz_app/             # Main application
│   ├── models.py         # Data models
│   ├── views.py          # Business logic
│   ├── urls.py           # App URL routing
│   └── storage.py        # JSON storage handler
│
├── templates/            # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── question_bank.html
│   ├── question_editor.html
│   └── quiz_list.html
│
├── data/                           # Your data (JSON files)
│   ├── README.md                  # Subject system documentation
│   ├── questions.json             # ← Default/legacy questions
│   ├── categories.json            # ← Default categories
│   ├── quizzes.json               # ← Default quizzes
│   ├── attempts.json              # ← Default quiz results
│   ├── Human-Computer-Interaction/  # HCI subject
│   │   ├── questions.json
│   │   ├── categories.json
│   │   ├── quizzes.json
│   │   └── attempts.json
│   └── Project_Management/        # PM subject
│       ├── questions.json
│       ├── categories.json
│       ├── quizzes.json
│       └── attempts.json
│
└── media/                # Uploaded files
    └── question_images/  # Question images
```

---

## 💾 Data Storage

All your data is stored in simple JSON files in the `data/` directory:

| File | Contains |
|------|----------|
| `questions.json` | All your questions with answers |
| `categories.json` | Question categories/topics |
| `quizzes.json` | Quiz definitions |
| `attempts.json` | Quiz results and scores |

### 📚 Subject-Based Organization

The system organizes data by **subject** - each course/topic has its own folder with separate data files:

```
data/
├── questions.json                    # Default/root data
├── categories.json
├── quizzes.json
├── attempts.json
│
├── Human-Computer-Interaction/       # HCI Course
│   ├── questions.json               # HCI questions only
│   ├── categories.json              # HCI categories (Design, Evaluation, etc.)
│   ├── quizzes.json                 # HCI quizzes
│   └── attempts.json                # HCI quiz attempts & scores
│
└── Project_Management/               # Project Management Course
    ├── questions.json               # PM questions only
    ├── categories.json              # PM categories (Planning, Risk, etc.)
    ├── quizzes.json                 # PM quizzes
    └── attempts.json                # PM quiz attempts & scores
```

**Key Benefits:**
- ✅ **Complete Isolation** - Each course's data is completely separate
- ✅ **Faster Loading** - Smaller files load much faster
- ✅ **Easy Organization** - Find what you need instantly
- ✅ **Simple Backup** - Backup individual courses
- ✅ **Easy Sharing** - Share specific course materials with classmates
- ✅ **Unlimited Subjects** - Add as many courses as you need

**How to use:**
1. **Select subject** from the dropdown in dashboard or question bank
2. **Create/edit questions** - automatically saved to current subject
3. **Build quizzes** - only from current subject's questions
4. **Switch anytime** - your work in each subject is preserved

**Adding a new subject (e.g., for a new course):**
```bash
# Create folder for new course (use underscores for spaces)
mkdir "data/Database_Systems"
echo "[]" > "data/Database_Systems/questions.json"
echo "[]" > "data/Database_Systems/categories.json"
echo "[]" > "data/Database_Systems/quizzes.json"
echo "[]" > "data/Database_Systems/attempts.json"
```

The new subject will automatically appear in the dropdown! See `data/README.md` for detailed documentation.

### Why JSON?
- ✅ No database installation needed
- ✅ Human-readable format
- ✅ Easy to backup (just copy the folder!)
- ✅ Works with Git (version control friendly)
- ✅ Easy to share with classmates
- ✅ Can be edited manually if needed

### Backup Your Data
```bash
# Backup all subjects at once
cp -r data/ data_backup_$(date +%Y%m%d)/

# Backup a specific subject/course
cp -r data/Human-Computer-Interaction/ backup_HCI_$(date +%Y%m%d)/
cp -r data/Project_Management/ backup_PM_$(date +%Y%m%d)/

# Or commit to Git for version control
git add data/
git commit -m "Updated HCI and PM questions"
git push
```

---

## 🤝 Sharing with Classmates

### Method 1: GitHub
```bash
cd "/Users/lijiayi/Desktop/Quiz System/quiz_system"
git init
git add .
git commit -m "My quiz bank"
git push to your GitHub repo
```

Friends can then:
```bash
git clone YOUR_REPO_URL
cd quiz_system
./setup.sh
source venv/bin/activate
python manage.py runserver
```

### Method 2: Direct Share
1. Zip the entire `quiz_system` folder
2. Share via Google Drive, Dropbox, or USB
3. Recipient just runs `./setup.sh` and starts using it!

---

## 🔧 Manual Setup (If Needed)

If you prefer not to use the setup script:

```bash
# 1. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create directories (if not exist)
mkdir -p media/question_images static

# 4. Run Django migrations
python manage.py migrate

# 5. Start server
python manage.py runserver
```

**Note**: The `data/` directory with INFO3315 questions is already included!

---

## 🐛 Troubleshooting

### Server won't start
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Check if dependencies are installed
pip install -r requirements.txt

# Run migrations
python manage.py migrate
```

### Port 8000 already in use
```bash
# Use a different port
python manage.py runserver 8080
# Then visit: http://127.0.0.1:8080/
```

### Can't create questions
- Check browser console for errors (F12)
- Check terminal for Django errors
- Verify `data/` directory exists and is writable

### Images not showing
- Check `media/question_images/` directory exists
- Verify file permissions
- Check if image file was actually uploaded

### Lost all my data
- Restore from backup (you made backups, right? 😅)
- Check if JSON files still exist in `data/`
- Files might be empty - check with: `cat data/questions.json`

---

## 💡 Study Tips

### Before the Exam (2-3 weeks)
- Input 5-10 questions daily as you study
- Add images for visual concepts
- Write detailed explanations (helps you learn)
- Organize by chapter/topic

### One Week Before
- Create practice quizzes by chapter
- Take each quiz at least twice
- Review explanations for wrong answers
- Create a "Tough Questions" category for weak areas

### Day Before Exam
- Take a full-length practice exam
- Time yourself like the real exam
- Review all explanations
- Get a good night's sleep! 😴

### Success Formula
```
Input Questions (Active Learning)
    +
Take Quizzes (Active Recall)
    +
Review Explanations (Understanding)
    +
Repeat Over Time (Spaced Repetition)
    =
EXAM SUCCESS! 🎉
```

---

## 📊 Example Study Schedule

**Week 1-2: Build Question Bank**
- Monday-Friday: Add 5-10 questions daily
- Weekend: Organize into categories, review and edit

**Week 3: Practice**
- Create chapter-specific quizzes
- Take each quiz, review explanations
- Focus on weak areas

**Week 4 (Exam Week): Final Review**
- Monday-Wednesday: Full practice exams
- Thursday: Review all explanations
- Friday: Light review, rest
- **Exam Day**: You got this! 💪

---

## 🛠️ Advanced Usage

### Adding More Features

The system is built with Django and is easy to extend. Some ideas:

- Add more question types (True/False, Fill-in-blank)
- Implement question randomization
- Add difficulty levels
- Create study statistics/analytics
- Add LaTeX support for math formulas
- Export quizzes to PDF

Check `quiz_app/views.py` and `quiz_app/storage.py` to add features.

### Using Django Admin

Create a superuser to access Django's admin interface:
```bash
python manage.py createsuperuser
```

Then visit: http://127.0.0.1:8000/admin/

---

## 📦 Technology Stack

- **Backend**: Django 4.2
- **Frontend**: HTML, Tailwind CSS, JavaScript
- **Icons**: Material Symbols
- **Storage**: JSON files
- **Image Processing**: Pillow

---

## 🎓 Perfect For

- ✅ Final exam preparation
- ✅ Self-study and review
- ✅ Study groups
- ✅ Building personal question banks
- ✅ Creating practice tests
- ✅ Tracking study progress

---

## 📄 License

Free to use for personal and educational purposes.

---

## 🎉 Ready to Start?

1. Run `./setup.sh`
2. Start server: `source venv/bin/activate && python manage.py runserver`
3. Open http://127.0.0.1:8000/
4. Select a subject from the dropdown
5. Browse questions or create your first quiz!

**Good luck on all your exams! You've got this!** 📚✨

---

## 🔄 Quick Reference

### Start Server
```bash
cd "/Users/lijiayi/Desktop/Quiz System/quiz_system"
source venv/bin/activate
python manage.py runserver
```

### Backup Data
```bash
cp -r data/ data_backup_$(date +%Y%m%d_%H%M%S)/
```

### Clear Database
```bash
rm data/*.json
echo "[]" > data/questions.json
echo "[]" > data/categories.json
echo "[]" > data/quizzes.json
echo "[]" > data/attempts.json
```

---

**Made with ❤️ for students preparing for multiple courses**

## 💡 Pro Tips

### Organize by Course
- Create one subject per course you're taking
- Use clear names: `Human-Computer-Interaction`, `Project_Management`, etc.
- Keep each course's materials completely separate

### Study Workflow
1. **During semester**: Add questions while studying each week
2. **Before midterms**: Create chapter-specific practice quizzes
3. **Final exam prep**: Create comprehensive mixed-topic exams
4. **Track progress**: Review attempt history per subject

### Collaboration
- Share subject folders with classmates taking the same course
- Each person can maintain their own subject folders
- Use Git for collaborative question bank building

### Best Practices
- Add explanations to every question (helps retention!)
- Use categories to organize by textbook chapters
- Include images for diagrams and visual concepts
- Review wrong answers and update explanations
- Create increasingly difficult quizzes as you learn

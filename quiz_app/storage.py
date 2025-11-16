"""
JSON Storage Module for Quiz System
This module handles reading and writing data to JSON files instead of a traditional database.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from django.conf import settings


class JSONStorage:
    """Handle JSON file operations for storing quiz data"""
    
    def __init__(self, subject: str = None):
        """
        Initialize storage with optional subject parameter.
        If subject is provided, data will be loaded from data/{subject}/ folder.
        If no subject is provided, data will be loaded from the root data/ folder.
        """
        self.storage_dir = Path(settings.JSON_STORAGE_DIR)
        self.subject = subject
        
        # If subject is provided, use subject-specific directory
        if subject:
            self.storage_dir = self.storage_dir / subject
        
        self.ensure_storage_directory()
        self.files = {
            'questions': self.storage_dir / 'questions.json',
            'categories': self.storage_dir / 'categories.json',
            'quizzes': self.storage_dir / 'quizzes.json',
            'attempts': self.storage_dir / 'attempts.json',
        }
        self.ensure_data_files()
    
    def ensure_storage_directory(self):
        """Create storage directory if it doesn't exist"""
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def ensure_data_files(self):
        """Create JSON files with empty arrays if they don't exist"""
        for file_path in self.files.values():
            if not file_path.exists():
                self.write_json(file_path, [])
    
    def read_json(self, file_path: Path) -> List[Dict]:
        """Read data from JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def write_json(self, file_path: Path, data: List[Dict]):
        """Write data to JSON file"""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    
    # Category operations
    def get_categories(self) -> List[Dict]:
        """Get all categories"""
        return self.read_json(self.files['categories'])
    
    def get_category(self, category_id: str) -> Optional[Dict]:
        """Get a specific category by ID"""
        categories = self.get_categories()
        for category in categories:
            if category['id'] == category_id:
                return category
        return None
    
    def save_category(self, category_data: Dict) -> Dict:
        """Save a new category or update existing one"""
        categories = self.get_categories()
        
        # Check if updating existing category
        for i, cat in enumerate(categories):
            if cat['id'] == category_data['id']:
                categories[i] = category_data
                self.write_json(self.files['categories'], categories)
                return category_data
        
        # Add new category
        categories.append(category_data)
        self.write_json(self.files['categories'], categories)
        return category_data
    
    def delete_category(self, category_id: str) -> bool:
        """Delete a category"""
        categories = self.get_categories()
        categories = [c for c in categories if c['id'] != category_id]
        self.write_json(self.files['categories'], categories)
        return True
    
    # Question operations
    def get_questions(self, filters: Optional[Dict] = None) -> List[Dict]:
        """Get all questions with optional filters"""
        questions = self.read_json(self.files['questions'])
        
        if not filters:
            return questions
        
        filtered = questions
        if 'category_id' in filters:
            filtered = [q for q in filtered if q.get('category_id') == filters['category_id']]
        if 'question_type' in filters:
            filtered = [q for q in filtered if q.get('question_type') == filters['question_type']]
        if 'search' in filters:
            search_term = filters['search'].lower()
            filtered = [q for q in filtered if search_term in q.get('question_text', '').lower()]
        
        return filtered
    
    def get_question(self, question_id: str) -> Optional[Dict]:
        """Get a specific question by ID"""
        questions = self.get_questions()
        for question in questions:
            if question['id'] == question_id:
                return question
        return None
    
    def save_question(self, question_data: Dict) -> Dict:
        """Save a new question or update existing one"""
        questions = self.get_questions()
        
        # Add timestamps
        if 'created_at' not in question_data:
            question_data['created_at'] = datetime.now().isoformat()
        question_data['updated_at'] = datetime.now().isoformat()
        
        # Check if updating existing question
        for i, q in enumerate(questions):
            if q['id'] == question_data['id']:
                questions[i] = question_data
                self.write_json(self.files['questions'], questions)
                return question_data
        
        # Add new question
        questions.append(question_data)
        self.write_json(self.files['questions'], questions)
        return question_data
    
    def delete_question(self, question_id: str) -> bool:
        """Delete a question"""
        questions = self.get_questions()
        questions = [q for q in questions if q['id'] != question_id]
        self.write_json(self.files['questions'], questions)
        return True
    
    # Quiz operations
    def get_quizzes(self) -> List[Dict]:
        """Get all quizzes"""
        return self.read_json(self.files['quizzes'])
    
    def get_quiz(self, quiz_id: str) -> Optional[Dict]:
        """Get a specific quiz by ID"""
        quizzes = self.get_quizzes()
        for quiz in quizzes:
            if quiz['id'] == quiz_id:
                return quiz
        return None
    
    def save_quiz(self, quiz_data: Dict) -> Dict:
        """Save a new quiz or update existing one"""
        quizzes = self.get_quizzes()
        
        # Add timestamps
        if 'created_at' not in quiz_data:
            quiz_data['created_at'] = datetime.now().isoformat()
        quiz_data['updated_at'] = datetime.now().isoformat()
        
        # Check if updating existing quiz
        for i, q in enumerate(quizzes):
            if q['id'] == quiz_data['id']:
                quizzes[i] = quiz_data
                self.write_json(self.files['quizzes'], quizzes)
                return quiz_data
        
        # Add new quiz
        quizzes.append(quiz_data)
        self.write_json(self.files['quizzes'], quizzes)
        return quiz_data
    
    def delete_quiz(self, quiz_id: str) -> bool:
        """Delete a quiz"""
        quizzes = self.get_quizzes()
        quizzes = [q for q in quizzes if q['id'] != quiz_id]
        self.write_json(self.files['quizzes'], quizzes)
        return True
    
    # Quiz Attempt operations
    def get_attempts(self, quiz_id: Optional[str] = None) -> List[Dict]:
        """Get all attempts, optionally filtered by quiz_id"""
        attempts = self.read_json(self.files['attempts'])
        if quiz_id:
            attempts = [a for a in attempts if a.get('quiz_id') == quiz_id]
        return attempts
    
    def get_attempt(self, attempt_id: str) -> Optional[Dict]:
        """Get a specific attempt by ID"""
        attempts = self.get_attempts()
        for attempt in attempts:
            if attempt['id'] == attempt_id:
                return attempt
        return None
    
    def save_attempt(self, attempt_data: Dict) -> Dict:
        """Save a new attempt or update existing one"""
        attempts = self.get_attempts()
        
        # Add timestamp
        if 'started_at' not in attempt_data:
            attempt_data['started_at'] = datetime.now().isoformat()
        
        # Check if updating existing attempt
        for i, a in enumerate(attempts):
            if a['id'] == attempt_data['id']:
                attempts[i] = attempt_data
                self.write_json(self.files['attempts'], attempts)
                return attempt_data
        
        # Add new attempt
        attempts.append(attempt_data)
        self.write_json(self.files['attempts'], attempts)
        return attempt_data


# Helper function to get available subjects
def get_available_subjects() -> List[str]:
    """Get list of available subject directories"""
    storage_dir = Path(settings.JSON_STORAGE_DIR)
    subjects = []
    
    # List all directories in the data folder
    if storage_dir.exists():
        for item in storage_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                subjects.append(item.name)
    
    return sorted(subjects)


# Helper function to get storage instance for a specific subject
def get_storage(subject: str = None) -> JSONStorage:
    """
    Get a storage instance for a specific subject.
    If subject is None, returns the default storage instance.
    """
    return JSONStorage(subject=subject)


# Global instance (default storage without subject)
storage = JSONStorage()

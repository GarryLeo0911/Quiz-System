#!/bin/bash

echo "🎯 Setting up Quiz System..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p data
mkdir -p media/question_images
mkdir -p static
mkdir -p staticfiles

# Initialize empty JSON files if they don't exist
if [ ! -f "data/questions.json" ]; then
    echo "[]" > data/questions.json
fi

if [ ! -f "data/categories.json" ]; then
    echo "[]" > data/categories.json
fi

if [ ! -f "data/quizzes.json" ]; then
    echo "[]" > data/quizzes.json
fi

if [ ! -f "data/attempts.json" ]; then
    echo "[]" > data/attempts.json
fi

# Run Django migrations
echo "🔄 Running Django migrations..."
python manage.py migrate

echo ""
echo "✨ Setup complete!"
echo ""
echo "To start the development server:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run the server: python manage.py runserver"
echo "  3. Open your browser to: http://127.0.0.1:8000/"
echo ""
echo "Happy quizzing! 📚✨"

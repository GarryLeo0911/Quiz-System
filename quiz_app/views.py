from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
import uuid
import random
from datetime import datetime
from .storage import storage, get_storage, get_available_subjects


# Helper function to get current storage based on session
def get_current_storage(request):
    """Get storage instance based on current subject in session"""
    current_subject = request.session.get('current_subject', None)
    return get_storage(current_subject)


# Subject Management
def switch_subject(request):
    """Switch to a different subject database"""
    if request.method == 'POST':
        subject = request.POST.get('subject')
        
        # If subject is 'default' or empty, clear the session
        if subject == 'default' or not subject:
            request.session.pop('current_subject', None)
        else:
            # Validate that the subject exists
            available_subjects = get_available_subjects()
            if subject in available_subjects:
                request.session['current_subject'] = subject
            else:
                return JsonResponse({'success': False, 'error': 'Invalid subject'})
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


# Dashboard
def dashboard(request):
    """Main dashboard view"""
    # Get current subject from session or use default
    current_subject = request.session.get('current_subject', None)
    subject_storage = get_storage(current_subject)
    
    questions = subject_storage.get_questions()
    quizzes = subject_storage.get_quizzes()
    categories = subject_storage.get_categories()
    
    # Get available subjects
    available_subjects = get_available_subjects()
    
    context = {
        'total_questions': len(questions),
        'total_quizzes': len(quizzes),
        'total_categories': len(categories),
        'current_subject': current_subject or 'Default',
        'available_subjects': available_subjects,
    }
    return render(request, 'dashboard.html', context)


# Question Bank Management
def question_bank(request):
    """View all questions"""
    # Get current subject from session
    current_subject = request.session.get('current_subject', None)
    subject_storage = get_storage(current_subject)
    
    questions = subject_storage.get_questions()
    categories = subject_storage.get_categories()
    
    # Apply filters if provided
    category_filter = request.GET.get('category')
    type_filter = request.GET.get('type')
    search_query = request.GET.get('search')
    
    filters = {}
    if category_filter:
        filters['category_id'] = category_filter
    if type_filter:
        filters['question_type'] = type_filter
    if search_query:
        filters['search'] = search_query
    
    if filters:
        questions = subject_storage.get_questions(filters)
    
    # Get available subjects
    available_subjects = get_available_subjects()
    
    context = {
        'questions': questions,
        'categories': categories,
        'current_subject': current_subject or 'Default',
        'available_subjects': available_subjects,
    }
    return render(request, 'question_bank.html', context)


def question_create(request):
    """Create a new question"""
    subject_storage = get_current_storage(request)
    
    if request.method == 'GET':
        categories = subject_storage.get_categories()
        context = {'categories': categories}
        return render(request, 'question_editor.html', context)
    
    elif request.method == 'POST':
        # Handle form submission
        question_id = str(uuid.uuid4())
        
        question_data = {
            'id': question_id,
            'question_text': request.POST.get('question_text'),
            'question_type': request.POST.get('question_type'),
            'category_id': request.POST.get('category_id'),
            'explanation': request.POST.get('explanation', ''),
            'points': int(request.POST.get('points', 1)),
        }
        
        # Handle image upload
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            file_name = f'question_images/{question_id}_{image_file.name}'
            file_path = default_storage.save(file_name, ContentFile(image_file.read()))
            question_data['image'] = file_path
        
        # Handle question type specific data
        question_type = question_data['question_type']
        
        if question_type in ['single_choice', 'multiple_choice']:
            # Get all options
            options = []
            option_texts = request.POST.getlist('option_text[]')
            correct_options = request.POST.getlist('correct_option[]')
            
            for i, option_text in enumerate(option_texts):
                if option_text.strip():
                    options.append({
                        'id': str(uuid.uuid4()),
                        'option_text': option_text,
                        'is_correct': str(i) in correct_options,
                        'order': i
                    })
            
            question_data['choices'] = options
        
        elif question_type == 'matching':
            # Get terms, definitions, and correct matches
            left_items = request.POST.getlist('left_item[]')
            right_items = request.POST.getlist('right_item[]')
            correct_matches = request.POST.getlist('correct_match[]')
            
            # Store all definitions
            definitions = []
            for i, right in enumerate(right_items):
                if right.strip():
                    definitions.append({
                        'id': str(uuid.uuid4()),
                        'right_item': right,
                        'order': i
                    })
            
            # Store all terms with their correct definition index
            pairs = []
            for i, left in enumerate(left_items):
                if left.strip() and i < len(correct_matches):
                    correct_def_index = int(correct_matches[i]) if correct_matches[i] else 0
                    pairs.append({
                        'id': str(uuid.uuid4()),
                        'left_item': left,
                        'right_item': definitions[correct_def_index]['right_item'] if correct_def_index < len(definitions) else '',
                        'correct_match': correct_def_index,
                        'order': i
                    })
            
            # Store both definitions and pairs
            question_data['matching_pairs'] = pairs
            question_data['matching_definitions'] = definitions
        
        subject_storage.save_question(question_data)
        return redirect('question_bank')


def question_edit(request, question_id):
    """Edit an existing question"""
    subject_storage = get_current_storage(request)
    
    question = subject_storage.get_question(question_id)
    if not question:
        return HttpResponse('Question not found', status=404)
    
    if request.method == 'GET':
        categories = subject_storage.get_categories()
        context = {
            'question': question,
            'question_json': json.dumps(question),
            'categories': categories,
            'is_edit': True
        }
        return render(request, 'question_editor.html', context)
    
    elif request.method == 'POST':
        # Update question data
        question['question_text'] = request.POST.get('question_text')
        question['question_type'] = request.POST.get('question_type')
        question['category_id'] = request.POST.get('category_id')
        question['explanation'] = request.POST.get('explanation', '')
        question['points'] = int(request.POST.get('points', 1))
        
        # Handle image upload
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            file_name = f'question_images/{question_id}_{image_file.name}'
            file_path = default_storage.save(file_name, ContentFile(image_file.read()))
            question['image'] = file_path
        
        # Handle question type specific data (similar to create)
        question_type = question['question_type']
        
        if question_type in ['single_choice', 'multiple_choice']:
            options = []
            option_texts = request.POST.getlist('option_text[]')
            correct_options = request.POST.getlist('correct_option[]')
            
            for i, option_text in enumerate(option_texts):
                if option_text.strip():
                    options.append({
                        'id': str(uuid.uuid4()),
                        'option_text': option_text,
                        'is_correct': str(i) in correct_options,
                        'order': i
                    })
            
            question['choices'] = options
        
        elif question_type == 'matching':
            # Get terms, definitions, and correct matches
            left_items = request.POST.getlist('left_item[]')
            right_items = request.POST.getlist('right_item[]')
            correct_matches = request.POST.getlist('correct_match[]')
            
            # Store all definitions
            definitions = []
            for i, right in enumerate(right_items):
                if right.strip():
                    definitions.append({
                        'id': str(uuid.uuid4()),
                        'right_item': right,
                        'order': i
                    })
            
            # Store all terms with their correct definition index
            pairs = []
            for i, left in enumerate(left_items):
                if left.strip() and i < len(correct_matches):
                    correct_def_index = int(correct_matches[i]) if correct_matches[i] else 0
                    pairs.append({
                        'id': str(uuid.uuid4()),
                        'left_item': left,
                        'right_item': definitions[correct_def_index]['right_item'] if correct_def_index < len(definitions) else '',
                        'correct_match': correct_def_index,
                        'order': i
                    })
            
            # Store both definitions and pairs
            question['matching_pairs'] = pairs
            question['matching_definitions'] = definitions
        
        subject_storage.save_question(question)
        return redirect('question_bank')


def question_delete(request, question_id):
    """Delete a question"""
    if request.method == 'POST':
        subject_storage = get_current_storage(request)
        subject_storage.delete_question(question_id)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=405)


# Quiz Management
def quiz_list(request):
    """View all quizzes"""
    subject_storage = get_current_storage(request)
    
    quizzes = subject_storage.get_quizzes()
    available_subjects = get_available_subjects()
    current_subject = request.session.get('current_subject', None)
    
    context = {
        'quizzes': quizzes,
        'current_subject': current_subject or 'Default',
        'available_subjects': available_subjects,
    }
    return render(request, 'quiz_list.html', context)


def quiz_create(request):
    """Create a new quiz"""
    subject_storage = get_current_storage(request)
    
    if request.method == 'GET':
        questions = subject_storage.get_questions()
        categories = subject_storage.get_categories()
        context = {
            'questions': questions,
            'categories': categories
        }
        return render(request, 'quiz_creation_interface.html', context)
    
    elif request.method == 'POST':
        quiz_id = str(uuid.uuid4())
        
        # Parse selected questions from JSON
        selected_questions_json = request.POST.get('selected_questions', '[]')
        selected_questions = json.loads(selected_questions_json)
        
        quiz_data = {
            'id': quiz_id,
            'title': request.POST.get('title'),
            'description': request.POST.get('description', ''),
            'instructions': request.POST.get('instructions', ''),
            'time_limit': int(request.POST.get('time_limit', 0)) if request.POST.get('time_limit') else None,
            'is_published': request.POST.get('is_published', 'false') == 'true',
            'questions': selected_questions  # List of {question_id, order, points}
        }
        
        subject_storage.save_quiz(quiz_data)
        return redirect('quiz_list')


def quiz_edit(request, quiz_id):
    """Edit an existing quiz"""
    subject_storage = get_current_storage(request)
    
    quiz = subject_storage.get_quiz(quiz_id)
    if not quiz:
        return HttpResponse('Quiz not found', status=404)
    
    if request.method == 'GET':
        questions = subject_storage.get_questions()
        categories = subject_storage.get_categories()
        
        # Get full question data for questions in this quiz
        quiz_questions = []
        for q in quiz.get('questions', []):
            # Handle both 'id' and 'question_id' for backward compatibility
            question_id = q.get('id') or q.get('question_id')
            if question_id:
                question_data = subject_storage.get_question(question_id)
                if question_data:
                    question_data['quiz_points'] = q.get('points', 1)
                    question_data['quiz_order'] = q.get('order', 0)
                    quiz_questions.append(question_data)
        
        context = {
            'quiz': quiz,
            'questions': questions,
            'categories': categories,
            'quiz_questions': quiz_questions,
            'is_edit': True
        }
        return render(request, 'quiz_creation_interface.html', context)
    
    elif request.method == 'POST':
        # Update quiz data
        selected_questions_json = request.POST.get('selected_questions', '[]')
        selected_questions = json.loads(selected_questions_json)
        
        quiz['title'] = request.POST.get('title')
        quiz['description'] = request.POST.get('description', '')
        quiz['instructions'] = request.POST.get('instructions', '')
        quiz['time_limit'] = int(request.POST.get('time_limit', 0)) if request.POST.get('time_limit') else None
        quiz['is_published'] = request.POST.get('is_published', 'false') == 'true'
        quiz['questions'] = selected_questions
        
        subject_storage.save_quiz(quiz)
        return redirect('quiz_list')


def quiz_delete(request, quiz_id):
    """Delete a quiz"""
    if request.method == 'POST':
        subject_storage = get_current_storage(request)
        subject_storage.delete_quiz(quiz_id)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False}, status=405)


def quiz_generate(request):
    """Auto-generate a quiz from question bank"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    
    subject_storage = get_current_storage(request)
    
    try:
        data = json.loads(request.body)
        generation_type = data.get('generation_type', 'random')
        quiz_title = data.get('title', 'Auto-Generated Quiz')
        
        all_questions = subject_storage.get_questions()
        
        if not all_questions:
            return JsonResponse({'success': False, 'error': 'No questions available in question bank'})
        
        selected_questions = []
        
        if generation_type == 'random':
            # Random selection: Select 50 questions randomly
            num_to_select = min(50, len(all_questions))
            random_questions = random.sample(all_questions, num_to_select)
            selected_questions = [
                {
                    'id': q['id'],
                    'text': q['question_text'],
                    'points': 10
                }
                for q in random_questions
            ]
        
        elif generation_type == 'category':
            # Category balanced: Select 5 questions from each category
            categories = subject_storage.get_categories()
            questions_by_category = {}
            
            # Group questions by category
            for q in all_questions:
                cat_id = q.get('category_id')
                if cat_id:
                    if cat_id not in questions_by_category:
                        questions_by_category[cat_id] = []
                    questions_by_category[cat_id].append(q)
            
            # Select 5 from each category
            for cat_id, questions in questions_by_category.items():
                num_to_select = min(5, len(questions))
                random_from_category = random.sample(questions, num_to_select)
                for q in random_from_category:
                    selected_questions.append({
                        'id': q['id'],
                        'text': q['question_text'],
                        'points': 10
                    })
        
        if not selected_questions:
            return JsonResponse({'success': False, 'error': 'Could not generate quiz with selected criteria'})
        
        # Create new quiz
        quiz_id = str(uuid.uuid4())
        quiz_data = {
            'id': quiz_id,
            'title': quiz_title,
            'description': f'Auto-generated quiz with {len(selected_questions)} questions',
            'instructions': 'Please answer all questions to the best of your ability.',
            'time_limit': 60,
            'is_published': False,
            'questions': selected_questions,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        subject_storage.save_quiz(quiz_data)
        
        return JsonResponse({
            'success': True,
            'quiz_id': quiz_id,
            'num_questions': len(selected_questions)
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


# Taking Quiz
def quiz_take(request, quiz_id):
    """Take a quiz"""
    subject_storage = get_current_storage(request)
    
    quiz = subject_storage.get_quiz(quiz_id)
    if not quiz:
        return HttpResponse('Quiz not found', status=404)
    
    # Get full question data
    quiz_questions = []
    for q in quiz.get('questions', []):
        # Handle both 'id' and 'question_id' for backward compatibility
        question_id = q.get('id') or q.get('question_id')
        if question_id:
            question_data = subject_storage.get_question(question_id)
            if question_data:
                # Create a structure matching template expectations
                quiz_questions.append({
                    'question': question_data,
                    'points': q.get('points', 1)
                })
    
    context = {
        'quiz': quiz,
        'quiz_questions': quiz_questions
    }
    return render(request, 'quiz_take.html', context)


def quiz_submit(request, quiz_id):
    """Submit quiz answers"""
    if request.method != 'POST':
        return JsonResponse({'success': False}, status=405)
    
    subject_storage = get_current_storage(request)
    
    quiz = subject_storage.get_quiz(quiz_id)
    if not quiz:
        return JsonResponse({'success': False, 'error': 'Quiz not found'}, status=404)
    
    # Create attempt
    attempt_id = str(uuid.uuid4())
    
    # Parse answers from request
    answers_json = request.POST.get('answers', '{}')
    answers = json.loads(answers_json)
    
    # Grade the quiz
    total_points = 0
    earned_points = 0
    graded_answers = []
    
    for q in quiz.get('questions', []):
        # Handle both 'id' and 'question_id' for backward compatibility
        question_id = q.get('id') or q.get('question_id')
        if not question_id:
            continue
            
        question_data = subject_storage.get_question(question_id)
        if not question_data:
            continue
        
        points = q.get('points', 1)
        total_points += points
        
        user_answer = answers.get(question_id, {})
        is_correct = False
        
        # Check answer based on question type
        if question_data['question_type'] in ['single_choice', 'multiple_choice']:
            correct_choices = [c['id'] for c in question_data.get('choices', []) if c['is_correct']]
            selected_choices = user_answer.get('selected_choices', [])
            
            if question_data['question_type'] == 'single_choice':
                is_correct = len(selected_choices) == 1 and selected_choices[0] in correct_choices
            else:  # multiple_choice
                is_correct = set(selected_choices) == set(correct_choices)
        
        elif question_data['question_type'] == 'matching':
            correct_pairs = {p['left_item']: p['right_item'] for p in question_data.get('matching_pairs', [])}
            user_pairs = user_answer.get('matching_answer', {})
            is_correct = correct_pairs == user_pairs
        
        if is_correct:
            earned_points += points
        
        graded_answers.append({
            'question_id': question_id,
            'user_answer': user_answer,
            'is_correct': is_correct,
            'points_earned': points if is_correct else 0
        })
    
    # Calculate score percentage
    score = (earned_points / total_points * 100) if total_points > 0 else 0
    
    # Save attempt
    attempt_data = {
        'id': attempt_id,
        'quiz_id': quiz_id,
        'student_name': request.POST.get('student_name', 'Anonymous'),
        'completed_at': datetime.now().isoformat(),
        'score': score,
        'total_points': total_points,
        'earned_points': earned_points,
        'answers': graded_answers
    }
    
    subject_storage.save_attempt(attempt_data)
    
    return JsonResponse({
        'success': True,
        'attempt_id': attempt_id,
        'score': score
    })


def quiz_results(request, attempt_id):
    """View quiz results"""
    subject_storage = get_current_storage(request)
    
    attempt = subject_storage.get_attempt(attempt_id)
    if not attempt:
        return HttpResponse('Attempt not found', status=404)
    
    quiz = subject_storage.get_quiz(attempt['quiz_id'])
    
    # Create a mapping of question_id to points from the quiz
    question_points_map = {}
    for q in quiz.get('questions', []):
        question_id = q.get('id') or q.get('question_id')
        if question_id:
            question_points_map[question_id] = q.get('points', 1)
    
    # Get full question data with answers
    answers = []
    correct_count = 0
    for answer_data in attempt.get('answers', []):
        question_id = answer_data['question_id']
        question_data = subject_storage.get_question(question_id)
        if question_data:
            is_correct = answer_data.get('is_correct', False)
            if is_correct:
                correct_count += 1
            
            # Get the points from the quiz (not from question bank)
            question_points = question_points_map.get(question_id, 1)
            
            # Get the correct answer based on question type
            correct_answer = get_correct_answer_text(question_data)
            user_answer_data = answer_data.get('user_answer', {})
            
            # Extract user answer IDs for display
            user_answer_ids = []
            user_answer_text = 'Not answered'
            user_matching = []
            
            if question_data['question_type'] in ['single_choice', 'multiple_choice']:
                selected_choices = user_answer_data.get('selected_choices', [])
                user_answer_ids = selected_choices
                # Get text of selected choices
                selected_texts = [c['option_text'] for c in question_data.get('choices', []) if c['id'] in selected_choices]
                user_answer_text = ', '.join(selected_texts) if selected_texts else 'Not answered'
            
            elif question_data['question_type'] == 'true_false':
                user_answer_text = user_answer_data.get('answer', 'Not answered')
            
            elif question_data['question_type'] == 'matching':
                matching_answer = user_answer_data.get('matching_answer', {})
                user_matching = [matching_answer.get(pair['left_item'], 0) for pair in question_data.get('matching_pairs', [])]
                matches = []
                for left, right_idx in matching_answer.items():
                    definitions = question_data.get('matching_definitions', [])
                    if right_idx < len(definitions):
                        matches.append(f"{left} → {definitions[right_idx]}")
                user_answer_text = '; '.join(matches) if matches else 'Not answered'
            
            elif question_data['question_type'] == 'short_answer':
                user_answer_text = user_answer_data.get('answer', 'Not answered')
            
            # Add question with points from quiz
            question_data['points'] = question_points
            
            answers.append({
                'question': question_data,
                'user_answer': user_answer_text,
                'user_answer_ids': user_answer_ids,
                'user_matching': user_matching,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'points_earned': answer_data.get('points_earned', 0)
            })
    
    total_questions = len(answers)
    
    context = {
        'attempt': attempt,
        'quiz': quiz,
        'answers': answers,
        'correct_count': correct_count,
        'total_questions': total_questions
    }
    return render(request, 'quiz_results.html', context)


def get_correct_answer_text(question_data):
    """Get the correct answer text for a question"""
    question_type = question_data.get('question_type')
    
    if question_type in ['single_choice', 'multiple_choice']:
        correct_choices = [choice['option_text'] for choice in question_data.get('choices', []) if choice.get('is_correct')]
        if question_type == 'single_choice':
            return correct_choices[0] if correct_choices else 'N/A'
        else:
            return ', '.join(correct_choices) if correct_choices else 'N/A'
    
    elif question_type == 'true_false':
        return question_data.get('correct_answer', 'N/A')
    
    elif question_type == 'matching':
        pairs = question_data.get('matching_pairs', [])
        definitions = question_data.get('matching_definitions', [])
        correct_matches = []
        for pair in pairs:
            left = pair.get('left_item', '')
            correct_idx = pair.get('correct_match', 0)
            if correct_idx < len(definitions):
                right = definitions[correct_idx]
                correct_matches.append(f"{left} → {right}")
        return '; '.join(correct_matches) if correct_matches else 'N/A'
    
    elif question_type == 'short_answer':
        return question_data.get('correct_answer', 'N/A')
    
    return 'N/A'


# Category Management (API endpoints)
@csrf_exempt
@require_http_methods(["GET", "POST"])
def category_list_create(request):
    """List all categories or create a new one"""
    subject_storage = get_current_storage(request)
    
    if request.method == 'GET':
        categories = subject_storage.get_categories()
        return JsonResponse({'categories': categories})
    
    elif request.method == 'POST':
        data = json.loads(request.body)
        category_id = str(uuid.uuid4())
        
        category_data = {
            'id': category_id,
            'name': data.get('name'),
            'description': data.get('description', '')
        }
        
        subject_storage.save_category(category_data)
        return JsonResponse({'success': True, 'category': category_data})


@csrf_exempt
@require_http_methods(["DELETE"])
def category_delete(request, category_id):
    """Delete a category"""
    subject_storage = get_current_storage(request)
    subject_storage.delete_category(category_id)
    return JsonResponse({'success': True})

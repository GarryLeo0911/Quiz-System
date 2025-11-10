from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class QuestionCategory(models.Model):
    """Category/Group for organizing questions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Question Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Question(models.Model):
    """Base question model"""
    QUESTION_TYPES = (
        ('single_choice', 'Single Choice'),
        ('multiple_choice', 'Multiple Choice'),
        ('matching', 'Matching'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question_text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)
    category = models.ForeignKey(QuestionCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
    explanation = models.TextField(help_text="Explanation for the correct answer", blank=True)
    image = models.ImageField(upload_to='question_images/', blank=True, null=True)
    points = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_question_type_display()}: {self.question_text[:50]}"


class ChoiceOption(models.Model):
    """Options for single and multiple choice questions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    option_text = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self):
        return self.option_text


class MatchingPair(models.Model):
    """Pairs for matching questions"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='matching_pairs')
    left_item = models.CharField(max_length=500, help_text="Term or item on the left")
    right_item = models.CharField(max_length=500, help_text="Matching description on the right")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.left_item} -> {self.right_item}"


class Quiz(models.Model):
    """Quiz/Exam model"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    instructions = models.TextField(blank=True)
    time_limit = models.IntegerField(help_text="Time limit in minutes", null=True, blank=True)
    questions = models.ManyToManyField(Question, through='QuizQuestion')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Quizzes"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def total_points(self):
        return sum(qq.points for qq in self.quiz_questions.all())


class QuizQuestion(models.Model):
    """Through model for Quiz-Question relationship with additional fields"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='quiz_questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='quiz_questions')
    order = models.IntegerField(default=0)
    points = models.IntegerField(default=1, validators=[MinValueValidator(1)], help_text="Points for this question in this quiz")
    
    class Meta:
        ordering = ['order', 'id']
        unique_together = ['quiz', 'question']
    
    def __str__(self):
        return f"{self.quiz.title} - Question {self.order}"


class QuizAttempt(models.Model):
    """Record of a user taking a quiz"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    student_name = models.CharField(max_length=200, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"Attempt for {self.quiz.title} by {self.student_name or 'Anonymous'}"


class QuestionAnswer(models.Model):
    """User's answer to a question in a quiz attempt"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    # For choice questions
    selected_choices = models.ManyToManyField(ChoiceOption, blank=True)
    
    # For matching questions (JSON field storing pairs)
    matching_answer = models.JSONField(null=True, blank=True, help_text="Dictionary mapping left items to right items")
    
    is_correct = models.BooleanField(default=False)
    points_earned = models.FloatField(default=0)
    
    class Meta:
        unique_together = ['attempt', 'question']
    
    def __str__(self):
        return f"Answer to {self.question} in {self.attempt}"

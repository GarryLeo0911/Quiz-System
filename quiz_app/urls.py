from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Subject Management
    path('switch-subject/', views.switch_subject, name='switch_subject'),
    
    # Question Bank
    path('questions/', views.question_bank, name='question_bank'),
    path('questions/create/', views.question_create, name='question_create'),
    path('questions/<str:question_id>/edit/', views.question_edit, name='question_edit'),
    path('questions/<str:question_id>/delete/', views.question_delete, name='question_delete'),
    
    # Quizzes/Exams
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quizzes/create/', views.quiz_create, name='quiz_create'),
    path('quizzes/generate/', views.quiz_generate, name='quiz_generate'),
    path('quizzes/<str:quiz_id>/edit/', views.quiz_edit, name='quiz_edit'),
    path('quizzes/<str:quiz_id>/delete/', views.quiz_delete, name='quiz_delete'),
    path('quizzes/<str:quiz_id>/take/', views.quiz_take, name='quiz_take'),
    path('quizzes/<str:quiz_id>/submit/', views.quiz_submit, name='quiz_submit'),
    
    # Results
    path('results/<str:attempt_id>/', views.quiz_results, name='quiz_results'),
    
    # Categories API
    path('api/categories/', views.category_list_create, name='category_list_create'),
    path('api/categories/<str:category_id>/delete/', views.category_delete, name='category_delete_api'),
]

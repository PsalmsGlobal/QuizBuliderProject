from django.contrib import admin
from django.urls import path, include
from .views import quiz, student, teacher
from . import views
from .views.quiz import *



urlpatterns = [
path('token/' , token_send , name="token_send"),
path('about/',  AboutView.as_view(), name="about"),
path('features/', FeaturesView.as_view(), name="features"),
path('success/' , success , name='success'),
path('logout/', LogoutView.as_view(), name="logout"),
path('verify/<auth_token>' , verify , name="verify"),
path('api/check_score', check_score, name="check_score"),
path('api/<id>', api_question, name="api_question"),
path('view_score/', view_score, name="view_score"),
path('<id>', take_quiz, name="take_quiz"),
path('error/' , error_page , name="error"),
    path('', quiz.home, name='home'),

    path('teacher/', include(([
        path('', teacher.teacher_home, name='teacher_home'),
        path('create/', teacher.create, name='create'),
    ],  'quiz'), namespace='teacher')),  
    
    path('student/', include(([
        path('', student.student_home, name='student_home'),
    ],  'quiz'), namespace='student')),    
]

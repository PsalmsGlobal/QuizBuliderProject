from django.contrib import admin
from django.urls import path, include
from .views import quiz, student, teacher
from . import views
from .views.quiz import *



urlpatterns = [
path('token/' , token_send , name="token_send"),
path('about/',  AboutView.as_view(), name="about"),
path('success/' , success , name='success'),
path('logout/', LogoutView.as_view(), name="logout"),
path('verify/<auth_token>' , verify , name="verify"),
path('api/check_score', check_score, name="check_score"),
path('api/<id>', api_question, name="api_question"),
path('view_score', view_score, name="view_score"),
path('<id>', take_quiz, name="take_quiz"),
path('error/' , error_page , name="error"),
    path('', quiz.home, name='home'),

    path('teacher/', include(([
        path('', teacher.teacher_home, name='teacher_home'),
        path('create/', teacher.create, name='create'),
        path('add_course/', teacher.add_course, name='add_course'),
        path('course/', teacher.course, name='course'),
        path('question/', teacher.question, name='question'),
        path('view_question/', teacher.view_question, name='view_question'),
        path('view_course/', teacher.view_course, name='view_course'),
        path('view_student/', teacher.view_student, name='view_student'),
        path('feature/', teacher.feature, name='feature'),
        #path('delete_course/<int:id>', teacher.delete, name="delete_course"),
    ],  'quiz'), namespace='teacher')),  
    
    path('student/', include(([
        path('', student.student_home, name='student_home'),
        path('take_quiz/', student.take_quiz, name='take_quiz'),
        path('instruction/', student.instruction, name='instruction'),
    ],  'quiz'), namespace='student')),    
]

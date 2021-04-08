from django.contrib import admin
from django.urls import path, include
from .views import quiz, students, teachers



urlpatterns = [
path('token/' , quiz.token_send , name="token_send"),
path('about/',  quiz.AboutView.as_view(), name="about"),
path('success/' , quiz.success , name='success'),
path('logout/', quiz.LogoutView.as_view(), name="logout"),
path('verify/<auth_token>' , quiz.verify , name="verify"),
path('error/' , quiz.error_page , name="error"),
path('change_password/',quiz.change_password, name= 'change_password'),
path('changepassword_success/', quiz.changepassword_success, name='changepassword_success'),

    path('', quiz.home, name='home'),

    path('teachers/', include(([
        path('', teachers.teacher_home, name='teacher_home'),
        path('quiz/change/', teachers.QuizListView.as_view(), name='quiz_change_list'),
        path('quiz/add/', teachers.QuizCreateView.as_view(), name='quiz_add'),
        path('quiz/<int:pk>/', teachers.QuizUpdateView.as_view(), name='quiz_change'),
        path('q/<int:pk>/delete/', teachers.QDeleteView.as_view(), name='q_delete'),
        path('quiz/<int:pk>/delete/', teachers.QuizDeleteView.as_view(), name='quiz_delete'),
        path('quiz/<int:pk>/results/', teachers.QuizResultsView.as_view(), name='quiz_results'),
        path('quiz/<int:pk>/question/add/', teachers.question_add, name='question_add'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/', teachers.question_change, name='question_change'),
        path('quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', teachers.QuestionDeleteView.as_view(), name='question_delete'),
        path('add/course/', teachers.add_course, name='add_course'),
        path('course/', teachers.course, name='course'),
    ],  'quiz'), namespace='teachers')),  
    
    path('students/', include(([
        path('', students.QuizListView.as_view(), name='quiz_list'),
        path('interests/', students.StudentInterestsView.as_view(), name='student_interests'),
        path('taken/', students.TakenQuizListView.as_view(), name='taken_quiz_list'),
        path('quiz/<int:pk>/', students.take_quiz, name='take_quiz'),
        path('student_home', students.student_home, name='student_home'),
    ],  'quiz'), namespace='students')),    
]

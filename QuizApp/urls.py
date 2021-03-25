from django.urls import include, path
from django.contrib import admin
from Quiz.views import quiz, student, teacher

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('Quiz.urls')),
    path('accounts/signup/', quiz.SignUpView.as_view(), name='signup'),
    path('accounts/signup/student/', student.StudentSignUpView.as_view(), name='student_signup'),
    path('accounts/signup/teacher/', teacher.TeacherSignUpView.as_view(), name='teacher_signup'),
]
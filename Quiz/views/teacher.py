from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView
from ..forms import TeacherSignUpForm
from ..models import Question, User, Profile, Course
from .quiz import *
from ..forms import CreateQuestionForm, CourseForm
import uuid
from django.contrib import messages

class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        request = self.request
        if request.method == 'POST':
            email = request.POST.get('email')
            try:
                if User.objects.filter(email = email).first():
                    messages.success(request, 'Email is taken.')
                    return redirect('signup')


                user = form.save()
                auth_token = str(uuid.uuid4())
                profile_obj = Profile.objects.create(user = user , auth_token = auth_token)
                profile_obj.save()
                send_mail_after_registration(email , auth_token)
                return redirect('/token/')

            except Exception as e:
                print(e)


        return render(request , 'registration/signup_form.html')

@login_required
def view_question(request):
    questions = Question.objects.all()

    context = {
        'questions' : questions
    }
    return render(request, 'teacher/view_question.html', context)

def view_course(request):
    course_names = Course.objects.all()

    context = {
        'course_names' : course_names
    }
    return render(request, 'teacher/view_course.html', context)

def delete_course_view(request,pk):
    course_names = Course.objects.get(id=pk)
    course_names.delete()
    return HttpResponseRedirect('teacher/view_course.html')

@login_required
def create(request):
    if request.method == 'POST':
        form = CreateQuestionForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data['question'])
            form.save()

            return redirect("teacher:question")
    else:
        form = CreateQuestionForm()

    context = {'form' : form}
    return render(request, 'teacher/create.html', context)

def add_course(request):
    
    if request.method=='POST':
        form=CourseForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['course_name'])        
            form.save()

            return redirect("teacher:course")

    else:
        form=CourseForm()
    context = {'form' : form}
    return render(request,'teacher/add_course.html',context)

def question(request):
    return render(request, 'teacher/question.html')

def teacher_home(request):
    dict={
    
    'total_course':Course.objects.all().count(),
    'total_question':Question.objects.all().count(),
    'total_student':Student.objects.all().count()
    }
    return render(request,'teacher/teacher_home.html',context=dict)

def course(request):
    return render(request, 'teacher/course.html')

def view_student(request):
    return render(request, 'teacher/view_student.html')

def feature(request):
    return render(request, 'teacher/feature.html')




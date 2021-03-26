from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView
from ..models import Question
from ..forms import TeacherSignUpForm
from ..models import Question, User, Profile
from .quiz import *
from ..forms import CreateQuestionForm
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
def teacher_home(request):
    questions = Question.objects.all()

    context = {
        'questions' : questions
    }
    return render(request, 'teacher/teacher_home.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = CreateQuestionForm(request.POST)

        if form.is_valid():
            print(form.cleaned_data['question'])
            form.save()

            return redirect("teacher:teacher_home")
    else:
        form = CreateQuestionForm()

    context = {'form' : form}
    return render(request, 'teacher/create.html', context)

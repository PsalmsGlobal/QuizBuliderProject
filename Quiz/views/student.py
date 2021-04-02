from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from ..forms import StudentSignUpForm
from ..models import User, Profile 
from .quiz import *
import uuid
from django.contrib import messages

class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
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
def student_home(request):
    return render(request, 'student/student_home.html')

def instruction(request):
    return render(request, 'student/instruction.html')

def features(request):
    return render(request, 'student/features.html')

def take_quiz(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'student/take_quiz.html', context)

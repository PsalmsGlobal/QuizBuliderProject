from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib.auth import logout
from django.http import JsonResponse
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages

from ..models import Question, Profile
from django.urls import reverse_lazy
from ..forms import* 
from ..models import* 
import json
import uuid



class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def verify(request , auth_token):
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('success')
        else:
            return redirect('/error/')

        return redirect('/success')

def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi, click the link for verification your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )

def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect("teachers:teacher_home")
        else:
            return redirect("students:student_home")

    return render(request, 'home.html')
    
@login_required
def error_page(request):
    return  render(request , 'registration/error.html')

class AboutView(View):
    def get(self, request):
        return render(request, 'quiz/about.html')

def success (request):
    return render(request, 'registration/success.html')

def token_send(request):
    return render(request, 'registration/token_send.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(data=request.POST, user= request.user)
		if form.is_valid():
			form.save()
			messages.success(request,('You Have Edited Your Password...'))
			return redirect('changepassword_success')
	else:
		form = PasswordChangeForm(user= request.user)

	context = {'form': form}
	return render(request, 'change_password.html', context)

def changepassword_success(request):
    return render(request, 'changepassword_success.html')




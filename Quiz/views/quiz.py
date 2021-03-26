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
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from ..models import Profile
from ..forms import CreateQuestionForm
from ..models import Question
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
                return redirect('success')
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


@login_required
def api_question(request, id):
    raw_questions = Question.objects.filter(course = id)[:20]
    questions = []
    
    for raw_question in raw_questions:
        question = {}
        question['id'] = raw_question.id
        question['question'] = raw_question.question
        question['answer'] = raw_question.answer
        question['marks'] = raw_question.marks
        options = []
        options.append(raw_question.option1)
        options.append(raw_question.option2)
        if raw_question.option3 !='':
            options.append(raw_question.option3)
        if raw_question.option4 !='':
            options.append(raw_question.option4)

        question['options'] = options
        questions.append(question)

    return JsonResponse(questions, safe=False)

@login_required
def view_score(request):
    user = request.user
    score = ScoreBoard.objects.filter(user=user)
    context = {'score': score}
    return render(request, 'quiz/score.html', context)

@login_required
def take_quiz (request, id):
        context = {'id' : id}
        return render(request, 'quiz/quizz.html', context)  

@csrf_exempt
@login_required
def check_score(request):
    data = json.loads(request.body)
    user = request.user
    course_id = data.get('course_id')
    solutions = json.loads(data.get('data'))
    course = Course.objects.get(id=course_id)
    score = 0
    for solution in solutions:
        question = Question.objects.filter(id = solution.get('question_id')).first()
        if (question.answer) == solution.get('option'):
            score = score + question.marks

    score_board = ScoreBoard(course = course, score = score, user = user)
    score_board.save()
    return JsonResponse({'message' : 'success', 'status':True})


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect("teacher:teacher_home")
        else:
            return redirect("student:student_home")

    return render(request, 'home.html')
    
@login_required
def error_page(request):
    return  render(request , 'registration/error.html')

class FeaturesView(View):
    def get (self, request):
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        return render(request, 'quiz/features.html', {'name': f_name}, {'name' : l_name})


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
        return redirect('signup')


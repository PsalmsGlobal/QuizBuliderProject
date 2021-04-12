from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView

from ..forms import StudentInterestsForm, StudentSignUpForm, TakeQuizForm
from ..models import Quiz, Student, TakenQuiz, User, Course, Question, Profile
from ..decorators import student_required
from .quiz import *
import uuid

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
                return redirect('/token')

            except Exception as e:
                print(e)


        return render(request , 'registration/signup_form.html')

@method_decorator([login_required, student_required], name='dispatch')
class StudentInterestsView(UpdateView):
    model = Student
    form_class = StudentInterestsForm
    template_name = 'students/interests_form.html'
    success_url = reverse_lazy('students:quiz_list')

    def get_object(self):
        return self.request.user.student

    def form_valid(self, form):
        messages.success(self.request, 'Courses updated with success!')
        return super().form_valid(form)


@method_decorator([login_required, student_required], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'students/quiz_list.html'

    def get_queryset(self):
        student = self.request.user.student
        student_courses = student.courses.values_list('pk', flat=True)
        taken_quizzes = student.quizzes.values_list('pk', flat=True)
        queryset = Quiz.objects.filter(course__in=student_courses) \
            .exclude(pk__in=taken_quizzes) \
            .annotate(questions_count=Count('questions')) \
            .filter(questions_count__gt=0)
        return queryset


@method_decorator([login_required, student_required], name='dispatch')
class TakenQuizListView(ListView):
    model = TakenQuiz
    context_object_name = 'taken_quizzes'
    template_name = 'students/taken_quiz_list.html'

    def get_queryset(self):
        queryset = self.request.user.student.taken_quizzes \
            .select_related('quiz', 'quiz__course') \
            .order_by('quiz__name')
        return queryset


@login_required
@student_required
def take_quiz(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    student = request.user.student

    if student.quizzes.filter(pk=pk).exists():
        return render(request, 'students/taken_quiz.html')

    total_questions = quiz.questions.count()
    unanswered_questions = student.get_unanswered_questions(quiz)
    total_unanswered_questions = unanswered_questions.count()
    progress = 100 - round(((total_unanswered_questions - 1) / total_questions) * 100)
    question = unanswered_questions.first()

    if request.method == 'POST':
        form = TakeQuizForm(question=question, data=request.POST)
        if form.is_valid():
            with transaction.atomic():
                student_answer = form.save(commit=False)
                student_answer.student = student
                student_answer.save()
                if student.get_unanswered_questions(quiz).exists():
                    return redirect('students:take_quiz', pk)
                else:
                    correct_answers = student.quiz_answers.filter(answer__question__quiz=quiz, answer__is_correct=True).count()
                    score = round((correct_answers / total_questions) * 100.0, 2)
                    TakenQuiz.objects.create(student=student, quiz=quiz, score=score)
                    if score < 74.0:
                        messages.warning(request, 'Better luck next time! Your score for the quiz %s was %s.' % (quiz.name, score))
                    else:
                        messages.success(request, 'Congratulations! perfect quiz %s! You scored %s points.' % (quiz.name, score))
                    return redirect('students:quiz_list')
    else:
        form = TakeQuizForm(question=question)

    return render(request, 'students/take_quiz_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'progress': progress
    })

        
# @login_required
def student_home(request):
    dict={
    
    'total_name':Course.objects.all().count(),
    'total_question':Question.objects.all().count(),
    'total_student':Student.objects.all().count(),
    'total_quiz':Quiz.objects.all().count()
    }
    return render(request,'students/student_home.html',context=dict)

# def instruction(request):
#     return render(request, 'student/instruction.html')

# def features(request):
#     return render(request, 'student/features.html')

# def take_quiz(request):
#     courses = Course.objects.all()
#     context = {'courses': courses}
#     return render(request, 'student/take_quiz.html', context)

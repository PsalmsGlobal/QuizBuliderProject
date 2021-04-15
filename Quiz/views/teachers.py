from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.db.models import Avg, Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..forms import BaseAnswerInlineFormSet, QuestionForm, TeacherSignUpForm , CourseForm
from ..decorators import teacher_required
from ..models import Answer, Question, Quiz, User, Course, Student
from .quiz import send_mail_after_registration
import uuid

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
                    return redirect('teacher_signup')

                user = form.save()
                auth_token = str(uuid.uuid4())
                profile_obj = Profile.objects.create(user = user , auth_token = auth_token)
                profile_obj.save()
                send_mail_after_registration(email , auth_token)
                return redirect('/token')
               

            except Exception as e:
                print(e)


        return render(request , 'registration/signup_form.html')

@method_decorator([login_required, teacher_required], name='dispatch')
class QuizListView(ListView):
    model = Quiz
    ordering = ('name', )
    context_object_name = 'quizzes'
    template_name = 'teachers/quiz_change_list.html'

    def get_queryset(self):
        queryset = self.request.user.quizzes \
            .select_related('course') \
            .annotate(questions_count=Count('questions', distinct=True)) \
            .annotate(taken_count=Count('taken_quizzes', distinct=True))
        return queryset


@method_decorator([login_required, teacher_required], name='dispatch')
class QuizCreateView(CreateView):
    model = Quiz
    fields = ('name', 'course', )
    template_name = 'teachers/quiz_add_form.html'

    def form_valid(self, form):
        quiz = form.save(commit=False)
        quiz.owner = self.request.user
        quiz.save()
        messages.success(self.request, '𝑇ℎ𝑒 𝑞𝑢𝑖𝑧 𝑤𝑎𝑠 𝑐𝑟𝑒𝑎𝑡𝑒𝑑 𝑠𝑢𝑐𝑐𝑒𝑠𝑠𝑓𝑢𝑙𝑙𝑦❗ 𝐺𝑜 𝑎ℎ𝑒𝑎𝑑 𝑎𝑛𝑑 𝑎𝑑𝑑 𝑠𝑜𝑚𝑒 𝑞𝑢𝑒𝑠𝑡𝑖𝑜𝑛𝑠 𝑛𝑜𝑤.')
        return redirect('teachers:add_more_quiz')


@method_decorator([login_required, teacher_required], name='dispatch')
class QuizUpdateView(UpdateView):
    model = Quiz
    fields = ('name', 'course', )
    context_object_name = 'quiz'
    template_name = 'teachers/quiz_change_form.html'

    def get_context_data(self, **kwargs):
        kwargs['questions'] = self.get_object().questions.annotate(answers_count=Count('answers'))
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        '''
        This method is an implicit object-level permission management
        This view will only match the ids of existing quizzes that belongs
        to the logged in user.
        '''
        return self.request.user.quizzes.all()

    def get_success_url(self):
        return reverse('teachers:quiz_change', kwargs={'pk': self.object.pk})


@method_decorator([login_required, teacher_required], name='dispatch')
class QuizDeleteView(DeleteView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'teachers/quiz_delete_confirm.html'
    success_url = reverse_lazy('teachers:quiz_change_list')

    def delete(self, request, *args, **kwargs):
        quiz = self.get_object()
        messages.success(request, '𝑇ℎ𝑒 𝑞𝑢𝑖𝑧 %s 𝑤𝑎𝑠 𝑑𝑒𝑙𝑒𝑡𝑒𝑑 𝑠𝑢𝑐𝑐𝑒𝑠𝑠𝑓𝑢𝑙𝑙𝑦❗' % quiz.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()


@method_decorator([login_required, teacher_required], name='dispatch')
class QDeleteView(DeleteView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'teachers/q_delete_confirm.html'
    success_url = reverse_lazy('teachers:quiz_change_list')

    def delete(self, request, *args, **kwargs):
        quiz = self.get_object()
        messages.success(request, '𝑇ℎ𝑒 𝑞𝑢𝑖𝑧 %s 𝑤𝑎𝑠 𝑑𝑒𝑙𝑒𝑡𝑒𝑑 𝑠𝑢𝑐𝑐𝑒𝑠𝑠𝑓𝑢𝑙𝑙𝑦❗' % quiz.name)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()



@method_decorator([login_required, teacher_required], name='dispatch')
class QuizResultsView(DetailView):
    model = Quiz
    context_object_name = 'quiz'
    template_name = 'teachers/quiz_results.html'

    def get_context_data(self, **kwargs):
        quiz = self.get_object()
        taken_quizzes = quiz.taken_quizzes.select_related('student__user').order_by('-date')
        total_taken_quizzes = taken_quizzes.count()
        quiz_score = quiz.taken_quizzes.aggregate(average_score=Avg('score'))
        extra_context = {
            'taken_quizzes': taken_quizzes,
            'total_taken_quizzes': total_taken_quizzes,
            'quiz_score': quiz_score
        }
        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()



@login_required
@teacher_required
def question_add(request, pk):
    # By filtering the quiz by the url keyword argument `pk` and
    # by the owner, which is the logged in user, we are protecting
    # this view at the object-level. Meaning only the owner of
    # quiz will be able to add questions to it.
    quiz = get_object_or_404(Quiz, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz
            question.save()
            messages.success(request, '𝑌𝑜𝑢 𝑐𝑎𝑛 𝑛𝑜𝑤 𝑎𝑑𝑑 𝑐ℎ𝑜𝑖𝑐𝑒𝑠 𝑡𝑜 𝑡ℎ𝑒 𝑞𝑢𝑒𝑠𝑡𝑖𝑜𝑛.')
            return redirect('teachers:question_change', quiz.pk, question.pk)
    else:
        form = QuestionForm()

    return render(request, 'teachers/question_add_form.html', {'quiz': quiz, 'form': form})


@login_required
@teacher_required
def question_change(request, quiz_pk, question_pk):
    # Simlar to the `question_add` view, this view is also managing
    # the permissions at object-level. By querying both `quiz` and
    # `question` we are making sure only the owner of the quiz can
    # change its details and also only questions that belongs to this
    # specific quiz can be changed via this url (in cases where the
    # user might have forged/player with the url params.
    quiz = get_object_or_404(Quiz, pk=quiz_pk, owner=request.user)
    question = get_object_or_404(Question, pk=question_pk, quiz=quiz)

    AnswerFormSet = inlineformset_factory(
        Question,  # parent model
        Answer,  # base model
        formset=BaseAnswerInlineFormSet,
        fields=('text', 'is_correct'),
        min_num=2,  
        validate_min=True,
        max_num=20  ,
        validate_max=True
    )

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()
            messages.success(request, '𝑄𝑢𝑒𝑠𝑡𝑖𝑜𝑛 𝑎𝑛𝑑 𝑐ℎ𝑜𝑖𝑐𝑒𝑠 𝑠𝑎𝑣𝑒𝑑 𝑠𝑢𝑐𝑐𝑒𝑠𝑠𝑓𝑢𝑙𝑙𝑦❗')
            return redirect('teachers:quiz_change', quiz.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)

    return render(request, 'teachers/question_change_form.html', {
        'quiz': quiz,
        'question': question,
        'form': form,
        'formset': formset
    })


@method_decorator([login_required, teacher_required], name='dispatch')
class QuestionDeleteView(DeleteView):
    model = Question
    context_object_name = 'question'
    template_name = 'teachers/question_delete_confirm.html'
    pk_url_kwarg = 'question_pk'

    def get_context_data(self, **kwargs):
        question = self.get_object()
        kwargs['quiz'] = question.quiz
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        question = self.get_object()
        messages.success(request, '𝑇ℎ𝑒 𝑞𝑢𝑒𝑠𝑡𝑖𝑜𝑛 %s 𝑤𝑎𝑠 𝑑𝑒𝑙𝑒𝑡𝑒𝑑 𝑠𝑢𝑐𝑐𝑒𝑠𝑠𝑓𝑢𝑙𝑙𝑦❗' % question.text)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Question.objects.filter(quiz__owner=self.request.user)

    def get_success_url(self):
        question = self.get_object()
        return reverse('teachers:quiz_change', kwargs={'pk': question.quiz_id})


def teacher_home(request):
    dict={
    
    'total_name':Course.objects.all().count(),
    'total_question':Question.objects.all().count(),
    'total_student':Student.objects.all().count(),
    'total_quiz':Quiz.objects.all().count()
    }
    return render(request,'teachers/teacher_home.html',context=dict)
  
def course(request):
    return render(request, 'teachers/course.html')

def view_course(request):
    name = Course.objects.all()

    context = {
        "name" : name,
    }
    return render(request, 'teachers/view_course.html', context)


def add_course(request):
    
    if request.method=='POST':
        form=CourseForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data['name'])        
            form.save()
            messages.success(request, 'Course Added successfully!')
            return redirect("teachers:course")

    else:
        form=CourseForm()
    context = {'form' : form}
    return render(request,'teachers/add_course.html',context)

def add_more_quiz(request):
    return render(request, 'teachers/add_more_quiz.html')


from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from .models import (Answer, Question, Student, StudentAnswer,
                              Course, User)


class StudentSignUpForm(UserCreationForm):
    email       = forms.EmailField(label="", widget=forms. TextInput(attrs={'class':'form-control form-control-sm rounded-pill mt-3 ', 'style':'text-align: center;font-size:15px;', 'placeholder': 'πΈππππ π΄πππππ π '}))
    first_name  = forms.CharField(label="", max_length=100, widget=forms. TextInput(attrs={'class':'form-control form-control-sm rounded-pill mt-3 ', 'style':'text-align: center;font-size:15px;', 'placeholder': 'πΉπππ π‘ ππππ'}))
    last_name   = forms.CharField(label="", max_length=100, widget=forms. TextInput(attrs={'class':'form-control form-control-sm rounded-pill mt-3 ', 'style':'text-align: center;font-size:15px;', 'placeholder': 'πΏππ π‘ ππππ'}))
  
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','password1', 'password2' )

    def __init__(self, *args, **kwargs):
        super(StudentSignUpForm, self).__init__(*args, **kwargs)


        self.fields['username'].widget.attrs['class']        = 'form-control form-control-sm rounded-pill '
        self.fields['username'].widget.attrs['style']       = 'text-align: center;font-size:15px;'
        self.fields['username'].widget.attrs['placeholder']  = 'ππ ππππππ'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class ="form-text text-muted"><small></small></span>'

        self.fields['password1'].widget.attrs['class']       = 'form-control form-control-sm rounded-pill mt-3'
        self.fields['password1'].widget.attrs['style']       = 'text-align: center;font-size:15px;'
        self.fields['password1'].widget.attrs['placeholder'] = 'πππ π π€πππ'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<span class ="form-text text-muted"><small></small></span>'

        self.fields['password2'].widget.attrs['class']       = 'form-control form-control-sm rounded-pill '
        self.fields['password2'].widget.attrs['style']       = 'text-align: center;font-size:15px;'
        self.fields['password2'].widget.attrs['placeholder'] = 'πΆππππππ πππ π π€πππ'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class ="form-text text-muted text-center"><small>******πΈππ‘ππ π‘βπ π πππ πππ π π€πππ πππ π£ππππππππ‘πππ.</small></span>'

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.email=self.cleaned_data.get('email')
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        return user


class TeacherSignUpForm(UserCreationForm):
    email       = forms.EmailField(label="", widget=forms. TextInput(attrs={'class':'form-control form-control-sm rounded-pill mt-3 ', 'style':'text-align: center;font-size:15px;', 'placeholder': 'πΈππππ π΄πππππ π '}))
    first_name  = forms.CharField(label="", max_length=100, widget=forms. TextInput(attrs={'class':'form-control form-control-sm rounded-pill mt-3  ', 'style':'text-align: center;font-size:15px;', 'placeholder': 'πΉπππ π‘ ππππ'}))
    last_name   = forms.CharField(label="", max_length=100, widget=forms. TextInput(attrs={'class':'form-control form-control-sm rounded-pill mt-3 ', 'style':'text-align: center;font-size:15px;', 'placeholder': 'πΏππ π‘ ππππ'}))
    

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','password1', 'password2' )

    def __init__(self, *args, **kwargs):
        super(TeacherSignUpForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class']        = 'form-control form-control-sm rounded-pill '
        self.fields['username'].widget.attrs['style']       = 'text-align: center;font-size:15px;'
        self.fields['username'].widget.attrs['placeholder']  = 'ππ ππππππ'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class ="form-text text-muted"><small></small></span>'

        self.fields['password1'].widget.attrs['class']       = 'form-control form-control-sm rounded-pill mt-3'
        self.fields['password1'].widget.attrs['style']       = 'text-align: center;font-size:15px;'
        self.fields['password1'].widget.attrs['placeholder'] = 'πππ π π€πππ'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<span class ="form-text text-muted"><small></small></span>'

        self.fields['password2'].widget.attrs['class']       = 'form-control form-control-sm rounded-pill'
        self.fields['password2'].widget.attrs['style']       = 'text-align: center;font-size:15px;'
        self.fields['password2'].widget.attrs['placeholder'] = 'πΆππππππ πππ π π€πππ'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class ="form-text text-muted"><small>******πΈππ‘ππ π‘βπ π πππ πππ π π€πππ πππ π£ππππππππ‘πππ.</small></span>'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email=self.cleaned_data.get('email')
        user.is_teacher = True
        if commit:
            user.save()
        return user


class StudentInterestsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('courses', )
        widgets = {
            'courses': forms.CheckboxSelectMultiple
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', )

class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields=['name']
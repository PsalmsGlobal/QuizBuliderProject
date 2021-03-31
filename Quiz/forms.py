from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Question, Course
from .models import User, Student

class StudentSignUpForm(UserCreationForm):
    email       = forms.EmailField(label="", widget=forms. TextInput(attrs={'class':'form-control form-control-sm rounded-pill  mt-2', 'style':'text-align: center;font-size:15px;', 'placeholder': '𝐸𝑚𝑎𝑖𝑙 𝐴𝑑𝑑𝑟𝑒𝑠𝑠'}))
    first_name  = forms.CharField(label="", max_length=100, widget=forms. TextInput(attrs={'class':'form-control form-control-sm rounded-pill  mt-2', 'style':'text-align: center;font-size:15px;', 'placeholder': '𝐹𝑖𝑟𝑠𝑡 𝑁𝑎𝑚𝑒'}))
    last_name   = forms.CharField(label="", max_length=100, widget=forms. TextInput(attrs={'class':'form-control form-control-sm rounded-pill  mt-2', 'style':'text-align: center;font-size:15px;', 'placeholder': '𝐿𝑎𝑠𝑡 𝑁𝑎𝑚𝑒'}))
  
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','password1', 'password2' )

    def __init__(self, *args, **kwargs):
        super(StudentSignUpForm, self).__init__(*args, **kwargs)


        self.fields['username'].widget.attrs['class']        = 'form-control form-control-sm rounded-pill '
        self.fields['username'].widget.attrs['style']       = 'text-align: center;font-size:15px;'
        self.fields['username'].widget.attrs['placeholder']  = '𝑈𝑠𝑒𝑟𝑛𝑎𝑚𝑒'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class ="form-text text-muted"><small></small></span>'

        self.fields['password1'].widget.attrs['class']       = 'form-control form-control-sm rounded-pill  mt-2'
        self.fields['password1'].widget.attrs['style']       = 'text-align: center;font-size:15px;'
        self.fields['password1'].widget.attrs['placeholder'] = '𝑃𝑎𝑠𝑠𝑤𝑜𝑟𝑑'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<span class ="form-text text-muted"><small></small></span>'

        self.fields['password2'].widget.attrs['class']       = 'form-control form-control-sm rounded-pill  mt-2'
        self.fields['password2'].widget.attrs['style']       = 'text-align: center;font-size:15px;'
        self.fields['password2'].widget.attrs['placeholder'] = '𝐶𝑜𝑛𝑓𝑖𝑟𝑚 𝑃𝑎𝑠𝑠𝑤𝑜𝑟𝑑'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class ="form-text text-muted text-center"><small>******𝐸𝑛𝑡𝑒𝑟 𝑡ℎ𝑒 𝑠𝑎𝑚𝑒 𝑝𝑎𝑠𝑠𝑤𝑜𝑟𝑑 𝑓𝑜𝑟 𝑣𝑒𝑟𝑖𝑓𝑖𝑐𝑎𝑡𝑖𝑜𝑛.</small></span>'

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.email=self.cleaned_data.get('email')
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        return user


class TeacherSignUpForm(UserCreationForm):
    email       = forms.EmailField(label="", widget=forms. TextInput(attrs={'class':'form-control form-control-sm rounded-pill  mt-2', 'style':'text-align: center;font-size:15px;', 'placeholder': '𝐸𝑚𝑎𝑖𝑙 𝐴𝑑𝑑𝑟𝑒𝑠𝑠'}))
    first_name  = forms.CharField(label="", max_length=100, widget=forms. TextInput(attrs={'class':'form-control form-control-sm rounded-pill  mt-2', 'style':'text-align: center;font-size:15px;', 'placeholder': '𝐹𝑖𝑟𝑠𝑡 𝑁𝑎𝑚𝑒'}))
    last_name   = forms.CharField(label="", max_length=100, widget=forms. TextInput(attrs={'class':'form-control form-control-sm rounded-pill  mt-2', 'style':'text-align: center;font-size:15px;', 'placeholder': '𝐿𝑎𝑠𝑡 𝑁𝑎𝑚𝑒'}))
    

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','password1', 'password2' )

    def __init__(self, *args, **kwargs):
        super(TeacherSignUpForm, self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['class']        = 'form-control form-control-sm rounded-pill '
        self.fields['username'].widget.attrs['style']       = 'text-align: center;font-size:15px;'
        self.fields['username'].widget.attrs['placeholder']  = '𝑈𝑠𝑒𝑟𝑛𝑎𝑚𝑒'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class ="form-text text-muted"><small></small></span>'

        self.fields['password1'].widget.attrs['class']       = 'form-control form-control-sm rounded-pill  mt-2'
        self.fields['password1'].widget.attrs['style']       = 'text-align: center;font-size:15px;'
        self.fields['password1'].widget.attrs['placeholder'] = '𝑃𝑎𝑠𝑠𝑤𝑜𝑟𝑑'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<span class ="form-text text-muted"><small></small></span>'

        self.fields['password2'].widget.attrs['class']       = 'form-control form-control-sm rounded-pill  mt-2'
        self.fields['password2'].widget.attrs['style']       = 'text-align: center;font-size:15px;'
        self.fields['password2'].widget.attrs['placeholder'] = '𝐶𝑜𝑛𝑓𝑖𝑟𝑚 𝑃𝑎𝑠𝑠𝑤𝑜𝑟𝑑'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class ="form-text text-muted"><small>******𝐸𝑛𝑡𝑒𝑟 𝑡ℎ𝑒 𝑠𝑎𝑚𝑒 𝑝𝑎𝑠𝑠𝑤𝑜𝑟𝑑 𝑓𝑜𝑟 𝑣𝑒𝑟𝑖𝑓𝑖𝑐𝑎𝑡𝑖𝑜𝑛.</small></span>'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email=self.cleaned_data.get('email')
        user.is_teacher = True
        if commit:
            user.save()
        return user


class CreateQuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['course', 'question', 'marks', 'answer', 'option1', 'option2', 'option3', 'option4']

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields=['course_name','marks']
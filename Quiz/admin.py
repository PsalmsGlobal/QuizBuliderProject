from django.contrib import admin
from .models import Answer, Student
from .import models
                    
@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
  list_display = ['name',]


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
  list_display = ( 'username', 'first_name', 'last_name', 'email', 'is_student', 'is_teacher',)
  list_filter = ('is_student', 'is_teacher')


@admin.register(models.Quiz)
class QuizAdmin(admin.ModelAdmin):
  list_display = ['owner', 'name', 'course', ]


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 3



@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
  fieldsets = [
      (None, {'fields': ['quiz', 'text', ]}),
  ]
  inlines = [AnswerInline]

  list_display = ('text', 'was_created_recently')
  search_fields = ['text']




@admin.register(models.StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
  list_display = ['student', 'answer']


@admin.register(models.TakenQuiz)
class TakenQuizAdmin(admin.ModelAdmin):
  list_display = ['student', 'quiz', 'score', 'date']


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ['user', 'auth_token', 'is_verified']


admin.site.register(Answer)
admin.site.register(Student)








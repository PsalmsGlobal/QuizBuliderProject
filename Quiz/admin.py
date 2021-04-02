from django.contrib import admin
#from .models import*
from .import models
from .models import Teacher, Student



@admin.register(models.Course)

class CourseAdmin(admin.ModelAdmin):
  list_display = ['course_name',]

@admin.register(models.Question)

class QuestionAdmin(admin.ModelAdmin):
  list_display = ['question','course',]

@admin.register(models.ScoreBoard)

class ScoreBoardAdmin(admin.ModelAdmin):
  list_display = ['course', 'Date_Answered', 'user', 'score',]

@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
  list_display = ['user']

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
  list_display = ( 'username', 'first_name', 'last_name', 'email', 'is_student', 'is_teacher',)
  list_filter = ('is_student', 'is_teacher')

admin.site.register(Student)
admin.site.register(Teacher)




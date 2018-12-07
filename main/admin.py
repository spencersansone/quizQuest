from django.contrib import admin
from .models import *

class UserProfileList(admin.ModelAdmin):
    list_display = ('user','role')
    ordering = ['user']

admin.site.register(UserProfile, UserProfileList)

#basically, this is just *NAMEOFMODEL* List
class SchoolList(admin.ModelAdmin):
    #these are the columns that will show up
    list_display = ('name','code',)
    
    #this is how the admin page will order them
    ordering = ['name']

admin.site.register(School, SchoolList)

class ClassList(admin.ModelAdmin):
    #these are the columns that will show up
    list_display = ('name', 'description','instructor','code',)
    
    #this is how the admin page will order them
    ordering = ['name']

admin.site.register(Class, ClassList)

class ClassRegistrationList(admin.ModelAdmin):
    #these are the columns that will show up
    list_display = ('student','Class',)
    
    #this is how the admin page will order them
    ordering = ['student']

admin.site.register(ClassRegistration, ClassRegistrationList)

class QuestionList(admin.ModelAdmin):
    #these are the columns that will show up
    list_display = ('index','question_text', 'quiz')
    
    #this is how the admin page will order them
    ordering = ['index']

admin.site.register(Question, QuestionList)

class QuizList(admin.ModelAdmin):
    #these are the columns that will show up
    list_display = ('index','Class','published', 'name')
    
    #this is how the admin page will order them
    ordering = ['index']

admin.site.register(Quiz, QuizList)

class AnswerList(admin.ModelAdmin):
    #these are the columns that will show up
    list_display = ('answer','question','correct',)
    
    #this is how the admin page will order them
    ordering = ['answer']

admin.site.register(Answer, AnswerList)

class QuizEntryList(admin.ModelAdmin):
    #these are the columns that will show up
    list_display = ('student','final_grade','certain_quiz',)
    
    #this is how the admin page will order them
    ordering = ['certain_quiz']

admin.site.register(QuizEntry, QuizEntryList)

class QuestionEntryList(admin.ModelAdmin):
    #these are the columns that will show up
    list_display = ('quiz_entry','selected_answer',)
    
    #this is how the admin page will order them
    ordering = ['quiz_entry']

admin.site.register(QuestionEntry, QuestionEntryList)

class CompQuizList(admin.ModelAdmin):
    #these are the columns that will show up
    list_display = ('quiz','Class','approved','declined','invited_instructor')
    
    #this is how the admin page will order them
    ordering = ['quiz']

admin.site.register(CompQuiz, CompQuizList)
# Register your models here.


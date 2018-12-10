from django.contrib import admin
from .models import *

class UserProfileList(admin.ModelAdmin):
    list_display = ('user','role')
    ordering = ['user']

admin.site.register(UserProfile, UserProfileList)

class SchoolList(admin.ModelAdmin):
    
    list_display = ('name','code',)
    
    ordering = ['name']

admin.site.register(School, SchoolList)

class ClassList(admin.ModelAdmin):
    
    list_display = ('name', 'description','instructor','code',)
    
    ordering = ['name']

admin.site.register(Class, ClassList)

class ClassRegistrationList(admin.ModelAdmin):
    
    list_display = ('student','Class',)
    
    ordering = ['student']

admin.site.register(ClassRegistration, ClassRegistrationList)

class QuestionList(admin.ModelAdmin):
    
    list_display = ('index','question_text', 'quiz')
    
    ordering = ['index']

admin.site.register(Question, QuestionList)

class QuizList(admin.ModelAdmin):
    
    list_display = ('index','Class','published', 'name')
    
    ordering = ['index']

admin.site.register(Quiz, QuizList)

class AnswerList(admin.ModelAdmin):
    
    list_display = ('answer','question','correct',)
    
    ordering = ['answer']

admin.site.register(Answer, AnswerList)

class QuizEntryList(admin.ModelAdmin):
    
    list_display = ('student','final_grade','certain_quiz',)
    
    ordering = ['certain_quiz']

admin.site.register(QuizEntry, QuizEntryList)

class CompQuizEntryList(admin.ModelAdmin):
    
    list_display = ('student','final_grade','certain_comp_quiz',)
    
    ordering = ['certain_comp_quiz']

admin.site.register(CompQuizEntry, CompQuizEntryList)

class QuestionEntryList(admin.ModelAdmin):
    
    list_display = ('quiz_entry','selected_answer',)
    
    ordering = ['quiz_entry']

admin.site.register(QuestionEntry, QuestionEntryList)

class CompQuestionEntryList(admin.ModelAdmin):
    
    list_display = ('comp_quiz_entry','selected_answer',)
    
    ordering = ['comp_quiz_entry']

admin.site.register(CompQuestionEntry, CompQuestionEntryList)

class CompQuizList(admin.ModelAdmin):
    
    list_display = ('quiz','Class','approved','declined','invited_instructor')
    
    ordering = ['quiz']

admin.site.register(CompQuiz, CompQuizList)
# Register your models here.


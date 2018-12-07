from django.db import models
from django.contrib.auth.models import User

# this is an example model
#
# class ModelNameHere(models.Model):
#     name = models.CharField()
#     number_value = models.IntegerField()'
#     ...
#     ...
#     ...

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    role = models.CharField(max_length=100)
    datetime_joined = models.DateTimeField()
    
    #this is the function for changing the "display name"
    def __str__(self):
        return str(self.user)
        
    @property
    def full_name(self):
        f_n = str(self.user.first_name)
        l_n = str(self.user.last_name)
        return f_n + " " + l_n
        
    
class School(models.Model):
    name = models.CharField(max_length=100)
    code = models.IntegerField(unique=True)
    
    #this is the function for changing the "display name"
    def __str__(self):
        return str(self.name)
    
class Class(models.Model):
    instructor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default="")
    #name example = MATH 3181
    name = models.CharField(max_length=100)
    #description example = Introduction to Geometry
    description = models.CharField(max_length=100)
    code = models.IntegerField(unique=True)
    
    #this is the function for changing the "display name"
    def __str__(self):
        return str(self.name)
        
    @property
    def get_instructor_name(self):
        return self.instructor.user.first_name + " " + self.instructor.user.last_name
    
class ClassRegistration(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default="")
    Class = models.ForeignKey(Class, on_delete=models.CASCADE, default="")
    approved = models.BooleanField(default=False)

class Quiz(models.Model):
    name = models.CharField(max_length=100)
    index = models.IntegerField()
    Class = models.ForeignKey(Class, on_delete=models.CASCADE, default="")
    published = models.BooleanField()
    
    def __str__(self):
        return str(self.name)
        
class CompQuiz(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, default="")
    Class = models.ForeignKey(Class, on_delete=models.CASCADE, default="")
    approved = models.BooleanField()
    declined = models.BooleanField()
    invited_instructor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default="")
    

    def __str__(self):
        return str(self.name)
    
class Question(models.Model):
    index = models.IntegerField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, default="")
    question_text = models.TextField(max_length=750)
    
    def __str__(self):
        return "#" + str(self.index) + ":" + str(self.question_text)

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default="")
    answer = models.CharField(max_length=300)
    correct = models.BooleanField()

class QuizEntry(models.Model):
    datetime_started = models.DateTimeField(blank=True,null=True)
    datetime_completed = models.DateTimeField(blank=True,null=True)
    certain_quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, default="")
    final_grade = models.FloatField(blank=True,null=True)
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default="")
    
    def __str__(self):
        return self.certain_quiz.name + " - " + str(self.datetime_started)
    
class QuestionEntry(models.Model):
    quiz_entry = models.ForeignKey(QuizEntry, on_delete=models.CASCADE, default="")
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name = "selected_answer", default="")
    correct_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name = "correct_answer", default="")
# Create your models here.

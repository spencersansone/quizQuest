from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")
    role = models.CharField(max_length=100)
    datetime_joined = models.DateTimeField()
    
    def __str__(self):
        return str(self.user)
        
    @property
    def full_name(self):
        f_n = str(self.user.first_name)
        l_n = str(self.user.last_name)
        return f_n + " " + l_n
        
    @property
    def is_instructor(self):
        role = str(self.role)
        if role == "Instructor":
            return True
        return False    
    
    @property
    def is_student(self):
        role = str(self.role)
        if role == "Student":
            return True
        return False

def get_user_profile(self):
    return UserProfile.objects.get(user=self)

User.add_to_class("get_user_profile", get_user_profile)
        
class School(models.Model):
    name = models.CharField(max_length=100)
    code = models.IntegerField(unique=True)
    
    def __str__(self):
        return str(self.name)
    
class Class(models.Model):
    instructor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default="")
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    code = models.IntegerField(unique=True)
    
    def __str__(self):
        return str(self.name)
        
    @property
    def get_instructor_name(self):
        return self.instructor.user.first_name + " " + self.instructor.user.last_name
    
class ClassRegistration(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default="")
    Class = models.ForeignKey(Class, on_delete=models.CASCADE, default="")
    approved = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.student) +" - "+ str(self.Class)

class Quiz(models.Model):
    name = models.CharField(max_length=100)
    index = models.IntegerField()
    Class = models.ForeignKey(Class, on_delete=models.CASCADE, default="")
    published = models.BooleanField()
    
    def __str__(self):
        return str(self.name)
    
    @property
    def get_num_questions(self):
        questions = Question.objects.filter(quiz=self)
        return len(questions)
    
        
class CompQuiz(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, default="")
    Class = models.ForeignKey(Class, on_delete=models.CASCADE, default="")
    approved = models.BooleanField()
    declined = models.BooleanField()
    invited_instructor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default="")
    
    def __str__(self):
        return str(self.quiz.name)
    
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
        
class CompQuizEntry(models.Model):
    datetime_started = models.DateTimeField(blank=True,null=True)
    datetime_completed = models.DateTimeField(blank=True,null=True)
    certain_comp_quiz = models.ForeignKey(CompQuiz, on_delete=models.CASCADE, default="")
    final_grade = models.FloatField(blank=True,null=True)
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default="")
    
    def __str__(self):
        return self.certain_comp_quiz.quiz.name + " - " + str(self.datetime_started)
    
class QuestionEntry(models.Model):
    quiz_entry = models.ForeignKey(QuizEntry, on_delete=models.CASCADE, default="")
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name = "selected_answer", default="")
    correct_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name = "correct_answer", default="")
    
class CompQuestionEntry(models.Model):
    comp_quiz_entry = models.ForeignKey(CompQuizEntry, on_delete=models.CASCADE, default="")
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name = "selected_comp_answer", default="")
    correct_answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name = "correct_comp_answer", default="")
# Create your models here.



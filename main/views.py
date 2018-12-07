from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import JsonResponse
from random import randint, shuffle
from django.db.models import Max
from django.urls import reverse
from datetime import datetime
from .models import *
# End imports #
# =========== #

def generateUniqueClassCode():
    # generate random number
    random_number = randint(0,1000000)
    
    #is the random number unique? must create test
    #the var that holds classes
    classes = Class.objects.filter(code = random_number)
        
    if len(classes) == 1:
        #code is already taken
        generateUniqueClassCode()
    else:
        #code is unique
        return random_number
        
def getNowDateTime():
    return datetime.now()

def logout_user(request):
    logout(request)
    return redirect('main:home')

def home(request):
    #if the request is a POST one...
    if request.method == "POST":
        
        # user is trying to log in...
        if 'login_email' in request.POST:
            # authenticate the user if their login is valid
            email = request.POST.get('login_email')
            password = request.POST.get('password')
            
            #check to see if the username and password are valid
            user = authenticate(username=email, password=password)
        
            if user is not None:
                if user.is_active:
                    #user gets logged in
                    login(request, user)
                    
                    # ignore this for now
                    # if 'next' in request.POST:
                    #     return redirect(request.POST.get('next'))
                    
                   
                    return redirect('main:landing')
            # if user is not authenticated
            else:
                c = {}
                c['error_message'] = 'Invalid login, please try again'
                return render(request, 'main/home.html', c)
        
        #user is trying to register...
        else:
            print(request.POST)
            # then we need to register them with a user account (and whatever else comes with that)
            
            # take in variables
            f_n = request.POST.get('first_name')
            l_n = request.POST.get('last_name')
            e = request.POST.get('email')
            c = request.POST.get('code')
            # u_n = request.POST.get('username')
            r = request.POST.get('role')
            p_w = request.POST.get('pword')
            
            # if the role is instructor,
            if r == 'instructor':
                # then we need to create an instructor acct
                
                # need to verify if the school code is actually legit
                schools = School.objects.filter(code=c)

                print(schools)
                # say the instructor enters the code 1111.....
                # if there is actually a school that has that code,
                # then the schools variable will look like (somthing like, but not exactly) this:
                # <QuerySet [<School: School object (5)>]>
                # this means that the length of schools is 1
                
                # if the school is not valid, school will be something like this:
                # <QuerySet []>
                # this means that then length of schools is 0
                
                if len(schools) == 0:
                    # this means the code is rejected
                    # redirect the user back to the register page
                    # preferrably with a message that says something like:
                    # "Wrong code" or something
                    dictionary = {}
                    
                    dictionary['error_message'] = 'School code does not exist. Please try again.'
                    
                    
                    # use 2 parameters (one is request and the other is the template location )
                    # return render(request, 'main/home.html')
                    
                    # OR, you can use 3 parameters, this is the same as the 
                    # option above except you add another parameter that is a dictionary
                    # this dictionary holds variables that go to the template (IMPORTANT)
                    return render(request, 'main/home.html', dictionary)
                print("username" + e)
                new_user = User.objects.create_user(
                    username=e,
                    password=p_w)
                new_user.first_name = f_n
                new_user.last_name = l_n
                new_user.save()
                
                new_user_profile = UserProfile.objects.create(
                    user = new_user,
                    role = 'Instructor',
                    datetime_joined = getNowDateTime())
            else:
                # this is if you're a student...
                # trying to make a new user acct...
                
                # need to verify if the class code/email are legit
                classes = Class.objects.filter(code=c)
                user_with_e = User.objects.filter(username=e)
                
                is_problem = False
                #class validity test
                if len(classes) == 0:
                    is_problem = True
                    dictionary = {}
                    dictionary['error_message'] = 'Class does not exist. Please try again.'
                
                # email validity test
                if len(user_with_e) != 0:
                    is_problem = True
                    dictionary['error_message'] = 'Email already taken. Please try another one or log in.'
                
                # if there's an issue, then return with error message
                if is_problem:
                    return render(request, 'main/home.html', dictionary)
                
                # user passed the validity test, user acct is created
                new_user = User.objects.create_user(
                    username=e,
                    password=p_w)
                new_user.first_name = f_n
                new_user.last_name = l_n
                new_user.save()
                
                #user profile is created
                new_user_profile = UserProfile.objects.create(
                    user = new_user,
                    role = 'Student',
                    datetime_joined = getNowDateTime())
                
                # register class
                ClassRegistration.objects.create(
                    student = new_user_profile,
                    Class = classes[0])
            
            user_auth = authenticate(
                username=e,
                password=p_w)
            
            login(request, user_auth)
            
            return redirect('main:landing')
            
    # if user is logged in already, just send them to landing
    if request.user.is_authenticated:
        return redirect('main:landing')
        
        
    return render(request, 'main/home.html')


def landing(request):
    u_name = request.user.username
    user_profile = UserProfile.objects.get(user__username=u_name)
    if request.method == "POST":
        dictionary = {}
        dictionary['user_profile'] = user_profile
        if user_profile.role == 'Instructor':
            # we need to gather that instructor's classes
            classes = Class.objects.filter(instructor=user_profile)
            dictionary['classes'] = classes
        else:
            #we need to pull out all of the ClassRegistration objects...
            class_regs = ClassRegistration.objects.filter(student=user_profile)
            dictionary['classRegs'] = class_regs
                
        if user_profile.role == "Student":
            #if user is student
            
            # get POST data
            c = request.POST.get('classCode')
            
            # test to see if class code is valid
            classes = Class.objects.filter(code=c)
            
            if len(classes) == 0:
                # redirect them to same page with error message
                dictionary['error_message'] = 'Class code does not exist. Please try again.'
                return render(request, 'main/landing.html', dictionary)
                
            # if they pass the test, then create the class registration
            ClassRegistration.objects.create(
                student = user_profile,
                Class = classes[0])
        else:
            # if user is instructor
            
            # get POST data
            n = request.POST.get('name')
            d = request.POST.get('description')
            
            # get instructor user profile and assign to variable: instructor_user_profile
            instructor_user_profile = UserProfile.objects.get(
                user = request.user)
                
            # generate a class based off of the POST data and instructor_user_profile
            Class.objects.create(
                instructor = instructor_user_profile,
                name = n,
                description = d,
                code = generateUniqueClassCode()
                # code = need to create a function that generates a unique class code
                )
        return redirect('main:landing')
    else:
        
        dictionary = {}
        dictionary['user_profile'] = user_profile
        
        # If you are an instructor
        if user_profile.role == 'Instructor':
            # we need to gather that instructor's classes
            classes = Class.objects.filter(instructor=user_profile)
            dictionary['classes'] = classes
            dictionary['comp_quiz_invites'] = CompQuiz.objects.filter(
                invited_instructor=user_profile,
                approved = False,
                declined = False)
            
        else:
            #we need to pull out all of the ClassRegistration objects...
            class_regs = ClassRegistration.objects.filter(student=user_profile)
            dictionary['classRegs'] = class_regs
        
        return render(request, 'main/landing.html', dictionary)

def add_class(request):#do we need this?
    return render(request, 'main/add_class.html')
    
def my_profile(request):
    u_name = request.user.username
    user_profile = UserProfile.objects.get(user__username=u_name)
    dictionary = {}
    dictionary['user_profile'] = user_profile
    return render(request, 'main/my_profile.html', dictionary)

def class_detail(request, code):
    u_name = request.user.username
    user_profile = UserProfile.objects.get(user__username=u_name)
    certain_class = Class.objects.get(code=code)
    quizzes = Quiz.objects.filter(Class=certain_class).order_by('index')
    dictionary = {}
    # if user_profile.role == "Instructor":
    #     dictionary['comp_quiz_invites'] = CompQuiz.objects.filter(invited_instructor=certain_class.instructor)
    dictionary['certain_class'] = certain_class
    dictionary['quizzes'] = quizzes
    dictionary['user_profile'] = user_profile
    return render(request, 'main/class_detail.html', dictionary)
    
def quiz(request, pk):
    certain_quiz = Quiz.objects.get(id=pk)
    user = request.user
    user_profile = UserProfile.objects.get(user__username=user)
    if request.method == "POST":
        certain_quiz_entry = QuizEntry.objects.get(
            certain_quiz=certain_quiz,
            student = user_profile,
            datetime_completed = None)
        # for when a student submits a quiz with answers
        
        print(request.POST)
        
        #total number of questions
        num_qs = 0
        
        # total number of correct questions
        num_cqs = 0
        print(request.POST)
        for answer in request.POST:
            s = str(answer)
            if s == "csrfmiddlewaretoken":
                pass
            else:
                num_qs += 1
                
                # question index number
                q_num = int(s)
                a_id = request.POST.get(answer)
                certain_answer = Answer.objects.get(pk=a_id)
                
                # store question entry
                certain_question_entry = QuestionEntry.objects.create(
                    quiz_entry = certain_quiz_entry,
                    selected_answer = certain_answer,
                    correct_answer = Answer.objects.get(
                        question= certain_answer.question,
                        correct = True)
                    )
                    
                if certain_question_entry.selected_answer.correct:
                    num_cqs += 1
        # dfwsfwfehuif
        certain_quiz_entry.final_grade = round(num_cqs / num_qs, 2)*100
        certain_quiz_entry.datetime_completed = getNowDateTime()
        certain_quiz_entry.save()
        
        
        
        
        #round(num_cqs / num_qs, 2)
        # GOAL!: return the results!
        # grade!
        # dictionary = {}
        # dictionary['certain_quiz_entry'] = certain_quiz_entry
        # dictionary['grade'] = num_cqs / num_qs
        
        # # what  are the correct vs not correct answers!
        # dictionary['question_entries'] = QuestionEntry.objects.filter(
        #     quiz_entry = certain_quiz_entry)
            
        # return render(request,'main/quiz_results.html', dictionary)
        
        # we have to send the user to a page showing them the results for the quiz
        # they took
        
        # we need to get the id/pk of the quiz entry and send it to the quiz_results link
        # ex: www.quizquest.com/quiz_results/*QUIZ ENTRY ID/PK GOES HERE*
        # return redirect('main:quiz_results' pk=??)
        
        return redirect(reverse('main:quiz_results', kwargs={ 'pk': certain_quiz_entry.id }))
    else:
        
        
        
        # either create a new quiz entry OR resume from one already created and in progress?
        
        # gets all quiz entries for certain_quiz and certain user_profile that are not complete
        quiz_entries = QuizEntry.objects.filter(
            datetime_completed=None,
            student=user_profile,
            certain_quiz=certain_quiz)
        
        if len(quiz_entries) == 0:
            #create a new quiz entry
            certain_quiz_entry = QuizEntry.objects.create(
                student = user_profile,
                datetime_started = getNowDateTime(),
                certain_quiz = certain_quiz)
        elif len(quiz_entries) == 1:
            # use quizentry that was found
            certain_quiz_entry = quiz_entries[0]
        else:
            pass
            
        
        questions = Question.objects.filter(quiz=certain_quiz)
    
        # # has the user attempted this quiz already?
        # quiz_entries = QuizEntry.objects.filter(certain_quiz=certain_quiz)
        # if len(quiz_entries) ==  0:
        #     certain_quiz_entry = QuizEntry.objects.create(
        #         certain_quiz = certain_quiz)
        # elif len(quiz_entries) == 1:
        #     certain_quiz_entry = quiz_entries[0]
        # else:
        #     pass
        
        questions_data = []
        for question in questions:
            answers = Answer.objects.filter(question=question)
            questions_data += [[question, answers]]

        dictionary = {}
        dictionary['certain_quiz'] = certain_quiz
        dictionary['user_profile'] = user_profile
        dictionary['questions_data'] = questions_data
        dictionary['certain_quiz_entry'] = certain_quiz_entry
        return render(request,'main/quiz.html', dictionary)

def quiz_results(request, pk):
    certain_user = request.user
    
    certain_user_profile = UserProfile.objects.get(user=certain_user)
    
    certain_quiz_entry = QuizEntry.objects.get(id=pk)
    
    all_certain_quiz_entries = QuizEntry.objects.filter(
        certain_quiz=certain_quiz_entry.certain_quiz,
        student = certain_user_profile)
    
    dictionary = {}
    dictionary['certain_quiz_entry'] = certain_quiz_entry
    dictionary['grade'] = certain_quiz_entry.final_grade
    dictionary['question_entries'] = QuestionEntry.objects.filter(
        quiz_entry = certain_quiz_entry)
    dictionary['attempt_num'] = len(all_certain_quiz_entries)
    
    return render(request, 'main/quiz_results.html', dictionary)


def create_quiz(request):
    dictionary = {}
    if 'question_1' in request.POST:
        u_name = request.user.username
        user_profile = UserProfile.objects.get(user__username=u_name)
        dictionary['user_profile'] = user_profile
        
        name = request.POST.get('quiz_name')
        quiz_index = request.POST.get('index')
        n = int(request.POST.get('num_questions'))
        
        code = int(request.POST.get('code'))
        certain_class = Class.objects.get(code=code)
        
        dictionary['certain_class'] = certain_class
        
        # get all quizzes for this class
        certain_class_quizzes = Quiz.objects.filter(Class=certain_class).order_by('index')
        print(certain_class_quizzes)
        
        index = 1
        num_quizzes = len(certain_class_quizzes)
        if num_quizzes != 0:
            index = num_quizzes + 1
        
        
        
        # is_competitive = request.POST.get('opp_ins_class_code')    
        is_competitive = request.POST.get('compete')
        opp_ins_class_code = 0
        print("compete: {}".format(is_competitive))
        if is_competitive == "yes":
            # try:
            opp_ins_class_code = int(request.POST.get('opp_ins_class_code'))
            print(123)
            try:
                opp_class = Class.objects.get(code=opp_ins_class_code)
            except:
                l = []
                for i in range(0,n):
                    l += [i+1]
                dictionary = {}
                dictionary['class'] = certain_class
                dictionary['n'] = n
                dictionary['l'] = l 
                dictionary['error_message'] = "Class code doesn't exist. Try another one." 
                # class, n, l
                return render(request, 'main/create_quiz.html', dictionary)
            
            print(321)
            
            
            # except:
            #     pass
        
        fresh_quiz = Quiz.objects.create(
            name = name,
            index = index,
            Class = certain_class,
            published = True
            )
        
        if is_competitive == "yes":
            opp_instructor = Class.objects.get(
                code=opp_ins_class_code).instructor
            CompQuiz.objects.create(
                quiz = fresh_quiz,
                Class = opp_class,
                approved = False,
                declined= False,
                invited_instructor = opp_instructor
            )
            print(123321)

            
        
        # taking in answers...
        # from each question, we need:
        # for data in request.POST:
        #     s = str(data)
        #     if s == "csrfmiddlewaretoken":
        #         pass
        #     else:
        
        
        count = 0
        no_problem = True
        while(no_problem):
            count += 1
            print("TRYING question_{}".format(count))
            print("HMM Q: " + str(request.POST.get('question_{}'.format(count))))
            x = request.POST.get('question_{}'.format(count))
            if x == "":
                no_problem = False
                print("PROB")
            elif x is None:
                no_problem = False
                print("PROB")
            else:
                print(x)
        count -= 1
        
        l=[] 
        for i in range(0,count):
            j = i + 1
            q = request.POST.get('question_{}'.format(j))
            # q = request.POST['question_{}'.format()]
            print("QUESTION " + str(q) + "{}".format(q))
            print(1)
            c_a = request.POST.get('correct_answer_{}'.format(j))
            print(2)
            o_a1 = request.POST.get('other1_answer_{}'.format(j))
            print(3)
            o_a2 = request.POST.get('other2_answer_{}'.format(j))
            print(4)
            o_a3 = request.POST.get('other3_answer_{}'.format(j))
            print(5)
            o_a4 = request.POST.get('other4_answer_{}'.format(j))
            print(6)
            
            # l += [q]
            # l += [c_a]
            l += [o_a1]
            try:
                if o_a2 != '':
                    l += [o_a2]
                if o_a3 != '':
                    l += [o_a3]
                if o_a4 != '':
                    l += [o_a4]
            except:
                pass
            print(7)
            print("LIST OF ANSWERS: " + str(l))
            
            
            certain_question = Question.objects.create(
                index = j,
                quiz = fresh_quiz,
                question_text = q
            )
            print(8)
            
            Answer.objects.create(
                question = certain_question,
                answer = c_a,
                correct = True
                )
            print(9)
            
            print("other answers: " + str(l))
            for answer in l:
                Answer.objects.create(
                    question = certain_question,
                    answer = answer,
                    correct = False
                )
            print(10)
            l=[]
        
        
        # l = []
        # while(is_problem == False):
        #     count += 1
        #     try:
        #         print(0)
        #         q = request.POST.get('question_{}'.format(count))
        #         print("QUESTION " + str(q))
        #         print(1)
        #         c_a = request.POST.get('correct_answer_{}'.format(count))
        #         print(2)
        #         o_a1 = request.POST.get('other1_answer_{}'.format(count))
        #         print(3)
        #         o_a2 = request.POST.get('other2_answer_{}'.format(count))
        #         print(4)
        #         o_a3 = request.POST.get('other3_answer_{}'.format(count))
        #         print(5)
        #         o_a4 = request.POST.get('other4_answer_{}'.format(count))
        #         print(6)
    
                
        #         # l += [q]
        #         # l += [c_a]
        #         l += [o_a1]
        #         try:
        #             if o_a2 != '':
        #                 l += [o_a2]
        #             if o_a3 != '':
        #                 l += [o_a3]
        #             if o_a4 != '':
        #                 l += [o_a4]
        #         except:
        #             pass
        #         print(7)
        #         print("LIST OF ANSWERS: " + str(l))
                
                
        #         certain_question = Question.objects.create(
        #             index = count,
        #             quiz = fresh_quiz,
        #             question_text = q
        #         )
        #         print(8)
                
        #         Answer.objects.create(
        #             question = certain_question,
        #             answer = c_a,
        #             correct = True
        #             )
        #         print(9)
                
        #         for answer in l:
        #             Answer.objects.create(
        #                 question = certain_question,
        #                 answer = answer,
        #                 correct = False
        #             )
        #         print(10)
        #     except:
        #         is_problem = True
                
            # print("YES: " + str(count))
        print(request.POST)
        print("{} Qs".format(count))
            
        return redirect(reverse('main:class_detail', kwargs={ 'code': fresh_quiz.Class.code }))
        raise Exception
                
                
                
                
                
                
        for i in range(0,num_questions):
            num = i + 1
                    
            for i in range(0,num_questions):
                num = i + 1
                q = request.POST.get('question_' + num)
                c_a = request.POST.get('correct_answer' + num)
                o_a1 = request.POST.get('other1_answer' + num)
                try:
                    o_a2 = request.POST.get('other2_answer' + num)
                    o_a3 = request.POST.get('other3_answer' + num)
                    o_a4 = request.POST.get('other4_answer' + num)
                except:
                    pass
                Question.objects.create(
                        quiz = fresh_quiz,
                        Class = Class.objects.get(code=is_competitive)
                )
            # question_{{number_question}}
                Answer.object.create(
                    question = q,
                    answer = c_a,
                    correct = True
                    )
                Answer.object.create(
                    question = q,
                    answer = o_a1,
                    correct = False
                    )
                try:
                    Answer.object.create(
                    question = q,
                    answer = o_a2,
                    correct = False
                    )
                    Answer.object.create(
                    question = q,
                    answer = o_a3,
                    correct = False
                    )
                    Answer.object.create(
                    question = q,
                    answer = o_a4,
                    correct = False
                    )
                except:
                    pass
            
            
            
            
        
    elif 'num_questions' in request.POST:
        # goal: is to give the template something like this: [1,2,3....]
        # what is the number?
        # print(request.POST.get('numberOfQuestions'))
        n = int(request.POST.get('num_questions'))
        code = request.POST.get('code')
        
        # create list going n times
        l = []
        for i in range(0,n+1):
            if i != 0:
                l += [i]
        
        dictionary["n"]= n
        dictionary["l"] = l
        dictionary["class"]= code
        return render(request, 'main/create_quiz.html', dictionary)
    else:
        pass
        
        
        
        
        

        
        
def profile_detail(request, pk):
    pass
    
def leaderboard(request, pk):
    certain_quiz = Quiz.objects.get(id=pk)
    
    #get all entries for this quiz
    all_certain_quiz_entries = QuizEntry.objects.filter(
        certain_quiz=certain_quiz)
    
    # get all students in a the class that the quiz comes from
    students = ClassRegistration.objects.filter(Class=certain_quiz.Class)
    
    # Go through the students and pull their best attempt. 
    # Then, add them to a dictionary. 
    # Then, convert the dictionary into an ordered list of subists with places put in.
    d = {}
    l = []
    place = 1
    total = 0
    num_students=0
    for student in students:
        best_student_certain_quiz_grade = all_certain_quiz_entries.filter(student=student.student).aggregate(Max('final_grade'))['final_grade__max']
        
        
        
        if best_student_certain_quiz_grade != None:
            try:
                total = total + best_student_certain_quiz_grade #need to collect all the best scores from the students in class
                len(d[best_student_certain_quiz_grade])
                d[best_student_certain_quiz_grade] += [student.student.full_name]
            except KeyError:
                d[best_student_certain_quiz_grade] = [student.student.full_name]
    for i,j in sorted(d.items(),reverse=True):
        l += [[place,j,i]]
        place += len(j)
            
    dictionary = {}
    dictionary['list'] = l
    dictionary['certain_quiz'] = certain_quiz
    return render(request, 'main/leaderboard.html', dictionary)

def accept_comp_quiz(request, pk):
    certain_comp_quiz = CompQuiz.objects.get(id=pk)
    certain_comp_quiz.approved = True
    return redirect(reverse('main:landing'))
    
def decline_comp_quiz(request, pk):
    certain_comp_quiz = CompQuiz.objects.get(id=pk)
    certain_comp_quiz.declined = True
    return redirect(reverse('main:landing'))
    
    
# Start APIS
def verify_login_API(request, username, password):
    user = authenticate(username=username, password=password)
    if user is None:
        is_verified = False
    else:
        is_verified = True
    return JsonResponse({'Verified': is_verified})
    
def get_user_info_API(request, username):
    response = {}
    try:
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        response['exists'] = True
        response['f_name'] = user_profile.user.first_name
        response['l_name'] = user_profile.user.last_name
    except:
        response['exists'] = False
        response['f_name'] = None
        response['l_name'] = None
    return JsonResponse(response)
    
def get_class_quiz_ids_API(request, class_code):
    response = {}
    try:
        certain_class = Class.objects.get(code=int(class_code))
        certain_quizzes = Quiz.objects.filter(Class=certain_class)
        l = []
        for quiz in certain_quizzes:
            l += [quiz.id]
        response['exists'] = True
        response['quiz_ids'] = l
    except:
        response['exists'] = False
        response['quiz_ids'] = None
    #all the relevant quizzes
    return JsonResponse(response)
    
def get_quiz_qas_API(request, quiz_id):
    response = {}
    l = []
    try:
        # [[question, answerslist],[],[]]
        
        
        certain_quiz = Quiz.objects.get(pk=quiz_id)
        
        # questions and answers
        Question.objects.filter()
        Answer.objects.filter()
        
        
        
        certain_class = Class.objects.get(code=int(class_code))
        certain_quizzes = Quiz.objects.filter(Class=certain_class)
        l = []
        for quiz in certain_quizzes:
            l += [quiz.id]
        response['exists'] = True
        response['quiz_ids'] = l
    except:
        response['exists'] = False
        response['quiz_ids'] = None
    #all the relevant quizzes
    return JsonResponse(response)

    
# class ClassesForStudentSerializerList(generics.ListAPIView):
#     serializer_class = ClassesForStudentSerializer
    
#     def get_queryset(self):
#         user = self.request.user
#         return Class.objects.filter()
        
        
# class ClassesForStudentSerializerList(APIView):
    
#     def get(self, request):
#         un = self.kwargs['username']
#         u = User.objects.get(username=un)
#         s = UserProfile.objects.get(user=u)
#         crs = ClassRegistration.objects.filter(student=s)
#         collected_classes = Class.objects.none()
#         for cr in crs:
#             pass
#             # get class
#             c = Class.objects.get(pk=cr.Class.id)
#             collected_classes = (collected_classes | c)
#             # add class to existing queryset
        
        
#         #this should be all classes for a student
#         # objects = Class.objects.all()
#         serializer = UserSerializer(collected_classes, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
        
#         serializer = UserSerializer(data=request.data, many=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        
# class ClassesForStudentSerializerList(generics.ListAPIView):
#     serializer_class = ClassesForStudentSerializer

#     def get_queryset(self):
#         up_id = self.kwargs['up_id']
#         u = User.objects.get(pk=up_id)
#         s = UserProfile.objects.get(user=u)
#         crs = ClassRegistration.objects.filter(student=s)
#         collected_classes = Class.objects.none()
#         for cr in crs:
#             pass
#             # get class
#             c = Class.objects.get(pk=cr.Class.id)
#             collected_classes = (collected_classes | c)
#             # add class to existing queryset
    
#         # return Class.objects.filter(purchaser__username=username)
#         return collected_classes
    
# # Create your views here.
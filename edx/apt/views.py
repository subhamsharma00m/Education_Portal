from django.shortcuts import render, redirect
from apt.models import *
from apt.forms import *
from django.contrib.auth import authenticate, login, logout

from django.contrib.sessions.models import *
from django.contrib.auth.models import User, _user_get_all_permissions
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.urls import reverse
from django.conf import settings

import datetime

from django.contrib import messages
from django.template import RequestContext

from .forms import *
from .models import *



def Login(request):
    model = User()
    username = model.username
    if request.method == "GET":
        if 'action' in request.GET:
            action = request.GET.get('action')
            if action == 'logout':
                if 'username' in request.session:
                    request.session.flush()
                    logout(request)
                    return redirect('login')
        elif 'username' in request.session:
            model.username = request.session['username']
            print(request.session.set_expiry(300))  # session lifetime in seconds(from now)
            print(request.session.get_expiry_date())  # datetime.datetime object which repre

    elif request.method == "POST":
        form = LogInForms(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST.get('username'), password=request.POST.get('Password'))
            if user:
                request.session['username'] = model.username
                login(request, user)
                if not user.is_staff:
                    return redirect('logsuccess')
                else:
                    return redirect('written_exam')
            else:
                messages.error(request, 'username or password not correct')
                return redirect('login')
        else:
            return redirect('login')
    return render(request, 'login.html', {'form': LogInForms(), 'Email': model.username})





#def log_out(request):
 #   logout(request)
 #   return render(request,'index.html',{})

def signup(request):
    form = SignupForms()
    model = SignupModel()
    if request.method == "POST":
        form = SignupForms(request.POST)
        if form.is_valid():
            form.name = request.POST.get('name')   #
            form.Email = request.POST.get('Email')    #
            form.Password = request.POST.get('Password')  #
            form.username = request.POST.get('username')  #

            model.save()     #form change to model
            User.objects.create_user(username=form.username, password=form.Password)  #
            return redirect("logsuccess")

        else:
            return HttpResponseRedirect("contact/")
    else:
        return render(request,'signup.html',{'form':form})


#def exam(request):
 #   templates='exam.html'
  #  context={}
    #if request.method == 'GET':
   #     return render(request,templates,context)

def log_out(request):
    logout(request)
    return render(request, 'login.html', {})

def about(request):
    templates='about.html'
    context={}
    if request.method == 'GET':
        return render(request,templates,context)

def contact(request):
    templates='contact.html'
    context={}
    if request.method == 'GET':
        return render(request,templates,context)

def home(request):
    templates='index.html'
    context={}
    if request.method=='GET':
        return render(request,templates,context)



#######
# Create your views here.

tot=[]
uname=''
topicname=''
subjectname=''
uid = 0
flag = 0
correct = 0
incorrect = 0
unanswered = 0
s = Subject()
t = Topics()
q = Question()


















@login_required(login_url='/login/')
def exam(request):
    test = TestGiven.objects.filter(username=request.user).order_by('-exam_date','-exam_time')
    test_id = request.GET.get('id')
    t_date = 'Click on Overview to see the piechart'
    if test_id:
        temp = 1;
        t_time = ''
        t_subject = '';     t_topic = ''
        p_correct = 0;      p_incorrect = 0;    p_unattempted = 0
        for i in test:
            if temp == int(test_id):
                t_date = i.exam_date
                t_time = i.exam_time
                t_subject = i.subject_name
                t_topic = i.topic_name
                p_correct = i.total_correct
                p_incorrect = i.total_incorrect
                p_unattempted = i.total_question - i.total_correct - i.total_incorrect
                #print(i.pk, '-', i.total_question, '-', p_correct, '-', p_incorrect, '-',p_unattempted)
                break
            temp += 1
        return render(request, 'widgets.html',
                      {'s': s, 't': t, 'name': uname, 'test': test,
                       'test_id':test_id,'t_date':t_date,'t_time':t_time,
                       't_subject':t_subject,'t_topic':t_topic,'p_correct':p_correct,
                       'p_incorrect':p_incorrect,'p_unattempted':p_unattempted
                       })
    return render(request,'widgets.html', {'s': s, 't': t,'name':uname,'test':test,'t_date':t_date})



@login_required(login_url='/login/')
def logsuccess(request):
    if request.method=='GET':
        global s
        global t
        q_count = 0;    q_percent = 0.0
        r_count = 0;    r_percent = 0.0
        l_count = 0;    l_percent = 0.0
        v_count = 0;    v_percent = 0.0
        s = Subject.objects.all()
        t = Topics.objects.all()
        context = {'s': s, 't': t, 'name': uname,
                   'q_count': q_count, 'l_count': l_count, 'r_count': r_count, 'v_count': v_count,
                   'q_percent': q_percent, 'l_percent': l_percent, 'r_percent': r_percent, 'v_percent': v_percent
                   }
        test = TestGiven.objects.filter(username=request.user)
        if test:
            #print(test)
            sub_count = test.order_by().values('subject_name').distinct()
            q_count = test.filter(subject_name='Quantitative').order_by().values('topic_name').distinct().count()
            q_percent = round((q_count/18)*100,2)
            l_count = test.filter(subject_name='Logical').order_by().values('topic_name').distinct().count()
            l_percent = round((l_count/12)*100,2)
            r_count = test.filter(subject_name='Reasoning').order_by().values('topic_name').distinct().count()
            r_percent = round((r_count/4)*100,2)
            v_count = test.filter(subject_name='Verbal').order_by().values('topic_name').distinct().count()
            v_percent = round((v_count/4)*100,2)
            #print(sub_count,q_count,l_count,r_count,v_count)
            context = {'s': s, 't': t, 'name': uname,
                       'q_count': q_count, 'l_count': l_count, 'r_count': r_count, 'v_count': v_count,
                       'q_percent': q_percent, 'l_percent': l_percent, 'r_percent': r_percent, 'v_percent': v_percent
                       }
        else:
            print('User Does not exist...')
        #print(uid,uname)
        data = Profile.objects.filter(user=request.user)
        for inf in data:
            xct = inf.total_fee
            dpt = inf.deposite
        ak = xct
        dk = dpt
        remain = ak - dk
        if remain!=0:
            df = "Your Fee is Due"
        else:
            df = "Your Due Fee id 0.0"


        return render(request, 'dashboard_l.html',{'data':data, 'remain':remain, 'df':df})
    else:
        global unanswered
        global correct
        global incorrect
        unanswered =0
        correct =0
        incorrect =0
        for i in range(1, c+1):
            s="q"+str(i)
            ua = request.POST.get(s)
            if ua==None:
                unanswered+=1
                print('You did not answer this question!!!')
            elif ua == a[i-1]:
                correct+=1
                print(ua,' is correct answer')
            else:
                incorrect+=1
                print(ua, ' is incorrect answer')

    return render(request, 'logsuccess.html',{})

@login_required(login_url='/login/')
def startexam(request):
    global topicname
    global subjectname
    global q
    global c
    global a
    global unanswered
    global correct
    global incorrect
    if request.method=='GET':
        tid = request.GET.get('id')
        topic = Topics.objects.get(pk=tid)
        topicname = topic.topicname
        sid = topic.subject_id
        subjectname = Subject.objects.get(id=sid)
        q = Question.objects.filter(topics_id=tid)
        c = Question.objects.filter(topics_id=tid).count()
        a = Question.objects.filter(topics_id=tid).values_list('answer')
        a = [i[0] for i in a]
        return render(request,'exam.html', {'s': s, 't': t,'name':uname,'q':q,'topicname':topicname,'subjectname':subjectname})
    else:
        unanswered =0
        correct =0
        incorrect =0
        for i in range(1, c+1):
            option="q"+str(i)
            user_answer = request.POST.get(option)
            if user_answer==None:
                unanswered+=1
                print('You did not answer this question!!!')
            elif user_answer == a[i-1]:
                correct+=1
                print(user_answer,' is correct answer')
            else:
                incorrect+=1
                print(user_answer, ' is incorrect answer')
        test1 = TestGiven()
        test1.exam_date = datetime.datetime.now()
        test1.exam_time = datetime.datetime.now().time().strftime('%H:%M:%S')
        test1.subject_name = subjectname
        test1.topic_name = topicname
        test1.total_question = c
        test1.total_attempted = c-unanswered
        test1.total_correct = correct
        test1.total_incorrect = incorrect
        test1.marks_obtained = correct
        test1.percent = round((correct/c)*100,2)
        test1.username = request.user
        test1.save()
        messages.info(request,'Test successfully submitted')
        return redirect(exam)
    return redirect(logsuccess)



@staff_member_required(login_url='/login')
def Assignmentview(request):

    cl = Profile.objects.filter(user=request.user)
    for clss in cl:
        cls = clss.Class

    if request.method=="GET":
        form = Assignmentform()
    else:
        form = Assignmentform(request.POST, request.FILES)
        if form.is_valid():
            ak = Assignments()
            ak.Class = form.cleaned_data['Class']
            ak.subject = form.cleaned_data['subject']
            ak.topic = form.cleaned_data['topic']
            ak.file = form.cleaned_data['file']
            ak.save()
            print("successful")

    return render(request, 'assignment.html', {'form':form, 'cls':cls})



#@staff_member_required(login_url='admin:login/')
#def info1(request):
#    Assign = Assignment.objects.all()
#    return render(request, "info1.html", {'Assign':Assign})


@staff_member_required(login_url='/login')
def written_exam(request):
    ex = Profile.objects.filter(user=request.user)
    for a in ex:
        x = a.Class


        if x == 'Class 12 Art':
            ex1 = Profile.objects.filter(Class="Class 10", user__is_staff=False)
            for b in ex1:
                y = b.user
                print(y)
                #return render(request, 'update_result.html', {'ex1': ex1})

            if request.method == "GET":
                form=ExamNumberForm()
            else:
                form=ExamNumberForm(request.POST)
                if form.is_valid():
                    k = ExamNumberModel()
                    k.Exam_Name = form.cleaned_data['Exam_Name']
                    k.username = form.cleaned_data['username']
                    k.Subject1 = form.cleaned_data['Subject1']
                    k.Subject2 = form.cleaned_data['Subject2']
                    k.Subject3 = form.cleaned_data['Subject3']
                    k.Subject4 = form.cleaned_data['Subject4']
                    k.Subject5 = form.cleaned_data['Subject5']
                    k.Subject6 = form.cleaned_data['Subject6']
                    k.MaxMarks = form.cleaned_data['MaxMarks']

                    k.save()
                    print("successful")
            return render(request, 'update_result.html',{'ex1':ex1}, {'form':form})


        if x == 'Class 12 Co.':
            ex1 = Profile.objects.filter(Class="Class 10", user__is_staff=False)
            for b in ex1:
                y = b.user
                print(y)
                #return render(request, 'update_result.html', {'ex1': ex1})

            if request.method == "GET":
                form=ExamNumberForm()
            else:
                form=ExamNumberForm(request.POST)
                if form.is_valid():
                    k = ExamNumberModel()
                    k.Exam_Name = form.cleaned_data['Exam_Name']
                    k.username = form.cleaned_data['username']
                    k.Subject1 = form.cleaned_data['Subject1']
                    k.Subject2 = form.cleaned_data['Subject2']
                    k.Subject3 = form.cleaned_data['Subject3']
                    k.Subject4 = form.cleaned_data['Subject4']
                    k.Subject5 = form.cleaned_data['Subject5']
                    k.Subject6 = form.cleaned_data['Subject6']
                    k.MaxMarks = form.cleaned_data['MaxMarks']

                    k.save()
                    print("successful")
            return render(request, 'update_result.html',{'ex1':ex1}, {'form':form})


        if x == 'Class 12 Sc.':
            ex1 = Profile.objects.filter(Class="Class 10", user__is_staff=False)
            for b in ex1:
                y = b.user
                print(y)
                #return render(request, 'update_result.html', {'ex1': ex1})

            if request.method == "GET":
                form=ExamNumberForm()
            else:
                form=ExamNumberForm(request.POST)
                if form.is_valid():
                    k = ExamNumberModel()
                    k.Exam_Name = form.cleaned_data['Exam_Name']
                    k.username = form.cleaned_data['username']
                    k.Subject1 = form.cleaned_data['Subject1']
                    k.Subject2 = form.cleaned_data['Subject2']
                    k.Subject3 = form.cleaned_data['Subject3']
                    k.Subject4 = form.cleaned_data['Subject4']
                    k.Subject5 = form.cleaned_data['Subject5']
                    k.Subject6 = form.cleaned_data['Subject6']
                    k.MaxMarks = form.cleaned_data['MaxMarks']

                    k.save()
                    print("successful")
            return render(request, 'update_result.html',{'ex1':ex1}, {'form':form})



        if x == 'Class 11 Art':
            ex1 = Profile.objects.filter(Class="Class 10", user__is_staff=False)
            for b in ex1:
                y = b.user
                print(y)
                #return render(request, 'update_result.html', {'ex1': ex1})

            if request.method == "GET":
                form=ExamNumberForm()
            else:
                form=ExamNumberForm(request.POST)
                if form.is_valid():
                    k = ExamNumberModel()
                    k.Exam_Name = form.cleaned_data['Exam_Name']
                    k.username = form.cleaned_data['username']
                    k.Subject1 = form.cleaned_data['Subject1']
                    k.Subject2 = form.cleaned_data['Subject2']
                    k.Subject3 = form.cleaned_data['Subject3']
                    k.Subject4 = form.cleaned_data['Subject4']
                    k.Subject5 = form.cleaned_data['Subject5']
                    k.Subject6 = form.cleaned_data['Subject6']
                    k.MaxMarks = form.cleaned_data['MaxMarks']

                    k.save()
                    print("successful")
            return render(request, 'update_result.html',{'ex1':ex1}, {'form':form})




        if x == 'Class 11 Co.':
            ex1 = Profile.objects.filter(Class="Class 10", user__is_staff=False)
            for b in ex1:
                y = b.user
                print(y)
                #return render(request, 'update_result.html', {'ex1': ex1})

            if request.method == "GET":
                form=ExamNumberForm()
            else:
                form=ExamNumberForm(request.POST)
                if form.is_valid():
                    k = ExamNumberModel()
                    k.Exam_Name = form.cleaned_data['Exam_Name']
                    k.username = form.cleaned_data['username']
                    k.Subject1 = form.cleaned_data['Subject1']
                    k.Subject2 = form.cleaned_data['Subject2']
                    k.Subject3 = form.cleaned_data['Subject3']
                    k.Subject4 = form.cleaned_data['Subject4']
                    k.Subject5 = form.cleaned_data['Subject5']
                    k.Subject6 = form.cleaned_data['Subject6']
                    k.MaxMarks = form.cleaned_data['MaxMarks']

                    k.save()
                    print("successful")
            return render(request, 'update_result.html',{'ex1':ex1}, {'form':form})



        if x == 'Class 11 Sc':
            ex1 = Profile.objects.filter(Class="Class 10", user__is_staff=False)
            for b in ex1:
                y = b.user
                print(y)
                #return render(request, 'update_result.html', {'ex1': ex1})

            if request.method == "GET":
                form=ExamNumberForm()
            else:
                form=ExamNumberForm(request.POST)
                if form.is_valid():
                    k = ExamNumberModel()
                    k.Exam_Name = form.cleaned_data['Exam_Name']
                    k.username = form.cleaned_data['username']
                    k.Subject1 = form.cleaned_data['Subject1']
                    k.Subject2 = form.cleaned_data['Subject2']
                    k.Subject3 = form.cleaned_data['Subject3']
                    k.Subject4 = form.cleaned_data['Subject4']
                    k.Subject5 = form.cleaned_data['Subject5']
                    k.Subject6 = form.cleaned_data['Subject6']
                    k.MaxMarks = form.cleaned_data['MaxMarks']

                    k.save()
                    print("successful")
            return render(request, 'update_result.html',{'ex1':ex1}, {'form':form})


        if x == 'Class 10':
            ex1 = Profile.objects.filter(Class="Class 10", user__is_staff=False)
            for b in ex1:
                y = b.user
                print(y)
                #return render(request, 'update_result.html', {'ex1': ex1})

            if request.method == "GET":
                form=ExamNumberForm()
            else:
                form=ExamNumberForm(request.POST)
                if form.is_valid():
                    k = ExamNumberModel()
                    k.Exam_Name = form.cleaned_data['Exam_Name']
                    k.username = form.cleaned_data['username']
                    k.Subject1 = form.cleaned_data['Subject1']
                    k.Subject2 = form.cleaned_data['Subject2']
                    k.Subject3 = form.cleaned_data['Subject3']
                    k.Subject4 = form.cleaned_data['Subject4']
                    k.Subject5 = form.cleaned_data['Subject5']
                    k.Subject6 = form.cleaned_data['Subject6']
                    k.MaxMarks = form.cleaned_data['MaxMarks']

                    k.save()
                    print("successful")
            return render(request, 'update_result.html',{'ex1':ex1}, {'form':form})



        elif x == 'Class 8':
            ex1 = Profile.objects.filter(Class="Class 10", user__is_staff=False)
            for b in ex1:
                y = b.user
                print(y)


            if request.method == "GET":
                form=ExamNumberForm()
            else:
                form=ExamNumberForm(request.POST)
                if form.is_valid():
                    k = ExamNumberModel()
                    k.Exam_Name = form.cleaned_data['Exam_Name']
                    k.username = form.cleaned_data['username']
                    k.Subject1 = form.cleaned_data['Subject1']
                    k.Subject2 = form.cleaned_data['Subject2']
                    k.Subject3 = form.cleaned_data['Subject3']
                    k.Subject4 = form.cleaned_data['Subject4']
                    k.Subject5 = form.cleaned_data['Subject5']
                    k.Subject6 = form.cleaned_data['Subject6']
                    k.MaxMarks = form.cleaned_data['MaxMarks']

                    k.save()
                    print("successful")
            return render(request, 'update_result.html',{'ex1':ex1}, {'form':form})


        elif x == 'Class 7':
            ex1 = Profile.objects.filter(Class="Class 10", user__is_staff=False)
            for b in ex1:
                y = b.user
                print(y)


            if request.method == "GET":
                form=ExamNumberForm()
            else:
                form=ExamNumberForm(request.POST)
                if form.is_valid():
                    k = ExamNumberModel()
                    k.Exam_Name = form.cleaned_data['Exam_Name']
                    k.username = form.cleaned_data['username']
                    k.Subject1 = form.cleaned_data['Subject1']
                    k.Subject2 = form.cleaned_data['Subject2']
                    k.Subject3 = form.cleaned_data['Subject3']
                    k.Subject4 = form.cleaned_data['Subject4']
                    k.Subject5 = form.cleaned_data['Subject5']
                    k.Subject6 = form.cleaned_data['Subject6']
                    k.MaxMarks = form.cleaned_data['MaxMarks']

                    k.save()
                    print("successful")
            return render(request, 'update_result.html',{'ex1':ex1}, {'form':form})


        elif x == 'Class 6':
            ex1 = Profile.objects.filter(Class="Class 10", user__is_staff=False)
            for b in ex1:
                y = b.user
                print(y)


            if request.method == "GET":
                form=ExamNumberForm()
            else:
                form=ExamNumberForm(request.POST)
                if form.is_valid():
                    k = ExamNumberModel()
                    k.Exam_Name = form.cleaned_data['Exam_Name']
                    k.username = form.cleaned_data['username']
                    k.Subject1 = form.cleaned_data['Subject1']
                    k.Subject2 = form.cleaned_data['Subject2']
                    k.Subject3 = form.cleaned_data['Subject3']
                    k.Subject4 = form.cleaned_data['Subject4']
                    k.Subject5 = form.cleaned_data['Subject5']
                    k.Subject6 = form.cleaned_data['Subject6']
                    k.MaxMarks = form.cleaned_data['MaxMarks']

                    k.save()
                    print("successful")
            return render(request, 'update_result.html',{'ex1':ex1}, {'form':form})


        elif x == 'Class 5':
            ex1 = Profile.objects.filter(Class="Class 10", user__is_staff=False)
            for b in ex1:
                y = b.user
                print(y)


            if request.method == "GET":
                form=ExamNumberForm()
            else:
                form=ExamNumberForm(request.POST)
                if form.is_valid():
                    k = ExamNumberModel()
                    k.Exam_Name = form.cleaned_data['Exam_Name']
                    k.username = form.cleaned_data['username']
                    k.Subject1 = form.cleaned_data['Subject1']
                    k.Subject2 = form.cleaned_data['Subject2']
                    k.Subject3 = form.cleaned_data['Subject3']
                    k.Subject4 = form.cleaned_data['Subject4']
                    k.Subject5 = form.cleaned_data['Subject5']
                    k.Subject6 = form.cleaned_data['Subject6']
                    k.MaxMarks = form.cleaned_data['MaxMarks']

                    k.save()
                    print("successful")
            return render(request, 'update_result.html',{'ex1':ex1}, {'form':form})

        elif x == 'Class 4':
            ex1 = Profile.objects.filter(Class="Class 10", user__is_staff=False)
            for b in ex1:
                y = b.user
                print(y)


            if request.method == "GET":
                form=ExamNumberForm()
            else:
                form=ExamNumberForm(request.POST)
                if form.is_valid():
                    k = ExamNumberModel()
                    k.Exam_Name = form.cleaned_data['Exam_Name']
                    k.username = form.cleaned_data['username']
                    k.Subject1 = form.cleaned_data['Subject1']
                    k.Subject2 = form.cleaned_data['Subject2']
                    k.Subject3 = form.cleaned_data['Subject3']
                    k.Subject4 = form.cleaned_data['Subject4']
                    k.Subject5 = form.cleaned_data['Subject5']
                    k.Subject6 = form.cleaned_data['Subject6']
                    k.MaxMarks = form.cleaned_data['MaxMarks']

                    k.save()
                    print("successful")
            return render(request, 'update_result.html',{'ex1':ex1}, {'form':form})



        elif x == 'Class 4':
            ex1 = Profile.objects.filter(Class="Class 10", user__is_staff=False)
            for b in ex1:
                y = b.user
                print(y)


            if request.method == "GET":
                form=ExamNumberForm()
            else:
                form=ExamNumberForm(request.POST)
                if form.is_valid():
                    k = ExamNumberModel()
                    k.Exam_Name = form.cleaned_data['Exam_Name']
                    k.username = form.cleaned_data['username']
                    k.Subject1 = form.cleaned_data['Subject1']
                    k.Subject2 = form.cleaned_data['Subject2']
                    k.Subject3 = form.cleaned_data['Subject3']
                    k.Subject4 = form.cleaned_data['Subject4']
                    k.Subject5 = form.cleaned_data['Subject5']
                    k.Subject6 = form.cleaned_data['Subject6']
                    k.MaxMarks = form.cleaned_data['MaxMarks']

                    k.save()
                    print("successful")
            return render(request, 'update_result.html',{'ex1':ex1}, {'form':form})

        elif x == 'Class 3':
            ex1 = Profile.objects.filter(Class="Class 10", user__is_staff=False)
            for b in ex1:
                y = b.user
                print(y)


            if request.method == "GET":
                form=ExamNumberForm()
            else:
                form=ExamNumberForm(request.POST)
                if form.is_valid():
                    k = ExamNumberModel()
                    k.Exam_Name = form.cleaned_data['Exam_Name']
                    k.username = form.cleaned_data['username']
                    k.Subject1 = form.cleaned_data['Subject1']
                    k.Subject2 = form.cleaned_data['Subject2']
                    k.Subject3 = form.cleaned_data['Subject3']
                    k.Subject4 = form.cleaned_data['Subject4']
                    k.Subject5 = form.cleaned_data['Subject5']
                    k.Subject6 = form.cleaned_data['Subject6']
                    k.MaxMarks = form.cleaned_data['MaxMarks']

                    k.save()
                    print("successful")
            return render(request, 'update_result.html',{'ex1':ex1}, {'form':form})


        elif x == 'Class 2':
            ex1 = Profile.objects.filter(Class="Class 10", user__is_staff=False)
            for b in ex1:
                y = b.user
                print(y)


            if request.method == "GET":
                form=ExamNumberForm()
            else:
                form=ExamNumberForm(request.POST)
                if form.is_valid():
                    k = ExamNumberModel()
                    k.Exam_Name = form.cleaned_data['Exam_Name']
                    k.username = form.cleaned_data['username']
                    k.Subject1 = form.cleaned_data['Subject1']
                    k.Subject2 = form.cleaned_data['Subject2']
                    k.Subject3 = form.cleaned_data['Subject3']
                    k.Subject4 = form.cleaned_data['Subject4']
                    k.Subject5 = form.cleaned_data['Subject5']
                    k.Subject6 = form.cleaned_data['Subject6']
                    k.MaxMarks = form.cleaned_data['MaxMarks']

                    k.save()
                    print("successful")
            return render(request, 'update_result.html',{'ex1':ex1}, {'form':form})


        elif x == 'Class 9':
            ex1 = Profile.objects.filter(Class="Class 10", user__is_staff=False)
            for b in ex1:
                y = b.user
                print(y)


            if request.method == "GET":
                form=ExamNumberForm()
            else:
                form=ExamNumberForm(request.POST)
                if form.is_valid():
                    k = ExamNumberModel()
                    k.Exam_Name = form.cleaned_data['Exam_Name']
                    k.username = form.cleaned_data['username']
                    k.Subject1 = form.cleaned_data['Subject1']
                    k.Subject2 = form.cleaned_data['Subject2']
                    k.Subject3 = form.cleaned_data['Subject3']
                    k.Subject4 = form.cleaned_data['Subject4']
                    k.Subject5 = form.cleaned_data['Subject5']
                    k.Subject6 = form.cleaned_data['Subject6']
                    k.MaxMarks = form.cleaned_data['MaxMarks']

                    k.save()
                    print("successful")
            return render(request, 'update_result.html',{'ex1':ex1}, {'form':form})

    return render(request,'index.html',{'ex':ex})


@staff_member_required(login_url='/login')
def attendance_update(request):
    ex = Profile.objects.filter(user=request.user)
    for a in ex:
        x = a.Class

        if x == 'Class 10':
            ex2 = Profile.objects.filter(Class="Class 10", user__is_staff=False)
            for b in ex2:
                y = b.user
                print(y)
                #return render(request, 'update_result.html', {'ex1': ex1})


            if request.method == "GET":
                form=AttendanceForm()
            else:
                form=AttendanceForm(request.POST)
                if form.is_valid():
                    ke = AttendanceModel()
                    ke.date = form.cleaned_data['date']
                    ke.username = form.cleaned_data['username']
                    ke.attend = form.cleaned_data['attend']
                    ke.totallecture = form.cleaned_data['totallecture']

                    ke.save()
                    print("successful")
            return render(request, 'Attendance_update.html',{'ex2':ex2}, {'form':form})

    return render(request,'index.html',{'ex':ex})

@login_required(login_url='/login/')
def result_view(request):
    res = ExamNumberModel.objects.filter(username=request.user)
    arr=[]
    prr=[]
    for re in res:
        u1 = re.username
        e1 = re.Exam_Name
        s1 = re.Subject1
        s2 = re.Subject2
        s3 = re.Subject3
        s4 = re.Subject4
        s5 = re.Subject5
        s6 = re.Subject6
        m1 = re.MaxMarks
        sum1 = s1+s2+s3+s4+s5+s6
        arr.append(sum1)
        pr = sum1/m1
        per = pr*100
        prr.append(per)
    vc=arr
    vx=prr

    return render(request,'exam_results.html', {'res':res, 'vc':vc, 'vx':vx})
    del arr[:]
    del prr[:]


@login_required(login_url='/login/')
def attendanceView(request):
    atd = AttendanceModel.objects.filter(username=request.user)
    att=[]
    for gf in atd:
        u2 = gf.username
        at1 = gf.attend
        tot1 = gf.totallecture
        da1 = gf.date
        per1 = at1/tot1
        per2 = per1*100
        att.append(per2)
    print(att)
    bv = att
    return render(request,'attendance-view.html',{'atd':atd, 'bv':bv})
    del att[:]


@login_required(login_url='/login/')
def infoview(request):
    vf = Profile.objects.filter(user = request.user )
    for vfg in vf:
        xcv = vfg.Class
    fg = Assignments.objects.filter(Class=xcv)
    return render(request,'info.html', {'fg':fg})
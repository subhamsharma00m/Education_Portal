from django import forms
#from datetime import datetime

class SignupForms(forms.Form):
    name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    Password = forms.CharField(max_length=100)
    Email = forms.CharField(max_length=100)


class LogInForms(forms.Form):
    username = forms.CharField(max_length=100)
    Password = forms.CharField(max_length=100)


class ExamNumberForm(forms.Form):
    Exam_Name = forms.CharField(max_length=200)
    username = forms.CharField(max_length=50)
    Subject1 = forms.IntegerField()
    Subject2 = forms.IntegerField()
    Subject3 = forms.IntegerField()
    Subject4 = forms.IntegerField()
    Subject5 = forms.IntegerField()
    Subject6 = forms.IntegerField()
    MaxMarks = forms.IntegerField()


class AttendanceForm(forms.Form):
    date = forms.DateField()
    username = forms.CharField(max_length=50)
    attend = forms.IntegerField()
    totallecture = forms.IntegerField()

class Contactform(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.Textarea()

class Assignmentform(forms.Form):
    Class = forms.CharField(max_length=50)
    subject = forms.CharField(max_length=100)
    topic = forms.CharField(max_length=500)
    file = forms.FileField()
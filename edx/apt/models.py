from django.db import models

#from apt.extra import ContentTypeRestrictedFileField

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.validators import MinValueValidator, MaxValueValidator



GENDER_CHOICES = (
   ('Male', 'Male'),
   ('Female', 'Female')
)

transport_CHOICES = (
   ('Yes', 'Yes'),
   ('No', 'No')
)

CLASS_CHOICES =(
    ('Class 1','Class 1'),
    ('Class 2','Class 2'),
    ('Class 3','Class 3'),
    ('Class 4','Class 4'),
    ('Class 5','Class 5'),
    ('Class 6','Class 6'),
    ('Class 7','Class 7'),
    ('Class 8','Class 8'),
    ('Class 9','Class 9'),
    ('Class 10','Class 10'),
    ('Class 11 Sc.','Class 11 Sc'),
    ('Class 11 Co.','Class 11 Co.'),
    ('Class 11 Art','Class 11 Art'),
    ('Class 12 Sc.','Class 12 Sc.'),
    ('Class 12 Co.','Class 12 Co.'),
    ('Class 12 Art','Class 12 Art'),
)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    birth_date = models.DateField(null=True, blank=True)
    mobile = models.PositiveIntegerField()
    total_fee = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(30000),MinValueValidator(0)],blank=True)
    deposite = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(30000),MinValueValidator(0)], blank=True)
    Transport = models.CharField(choices=transport_CHOICES, max_length=10)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=128)
    Father_name = models.CharField(max_length=50, blank=True)
    Mother_name = models.CharField(max_length=50, blank=True)
    parents_contact =models.PositiveIntegerField(blank=True)
    photo = models.FileField(upload_to='post_image')
    Class = models.CharField(choices=CLASS_CHOICES,max_length=50, blank=True)
    Designation = models.CharField(max_length=100, blank=True)
    def __str__(self):  # __unicode__ for Python 2
        return self.user.username

class Assignments(models.Model):
    Class = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    topic = models.CharField(max_length=500)
    file = models.FileField(upload_to='Assignment/%Y/%m/%d/')

    def __str__(self):
        return self.Class

        #@receiver(post_save, sender=User)
#def create_or_update_user_profile(sender, instance, created, **kwargs):
 #   if created:
  #      Profile.objects.create(user=instance)
   # instance.profile.save()







# Create your models here.
class SignupModel(models.Model):
    name = models.CharField(max_length=250)
    Email = models.EmailField(max_length=250,unique=True)
    Password = models.CharField(max_length=50)
    username = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.Email

class Subject(models.Model):
    subject_id = models.CharField(max_length=50)
    subname=models.CharField(max_length=50)

    def __str__(self):
        return '%s'%(self.subname)

class Topics(models.Model):
    subject = models.ForeignKey( Subject, on_delete=models.CASCADE )
    topicname=models.CharField(max_length=80)

    def __str__(self):
        return '%s'%(self.topicname)

class Question(models.Model):
    topics=models.ForeignKey(Topics,on_delete=models.CASCADE)
    question=models.TextField()
    optionA=models.CharField(max_length=50)
    optionB=models.CharField(max_length=50)
    optionC=models.CharField(max_length=50)
    optionD=models.CharField(max_length=50)
    answer=models.CharField(max_length=50)
    marks=models.IntegerField()

    def __str__(self):
        return '%s - %s'%(self.topics.topicname,self.question)

class TestGiven(models.Model):
    exam_date = models.DateField()
    exam_time = models.TimeField()
    username = models.CharField(max_length=50)
    subject_name = models.CharField(max_length=50)
    topic_name = models.CharField(max_length=50)
    total_question = models.IntegerField()
    total_attempted = models.IntegerField()
    total_correct = models.IntegerField()
    total_incorrect = models.IntegerField()
    marks_obtained = models.FloatField()
    percent = models.FloatField()

    def __str__(self):
        return '%s - %s - %s'%(self.username,self.subject_name,self.topic_name)




class ExamNumberModel(models.Model):
    Exam_Name = models.CharField(max_length=200)
    username = models.CharField(max_length=50)
    Subject1 = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(100)])
    Subject2 = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(100)])
    Subject3 = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(100)])
    Subject4 = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(100)])
    Subject5 = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(100)])
    Subject6 = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(100)])
    MaxMarks = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(1000)])

    def __str__(self):
        return '%s - %s'%(self.username,self.Exam_Name)

class AttendanceModel(models.Model):
    date = models.DateField()
    username = models.CharField(max_length=50)
    attend = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(500)])
    totallecture = models.IntegerField(default=0, validators=[MinValueValidator(0),MaxValueValidator(500)])

    def __str__(self):
        return '%s - %s'%(self.username, self.date)

class ContactModel(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    def __str__(self):
        return '%s'%(self.name)

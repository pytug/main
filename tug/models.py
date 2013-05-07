# /svr/my_project/app/webapp/tug/models.py describes the database structure of the application.


from django.db import models
import datetime
from django.utils import timezone


# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

class TrainingType(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=150)

class TrainingSession(models.Model):
    date = models.DateTimeField("session's datetime")
    user = models.ForeignKey(User)
    training_type = models.ForeignKey(TrainingType)
    feedback = models.CharField(max_length=250)

class TrainingSet(models.Model):
    training_session = models.ForeignKey(TrainingSession)
    set_number = models.IntegerField()
    reps = models.IntegerField()

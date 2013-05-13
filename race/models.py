# models for the 'race' app, the db structure

from django.db import models
import datetime
from django.utils import timezone


# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Session(models.Model):
    date = models.DateTimeField("session date")
    reps = models.IntegerField()
    user = models.ForeignKey(User)

    def __unicode__(self):
        return str(self.date)

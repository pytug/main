# Create your views here.

from django.db import models
import datetime
from django.utils import timezone


# Create your models here.

class Session(models.Model):
    date = models.DateTimeField("session date")
    reps = models.IntegerField()

    def __unicode__(self):
        return str(self.date)

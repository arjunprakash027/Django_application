from django.db import models
from datetime import datetime

# Create your models here.

class report(models.Model):
    name = models.CharField(max_length=15)
    user_feedback = models.CharField(max_length=300)

class Room(models.Model):
    name = models.CharField(max_length=1000)


class Message(models.Model):
    value = models.CharField(max_length=1000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    user = models.CharField(max_length=1000000)
    room = models.CharField(max_length=1000000)
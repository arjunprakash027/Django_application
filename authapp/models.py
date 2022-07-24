from django.db import models

# Create your models here.

class report(models.Model):
    name = models.CharField(max_length=15)
    user_feedback = models.CharField(max_length=300)
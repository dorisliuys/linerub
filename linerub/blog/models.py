from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Share(models.Model):
    user = models.ForeignKey(User)
    publish = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    paragraph = models.CharField(max_length=1000)

class Highlight(models.Model):
    story = models.ForeignKey(Share)
    user = models.ForeignKey(User)
    highlights = models.CharField(max_length=1000)
    
  

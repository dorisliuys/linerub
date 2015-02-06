from django.db import models
from django.contrib.auth.models import User
from datetime import datetime 

# Create your models here.

class Share(models.Model):
    user = models.ForeignKey(User)
    publish = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    paragraph = models.CharField(max_length=1000)
    id = models.AutoField('#', primary_key=True)
    date = models.DateTimeField(default = datetime.now())

class Highlight(models.Model):
    story = models.ForeignKey(Share)
    user = models.ForeignKey(User)
    highlights = models.CharField(max_length=1000)
    tags = models.CharField(max_length=1000)

class Link(models.Model):
    story = models.ForeignKey(Share)
    links = models.CharField(max_length=20)
    path = models.ImageField(upload_to='%Y/%m/%d', null=True)
    id = models.AutoField('#', primary_key=True)
    
  

from django.db import models

# Create your models here.
class Tokens(models.Model):
    username = models.CharField(max_length=100)
    token = models.CharField(max_length=100)
    expire = models.DateTimeField()
    login = models.DateTimeField(auto_now=True)
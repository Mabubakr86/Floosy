from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django_countries.fields import CountryField


class Account(models.Model):
    user        = models.OneToOneField(to=User, on_delete=models.CASCADE)
    first_name  = models.CharField(max_length=50, blank=True,null=True)
    last_name   = models.CharField(max_length=50, blank=True,null=True)
    email       = models.EmailField(null=True,blank=True)
    image       = models.ImageField(upload_to='profileimages/',default='profileimages/default.jpg')
    bio         = models.TextField(blank=True,null=True)
    country     = CountryField(blank_label='(select country)', null=True)


    def __str__(self):
        return self.user.username
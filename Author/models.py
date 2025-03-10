from django.db import models
from django.contrib.auth.models import User
from .constants import GENDER_TYPE
# Create your models here.


class UserAccount(models.Model):
    author = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='account')
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_TYPE, null=True, blank=True)

    def __str__(self):
        return self.author.first_name

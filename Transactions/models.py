from django.db import models
from Author . models import UserAccount
# Create your models here.


class Transaction(models.Model):
    account = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.account.author.first_name}-{self.amount}"
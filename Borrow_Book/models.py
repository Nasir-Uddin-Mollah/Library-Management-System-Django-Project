from django.db import models
from django.contrib.auth.models import User
from Book.models import BookModel
# Create your models here.


class BorrowBook(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='borrow')
    book = models.ForeignKey(BookModel, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    balance_after_borrow = models.DecimalField(max_digits=12, decimal_places=2)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.author.first_name}-{self.book.title}'

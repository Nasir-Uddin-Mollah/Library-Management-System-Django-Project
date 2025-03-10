from django.db import models
from Category.models import CategoryModel
from django.contrib.auth.models import User
# Create your models here.


class BookModel(models.Model):
    image = models.ImageField(upload_to='book_images/')
    title = models.CharField(max_length=100)
    description = models.TextField()
    borrowing_price = models.DecimalField(max_digits=5, decimal_places=2)
    borrowing_date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        CategoryModel, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title


class ReviewModel(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(
        BookModel, on_delete=models.CASCADE, related_name='reviews')
    ratings = models.PositiveIntegerField(default=1)
    comment = models.TextField()
    comment_date = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.author.first_name

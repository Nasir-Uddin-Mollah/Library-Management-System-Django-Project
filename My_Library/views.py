from django.shortcuts import render
from Book.models import BookModel
from Category.models import CategoryModel


def home(request, slug=None):
    books = BookModel.objects.all()
    if slug is not None:
        category = CategoryModel.objects.get(slug=slug)
        books = BookModel.objects.filter(category=category)
    categories = CategoryModel.objects.all()

    return render(request, 'home.html', {'categories': categories, 'books': books})

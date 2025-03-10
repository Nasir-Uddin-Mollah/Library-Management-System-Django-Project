from django.shortcuts import render
from django.views.generic import DetailView
from .models import BookModel
from Category.models import CategoryModel
from . import forms
from Borrow_Book.models import BorrowBook

# Create your views here.


class BookDetailsView(DetailView):
    model = BookModel
    template_name = 'books/book_details.html'
    pk_url_kwarg = 'id'
    context_object_name = 'book'

    def post(self, request, *args, **kwargs):
        comment_form = forms.CommentForm(data=self.request.POST)
        book = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.author = request.user
            new_comment.save()
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        user = self.request.user
        has_borrowed = BorrowBook.objects.filter(
            author=user, book=book, is_returned=False).exists()
        comments = book.reviews.all()
        comment_form = forms.CommentForm()
        context["comments"] = comments
        context["comment_form"] = comment_form
        context["has_borrowed"] = has_borrowed
        return context

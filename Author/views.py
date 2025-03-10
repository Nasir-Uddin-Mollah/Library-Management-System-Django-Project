from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm
from django.views.generic import CreateView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import FormView
from .models import UserAccount
from Borrow_Book.models import BorrowBook
from Book.models import BookModel
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.


def send_mail(user, amount, subject, template, book=None):
    context = {
        'user': user,
        'amount': amount,
    }

    if book is not None:
        context['book'] = book

    message = render_to_string(template, context)
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()


class SignupView(FormView):
    form_class = SignupForm
    template_name = 'author/signup.html'
    success_url = reverse_lazy('homepage')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Account Created Successfully')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Signup'
        return context


class UserLoginView(LoginView):
    template_name = 'author/signup.html'

    def get_success_url(self):
        return reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, 'Logged In Successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Login Information Incorrect')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Login'
        return context


def UserLogout(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')


@login_required
def profile(request):
    borrowed_books = BorrowBook.objects.filter(author=request.user)
    return render(request, 'author/profile.html', {'borrowed_books': borrowed_books})


@login_required
def borrow_book(request, id):
    book = BookModel.objects.get(id=id)
    account = UserAccount.objects.get(author=request.user)
    if account.balance >= book.borrowing_price:
        account.balance -= book.borrowing_price
        account.save()
        BorrowBook.objects.create(
            author=request.user,
            book=book,
            balance_after_borrow=account.balance
        )

        messages.success(
            request, f'Successfully borrowed {book.title}.')

        send_mail(request.user, book.borrowing_price, "Borrowed Book",
                  "author/borrow_book_email.html", book.title)
    else:
        messages.error(
            request, 'Insufficient balance.')

    return redirect('profile')


@login_required
def return_book(request, id):
    borrowed_book = get_object_or_404(BorrowBook, id=id)
    account = UserAccount.objects.get(author=request.user)
    account.balance += borrowed_book.book.borrowing_price
    borrowed_book.is_returned = True
    account.save()
    borrowed_book.delete()
    send_mail(request.user, borrowed_book.book.borrowing_price, "Returned Book",
              "author/return_book_email.html", borrowed_book.book.title)
    return redirect('profile')

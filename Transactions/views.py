from django.shortcuts import render
from .forms import DepositForm
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Transaction
from Author.views import send_mail
# Create your views here.


class DepositeMoneyView(LoginRequiredMixin, FormView):
    template_name = 'author/signup.html'
    form_class = DepositForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount
        account.save(
            update_fields=['balance']
        )

        Transaction.objects.create(
            account=account,
            amount=amount,
        )

        messages.success(self.request, f'Amount {amount} deposit successful')
        send_mail(self.request.user, amount, "Deposit Successful",
                  "author/deposite_email.html")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = 'Deposit'
        return context

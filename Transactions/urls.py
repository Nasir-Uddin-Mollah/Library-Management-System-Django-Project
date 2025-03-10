from django.urls import path
from .views import DepositeMoneyView

urlpatterns = [
    path('deposit/', DepositeMoneyView.as_view(), name='deposit'),
]

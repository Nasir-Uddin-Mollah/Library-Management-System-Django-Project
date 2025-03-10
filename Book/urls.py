from django.urls import path
from . import views

urlpatterns = [
    path('detail/<int:id>/', views.BookDetailsView.as_view(), name='book_details')
]

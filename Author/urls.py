from django.urls import path
from .views import SignupView, UserLoginView, UserLogout, profile, borrow_book, return_book

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogout, name='logout'),
    path('profile/', profile, name='profile'),
    path('borrow_book/<int:id>/', borrow_book, name='borrow_book'),
    path('return_book/<int:id>/', return_book, name='return_book'),
]

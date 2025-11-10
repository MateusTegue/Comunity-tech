from django.urls import path
from .views import RegisterView, login_view, profile_view, UserDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('user/<int:id>/', UserDetailView.as_view(), name='user-detail'),
]


from django.urls import path
from .views import FollowListCreateView, unfollow_user

urlpatterns = [
    path('', FollowListCreateView.as_view(), name='follow-list-create'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow'),
]


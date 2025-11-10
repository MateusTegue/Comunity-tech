from django.urls import path
from .views import (
    FriendRequestListCreateView,
    accept_friend_request,
    reject_friend_request,
    cancel_friend_request,
    FriendListView
)

urlpatterns = [
    path('requests/', FriendRequestListCreateView.as_view(), name='friend-request-list-create'),
    path('requests/<int:request_id>/accept/', accept_friend_request, name='accept-friend-request'),
    path('requests/<int:request_id>/reject/', reject_friend_request, name='reject-friend-request'),
    path('requests/<int:request_id>/cancel/', cancel_friend_request, name='cancel-friend-request'),
    path('list/', FriendListView.as_view(), name='friend-list'),
]


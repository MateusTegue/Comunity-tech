from django.urls import path
from .views import CommentListCreateView, CommentDetailView, CommentRepliesView

urlpatterns = [
    path('', CommentListCreateView.as_view(), name='comment-list-create'),
    path('<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('<int:comment_id>/replies/', CommentRepliesView.as_view(), name='comment-replies'),
]


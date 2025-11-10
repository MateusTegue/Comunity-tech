from django.urls import path
from .views import toggle_post_like, toggle_comment_like

urlpatterns = [
    path('post/<int:post_id>/', toggle_post_like, name='toggle-post-like'),
    path('comment/<int:comment_id>/', toggle_comment_like, name='toggle-comment-like'),
]


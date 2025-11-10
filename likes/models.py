from django.db import models
from django.conf import settings


class PostLike(models.Model):
    """Modelo para likes en posts"""
    post = models.ForeignKey(
        'posts.Post',
        on_delete=models.CASCADE,
        related_name='likes'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='post_likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'post_likes'
        unique_together = ['post', 'user']
        indexes = [
            models.Index(fields=['post', 'user']),
        ]

    def __str__(self):
        return f'{self.user.username} likes post {self.post.id}'


class CommentLike(models.Model):
    """Modelo para likes en comentarios"""
    comment = models.ForeignKey(
        'comments.Comment',
        on_delete=models.CASCADE,
        related_name='comment_likes'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comment_likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'comment_likes'
        unique_together = ['comment', 'user']
        indexes = [
            models.Index(fields=['comment', 'user']),
        ]

    def __str__(self):
        return f'{self.user.username} likes comment {self.comment.id}'


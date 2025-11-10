from django.db import models
from django.conf import settings


class Share(models.Model):
    """Modelo para compartir publicaciones"""
    post = models.ForeignKey(
        'posts.Post',
        on_delete=models.CASCADE,
        related_name='shares'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='shares'
    )
    comment = models.TextField(blank=True, null=True)  # Comentario opcional al compartir
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'shares'
        unique_together = ['post', 'user']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post', '-created_at']),
            models.Index(fields=['user', '-created_at']),
        ]

    def __str__(self):
        return f'{self.user.username} compartió post {self.post.id}'


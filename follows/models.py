from django.db import models
from django.conf import settings


class Follow(models.Model):
    """Modelo para seguir a otros usuarios"""
    follower = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='following'
    )
    following = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='followers'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'follows'
        unique_together = ['follower', 'following']
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.follower.username} sigue a {self.following.username}'

    def clean(self):
        if self.follower == self.following:
            from django.core.exceptions import ValidationError
            raise ValidationError("No puedes seguirte a ti mismo.")


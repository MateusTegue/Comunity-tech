from django.db import models
from django.conf import settings


class FriendRequest(models.Model):
    """Modelo para solicitudes de amistad"""
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (PENDING, 'Pendiente'),
        (ACCEPTED, 'Aceptada'),
        (REJECTED, 'Rechazada'),
        (CANCELLED, 'Cancelada'),
    ]

    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_friend_requests'
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_friend_requests'
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'friend_requests'
        unique_together = ['from_user', 'to_user']
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.from_user.username} -> {self.to_user.username} ({self.status})'


class Friendship(models.Model):
    """Modelo para relaciones de amistad"""
    user1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='friendships_as_user1'
    )
    user2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='friendships_as_user2'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'friendships'
        unique_together = ['user1', 'user2']
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user1.username} <-> {self.user2.username}'


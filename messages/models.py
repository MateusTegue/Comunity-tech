from django.db import models
from django.conf import settings


class Conversation(models.Model):
    """Modelo para conversaciones entre usuarios"""
    participant1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversations_as_participant1'
    )
    participant2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversations_as_participant2'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'conversations'
        unique_together = ['participant1', 'participant2']
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['-updated_at']),
        ]

    def __str__(self):
        return f'Conversation: {self.participant1.username} <-> {self.participant2.username}'


class Message(models.Model):
    """Modelo para mensajes en conversaciones"""
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['conversation', 'created_at']),
            models.Index(fields=['sender', 'created_at']),
        ]

    def __str__(self):
        return f'Message from {self.sender.username} in conversation {self.conversation.id}'


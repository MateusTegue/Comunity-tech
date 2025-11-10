from django.db import models
from django.conf import settings


class PostRecommendation(models.Model):
    """Modelo para recomendaciones de posts"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recommended_posts'
    )
    post = models.ForeignKey(
        'posts.Post',
        on_delete=models.CASCADE,
        related_name='recommendations'
    )
    score = models.FloatField(default=0.0)  # Score de relevancia
    reason = models.CharField(max_length=255, blank=True)  # Razón de la recomendación
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'post_recommendations'
        unique_together = ['user', 'post']
        ordering = ['-score', '-created_at']
        indexes = [
            models.Index(fields=['user', '-score']),
        ]

    def __str__(self):
        return f'Recommendation for {self.user.username}: Post {self.post.id} (score: {self.score})'


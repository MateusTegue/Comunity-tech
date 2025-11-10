from rest_framework import generics, permissions
from django.db.models import Q, Count, F
from follows.models import Follow
from friends.models import Friendship
from posts.models import Post
from likes.models import PostLike
from .models import PostRecommendation
from .serializers import PostRecommendationSerializer


class RecommendationListView(generics.ListAPIView):
    """Vista para obtener recomendaciones de posts"""
    serializer_class = PostRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # Obtener usuarios seguidos
        following_users = Follow.objects.filter(follower=user).values_list('following', flat=True)
        
        # Obtener amigos
        friends = Friendship.objects.filter(
            Q(user1=user) | Q(user2=user)
        ).values_list('user1', 'user2')
        friend_ids = set()
        for friend_pair in friends:
            friend_ids.add(friend_pair[0])
            friend_ids.add(friend_pair[1])
        friend_ids.discard(user.id)
        
        # Combinar usuarios seguidos y amigos
        connected_users = list(following_users) + list(friend_ids)
        
        # Obtener posts de usuarios conectados que el usuario aún no ha visto
        # (no son del usuario, no los ha compartido, y no son de usuarios que ya sigue)
        seen_posts = Post.objects.filter(
            Q(author=user) |
            Q(shares__user=user) |
            Q(author_id__in=connected_users)
        ).values_list('id', flat=True)
        
        # Posts de usuarios no conectados que tienen muchos likes
        recommended_posts = Post.objects.filter(
            is_deleted=False
        ).exclude(
            id__in=seen_posts
        ).exclude(
            author=user
        ).annotate(
            likes_count=Count('likes', filter=Q(likes__is_active=True)),
            comments_count=Count('comments', filter=Q(comments__is_deleted=False))
        ).order_by('-likes_count', '-comments_count', '-created_at')[:50]
        
        # Crear o actualizar recomendaciones
        recommendations = []
        for idx, post in enumerate(recommended_posts):
            score = float(post.likes_count * 2 + post.comments_count + (50 - idx))
            reason = f"Post popular con {post.likes_count} likes y {post.comments_count} comentarios"
            
            recommendation, created = PostRecommendation.objects.update_or_create(
                user=user,
                post=post,
                defaults={'score': score, 'reason': reason}
            )
            recommendations.append(recommendation)
        
        return PostRecommendation.objects.filter(
            user=user,
            post__in=[r.post for r in recommendations]
        ).select_related('post__author').order_by('-score', '-created_at')


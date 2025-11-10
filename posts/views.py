from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models import Q
from follows.models import Follow
from friends.models import Friendship
from .models import Post
from .serializers import PostSerializer, PostCreateSerializer


class PostListCreateView(generics.ListCreateAPIView):
    """Vista para listar y crear posts"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateSerializer
        return PostSerializer

    def get_queryset(self):
        # Por defecto muestra posts de usuarios que sigue o son amigos
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
        
        # Combinar usuarios seguidos y amigos, más los propios posts
        all_user_ids = list(following_users) + list(friend_ids) + [user.id]
        
        return Post.objects.filter(
            author_id__in=all_user_ids,
            is_deleted=False
        ).select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Vista para ver, actualizar y eliminar un post"""
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(is_deleted=False)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_destroy(self, instance):
        # Soft delete
        instance.is_deleted = True
        instance.save()


class UserPostsView(generics.ListAPIView):
    """Vista para listar posts de un usuario específico"""
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Post.objects.filter(
            author_id=user_id,
            is_deleted=False
        ).select_related('author')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


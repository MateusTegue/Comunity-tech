from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Comment
from .serializers import CommentSerializer, CommentCreateSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    """Vista para listar y crear comentarios"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CommentCreateSerializer
        return CommentSerializer

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        if post_id:
            return Comment.objects.filter(
                post_id=post_id,
                parent=None,
                is_deleted=False
            ).select_related('author')
        return Comment.objects.none()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Vista para ver, actualizar y eliminar un comentario"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(is_deleted=False)

    def perform_destroy(self, instance):
        # Soft delete
        instance.is_deleted = True
        instance.save()


class CommentRepliesView(generics.ListAPIView):
    """Vista para listar respuestas de un comentario"""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        comment_id = self.kwargs['comment_id']
        return Comment.objects.filter(
            parent_id=comment_id,
            is_deleted=False
        ).select_related('author')


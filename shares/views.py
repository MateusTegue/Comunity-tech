from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Share
from .serializers import ShareSerializer, ShareCreateSerializer


class ShareListCreateView(generics.ListCreateAPIView):
    """Vista para listar y crear shares"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ShareCreateSerializer
        return ShareSerializer

    def get_queryset(self):
        # Por defecto muestra shares del usuario
        post_id = self.request.query_params.get('post_id')
        if post_id:
            return Share.objects.filter(post_id=post_id).select_related('user', 'post__author')
        return Share.objects.filter(user=self.request.user).select_related('user', 'post__author')

    def perform_create(self, serializer):
        # Verificar si ya compartió este post
        post = serializer.validated_data['post']
        if Share.objects.filter(post=post, user=self.request.user).exists():
            raise ValidationError("Ya has compartido este post.")
        serializer.save(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_share(request, share_id):
    """Eliminar un share"""
    try:
        share = Share.objects.get(id=share_id, user=request.user)
        share.delete()
        return Response({'message': 'Share eliminado'}, status=status.HTTP_200_OK)
    except Share.DoesNotExist:
        return Response(
            {'error': 'Share no encontrado'},
            status=status.HTTP_404_NOT_FOUND
        )


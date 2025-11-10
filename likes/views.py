from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import PostLike, CommentLike
from .serializers import PostLikeSerializer, CommentLikeSerializer


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def toggle_post_like(request, post_id):
    """Dar o quitar like a un post"""
    try:
        like = PostLike.objects.get(post_id=post_id, user=request.user)
        if request.method == 'POST':
            # Si existe y está inactivo, reactivarlo
            if not like.is_active:
                like.is_active = True
                like.save()
                return Response({
                    'message': 'Like agregado',
                    'like': PostLikeSerializer(like).data
                }, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Ya has dado like a este post'}, status=status.HTTP_400_BAD_REQUEST)
        else:  # DELETE
            # Soft delete del like
            like.is_active = False
            like.save()
            return Response({'message': 'Like eliminado'}, status=status.HTTP_200_OK)
    except PostLike.DoesNotExist:
        if request.method == 'POST':
            like = PostLike.objects.create(post_id=post_id, user=request.user)
            return Response({
                'message': 'Like agregado',
                'like': PostLikeSerializer(like).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'No has dado like a este post'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def toggle_comment_like(request, comment_id):
    """Dar o quitar like a un comentario"""
    try:
        like = CommentLike.objects.get(comment_id=comment_id, user=request.user)
        if request.method == 'POST':
            if not like.is_active:
                like.is_active = True
                like.save()
                return Response({
                    'message': 'Like agregado',
                    'like': CommentLikeSerializer(like).data
                }, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Ya has dado like a este comentario'}, status=status.HTTP_400_BAD_REQUEST)
        else:  # DELETE
            like.is_active = False
            like.save()
            return Response({'message': 'Like eliminado'}, status=status.HTTP_200_OK)
    except CommentLike.DoesNotExist:
        if request.method == 'POST':
            like = CommentLike.objects.create(comment_id=comment_id, user=request.user)
            return Response({
                'message': 'Like agregado',
                'like': CommentLikeSerializer(like).data
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'No has dado like a este comentario'}, status=status.HTTP_404_NOT_FOUND)


from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Follow
from .serializers import FollowSerializer, FollowCreateSerializer


class FollowListCreateView(generics.ListCreateAPIView):
    """Vista para listar y crear follows"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FollowCreateSerializer
        return FollowSerializer

    def get_queryset(self):
        user = self.request.user
        # Por defecto muestra a quién sigue el usuario
        following_type = self.request.query_params.get('type', 'following')
        
        if following_type == 'followers':
            return Follow.objects.filter(following=user)
        else:
            return Follow.objects.filter(follower=user)

    def perform_create(self, serializer):
        following_user = serializer.validated_data['following']
        
        if following_user == self.request.user:
            raise ValidationError("No puedes seguirte a ti mismo.")
        
        # Verificar si ya lo sigue
        if Follow.objects.filter(
            follower=self.request.user,
            following=following_user
        ).exists():
            raise ValidationError("Ya sigues a este usuario.")
        
        serializer.save(follower=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    """Dejar de seguir a un usuario"""
    try:
        follow = Follow.objects.get(
            follower=request.user,
            following_id=user_id
        )
        follow.delete()
        return Response({'message': 'Has dejado de seguir a este usuario'}, status=status.HTTP_200_OK)
    except Follow.DoesNotExist:
        return Response(
            {'error': 'No sigues a este usuario'},
            status=status.HTTP_404_NOT_FOUND
        )


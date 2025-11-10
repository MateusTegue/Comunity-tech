from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from .models import FriendRequest, Friendship
from .serializers import (
    FriendRequestSerializer, 
    FriendRequestCreateSerializer, 
    FriendshipSerializer
)


class FriendRequestListCreateView(generics.ListCreateAPIView):
    """Vista para listar y crear solicitudes de amistad"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FriendRequestCreateSerializer
        return FriendRequestSerializer

    def get_queryset(self):
        user = self.request.user
        return FriendRequest.objects.filter(
            Q(from_user=user) | Q(to_user=user)
        )

    def perform_create(self, serializer):
        to_user = serializer.validated_data['to_user']
        if to_user == self.request.user:
            raise ValidationError("No puedes enviarte una solicitud a ti mismo.")
        
        # Verificar si ya existe una solicitud
        existing_request = FriendRequest.objects.filter(
            Q(from_user=self.request.user, to_user=to_user) |
            Q(from_user=to_user, to_user=self.request.user)
        ).first()
        
        if existing_request:
            raise ValidationError("Ya existe una solicitud entre estos usuarios.")
        
        # Verificar si ya son amigos
        if Friendship.objects.filter(
            Q(user1=self.request.user, user2=to_user) |
            Q(user1=to_user, user2=self.request.user)
        ).exists():
            raise ValidationError("Ya son amigos.")
        
        serializer.save(from_user=self.request.user)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def accept_friend_request(request, request_id):
    """Aceptar una solicitud de amistad"""
    try:
        friend_request = FriendRequest.objects.get(
            id=request_id,
            to_user=request.user,
            status=FriendRequest.PENDING
        )
        friend_request.status = FriendRequest.ACCEPTED
        friend_request.save()
        
        # Crear la relación de amistad (ordenar por ID para mantener consistencia)
        users = [friend_request.from_user, friend_request.to_user]
        users_sorted = sorted(users, key=lambda u: u.id)
        user1, user2 = users_sorted[0], users_sorted[1]
        
        friendship, created = Friendship.objects.get_or_create(
            user1=user1,
            user2=user2
        )
        
        return Response({
            'message': 'Solicitud de amistad aceptada',
            'friendship': FriendshipSerializer(friendship).data
        }, status=status.HTTP_200_OK)
    except FriendRequest.DoesNotExist:
        return Response(
            {'error': 'Solicitud no encontrada o ya procesada'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def reject_friend_request(request, request_id):
    """Rechazar una solicitud de amistad"""
    try:
        friend_request = FriendRequest.objects.get(
            id=request_id,
            to_user=request.user,
            status=FriendRequest.PENDING
        )
        friend_request.status = FriendRequest.REJECTED
        friend_request.save()
        return Response({'message': 'Solicitud de amistad rechazada'}, status=status.HTTP_200_OK)
    except FriendRequest.DoesNotExist:
        return Response(
            {'error': 'Solicitud no encontrada o ya procesada'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def cancel_friend_request(request, request_id):
    """Cancelar una solicitud de amistad enviada"""
    try:
        friend_request = FriendRequest.objects.get(
            id=request_id,
            from_user=request.user,
            status=FriendRequest.PENDING
        )
        friend_request.status = FriendRequest.CANCELLED
        friend_request.save()
        return Response({'message': 'Solicitud de amistad cancelada'}, status=status.HTTP_200_OK)
    except FriendRequest.DoesNotExist:
        return Response(
            {'error': 'Solicitud no encontrada o ya procesada'},
            status=status.HTTP_404_NOT_FOUND
        )


class FriendListView(generics.ListAPIView):
    """Vista para listar amigos del usuario"""
    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Friendship.objects.filter(
            Q(user1=user) | Q(user2=user)
        )


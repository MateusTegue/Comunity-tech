from rest_framework import status, generics, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from .models import Conversation, Message
from .serializers import (
    ConversationSerializer, 
    ConversationCreateSerializer,
    MessageSerializer,
    MessageCreateSerializer
)


class ConversationListCreateView(generics.ListCreateAPIView):
    """Vista para listar y crear conversaciones"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ConversationCreateSerializer
        return ConversationSerializer

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(
            Q(participant1=user) | Q(participant2=user)
        ).select_related('participant1', 'participant2')

    def perform_create(self, serializer):
        participant2 = serializer.validated_data['participant2']
        if participant2 == self.request.user:
            raise ValidationError("No puedes crear una conversación contigo mismo.")
        
        # Verificar si ya existe una conversación
        existing_conversation = Conversation.objects.filter(
            Q(participant1=self.request.user, participant2=participant2) |
            Q(participant1=participant2, participant2=self.request.user)
        ).first()
        
        if existing_conversation:
            raise ValidationError("Ya existe una conversación con este usuario.")
        
        serializer.save(participant1=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ConversationDetailView(generics.RetrieveAPIView):
    """Vista para ver detalles de una conversación"""
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Conversation.objects.filter(
            Q(participant1=user) | Q(participant2=user)
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class MessageListCreateView(generics.ListCreateAPIView):
    """Vista para listar y crear mensajes en una conversación"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return MessageCreateSerializer
        return MessageSerializer

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        # Verificar que el usuario es participante de la conversación
        conversation = Conversation.objects.filter(
            Q(id=conversation_id) &
            (Q(participant1=self.request.user) | Q(participant2=self.request.user))
        ).first()
        
        if not conversation:
            return Message.objects.none()
        
        return Message.objects.filter(conversation_id=conversation_id).select_related('sender')

    def perform_create(self, serializer):
        conversation_id = self.kwargs['conversation_id']
        conversation = Conversation.objects.filter(
            Q(id=conversation_id) &
            (Q(participant1=self.request.user) | Q(participant2=self.request.user))
        ).first()
        
        if not conversation:
            raise ValidationError("No tienes acceso a esta conversación.")
        
        serializer.save(conversation=conversation, sender=self.request.user)
        
        # Actualizar updated_at de la conversación
        conversation.save()


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def mark_messages_as_read(request, conversation_id):
    """Marcar mensajes como leídos"""
    conversation = Conversation.objects.filter(
        Q(id=conversation_id) &
        (Q(participant1=request.user) | Q(participant2=request.user))
    ).first()
    
    if not conversation:
        return Response(
            {'error': 'Conversación no encontrada'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    Message.objects.filter(
        conversation=conversation,
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)
    
    return Response({'message': 'Mensajes marcados como leídos'}, status=status.HTTP_200_OK)


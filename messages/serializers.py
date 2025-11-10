from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ('id', 'conversation', 'sender', 'content', 'is_read', 'created_at')
        read_only_fields = ('id', 'created_at')


class MessageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('conversation', 'content')


class ConversationSerializer(serializers.ModelSerializer):
    participant1 = UserSerializer(read_only=True)
    participant2 = UserSerializer(read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ('id', 'participant1', 'participant2', 'created_at', 'updated_at', 
                  'last_message', 'unread_count')
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None

    def get_unread_count(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.messages.filter(is_read=False).exclude(sender=request.user).count()
        return 0


class ConversationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = ('participant2',)


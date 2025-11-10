from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import FriendRequest, Friendship


class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ('id', 'from_user', 'to_user', 'status', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class FriendRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ('to_user',)


class FriendshipSerializer(serializers.ModelSerializer):
    user1 = UserSerializer(read_only=True)
    user2 = UserSerializer(read_only=True)

    class Meta:
        model = Friendship
        fields = ('id', 'user1', 'user2', 'created_at')
        read_only_fields = ('id', 'created_at')


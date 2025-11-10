from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Follow


class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    following = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ('id', 'follower', 'following', 'created_at')
        read_only_fields = ('id', 'created_at')


class FollowCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('following',)


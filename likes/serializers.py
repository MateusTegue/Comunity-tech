from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import PostLike, CommentLike


class PostLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PostLike
        fields = ('id', 'post', 'user', 'created_at')
        read_only_fields = ('id', 'created_at')


class CommentLikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = CommentLike
        fields = ('id', 'comment', 'user', 'created_at')
        read_only_fields = ('id', 'created_at')


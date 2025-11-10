from rest_framework import serializers
from accounts.serializers import UserSerializer
from posts.serializers import PostSerializer
from .models import Share


class ShareSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Share
        fields = ('id', 'post', 'user', 'comment', 'created_at')
        read_only_fields = ('id', 'created_at')


class ShareCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = ('post', 'comment')


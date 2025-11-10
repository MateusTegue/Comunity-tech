from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    replies_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'parent', 'created_at', 
                  'updated_at', 'replies_count', 'likes_count')
        read_only_fields = ('id', 'created_at', 'updated_at', 'author')

    def get_replies_count(self, obj):
        return obj.replies.filter(is_deleted=False).count()

    def get_likes_count(self, obj):
        return obj.comment_likes.filter(is_active=True).count()


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('post', 'content', 'parent')


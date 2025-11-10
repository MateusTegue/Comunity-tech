from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    shares_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'author', 'content', 'created_at', 'updated_at', 
                  'likes_count', 'comments_count', 'shares_count', 'is_liked')
        read_only_fields = ('id', 'created_at', 'updated_at', 'author')

    def get_likes_count(self, obj):
        return obj.likes.filter(is_active=True).count()

    def get_comments_count(self, obj):
        return obj.comments.filter(is_deleted=False).count()

    def get_shares_count(self, obj):
        return obj.shares.count()

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user, is_active=True).exists()
        return False


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('content',)


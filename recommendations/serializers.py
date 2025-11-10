from rest_framework import serializers
from posts.serializers import PostSerializer
from .models import PostRecommendation


class PostRecommendationSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)

    class Meta:
        model = PostRecommendation
        fields = ('id', 'post', 'score', 'reason', 'created_at')
        read_only_fields = ('id', 'created_at')


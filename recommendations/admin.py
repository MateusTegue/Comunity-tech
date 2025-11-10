from django.contrib import admin
from .models import PostRecommendation


@admin.register(PostRecommendation)
class PostRecommendationAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'score', 'reason', 'created_at')
    list_filter = ('created_at', 'score')
    search_fields = ('user__username', 'post__id', 'reason')
    readonly_fields = ('created_at',)


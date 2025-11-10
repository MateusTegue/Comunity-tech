from django.contrib import admin
from .models import PostLike, CommentLike


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at', 'is_active')
    list_filter = ('created_at', 'is_active')
    search_fields = ('user__username', 'post__id')


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'comment', 'created_at', 'is_active')
    list_filter = ('created_at', 'is_active')
    search_fields = ('user__username', 'comment__id')


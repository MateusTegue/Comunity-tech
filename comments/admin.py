from django.contrib import admin
from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'content_preview', 'parent', 'created_at', 'is_deleted')
    list_filter = ('created_at', 'is_deleted')
    search_fields = ('author__username', 'content', 'post__id')
    readonly_fields = ('created_at', 'updated_at')

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


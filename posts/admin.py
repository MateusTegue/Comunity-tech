from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content_preview', 'created_at', 'is_deleted')
    list_filter = ('created_at', 'is_deleted')
    search_fields = ('author__username', 'content')
    readonly_fields = ('created_at', 'updated_at')

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'


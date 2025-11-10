from django.contrib import admin
from .models import Share


@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'comment_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'post__id', 'comment')
    readonly_fields = ('created_at',)

    def comment_preview(self, obj):
        if obj.comment:
            return obj.comment[:50] + '...' if len(obj.comment) > 50 else obj.comment
        return '-'
    comment_preview.short_description = 'Comment'


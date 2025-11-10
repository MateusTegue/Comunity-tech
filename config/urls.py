"""
URL configuration for comunitytech project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import welcome_view

urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/friends/', include('friends.urls')),
    path('api/follows/', include('follows.urls')),
    path('api/posts/', include('posts.urls')),
    path('api/comments/', include('comments.urls')),
    path('api/likes/', include('likes.urls')),
    path('api/shares/', include('shares.urls')),
    path('api/messages/', include('messages.urls')),
    path('api/recommendations/', include('recommendations.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


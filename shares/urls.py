from django.urls import path
from .views import ShareListCreateView, delete_share

urlpatterns = [
    path('', ShareListCreateView.as_view(), name='share-list-create'),
    path('<int:share_id>/', delete_share, name='delete-share'),
]


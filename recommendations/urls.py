from django.urls import path
from .views import RecommendationListView

urlpatterns = [
    path('posts/', RecommendationListView.as_view(), name='recommendation-list'),
]


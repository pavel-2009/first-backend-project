from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostsViewSet

router = DefaultRouter()
router.register('posts', PostsViewSet, basename='post')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
]

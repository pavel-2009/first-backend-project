from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import PostsViewSet, CommentsViewSet, GroupViewSet, FollowViewSet

router = DefaultRouter()
router.register('posts', PostsViewSet, basename='post')
router.register('groups', GroupViewSet)
router.register('follow', FollowViewSet)

posts_router = NestedSimpleRouter(router, r'posts', lookup='post')
posts_router.register(r'comments', CommentsViewSet, basename='post-comments')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('', include(posts_router.urls)),
    path('jwt/create/', TokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify')
]

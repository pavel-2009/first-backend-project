from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotAuthenticated, PermissionDenied, AuthenticationFailed
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404

from posts.models import Post, Comment, Group, Follow
from .serializers import PostSerializer, CommentSerializer, GroupSerializer, FollowSerializer
from .permissions import IsAuthorOrReadOnly


class BaseViewSet(ModelViewSet):

    def initial(self, request, *args, **kwargs):
        try:
            super().initial(request, *args, **kwargs)
        except (NotAuthenticated, AuthenticationFailed):
            raise NotAuthenticated('Запрос от имени анонимного пользователя')

    def permission_denied(self, request, message=None, code=None):
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated('Запрос от имени анонимного пользователя')
        raise PermissionDenied(message or "Попытка изменения чужого контента")


class PostsViewSet(BaseViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentsViewSet(BaseViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs.get('post_pk')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_id)
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    http_method_names = ('get',)


class FollowViewSet(BaseViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer 

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

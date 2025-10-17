from rest_framework.viewsets import ModelViewSet

from posts.models import Post, Group, Comment
from .serializers import PostSerializer

class PostsViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)




from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.decorators import api_view


from posts.models import Comment, Post, Group, Follow, User


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    text = serializers.CharField(required=True)

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')
        model = Post

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key, value in data.items():
            if not value:
                data[key] = 0
        return data
    
    def create(self, validated_data):
        return Post.objects.create(**validated_data)
        


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    text = serializers.CharField(required=True)

    class Meta:
        fields = ('id', 'author', 'text', 'created', 'post')
        read_only_fields = ('author', 'post')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Follow
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["user"] = instance.user.username
        rep["following"] = instance.following.username
        return rep
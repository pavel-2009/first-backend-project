from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.decorators import api_view


from posts.models import Comment, Post


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
        post = Post.objects.create(**validated_data)
        return post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment

from rest_framework import serializers
from users.models import Blog, Follow
from blog.models import Post
from rest_framework.validators import UniqueTogetherValidator


class BlogSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Blog
        fields = ('id', 'author', 'name', 'is_subscribed')

    def get_author(self, obj):
        return obj.author.username

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if self.context.get('request').user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user).exists()


class FollowSerializer(serializers.ModelSerializer):
    blog = serializers.CharField(source='blog.name')
    user = serializers.CharField(source='user.username')

    class Meta:
        model = Follow
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'blog'),
                message='Вы уже подписаны на этот блог'
            )
        ]


class PostSerializer(serializers.ModelSerializer):
    blog = serializers.SlugRelatedField(
        slug_field='name', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class SendDailyNewsFeedSerializer(serializers.Serializer):
    pass

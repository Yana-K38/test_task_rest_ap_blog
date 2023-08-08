from itertools import chain

from api.serializers import BlogSerializer, FollowSerializer, PostSerializer
from blog.models import Post
from django.contrib.auth import get_user_model
from django_redis import get_redis_connection
from rest_framework import generics, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import Blog, Follow

from .pagination import CustomPageNumberPagination
from .serializers import SendDailyNewsFeedSerializer
from .tasks import send_daily_news_feed


User = get_user_model()

redis_connection = get_redis_connection()


class BlogViewSet(viewsets.ModelViewSet):
    """Редактирование имени блога."""
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['put']

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Blog.DoesNotExist:
            return Response({"error": "Блог не существует"},
                            status=status.HTTP_404_NOT_FOUND)
        data = {'name': request.data.get('name', instance.name)}
        serializer = self.get_serializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class FollowViewSet(viewsets.ModelViewSet):
    """Подписки на блог."""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete',]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_destroy(self, instance):
        instance.delete()


class PostViewSet(viewsets.ModelViewSet):
    """CRUD для поста."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'delete',]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(blog__following__user=user)

    def perform_create(self, serializer):
        serializer.save(blog=self.request.user.blog)


class PublicationsViewSet(viewsets.ModelViewSet):
    """Лента постов."""
    serializer_class = PostSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [IsAuthenticated]
    http_method_names = ['get',]

    def get_queryset(self):
        user = self.request.user
        subscribed_blogs = Follow.objects.filter(
            user=user).values_list('blog', flat=True)
        queryset = Post.objects.filter(
            blog__in=subscribed_blogs).order_by('-created_at')
        updated_queryset = self.update_publications(
            user, subscribed_blogs, queryset)
        return updated_queryset

    def update_publications(self, user, subscribed_blogs, queryset):
        current_posts_ids = set(queryset.values_list('id', flat=True))
        all_posts = Post.objects.filter(
            blog__in=subscribed_blogs).order_by('-created_at')
        all_posts_ids = set(all_posts.values_list('id', flat=True))
        new_posts = all_posts.filter(id__in=all_posts_ids - current_posts_ids)
        updated_queryset = list(chain(new_posts, queryset))
        return updated_queryset


class PostReadStatusUpdateAPIView(viewsets.ModelViewSet):
    """Пост прочитан."""
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post',]

    def post(self, request, post_id):
        try:
            Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found.'},
                            status=status.HTTP_404_NOT_FOUND)
        if request.user.blog:
            request.user.blog.mark_post_as_read(post_id)
        return Response({'message': 'Post marked as read.'},
                        status=status.HTTP_200_OK)


class GetReadPostsAPIView(generics.ListAPIView):
    """Список прочитаных постов."""
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.blog:
            redis_connection = get_redis_connection()
            read_posts_ids = redis_connection.smembers(
                f'blog:{self.request.user.blog.id}:read_posts')
            return Post.objects.filter(pk__in=read_posts_ids)
        return Post.objects.none()


@api_view(['POST'])
def send_daily_news_feed_view(request):
    serializer = SendDailyNewsFeedSerializer(data=request.data)
    if serializer.is_valid():
        send_daily_news_feed.delay()
        send_daily_news_feed()
        return Response({"message": "Задача для отправки постов запущена."},
                        status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

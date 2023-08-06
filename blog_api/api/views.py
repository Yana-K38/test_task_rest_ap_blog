from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from api.serializers import BlogSerializer, FollowSerializer, PostSerializer
from users.models import Blog, Follow
from blog.models import Post
from django.contrib.auth import get_user_model
from .pagination import CustomPageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import mixins, status, viewsets



User = get_user_model()


class BlogViewSet(viewsets.ModelViewSet):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ['put']

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Blog.DoesNotExist:
            return Response({"error": "Блог не существует"}, status=status.HTTP_404_NOT_FOUND)

        data = {'name': request.data.get('name', instance.name)}
        serializer = self.get_serializer(instance, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete',]
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_destroy(self, instance):
        instance.delete()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    http_method_names = ['get', 'post', 'put', 'delete',]

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(blog__following__user=user)

    def perform_create(self, serializer):
        serializer.save(blog=self.request.user.blog)




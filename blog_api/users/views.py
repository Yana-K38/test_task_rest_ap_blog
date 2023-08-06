from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from ..api.serializers import BlogSerializer
from .models import Blog

class BlogViewSet(ModelViewSet):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()

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

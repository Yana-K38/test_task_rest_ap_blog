from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import BlogViewSet, FollowViewSet, PostViewSet


app_name = 'api'
router = DefaultRouter()
router.register(r'blog', BlogViewSet, basename='blog')
router.register(r'subscriptions', FollowViewSet, basename='subscriptions')
router.register(r'post', PostViewSet, basename='post')


urlpatterns = [
    path('users/', include(router.urls)),
]

from api.views import (BlogViewSet, FollowViewSet, GetReadPostsAPIView,
                       PostReadStatusUpdateAPIView, PostViewSet,
                       PublicationsViewSet, send_daily_news_feed_view)
from django.urls import include, path
from rest_framework.routers import DefaultRouter


app_name = 'api'
router = DefaultRouter()
router.register(r'blog', BlogViewSet, basename='blog')
router.register(r'subscriptions', FollowViewSet, basename='subscriptions')
router.register(r'post', PostViewSet, basename='post')

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    path('send_daily_news/', send_daily_news_feed_view,
         name='send_daily_news_feed_view'),
    path('posts-read/<int:post_id>/read', PostReadStatusUpdateAPIView.as_view(
        {'post': 'post'}), name='post-as-read'),
    path('posts-read/', GetReadPostsAPIView.as_view(), name='get-read'),
    path('publications/', PublicationsViewSet.as_view(), name='publications')
]

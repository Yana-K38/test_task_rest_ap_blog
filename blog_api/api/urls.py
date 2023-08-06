from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (BlogViewSet, FollowViewSet,
                       PostViewSet, PublicationsViewSet,
                       PostReadStatusUpdateAPIView,
                       GetReadPostsAPIView,
                       send_daily_news_feed_view,
                       )


app_name = 'api'
router = DefaultRouter()
router.register(r'blog', BlogViewSet, basename='blog')
router.register(r'subscriptions', FollowViewSet, basename='subscriptions')
router.register(r'post', PostViewSet, basename='post')
router.register(r'publications', PublicationsViewSet, basename='publications')



urlpatterns = [
    path('users/', include(router.urls)),
    
]

urlpatterns += [
    path('send_daily_news/', send_daily_news_feed_view, name='send_daily_news_feed_view'),
    path('posts/<int:post_id>/read/', PostReadStatusUpdateAPIView.as_view({'post': 'post'}), name='post-as-read'),
    path('posts/read/', GetReadPostsAPIView.as_view({'get': 'list'}), name='get-read'),
]

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_api.settings')
import django
django.setup()

from blog.models import Post
from users.models import Blog
from mixer.backend.django import mixer

users = mixer.cycle(100).blend('auth.User')
posts = mixer.cycle(300).blend(Post, blog=mixer.SELECT)

for user in users:
    user.save()

for post in posts:
    post.save()


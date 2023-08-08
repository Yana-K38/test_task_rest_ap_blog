import datetime

from blog_api.celery import app

from blog.models import Post
from django.contrib.auth.models import User
from users.models import Follow


@app.task
def send_daily_news_feed():
    now = datetime.datetime.now()
    now.replace(hour=0, minute=0,
                second=0, microsecond=0) + datetime.timedelta(days=1)
    users = User.objects.all()
    for user in users:
        subscribed_blogs = Follow.objects.filter(
            user=user).values_list('blog', flat=True)
        queryset = Post.objects.filter(
            blog__in=subscribed_blogs).order_by('-created_at')[:5]
        print(f"Подборка последних постов из ленты для {user.username}:")
        for post in queryset:
            print(f"- {post.title}")
        print("Подборка постов успешно выведена в консоль!")

        # message = "Последние пять постов из ленты:\n\n"
        # for post in queryset:
        #     message += f"- {post.title}\n"
        # send_mail(
        #     subject='Подборка последних постов ленты',
        #     message=message,
        #     from_email='email@example.com',
        #     recipient_list=[user.email],
        #     fail_silently=True,
        # )

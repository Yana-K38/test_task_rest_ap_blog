from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django_redis import get_redis_connection


User = get_user_model()
redis_connection = get_redis_connection()


class Blog(models.Model):
    """Модель для создания блога."""
    author = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='blog')
    name = models.CharField('Название блога', max_length=100)
    read_posts = models.ManyToManyField(
        'blog.Post', blank=True, related_name='read_by')

    def __str__(self):
        return self.name

    def mark_post_as_read(self, post_id):
        redis_connection.sadd(f'blog:{self.id}:read_posts', post_id)

    def is_post_read(self, post_id):
        return redis_connection.sismember(
            f'blog:{self.id}:read_posts', post_id)


class Follow(models.Model):
    """Модель для подписок на блог."""
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='following')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower')

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'blog'],
                name='unique_name_follow'
            )
        ]

    def clean(self):
        if self.user == self.blog.author:
            raise ValidationError(
                "Вы не можете подписаться на свой собственный блог.")

    def __str__(self):
        return f'{self.user} подписана на {self.blog}'

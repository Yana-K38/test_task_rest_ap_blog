from django.contrib.auth.models import User
from django.db import models


class Blog(models.Model):
    """Модель для создания блога."""
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='blog')
    name = models.CharField(max_length=100)
        

class Follow(models.Model):
    """Модель для подписок на автора."""
    author = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name='following')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='follower')

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_name_follow'
            )
        ]

    def __str__(self):
        return f'{self.user} подписана на {self.author}'

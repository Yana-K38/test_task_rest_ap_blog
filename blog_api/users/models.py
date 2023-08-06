from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Blog(models.Model):
    """Модель для создания блога."""
    author = models.OneToOneField(User, on_delete=models.CASCADE, related_name='blog')
    name = models.CharField('Название блога', max_length=100)
    
    def __str__(self):
        return self.name
        

class Follow(models.Model):
    """Модель для подписок на автора."""
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

    def __str__(self):
        return f'{self.user} подписана на {self.blog}'

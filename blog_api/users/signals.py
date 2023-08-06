from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Blog
User = get_user_model()


@receiver(post_save, sender=User)
def create_personal_blog(sender, instance, created, **kwargs):
    if created:
        Blog.objects.create(owner=instance, name=f"{instance.username}'s Blog")
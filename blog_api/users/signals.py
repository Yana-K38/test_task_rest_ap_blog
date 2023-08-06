from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Blog
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_personal_blog(sender, instance, created, **kwargs):
    if created:
        Blog.objects.create(owner=instance, name=f"{instance.username} создатель блога")
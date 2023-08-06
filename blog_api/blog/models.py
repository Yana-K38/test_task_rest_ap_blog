from django.db import models
from users.models import Blog


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100, blank=False, null=False)
    text = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read_by_user = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

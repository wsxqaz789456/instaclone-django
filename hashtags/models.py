from django.db import models

# Create your models here.
from posts.models import Post


class Hashtag(models.Model):
    name = models.CharField("Name", max_length=500, blank=False, unique=True)

    def related_posts(self):
        return Post.objects.filter(hashtags__id=self.pk)

    def __str__(self) -> str:
        return self.name

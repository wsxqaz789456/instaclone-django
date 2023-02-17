from django.db import models
from django.contrib.auth.models import AbstractUser

from posts.models import Post


class User(AbstractUser):
    first_name = models.CharField(
        max_length=150,
        blank=False,
    )
    email = models.EmailField(
        blank=False,
        unique=True,
    )
    bio = models.CharField(
        max_length=250,
        blank=True,
    )
    avatar = models.URLField(blank=True)
    following = models.ManyToManyField(
        "self",
        related_name="Following",
        blank=True,
        symmetrical=False,
    )
    followers = models.ManyToManyField(
        "self",
        related_name="Followers",
        blank=True,
        symmetrical=False,
    )

    def __str__(self):
        return self.username

    def followers_count(self):
        """No of followers"""
        if self.followers.count():
            return self.followers.count()
        return 0

    def following_count(self):
        """No of following"""
        if self.following.count():
            return self.following.count()
        return 0

    def posts(self):
        """Get all the posts"""
        return Post.objects.filter(author__id=self.pk)

    def tagged_posts(self):
        """Get all tagged in posts"""
        return Post.objects.filter(tags__id=self.pk)

    def saved_posts(self):
        """Get all saved posts"""
        return Post.objects.filter(saves__id=self.pk)

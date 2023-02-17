from django.db import models
from comments.models import Comment

from common.models import CommonModel

# Create your models here.


class Post(CommonModel):

    author = models.ForeignKey(
        "users.User",
        related_name="Author",
        on_delete=models.CASCADE,
    )
    image = models.URLField()
    caption = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=30, blank=True)
    likes = models.ManyToManyField(
        "users.User", related_name="Post_Likes", blank=True, symmetrical=False
    )
    saves = models.ManyToManyField(
        "users.User", related_name="Post_Saves", blank=True, symmetrical=False
    )

    usertags = models.ManyToManyField(
        "users.User", related_name="Post_Tags", blank=True
    )
    hashtags = models.ManyToManyField(
        "hashtags.Hashtag", related_name="Post_Hashtags", blank=True
    )

    def __str__(self):
        return "{}'s post({})".format(self.author, self.pk)

    def comments(self):
        """Get all comments"""
        return Comment.objects.filter(post__id=self.pk)

    def comments_count(self):
        if self.comments.count():
            return self.comments.count()
        return 0

    def likes_count(self):
        if self.likes.count():
            return self.likes.count()
        return 0

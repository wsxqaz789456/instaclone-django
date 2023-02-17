from django.db import models


# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey(
        "posts.Post", related_name="comments", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        "users.User", related_name="comments", on_delete=models.CASCADE
    )
    content = models.CharField(max_length=400, blank=True)
    usertags = models.ManyToManyField("users.User", blank=True, symmetrical=True)
    likes = models.ManyToManyField(
        "users.User", related_name="Comment_Likes", blank=True, symmetrical=False
    )
    posted_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}'s comment in {}".format(self.author, self.post)

    def likes_count(self):
        if self.likes.count():
            return self.likes.count()
        return 0

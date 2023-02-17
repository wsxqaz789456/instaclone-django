from rest_framework import serializers
from .models import Comment
from users.serializers import PostCreateUserSerializer

from posts.models import Post
from users.models import User


class CommentPostSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("pk", "author")


class CommentAuthorSerialzier(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk", "username", "avatar")


class CreateCommentSerializer(serializers.ModelSerializer):
    author = PostCreateUserSerializer(read_only=True)
    post = CommentPostSerialzier(
        read_only=True,
    )
    usertag = PostCreateUserSerializer(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = ["pk", "author", "post", "content", "usertag", "likes", "posted_time"]


class CommentSerialzier(serializers.ModelSerializer):
    author = CommentAuthorSerialzier()
    is_mine = serializers.SerializerMethodField()

    def get_is_mine(self, comment):
        request = self.context.get("request")
        if request:
            if request.user != comment.author:
                return False
            else:
                return True
        else:
            return False

    class Meta:
        model = Comment
        fields = "__all__"

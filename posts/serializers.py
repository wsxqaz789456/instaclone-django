from rest_framework import serializers
from .models import Post

from comments.serializers import CommentSerialzier
from users.serializers import PostCreateUserSerializer
from hashtags.serializers import HashtagSerializer


class PostSerialzier(serializers.ModelSerializer):
    author = PostCreateUserSerializer(
        read_only=True,
    )
    usertags = PostCreateUserSerializer(
        read_only=True,
        many=True,
    )
    hashtags = HashtagSerializer(
        read_only=True,
        many=True,
    )
    saves = PostCreateUserSerializer(
        many=True,
        read_only=True,
    )
    is_saved = serializers.SerializerMethodField()

    def get_is_saved(self, post):
        request = self.context.get("request")
        if request:
            user = request.user
            if user in post.saves.all():
                return True
            else:
                return False
        else:
            return False

    likes = PostCreateUserSerializer(many=True)

    is_liked = serializers.SerializerMethodField()

    def get_is_liked(self, post):
        request = self.context.get("request")
        if request:
            user = request.user
            if user in post.likes.all():
                return True
            else:
                return False
        else:
            return False

    comments = CommentSerialzier(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            "pk",
            "author",
            "image",
            "caption",
            "location",
            "likes",
            "likes_count",
            "is_liked",
            "saves",
            "is_saved",
            "comments",
            "comments_count",
            "usertags",
            "hashtags",
            "created_at",
        )


class PostCreateSerializer(serializers.ModelSerializer):

    author = PostCreateUserSerializer(
        read_only=True,
    )
    usertags = PostCreateUserSerializer(
        read_only=True,
        many=True,
    )
    hashtags = HashtagSerializer(
        read_only=True,
        many=True,
    )
    comments = CommentSerialzier(many=True, read_only=True)

    likes = PostCreateUserSerializer(
        many=True,
        read_only=True,
    )
    saves = PostCreateUserSerializer(
        many=True,
        read_only=True,
    )

    is_liked = serializers.SerializerMethodField()

    def get_is_liked(self, post):
        request = self.context.get("request")
        if request:
            user = request.user
            if user in post.likes.all():
                return True
            else:
                return False
        else:
            return False

    saves = PostCreateUserSerializer(
        many=True,
        read_only=True,
    )
    is_saved = serializers.SerializerMethodField()

    def get_is_saved(self, post):
        request = self.context.get("request")
        if request:
            user = request.user
            if user in post.saves.all():
                return True
            else:
                return False
        else:
            return False

    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, post):
        request = self.context.get("request")
        if request:
            user = request.user
            if user == post.author:
                return True
            else:
                return False
        else:
            return False

    class Meta:
        model = Post
        fields = (
            "pk",
            "author",
            "image",
            "caption",
            "location",
            "usertags",
            "hashtags",
            "likes",
            "likes_count",
            "is_liked",
            "comments",
            "comments_count",
            "is_owner",
            "saves",
            "is_saved",
        )

from rest_framework import serializers
from .models import User
from posts.models import Post


class userProfilePost(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("pk", "image", "comments_count", "likes_count")


class PostCreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk", "avatar", "username", "first_name", "last_name")


class PrivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password",
            "is_superuser",
            "id",
            "is_staff",
            "is_active",
            "groups",
            "user_permissions",
            "following",
            "followers",
        )


class PublicSerializer(serializers.ModelSerializer):
    posts = userProfilePost(read_only=True, many=True)
    saved_posts = userProfilePost(read_only=True, many=True)
    is_me = serializers.SerializerMethodField()

    def get_is_me(self, instance):
        request = self.context["request"]
        if instance != request.user:
            return False
        else:
            return True

    is_following = serializers.SerializerMethodField()

    def get_is_following(self, instance):
        request = self.context["request"]
        if request.user in instance.followers.all():
            return True
        else:
            return False

    class Meta:
        model = User
        fields = (
            "pk",
            "first_name",
            "last_name",
            "username",
            "bio",
            "avatar",
            "followers_count",
            "following_count",
            "posts",
            "saved_posts",
            "is_me",
            "is_following",
        )


class SearchUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("avatar", "username", "pk", "last_name", "first_name")

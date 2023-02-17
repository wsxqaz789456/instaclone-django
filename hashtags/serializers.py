from rest_framework import serializers
from .models import Hashtag
from posts.models import Post


class HashTagPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("pk", "likes_count", "comments_count", "image")


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ("pk", "name")


class HashtagDetailSerializer(serializers.ModelSerializer):
    related_posts = HashTagPostSerializer(
        read_only=True,
        many=True,
    )

    class Meta:
        model = Hashtag
        fields = ("pk", "name", "related_posts")

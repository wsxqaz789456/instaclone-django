from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ParseError, NotFound, PermissionDenied
from rest_framework import status

from . import serializers, models

from users.models import User
from users.serializers import SearchUser

from hashtags.models import Hashtag
from hashtags.serializers import HashtagSerializer
from users.tests import message

# Create your views here.


class CreatePost(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        author = request.user
        serializer = serializers.PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(author=author)
            usertags = request.data.get("usertags")
            caption = request.data.get("caption")
            hashtags = []
            if caption:
                words = caption.split()
                for word in words:
                    if word.startswith("#"):
                        hashtag, created = Hashtag.objects.get_or_create(name=word[1:])
                        hashtags.append(hashtag)
                post.hashtags.set(hashtags)
            if usertags:
                for usertag_pk in usertags:
                    try:
                        usertag = User.objects.get(pk=usertag_pk)
                    except User.DoesNotExist:
                        raise ParseError("유저가 존재하지 않습니다.")
                    post.usertags.add(usertag)
            serializer = serializers.PostCreateSerializer(post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class PostDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return models.Post.objects.get(pk=pk)
        except models.Post.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        post = self.get_object(pk)
        serializer = serializers.PostCreateSerializer(
            post, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        post = self.get_object(pk)
        if post.author != request.user:
            raise PermissionDenied
        serializer = serializers.PostCreateSerializer(
            post,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            usertags = request.data.get("usertags")
            caption = request.data.get("caption")
            if caption:
                hashtags = []
                post.hashtags.clear()
                words = caption.split()
                for word in words:
                    if word.startswith("#"):
                        hashtag, created = Hashtag.objects.get_or_create(name=word[1:])
                        hashtags.append(hashtag)
                post.hashtags.set(hashtags)
            if usertags:
                post.usertags.clear()
                for usertag_pk in usertags:
                    try:
                        usertag = User.objects.get(pk=usertag_pk)
                    except User.DoesNotExist:
                        raise ParseError("유저가 존재하지 않습니다.")
                    post.usertags.add(usertag)
            updated_post = serializer.save()
            serializer = serializers.PostCreateSerializer(updated_post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        post = self.get_object(pk)
        if post.author != request.user:
            raise PermissionDenied
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LikePostAPI(APIView):

    """게시글 좋아요"""

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return models.Post.objects.get(pk=pk)
        except models.Post.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        user = request.user
        post = self.get_object(pk)
        if user in post.likes.all():
            post.likes.remove(user)
            message(user.username + " unliked the post '{}'".format(post.pk))
        else:
            post.likes.add(user)
            message(user.username + " liked the post '{}'".format(post.pk))
        return Response(status=status.HTTP_200_OK)


class SavePostAPI(APIView):

    """게시글 저장"""

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return models.Post.objects.get(pk=pk)
        except models.Post.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        user = request.user
        post = self.get_object(pk)
        if user in post.saves.all():
            post.saves.remove(user)
            message(user.username + " unsaved the post '{}'".format(post.pk))
        else:
            post.saves.add(user)
            message(user.username + " saved the post '{}'".format(post.pk))
        return Response(status=status.HTTP_200_OK)


class SearchAPI(APIView):

    """검색"""

    permission_classes = [IsAuthenticated]

    def get(self, request, keyword):

        hashtags = Hashtag.objects.filter(name__contains=keyword)
        users = User.objects.filter(username__contains=keyword)

        users_serialzier = SearchUser(users, many=True)
        hashtags_serializer = HashtagSerializer(hashtags, many=True)

        return Response(
            {"hashtags": hashtags_serializer.data, "users": users_serialzier.data}
        )

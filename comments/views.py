from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied

from . import serializers

from posts import models
from comments.models import Comment
from users import models


class CreateCommentAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, post_pk):
        try:
            return models.Post.objects.get(pk=post_pk)
        except models.Post.DoesNotExist:
            raise NotFound

    def post(self, request, post_pk):

        post = self.get_object(post_pk)
        serializer = serializers.CreateCommentSerializer(data=request.data)
        if serializer.is_valid():
            comment = serializer.save(author=request.user, post=post)
            usertags = request.data.get("usertags")
            if usertags:
                for usertag_pk in usertags:
                    try:
                        usertag = models.User.objects.get(pk=usertag_pk)
                    except models.User.DoesNotExist:
                        raise ParseError("유저가 존재하지 않습니다.")
                    post.usertags.add(usertag)
            serializer = serializers.CreateCommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class DeleteCommentAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get_post(self, pk):
        try:
            return models.Post.objects.get(pk=pk)
        except models.Post.DoesNotExist:
            raise NotFound

    def get_comment(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise NotFound

    def delete(self, request, post_pk, comm_pk):
        comment = self.get_comment(pk=comm_pk)
        if comment.author != request.user:
            raise PermissionDenied
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

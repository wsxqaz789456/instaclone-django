from django.contrib.auth import authenticate, login, logout
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ParseError, NotFound
from rest_framework.permissions import IsAuthenticated

from . import serializers, models

from posts.serializers import PostSerialzier

from users.tests import message

import jwt


class Login(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"error": "비밀번호가 틀렸습니다."})


class JWTLogin(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            token = jwt.encode(
                {"pk": user.pk},
                settings.SECRET_KEY,
                algorithm="HS256",
            )
            return Response({"token": token})
        else:
            return Response({"error": "비밀번호가 틀렸습니다."})


class Logout(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class Me(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        """자신의 프로필 조회"""
        user = request.user
        serializer = serializers.PrivateSerializer(user)
        return Response(serializer.data)

    def put(self, request):

        """유저 프로필 수정"""
        user = request.user
        serializer = serializers.PrivateSerializer(
            user,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            user = serializer.save()
            serializer = serializers.PrivateSerializer(user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class Users(APIView):

    """회원가입"""

    def post(self, request):
        password = request.data.get("password")
        if not password:
            raise ParseError("비밀번호가 존재하지 않습니다.")
        serializer = serializers.PrivateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            serializer = serializers.PrivateSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class PublicUser(APIView):

    """유저 조회"""

    def get(self, request, username):
        try:
            user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            raise NotFound
        serializer = serializers.PublicSerializer(user, context={"request": request})
        return Response(serializer.data)


class ChangePassword(APIView):

    """비밀번호 변경"""

    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class FollowUser(APIView):
    """팔로우"""

    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        req_user = request.user
        try:
            ig_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            raise NotFound("존재하지 않는 유저입니다.")
        if req_user not in ig_user.followers.all():
            ig_user.followers.add(req_user)
            req_user.following.add(ig_user)
            message(req_user.username + " followed " + ig_user.username)
        return Response(status=status.HTTP_200_OK)


class UnFollowUser(APIView):

    """언팔로우"""

    permission_classes = [IsAuthenticated]

    def get(self, request, username):
        req_user = request.user
        try:
            ig_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            raise NotFound("존재하지 않는 유저입니다.")
        if req_user in ig_user.followers.all():
            ig_user.followers.remove(req_user)
            req_user.following.remove(ig_user)
            message(req_user.username + " unfollowed " + ig_user.username)

        return Response(status=status.HTTP_200_OK)


class FeedAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = user.posts()
        for following in user.following.all():
            data = data | following.posts()
        data = data.order_by("-created_at")
        serializer = PostSerialzier(data, context={"request": request}, many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

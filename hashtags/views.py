from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Hashtag
from .serializers import HashtagDetailSerializer


class HashTagAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, hashtag):
        try:
            return Hashtag.objects.get(name=hashtag)
        except Hashtag.DoesNotExist:
            raise NotFound

    def get(self, request, hashtag):
        hashtag = self.get_object(hashtag)
        serializer = HashtagDetailSerializer(hashtag)
        return Response(serializer.data, status=status.HTTP_200_OK)

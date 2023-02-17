from django.urls import path
from . import views

urlpatterns = [
    path("<str:hashtag>", views.HashTagAPI.as_view()),
]

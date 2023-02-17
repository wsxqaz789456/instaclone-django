from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.CreatePost.as_view()),
    path("<int:pk>", views.PostDetail.as_view()),
    path("like/<int:pk>", views.LikePostAPI.as_view()),
    path("save/<int:pk>", views.SavePostAPI.as_view()),
    path("search/<str:keyword>", views.SearchAPI.as_view()),
]

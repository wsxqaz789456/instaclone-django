from django.urls import path
from . import views

urlpatterns = [
    path("create/<int:post_pk>", views.CreateCommentAPI.as_view()),
    path("delete/<int:post_pk>/<int:comm_pk>", views.DeleteCommentAPI.as_view()),
]

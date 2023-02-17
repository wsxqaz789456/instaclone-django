from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("me", views.Me.as_view()),
    path("change-password", views.ChangePassword.as_view()),
    path("login", views.Login.as_view()),
    path("logout", views.Logout.as_view()),
    path("token-login", obtain_auth_token),
    path("jwt-login", views.JWTLogin.as_view()),
    path("feed", views.FeedAPI.as_view()),
    path("@<str:username>", views.PublicUser.as_view()),
    path("@<str:username>/follow", views.FollowUser.as_view()),
    path("@<str:username>/unfollow", views.UnFollowUser.as_view()),
]

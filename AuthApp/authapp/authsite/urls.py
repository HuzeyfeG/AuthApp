from django.urls import path
from . import views


urlpatterns = [
    path("", views.explore),
    path("explore", views.explore, name="explore"),
    path("login", views.loginReq, name="login"),
    path("signup", views.signupReq),
    path("logout", views.logoutReq),
]
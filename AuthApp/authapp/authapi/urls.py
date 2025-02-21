from django.urls import path
from . import views


urlpatterns = [
    path("login", views.loginRes),
    path("signup", views.signupRes),
    path("logout", views.logoutRes),
    path("explore", views.exploreRes)
]
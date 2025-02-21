from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
import requests

# Create your views here.


@api_view(["GET", "POST"])
def explore(request):
    if request.COOKIES.get("isLoggedIn") is not None:
        res = requests.post("http://localhost:8000/api-auth/explore", data={"sessionKey": request.COOKIES.get("sessionKey")})
        if res.status_code == 200:
            loggedUser = res.json()["loggedUser"]
            return render(request, "explore.html", {"isLoggedIn": True, "message": "hello {}".format(loggedUser["username"])})
        else:
            return redirect("login")
    else:
        return redirect("login")


@api_view(["GET", "POST"])
def loginReq(request):
    if request.method == "POST":
        email = request.data["email"]
        password = request.data["password"]
        res = requests.post("http://localhost:8000/api-auth/login", data={"email": email, "password": password})
        if res.status_code == 200:
            response = redirect("explore")
            response.set_cookie("isLoggedIn", True)
            response.set_cookie("sessionKey", res.json()["sessionKey"])
            return response
        else:
            return render(request, "login.html", {"isLoggedIn": False, "message": res.json()["message"]})
    else:
        if request.COOKIES.get("isLoggedIn") is not None:
            return redirect("explore")
        else:
            return render(request, "login.html", {"isLoggedIn": False})


@api_view(["GET", "POST"])
def signupReq(request):
    if request.method == "POST":
        username = request.data["username"]
        email = request.data["email"]
        password = request.data["password"]
        res = requests.post("http://localhost:8000/api-auth/signup", data={"username": username, "email": email, "password": password})
        if res.status_code == 200:
            return render(request, "signup.html", {"message": res.json()["message"]})
        else:
            return render(request, "signup.html", {"message": res.json()["message"]})
    else:        
        if request.COOKIES.get("isLoggedIn") is not None:
            return redirect("explore")
        else:
            return render(request, "signup.html", {"isLoggedIn": False})


@api_view(["GET", "POST"])
def logoutReq(request):
    res = requests.post("http://localhost:8000/api-auth/logout", data={"sessionKey": request.COOKIES.get("sessionKey")})
    if res.status_code == 200:
        response = redirect("login")
        response.delete_cookie("isLoggedIn")
        response.delete_cookie("sessionKey")
        return response
    else:
        return redirect("explore")



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import UserModel, UserSession
import datetime
import random, string

# Create your views here.


@api_view(["POST"])
def loginRes(request):
    userCheck = UserModel.objects.filter(email=request.data["email"], password=request.data["password"]).exists()
    if userCheck:
        user = UserModel.objects.get(email=request.data["email"])
        authKey = ''.join(random.choice(string.ascii_lowercase) for i in range(8))
        UserSession.objects.create(userID = user.id, authKey=authKey, lastLoggedIn=datetime.datetime.now())
        return Response({"message": "Succesfully Logged In!", "sessionKey": authKey}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Log In Failure!"}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["POST"])
def signupRes(request):
    emailCheck = UserModel.objects.filter(email=request.data["email"]).exists()
    if not emailCheck:
        UserModel.objects.create(email=request.data["email"], username=request.data["username"], password=request.data["password"])
        return Response({"message": "Succesfully Signed Up!"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Sign Up Failure!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def exploreRes(request):
    session = UserSession.objects.get(authKey=request.data["sessionKey"])
    user = UserModel.objects.get(id=session.userID)
    return Response({"loggedUser": {"id": user.id, "email": user.email, "username": user.username, "password": user.password}}, status=status.HTTP_200_OK)
    

@api_view(["POST"])
def logoutRes(request):
    if UserSession.objects.filter(authKey=request.data["sessionKey"]).exists():
        UserSession.objects.all().filter(authKey=request.data["sessionKey"]).delete()
        return Response(data="logout OK!", status=status.HTTP_200_OK)
    else:
        return Response(data="logout Failed!", status=status.HTTP_400_BAD_REQUEST)
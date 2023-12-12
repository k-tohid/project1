from django.shortcuts import render
from django.contrib.auth.models import User
from .models import CustomUser
from django.shortcuts import get_object_or_404

# rest_framework
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication

from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

# imports
from .serializers import UserSerializer


@api_view(['POST'])
def login(request):
    user = get_object_or_404(CustomUser, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"details": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    token, is_created = Token.objects.get_or_create(user=user)
    # ???
    # is instance necessary here
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    # save the password manually to hash it.
    user = CustomUser.objects.get(username=request.data['username'])
    user.set_password(request.data['password'])
    user.save()
    token = Token.objects.create(user=user)
    return Response({"token": token.key, "user": serializer.data})


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def test_token(request):
    return Response(request.user.username)

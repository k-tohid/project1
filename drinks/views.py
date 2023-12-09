# django
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.models import AnonymousUser

# rest framework
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status

# apps
from .models import Drink
from .serializers import DrinkSerializer

# dev imports
from .helpers import create_uuid


# How to customize this for 401 and 403
class MyException(APIException):
    def __init__(self, status_code, default_detail):
        self.status_code = status_code
        self.default_detail = default_detail


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def drink_list(request):
    if request.method == 'GET':
        drinks = Drink.objects.filter(Q(is_publishable=True) | Q(createdBy=request.user.id)).all()
        serializer = DrinkSerializer(drinks, many=True)
        return Response(serializer.data)

    if not request.user.is_authenticated:
        raise MyException(401, "Please Login.")

    request.data["createdBy"] = request.user.id
    request.data['uuid'] = create_uuid()
    serializer = DrinkSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
def drink_detail(request, drink_id):
    def raise_has_no_access():
        if request.user.is_authenticated and (request.user.username == drink.createdBy.username):
            return True
        raise MyException(403, "UnAuthorized.")

    try:
        drink = Drink.objects.get(uuid=drink_id)
    except Drink.DoesNotExist:
        raise MyException(404, "No such Drink!")

    if (not drink.is_publishable) and drink.createdBy != request.user:
        raise MyException(403, "Unauthorized Access!")

    match request.method:
        case 'GET':
            serializer = DrinkSerializer(drink)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        case 'PUT':
            raise_has_no_access()
            serializer = DrinkSerializer(drink, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        case 'DELETE':
            raise_has_no_access()
            drink.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        case _:
            raise MyException(500, "Internal Error")

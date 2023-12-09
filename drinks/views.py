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


class MyException(APIException):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def drink_list(request):
    # ???
    # why this code results in 7 queries?
    if request.method == 'GET':
        # should I hide private objects in here even to the owner?
        q = Q(is_publishable=True)
        # is this nested if ok? better way?
        if request.user.is_authenticated:
            q |= Q(createdBy=request.user.id)

        drinks = Drink.objects.filter(q)
        serializer = DrinkSerializer(drinks, many=True)
        return Response(serializer.data)

    if not request.user.is_authenticated:
        raise MyException(401, "Please Login.")

    context = {'user': request.user}
    serializer = DrinkSerializer(data=request.data, context=context)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
def drink_detail(request, drink_uuid):
    q = Q(uuid=drink_uuid)
    if 'private/' not in request.get_full_path():
        q &= Q(is_publishable=True)
    else:
        q &= Q(createdBy=request.user.id)

    try:
        drink = Drink.objects.get(q)
    except Drink.DoesNotExist:
        raise MyException(404, "No such Drink!")

    match request.method:
        case 'GET':
            serializer = DrinkSerializer(drink)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        case 'PUT':
            serializer = DrinkSerializer(drink, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        case 'DELETE':
            drink.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        case _:
            raise MyException(500, "Internal Error")

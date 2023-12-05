# django
from django.shortcuts import render
from django.http import JsonResponse

# rest framework
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status

# apps
from .models import Drink
from .serializers import DrinkSerializer


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def drink_list(request):
    if request.method == 'GET':
        drinks = Drink.objects.all()
        serializer = DrinkSerializer(drinks, many=True)
        return Response(serializer.data)

    if request.user.is_authenticated:
        request.data["createdBy"] = request.user.id
        serializer = DrinkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # ???
    # how to give status code
    raise APIException("Not authenticated.")


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([TokenAuthentication])
def drink_detail(request, drink_id):
    def raise_has_no_access():
        if request.user.is_authenticated and (request.user.username == drink.createdBy.username):
            return True
        raise APIException("Not Authorized")

    try:
        drink = Drink.objects.get(pk=drink_id)
    except Drink.DoesNotExist:
        raise APIException("No such Drink!")

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
            raise APIException("Internal Error")



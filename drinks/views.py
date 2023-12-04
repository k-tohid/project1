# django
from django.shortcuts import render
from django.http import JsonResponse

# rest framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status

# apps
from .models import Drink
from .serializers import DrinkSerializer


# get all drinks - serialize them return json
# accept get and post
@api_view(['GET', 'POST'])
def drink_list(request):

    if request.method == 'GET':
        drinks = Drink.objects.all()
        serializer = DrinkSerializer(drinks, many=True)
        return Response(serializer.data)

    serializer = DrinkSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    # serializer.is_valid()
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def drink_detail(request, drink_id):
    try:
        drink = Drink.objects.get(pk=drink_id)
    except Drink.DoesNotExist:
        raise APIException("No such Drink!")

    match request.method:
        case 'GET':
            serializer = DrinkSerializer(drink)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
        case 'PUT':
            serializer = DrinkSerializer(drink, data=request.data)
            # serializer.is_valid()
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        case 'DELETE':
            drink.delete()
            return Response(status = status.HTTP_204_NO_CONTENT)
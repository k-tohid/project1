# django
from django.shortcuts import render
from django.http import JsonResponse

# rest framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# apps
from .models import Drink
from .serializers import DrinkSerializer

# Create your views here.

# get all drinks - serialize them return json
# accept get and post
@api_view(['GET', 'POST'])
def drink_list(request):

    if request.method == 'GET':
        drinks = Drink.objects.all()
        serializer = DrinkSerializer(drinks, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = DrinkSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def drink_detail(request, drink_id):
    try:
        drink = Drink.objects.get(pk=drink_id)
    except Drink.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DrinkSerializer(drink)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    elif  request.method == 'PUT':
        serializer = DrinkSerializer(drink, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
        
    elif  request.method == 'DELETE':
        drink.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
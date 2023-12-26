# django
from django.db.models import Q
from django.core.cache import cache

# rest framework
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

# apps
from .models import Drink
from .serializers import DrinkSerializer

# helpers
from .helpers import convert_date_to_gregorian


class MyException(APIException):
    def __init__(self, status_code, detail):
        self.status_code = status_code
        self.detail = detail


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def drink_list(request):
    if request.method == 'GET':

        q = Q(is_publishable=True)
        if request.user.is_authenticated:
            q |= Q(created_by=request.user.id)

        # query search parameters
        if creator_query := request.query_params.get('creator'):
            q &= Q(created_by__username__contains=creator_query)

        if date_query := request.query_params.get('createdOnFrom'):
            date = convert_date_to_gregorian(date_query)
            q &= Q(created_on__date__gte=date)

        if date_query := request.query_params.get('createdOnTo'):
            date = convert_date_to_gregorian(date_query)
            q &= Q(created_on__date__lte=date)


            # ************** ? *********************
            # is this the correct way?
        if min_price_query := request.query_params.get('minPrice'):
            if not min_price_query.isdigit():
                min_price_query = 0
            q &= Q(price__gte=min_price_query)
        if request.query_params.get('maxPrice'):
            q &= Q(price__lte=request.query_params.get('maxPrice'))

        drinks = Drink.objects.select_related('created_by').prefetch_related('images').filter(q)

        paginator = PageNumberPagination()
        paginator.page_size = 5
        result_page = paginator.paginate_queryset(drinks, request)
        serializer = DrinkSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

        # serializer = DrinkSerializer(drinks, many=True)
        # return Response(serializer.data)

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


    if drink_uuid in cache:
        drink_id = cache.get(drink_uuid)
        q = Q(pk=drink_id)
    else:
        q = Q(uuid=drink_uuid)

    if 'private/' not in request.get_full_path():
        q &= Q(is_publishable=True)
    else:
        q &= Q(created_by=request.user.id)

    try:
        # ****************************** ? ***************************************
        # can i optimize here in regard to select related and prefetch related
        drink = Drink.objects.get(q)
        cache.set(drink_uuid, drink.id, timeout=60 * 60)
    except Drink.DoesNotExist:
        raise MyException(404, "No such Drink!")

    # ******************** ? *********************
    # is this the correct way to forbid private methods
    def has_permission():
        if request.user.id == drink.created_by.id:
            return True
        return False

    match request.method:
        case 'GET':
            serializer = DrinkSerializer(drink)
            return Response(serializer.data, status=status.HTTP_200_OK)

        case 'PUT':
            if has_permission():
                serializer = DrinkSerializer(drink, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            return Response(status=status.HTTP_403_FORBIDDEN)

        case 'DELETE':
            if has_permission():
                drink.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(status=status.HTTP_403_FORBIDDEN)

        case _:
            raise MyException(500, "Internal Error")

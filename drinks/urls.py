from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('', views.drink_list, name='drink_list'),
    path('<drink_uuid>', views.drink_detail, name='drink_detail'),
    path('images/<drink_uuid>', views.drink_image, name='drink_image'),
    path('private/<drink_uuid>', views.drink_detail, name='drink_detail_private'),

]

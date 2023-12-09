from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('', views.drink_list),
    path('<drink_uuid>', views.drink_detail),
    path('private/<drink_uuid>', views.drink_detail),

]

from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='user_login'),
    path('signup', views.signup, name='user_signup'),
    path('test_token', views.test_token),

]
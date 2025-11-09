from django.urls import path
from . import views

urlpatterns = [
    path('function', views.hello_world, name='hello_world'),
    path('class', views.HelloWorldView.as_view(), name='hello_world_class'),
    path('reservation', views.home, name='home'),
]
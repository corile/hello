from django.urls import path
from . import views

urlpatterns = [
    path('calc', views.calc, name='calc'),
    path('ajax/brand-field', views.ajaxBrandField, name='ajax_brand_field'),
]

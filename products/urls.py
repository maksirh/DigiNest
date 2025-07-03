from django.urls import path
from products.views import home

urlpatterns = [
    path("", home),
]
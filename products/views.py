from django.shortcuts import render
from .models import Product


def home(request):
    return render(request, "products/home.html")


def detail(request, my_id):
    context = {
        "item": Product.objects.get(id=my_id)
    }
    return render(request, "products/detail.html", context)

def catalog(request):
    context = {
        "products": Product.objects.all()
    }
    return render(request, "products/catalog.html", context)
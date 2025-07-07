from django.shortcuts import render, redirect
from .models import Product, TypeProduct


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


def addproduct(request):
    types = TypeProduct.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        short_desc = request.POST.get("shortDescription")
        description = request.POST.get("description")
        price = request.POST.get("price")
        type_id = request.POST.get("type")
        image = request.FILES.get("image")

        type_obj = TypeProduct.objects.get(id=type_id) if type_id else None

        product = Product.objects.create(name=name, shortDescription=short_desc, description=description,
            price=price, type=type_obj, image=image)


        return redirect('product-detail', product.id)

    return render(request, "products/addproduct.html", {"types": types})
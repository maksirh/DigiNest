from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, TypeProduct, Basket
from django.contrib.auth.decorators import login_required


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


@login_required
def addproduct(request):
    types = TypeProduct.objects.all()
    if request.method == "POST":
        name = request.POST.get("name")
        short_desc = request.POST.get("shortDescription")
        description = request.POST.get("description")
        price = request.POST.get("price")
        type_id = request.POST.get("type")
        image = request.FILES.get("image")
        seller = request.user

        type_obj = TypeProduct.objects.get(id=type_id) if type_id else None

        product = Product.objects.create(name=name, shortDescription=short_desc, description=description,
            price=price, type=type_obj, image=image, seller=seller)


        return redirect('products:product-detail', product.id)

    return render(request, "products/addproduct.html", {"types": types})


@login_required
def basket(request):
    basket,_ = Basket.objects.get_or_create(user=request.user)
    items = basket.products.all()
    total = sum(p.price for p in items)

    return render(
        request,
        "products/basket.html",
        {"basket_items": items, "basket_total": total},
    )



@login_required
def add_to_basket(request, product_id):

    product = get_object_or_404(Product, id=product_id)
    basket, _ = Basket.objects.get_or_create(user=request.user)
    basket.products.add(product) 

    return redirect("products:basket")
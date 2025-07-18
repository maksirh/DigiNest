from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, TypeProduct, Basket
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from .forms import ProductForm


class ProductHome(ListView):
    model = Product
    template_name = "products/home.html"
    context_object_name = "items"


class ProductDetail(DetailView):
    model = Product
    template_name = "products/detail.html"
    context_object_name = "item"



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


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("users:profile")


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    context_object_name = "item"
    template_name = "products/editproduct.html"
    success_url = reverse_lazy("products:catalog")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["types"] = TypeProduct.objects.all()
        return context



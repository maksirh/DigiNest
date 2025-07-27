from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, TypeProduct, Basket
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator
from .forms import ProductForm
from django.http import JsonResponse, HttpResponse, Http404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json
import stripe
from django.db.models import F

stripe.api_key = settings.STRIPE_SECRET_KEY

class ProductHome(ListView):
    template_name = "products/home.html"
    context_object_name = "items"

    def get_queryset(self):
        return Product.objects.order_by("-views")[:3]


class ProductDetail(DetailView):
    model = Product
    template_name = "products/detail.html"
    context_object_name = "item"
    pk_url_kwarg = "pk"
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        Product.objects.filter(pk=obj.pk).update(views=F("views") + 1)
        obj.refresh_from_db(fields=["views"])
        return obj
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    



def catalog(request):
    page_obj = items = Product.objects.all()

    item_name = request.GET.get("search")

    if item_name != '' and item_name is not None:
        page_obj = items.filter(name__icontains = item_name)

    paginator = Paginator(page_obj, 2) 
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number) 

    context = {
        "products": page_obj, 
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
        {"basket_items": items, "basket_total": total, "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY,},
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

    
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig = request.META.get("HTTP_STRIPE_SIGNATURE")
    endpoint_secret = "whsec_..."

    try:
        event = stripe.Webhook.construct_event(
            payload, sig, endpoint_secret
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        basket_id = session.get("client_reference_id")
        Basket.objects.filter(pk=basket_id).update(paid=True)

    return HttpResponse(status=200)


def basket_success(request):
    return render(request, "products/payment_success.html")


def basket_cancel(request):
    return render(request, "products/payment_cancel.html")


@login_required
def create_checkout_session(request):
    basket, _ = Basket.objects.get_or_create(user=request.user)
    items = basket.products.all()
    if not items:
        raise Http404("Basket is empty")

    line_items = []
    for p in items:
        line_items.append({
            "price_data": {
                "currency": "uah",
                "unit_amount": p.price * 100,
                "product_data": {"name": p.name},
            },
            "quantity": 1,
        })

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        line_items=line_items,
        success_url=f"{settings.DOMAIN}/products/basket/success/?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{settings.DOMAIN}/products/basket/cancel/",
        client_reference_id=str(basket.id),
        metadata={"user_id": request.user.id},
    )
    return JsonResponse({"id": session.id})
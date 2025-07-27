from django.shortcuts import render
from .forms import NewUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from products.models import Product

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
        else:
            print(form.errors)
    form = NewUserForm()
    context = {"form": form,}
    return render(request, "users/register.html", context)


@login_required
def profile(request):
    return render(request, "users/profile.html", {"my_products": Product.objects.filter(seller=request.user)})


def sellerprofile(request, seller_id):
    context = {
        "seller": User.objects.get(id=seller_id),
         "items": Product.objects.filter(id=seller_id)
               }
    return render(request, "users/sellerprofile.html", context)
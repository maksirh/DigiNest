from django.shortcuts import render, redirect
from .forms import NewUserForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from products.models import Product
from django.contrib import messages

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


@login_required
def profile_edit(request):
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=request.user.profile)

    if request.method == "POST":
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Профіль успішно оновлено!")
            return redirect("users:profile")

    return render(
        request,
        "users/profile_edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )
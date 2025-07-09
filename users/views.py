from django.shortcuts import render
from .forms import NewUserForm
from django.contrib.auth.decorators import login_required


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
    return render(request, "users/profile.html")


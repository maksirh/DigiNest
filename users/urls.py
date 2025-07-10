from django.urls import path
from .views import register, profile
from django.contrib.auth.views import LoginView, LogoutView

class LogoutPostOnly(LogoutView):
    http_method_names = ["post"]         
    next_page = "home" 

app_name = "users"

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", LoginView.as_view(template_name='users/login.html'), name="login"),
    path("logout/", LogoutPostOnly.as_view(), name="logout"),
    path("profile/", profile, name="profile"),

]
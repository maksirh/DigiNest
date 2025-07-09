from .models import Profile

def user_profile(request):
    if request.user.is_authenticated:
        profile = Profile.objects.select_related("user").get(user=request.user)
        return {"profile": profile}
    return {}

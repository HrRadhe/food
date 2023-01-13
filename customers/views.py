from django.shortcuts import render , HttpResponse, get_object_or_404 ,redirect
from accounts.models import User, UserProfile
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm
from .forms import UserInfoForm
from django.contrib import messages


# # helper function for get vendor
# def get_user(request):
#     user = user.objects.get(user=request.user)
#     return user

    
# Create your views here.
@login_required(login_url="login")
def cprofile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    userInfo = get_object_or_404(User, email=request.user)


    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        user_form = UserInfoForm(request.POST, instance=userInfo)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            messages.success(request, "Profile Updated")
            return redirect('cprofile')

        else:
            print(user_form.errors)
            print(profile_form.errors)

    else:
        profile_form = UserProfileForm(instance=profile)
        user_form = UserInfoForm(instance=userInfo)

    context = {
        'profile_form': profile_form,
        'user_form' : user_form,
        'profile' : profile,
    }
    return render(request , 'customers/profile.html' ,context)

# from http.client import HTTPResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse

from .forms import UserForm
from .models import User ,UserProfile
from django.contrib import messages,auth
from vendor.forms import VendorForm
from .utils import detectuser
from django.contrib.auth.decorators import login_required, user_passes_test

from django.core.exceptions import PermissionDenied
# restrict the vendor from accessing customer page
def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied

# restric the customer from accessing vendor page
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied 

# Create your views here.

def registerUser(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in.')
        return redirect('myAccount')
    elif request.method == 'POST':
        print(request.POST)
        form = UserForm(request.POST)
        if form.is_valid():
            # #create user using from
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # #form.save()
            # user.set_password(password)
            # user.role = User.CUSTOMER
            # user.save()

            #create user using create_user method from models.py file
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.role = User.CUSTOMER
            user.save() 
            print("user is created")
            messages.success(request,"Your registration is complete.")
            return redirect('registerUser')

        else : 
            print('invalid')
            print(form.errors)

    else:   
        form = UserForm()

    context = {
        'from' : form,
    }

    return  render(request, 'accounts/registerUser.html',context)

def registerVendor(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in.')
        return redirect('myAccount')
    elif request.method == 'POST':
        #store data and create user
        form = UserForm(request.POST)
        v_form =VendorForm(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.role = User.RESTAURANT
            user.save()
            vendor = v_form.save(commit=False) 
            vendor.user = user
            user_profile = UserProfile.objects.get(user = user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'Your account has been registered successfully! Please wait for the approval.')
            return redirect('registerVendor')

    else:
        form = UserForm()
        v_form = VendorForm()

    context = {
        'from' : form,
        'v_form' : v_form,
    }

    return render(request, 'accounts/registerVendor.html',context)


def login(request):
    if request.user.is_authenticated:
        messages.warning(request,'You are already logged in.')
        return redirect('myAccount')
    if request.method == 'POST': 
        email = request.POST['email']
        password =  request.POST['password']

        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login successful')
            return redirect('myAccount')
        else:
            messages.error(request, 'invalid login')
            return redirect('login')
        

    return render(request , 'accounts/login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'Logout successful')
    return redirect('login')
    # return render(request , 'accounts/logout.html')

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
    return render(request , 'accounts/vendorDashboard.html')

@login_required(login_url='login')
@user_passes_test(check_role_customer)   
def custDashboard(request):
    return render(request , 'accounts/custDashboard.html')

@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectuser(user)
    return redirect(redirectUrl)
# from http.client import HTTPResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse

from .forms import UserForm
from .models import User ,UserProfile
from django.contrib import messages
from vendor.forms import VendorForm

# Create your views here.

def registerUser(request):

    if request.method == 'POST':
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
            messages.success(request,"Your registration is complet.")
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
    if request.method == 'POST':
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
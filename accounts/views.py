# from http.client import HTTPResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserForm
from .models import User
from django.contrib import messages

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
            username = form.changed_data['username']
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
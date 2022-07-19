from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout


# Create your views here.
def home(request):
    return render(request, 'authapp/index.html')

def signup(request):

    if request.method == "POST":
        username = request.POST.get('username')
        name = request.POST.get('firstname')
        email = request.POST.get('email')
        password = request.POST.get('pwd')
        confirm_password = request.POST.get('pwd2')
        print(username,name,email,password,confirm_password)

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, password=password, 
                                        email=email, first_name=name)
                user.save()
                
                return redirect('signup')
        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect('signup')

    else:
         return render(request, 'authapp/signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pwd3 = request.POST.get('pwd3')

        print(username,pwd3)

        user = authenticate(username=username, password=pwd3)

        if user is not None:
            auth.login(request, user)
            fname = username
            print(fname)
            return redirect('home')
            
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('signin')
     
    return render(request, 'authapp/signin.html')

def signout(request):
    auth.logout(request)
    return redirect('home')
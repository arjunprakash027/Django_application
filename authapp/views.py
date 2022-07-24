from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import report,Room,Message
from django import forms
from django.http import JsonResponse


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

def show(request):
    reviewz = report.objects
    return render(request, 'authapp/show.html', {'reviewz':reviewz})

def feedback(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user_report = request.POST.get('report')

        new_report = report(name=username,user_feedback=user_report)
        new_report.save()
        return redirect('home')

    return render(request, 'authapp/feedback.html')

def room(request, room):
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'authapp/room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/'+room+'/?username='+username)
    

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})


def signout(request):
    auth.logout(request)
    return redirect('home')
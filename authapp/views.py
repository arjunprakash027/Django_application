from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import report,Room,Message,Post
from django import forms
from django.http import JsonResponse
from django.views import generic
from datetime import datetime
import urllib.request
from gtts import gTTS
import requests
import pandas as pd
import numpy as np
import datetime
from datetime import date
from yahoofinancials import YahooFinancials
from datetime import timedelta
from django.views import View
from django.http import JsonResponse
import json


# Create your views here.
def home(request):

    queryset = Post.objects.all()
    joke = requests.get('https://geek-jokes.sameerkumar.website/api?format=json')
    context = {
        'query': queryset,
        'joke':joke.text,
    }
    return render(request, 'authapp/index.html', context)   
def blog(request):
    return render(request, 'authapp/portfolio.html')

def signup(request):#registers a new user

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

def signin(request):#gets login info from the user to signin
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

def show(request):#show the feedback..its not present as a button in website...it just for authenticated user to read the comments
    reviewz = report.objects
    return render(request, 'authapp/show.html', {'reviewz':reviewz})

def feedback(request):#get feedback from user
    if request.method == 'POST':
        username = request.POST.get('username')
        user_report = request.POST.get('report')

        new_report = report(name=username,user_feedback=user_report)
        new_report.save()
        return redirect('home')

    return render(request, 'authapp/feedback.html')

def room(request, room):#fetches the given room
    username = request.GET.get('username')
    room_details = Room.objects.get(name=room)
    return render(request, 'authapp/room.html', {
        'username': username,
        'room': room,
        'room_details': room_details
    })

def checkview(request):#checks if the given room is already present or not
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name=room).exists():
        return redirect('room/'+room+'/?username='+username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('room/'+room+'/?username='+username)
    

def send(request):#posts the message
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):#recieves and shows the message
    room_details = Room.objects.get(name=room)

    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})


def signout(request):#signout
    auth.logout(request)
    return redirect('home')

def PostDetail(request,slug):#show the details of the blog
    blog_details = Post.objects.get(slug=slug)
    return render(request, 'authapp/post_detail.html',{'details': blog_details})

class get_stock(View):
    #if request.method == "POST":
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        stock = data.get('stock')
        positive = 0
        negative = 0
        total_for_MO = 0
        today = date.today()
        period = timedelta(days=20)
        twenty_days = today - period
        d = datetime.date(2020, 1, 1)
        print(stock)
        yahoo_financials = YahooFinancials('{}.NS'.format(stock))
        data = yahoo_financials.get_historical_price_data(start_date=str(d), 
                                                  end_date=str(today), 
                                                  time_interval='monthly')
        df = pd.DataFrame(data['{}.NS'.format(stock)]['prices'])
        df = df.drop('date', axis=1).set_index('formatted_date')
        price =  yahoo_financials.get_current_price()
        fifty_ma = yahoo_financials.get_50day_moving_avg()
        twohundred_ma = yahoo_financials.get_200day_moving_avg()

        historical_stock_prices = yahoo_financials.get_historical_price_data(str(twenty_days), str(today) , 'daily')
        hist_prices = historical_stock_prices['{}.NS'.format(stock)]['prices']

        price =  yahoo_financials.get_current_price()
        #-----fifty day moving avg------#
        fifty_ma = yahoo_financials.get_50day_moving_avg()
        if fifty_ma - price > 0:
            positive += 1
        else:
            negative += 1

        #--------momentum osccilator------#
        for i in range(len(hist_prices)):
                total_for_MO += hist_prices[i]['close']
        MO = (price/total_for_MO) * 100	

        #------calculating VWAP----------#

        cummulative_price = 0
        cummulative_volume = 0 
        for i in range(len(hist_prices)):
            hist_prices[i]['close']
            cummulative_total = ((hist_prices[i]['high']+hist_prices[i]['low']+hist_prices[i]['close'])/3) * hist_prices[i]['volume']
            cummulative_price += cummulative_total
            cummulative_volume += hist_prices[i]['volume']
        VWAP = cummulative_price/cummulative_volume
        if VWAP > price:
            positive += 1
        else:
            negative += 1

    #-------------final result--------------------#

        if positive > negative:
            conclusion = "positive growth your way"
        else:
            conclusion = "negative growth your way"

        details = {"price":price,"50 days moving average":fifty_ma,"200 days moving average":twohundred_ma,"our prediction":conclusion}
        print(details)
        return JsonResponse(details, status=201)
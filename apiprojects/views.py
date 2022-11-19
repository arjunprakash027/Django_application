from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
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
import requests

class get_stock(View):
    #if request.method == "POST":
    def get(self,request,stock):
        # data = json.loads(request.body.decode("utf-8"))
        # stockname = data.get('stock')
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

        details = {"price":price,"50days":fifty_ma,"200days":twohundred_ma,"prediction":conclusion}
        print(details)
        return JsonResponse(details, status=201)
# Create your views here.

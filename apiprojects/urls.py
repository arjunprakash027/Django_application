from django.contrib import admin
from django.urls import path,include
from . import views
from .views import get_stock

urlpatterns = [
    path('get_stock/<str:stock>',get_stock.as_view()),
]
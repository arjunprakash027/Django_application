from django.contrib import admin
from django.urls import path,include
from . import views
from .views import get_stock

urlpatterns = [
    path('',views.home,name="home"),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('signout',views.signout,name="signout"),
    path('feedback',views.feedback,name="feedback"),
    path('room/<str:room>/', views.room, name='room'),
    path('checkview', views.checkview, name='checkview'),
    path('send', views.send, name='send'),
    path('getMessages/<str:room>/', views.getMessages, name='getMessages'),
    path('portfolio',views.blog,name ='blog'),
    path('blog/<slug:slug>/', views.PostDetail, name='post_detail'),
    path('get_stock/<str:stock>',get_stock.as_view()),
]

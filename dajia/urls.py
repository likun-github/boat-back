from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views
from django.conf.urls import  include
urlpatterns = [
    path('justtry',views.justtry,name='尝试'),
    path('login',views.login,name='登陆'),
    path('verify',views.verify,name='实名认证'),
    path('home',views.home,name='首页'),
    path('secondpage',views.secondpage,name='次页'),
    path('thirdpage',views.thirdpage,name='详情页'),
    path('scancomment',views.scancomment,name='浏览评论'),
    path('orderlist',views.orderlist,name='订单信息'),
    path('orderdetail',views.orderdetail,name='订单信息'),
    path('cancel',views.cancel,name='取消'),
    path('comment',views.comment,name='评论'),
    path('buyalone', views.buyalone, name='购买'),
    path('buytogether', views.buytogether, name='购买'),
    path('cutprice', views.cutprice, name='我要砍价'),
]
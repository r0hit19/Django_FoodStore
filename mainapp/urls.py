"""eato URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from .middlewaress.auth import auth_middleware
from .views import orders,cart
from . import views

urlpatterns = [
    path('',views.home,name='homepage'),
    path('menuitem',views.menu,name='menuitem'),
    path('signup',views.signup,name='signup'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('cart',auth_middleware(cart.as_view()),name='cart'),
    path('confirmation',views.confirmation,name='confirmation'),
    path('orders',orders.as_view(),name='orderpage'),
    path('checkout',views.checkout,name='checkout'),
path('payment',views.payment,name='payment'),
    path('aboutus',views.aboutus,name='aboutus')
]

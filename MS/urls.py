"""MS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from medicines import views
urlpatterns = [
    path('admin/',admin.site.urls),
    path('ms',views.ms),
    path('login',views.login),
    path('addm',views.addm),
    path('addmed',views.addmed),
    path('dem',views.dem),
    path('editp',views.editp),
    path('editpro',views.editpro),
    path('deletepro',views.deletepro),
    path('gab',views.gab),
    path('search',views.search),
    path('add',views.add),
    path('checkout',views.checkout),
    path('Bill',views.bill),
    path('back',views.back),
    path('pbill',views.pbill),
    path('searchbill',views.searchbill),
    path('remove',views.remove),
    path('em',views.em)
]

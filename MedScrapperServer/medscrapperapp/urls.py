from django.urls import path
from django.urls.resolvers import URLPattern 

from . import views

urlpatterns = [
    path('1mg', views.medicine_from_1mg),
    path('', views.home, name='home'),
    path('netmeds', views.medicine_from_netmeds),
    path('pharmeasy', views.medicine_from_pharmeasy),
    path('search', views.searchsuggestions),
]
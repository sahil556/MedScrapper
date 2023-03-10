from django.urls import path
from django.urls.resolvers import URLPattern 

from . import views

urlpatterns = [
    path('1mg', views.medicine_from_1mg),
    path('', views.home, name='home'),
    path('netmeds', views.medicine_from_netmeds),
    path('pharmeasy', views.medicine_from_pharmeasy),
    path('search', views.searchsuggestions),
    path('addSubscription',views.add_subscription),
    path('removeSubscription',views.remove_subscription),
    path('send_price_alert',views.send_price_alerts),
    path('findbymedicinename',views.findbymedicinename),
    path('showsubscription',views.give_user_by_email),
    path('searchbycontent', views.searchsuggestionsbycontent)

]
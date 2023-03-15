from django.shortcuts import render
from django.http import HttpResponse
import json 
from django.forms.models import model_to_dict
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
from medscrapperapp.netmeds_models import MedicineNetMeds
from medscrapperapp.pharmeasy_models import MedicinePharmEasy
from medscrapperapp.onemg_models import Medicine1mg
from medscrapperapp.subscription_models import Subscription
from django.db.models import Q
from medscrapperapp.price_scrapping import get_price_1mg, get_price_netmeds, get_price_pharmeasy, trim_text
from medscrapperapp.send_price_alert_email import send_mail
from medscrapperapp.Scrapping.onemg import scrap_1mg
from medscrapperapp.Scrapping.pharmeasy import scrap_pharmeasy
from medscrapperapp.Scrapping.netmeds import scrap_netmeds
from medscrapperapp.findmedicinebyword import get_medicine
from medscrapperapp.giveuserbyemail import giveuserbyemail
from medscrapperapp.contentseparator import separatecontentPhameasy
from medscrapperapp.contentseparator import separatecontent1mg
from medscrapperapp.findcontentbymedicinename import findContentByMedicineName
from medscrapperapp.getmedicinebycontent import get_medicinebycontent
# Create your views here.



def home(request):
    return HttpResponse("Welcome to MedScrapper")

# subscription  of user
def give_user_by_email(request):
    email = json.loads(request.body)
    return  HttpResponse(json.dumps(giveuserbyemail(email)))


def add_subscription(request) :
    details = json.loads(request.body)
    try :
        objects = Subscription.objects.filter( Q(email = details['email']) & Q(medicine_name = details['medicine_name']) & Q(website_name = details['website_name']))
        if objects.count() > 0 :
            return HttpResponse("Already Exist none")
        else :
            Subscription(email = details['email'] , medicine_name = details['medicine_name'] , website_name = details['website_name']).save()
        return HttpResponse("saved in database")
    except :
        return HttpResponse("Some Thing Went Wrong Try again later")

def remove_subscription(request) :
    details = json.loads(request.body)
    try :
        Subscription.objects.filter( Q(id = details['id'])).delete()
    except :
        return HttpResponse("Some Thing Went Wront Try again later")  
    return HttpResponse("Subscription Removed Successfully")

def send_price_alerts(request) :
    subscription_list = Subscription.objects.all()
    
    for s in subscription_list :
        if s.website_name == '1mg' :
            old_details = Medicine1mg.objects.get(name = s.medicine_name)
            new_price = get_price_1mg(old_details.medlink)
            if new_price != float(old_details.price) :
               send_mail(s.email,old_details,new_price)
                
        elif s.website_name == 'netmeds' :
            old_details = MedicineNetMeds.objects.get(name = s.medicine_name)
            new_price = trim_text(get_price_netmeds(old_details.medlink))
            if new_price != trim_text(old_details.price) :
               send_mail(s.email,old_details,new_price)
        else :
            old_details = MedicinePharmEasy.objects.get(name = s.medicine_name)
            new_price = trim_text(get_price_pharmeasy(old_details.medlink))
            if new_price != trim_text(old_details.price) :
               send_mail(s.email,old_details,new_price)
    return HttpResponse("done")

def searchsuggestions(request):
    medicine_prefix = json.loads(request.body)['name']
    print(medicine_prefix)
    print(type(medicine_prefix))
    medicine_name = []
    results = MedicinePharmEasy.objects.filter(name__startswith = medicine_prefix).values('name','id')

    for result in results:
        print(type(result))
        result["company"] = "pharmeasy"
        medicine_name.append(result)
        
    results = MedicineNetMeds.objects.filter(name__startswith = medicine_prefix).values('name','id')

    for result in results:
        result["company"] = "netmeds"
        medicine_name.append(result)

    results = Medicine1mg.objects.filter(name__startswith = medicine_prefix).values('name','id')
    for result in results:
        result["company"] = "1mg"
        medicine_name.append(result)
    print(medicine_name)
    
    return HttpResponse(json.dumps(medicine_name))

def searchsuggestionsbycontent(request):
    medicine_prefix = json.loads(request.body)['name']
    print(medicine_prefix)
    print(type(medicine_prefix))
    medicine_name = []
    results = MedicinePharmEasy.objects.filter(content__icontains = medicine_prefix).values('content','id')

    for result in results:
        listofcontent = separatecontentPhameasy(result)
        for content in listofcontent:
            medicine_name.append(content.replace(" ",""))
        
    results = MedicineNetMeds.objects.filter(content__icontains = medicine_prefix).values('content','id')

    for result in results:
        singleContent = result['content']
        if singleContent != "Not Available":
            singleContent = singleContent.replace(" ","")
            medicine_name.append(singleContent)

    results = Medicine1mg.objects.filter(content__icontains = medicine_prefix).values('content','id')
    for result in results:
        print(result)
        listofcontent = separatecontent1mg(result['content'])
        for content in listofcontent:
            medicine_name.append(content.replace(" ",""))
    
    return HttpResponse(json.dumps(list(set(medicine_name))))

undef = 0;
terminate = 5
def medicine_from_1mg(request):
    print(json.loads(request.body))
    return HttpResponse(json.dumps(scrap_1mg(json.loads(request.body) )))

def medicine_from_pharmeasy(request):
    print("Requesting for pharmeasy medicine...")
    return HttpResponse(scrap_pharmeasy(json.loads(request.body)), content_type='application/json')

def medicine_from_netmeds(request):
    print("Requesting medicine from netmeds")
    return HttpResponse(scrap_netmeds(json.loads(request.body)), content_type='application/json')

def findbymedicinename(request) :
    data = json.loads(request.body)
    return HttpResponse(json.dumps(get_medicine(data['name'], data['website'])))
    

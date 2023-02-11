from django.shortcuts import render
from django.http import HttpResponse
import json 
from django.forms.models import model_to_dict
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from medscrapperapp.models import Medicine
# Create your views here.



def home(request):
    return HttpResponse("Welcome to MedScrapper")


def medicine_from_1mg(request):
    medicine_name = json.loads(request.body)['name']
    medicine_details = []
    medicine_details_for_save = []
    with sync_playwright () as p:

        browser = p.chromium.launch(headless=False)
        
        page = browser.new_page()

        page.goto('https://www.1mg.com/search/all?name=' + medicine_name)

        page.is_visible('#category-container > div > div.col-xs-12.col-md-10.col-sm-9.style__search-info-container___3s3zV > div:nth-child(2) > div.col-md-9 > div > div:nth-child(2) > div.row.style__grid-container___3OfcL') 
        html = page.inner_html("#category-container > div > div.col-xs-12.col-md-10.col-sm-9.style__search-info-container___3s3zV > div:nth-child(2) > div.col-md-9 > div > div:nth-child(2) > div.row.style__grid-container___3OfcL")
        
        soup = BeautifulSoup (html, 'html.parser')
        links = soup.find_all('a')
     
        details_link = []
        for link in links:
            details_link.append("https://www.1mg.com" + link['href'])
        i = 0
        
        
        
        # print(details_link)
        for link in details_link :
            i = i+1
            medi = []
            medicine  = Medicine()
            medicine.medlink = link
            page.goto(link)
            page.is_visible('#drug_header > div > div')
            html = page.inner_html('body')
            
            soup = BeautifulSoup(html,'html.parser')
            title = soup.find('h1', {'class' : 'DrugHeader__title-content___2ZaPo'}).getText()
            
        
            medicine.name = title
            description = soup.find(id='overview').find('div',{'class':'DrugOverview__content___22ZBX'}).getText()
            
            medicine.description = description
            details = soup.find_all('div',{'class':'DrugHeader__meta-value___vqYM0'})
            
            manufacturer = details[0].contents[0].getText()
            medicine.manufacturer = manufacturer
            components  = ""
            if len(manufacturer) == 4 :
                components = details[2].contents[0].getText()
            else :
                components = details[1].contents[0].getText()
            medicine.content = components
            
            
            images = soup.find_all('img',{'class':'style__image___Ny-Sa style__loaded___22epL'})
            images_link = []
            for img in images : 
                images_link.append(img['src'])
            medicine.imglink = images_link
            
            price_text = soup.find_all('div',{'class':'DrugPriceBox__box___LSjIn'})
            price_text = price_text.__str__() 
            price = 10000000
            take_price = 10000000
            temp_price = ""
            
            for text in price_text:
                take_price = take_price -1
                
                if(text == "₹"):
                    take_price = 9
               
                if(take_price == 0 and not text.isdigit()):
                    take_price = 1000000000

                    if temp_price != "" and price > float(temp_price) :
                        price = float(temp_price)
                    temp_price = ""
                if(take_price == 0) :
                    temp_price = temp_price + text
                    take_price = 1
                                  
            
            medicine.price = price
            how_to_use = soup.find(id="how_to_use")
            if how_to_use :
                how_to_use = how_to_use.find('div',{'class':'DrugOverview__content___22ZBX'}).getText()
        
            medicine.howtouse = how_to_use
            side_effect = soup.find(id="side_effects")
            if side_effect :
                side_effect = side_effect.find('div',{'class':'DrugOverview__list-container___2eAr6 DrugOverview__content___22ZBX'}).getText()
        
            medicine.sideeffect = side_effect
            medicine_details_for_save.append(medicine)
            medicine_details.append(model_to_dict(medicine))

            if i== 5 :
                break

    for medicine in medicine_details_for_save :
        medicine.save() 

    return HttpResponse(json.dumps(medicine_details))

def medicine_from_pharmeasy(request):
    medicine_name = json.loads(request.body)['name']
    return HttpResponse("pharmeasy link")

def medicine_from_netmeds(request):
    medicine_name = json.loads(request.body)['name']
    return HttpResponse("netmeds link")
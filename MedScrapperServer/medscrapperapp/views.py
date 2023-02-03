from django.shortcuts import render
from django.http import HttpResponse
import json 
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
from medscrapperapp.medicine_class import MedicineDetails
# Create your views here.



def home(request):
    return HttpResponse("Welcome to MedScrapper")


def medicine_from_1mg(request):
    medicine_name = json.loads(request.body)['name']
    return HttpResponse("1mg link")

def medicine_from_pharmeasy(request):
    print("Requesting for pharmeasy medicine...")
    medicine_name = json.loads(request.body)['name']
    with sync_playwright () as p: 

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()
        # pharmeasy scrapping starts from here
        hiturl = 'https://pharmeasy.in/search/all?name=' + medicine_name
        page.goto(hiturl)
        page.is_visible('.LHS_container__mrQkM')
        html = page.inner_html('.LHS_container__mrQkM')
        soup = BeautifulSoup (html, 'html.parser')
        links = soup.find_all('a')
   
        details_link =[]
    
        for link in links:
            details_link.append("https://pharmeasy.in/" + link['href'])
        
    # print(details_link)
    
    # hitting first full detail link
        available_searched_medicine_pharmeasy = []
        for link in details_link:
            page.goto(link)
            page.is_visible('html body div#__next main.PreCheckoutLayout_mainSpacingFull__u4CD1 div.Content_wrapper__0Gx95 div.Content_container__oOxF6 div.LHS_container__mrQkM div.PDPDesktop_infoContainer__LCH8b')
            html = page.content()
            
            soup = BeautifulSoup (html, 'html.parser')
            
            medicine_name_node = soup.find('h1')
            medicine_name = medicine_name_node.get_text()
            price = soup.find('div', {'class':'PriceInfo_ourPrice__jFYXr'}).getText()
            imgurl = (soup.find('img', {'class' : 'ProductImageCarousel_productImage__yzafa'}))['src']
            medicine_link = link
            manufacturer = medicine_name_node.parent.next_sibling.getText()
            descnode = soup.find('p', class_ =  re.compile('^MedicalDescription_contentToBeShown'))
            description = "None"
            if descnode is not None:
                description = descnode.get_text() + descnode.next_sibling.get_text()
            howtouse = soup.find(id='directionsForUse')
            if howtouse is not None:
                howtouse = howtouse.contents[1].get_text()
            
            #finding saltsynonyms
            med_table = soup.find_all('td')
            index = 0
            found = False
            saltsynonyms = "Not Available"
            sideeffect = "Not Available"
            
            for info in med_table:
                if info.string  == 'Contains':
                    found = True
                    break
                index = index + 1
            if found :
                saltsynonyms = med_table[index+1].string

            index = 0
            found = False
            for info in med_table:
                if index % 2 == 0 and info.get_text()  == 'Side effects':
                    found = True
                    break
                index = index + 1
            if found : 
                sideeffect = med_table[index+1].string

        
        

            medicine = MedicineDetails(medicine_name, price, imgurl, saltsynonyms, sideeffect, manufacturer, howtouse, description, medicine_link)
            available_searched_medicine_pharmeasy.append(medicine)

        
    return HttpResponse("Successfully Scrapped :")

def medicine_from_netmeds(request):
    print("Requesting medicine from netmeds")
    medicine_name = json.loads(request.body)['name']
    with sync_playwright () as p: 

        browser = p.chromium.launch(headless=False)

        page = browser.new_page()
        hiturl = 'https://www.netmeds.com/catalogsearch/result/' + medicine_name + '/all'
        page.goto(hiturl)
        page.is_visible('.ais-InfiniteHits')
        html = page.inner_html('.ais-InfiniteHits')

        soup = BeautifulSoup (html, 'html.parser')
        links = soup.find_all('a')

        details_link = []

        i = 0
        for link in links:
            if i%2 == 0:
                details_link.append("https://www.netmeds.com" + link['href'])
            i = i+1
        
        # hitting individual url of netmeds 

        available_searched_medicine_netmeds=[]
    
        for link in details_link:
            page.goto(link)
            page.is_visible("#maincontent > div.content-section > div.product-top > div.product-right-block > div.product-detail > h1")
            html = page.content()
            soup = BeautifulSoup (html, 'html.parser')

            medicine_name = soup.find('h1',{'class':'black-txt'}).get_text()
            price = soup.find('span',class_ = 'final-price').get_text()
            imgurl = soup.find('figure',{'class':'figure figure-m-0 largeimage'}).find_all('img')[0]['src']
            medicine_link = link
            
            manufacturer = soup.find('span', class_ ='drug-manu').find('a').get_text()
            desc_node = soup.find_all('div',{'class':'inner-content'})
            description = "None"
            if len(desc_node) > 0:
                description = desc_node[0].getText()[12:]

            side_effect_node = soup.find(string = re.compile("^SIDE EFFECTS"))
            if side_effect_node is not None:
                side_effect_node = side_effect_node.parent.parent.find_all('li')
            side_effect = ""
            for sideeffect in side_effect_node:
                side_effect += sideeffect.getText() + ' '
            
            howtouse=soup.find(string= re.compile('^USES OF'))
            if howtouse is not None:
                howtouse = howtouse.parent.parent.find('ul').get_text()

            med_table = soup.find_all('td')
            index = 0
            found = False
            saltsynonyms = "Not Available"
            
            for info in med_table:
                if info.string  == 'Drug':
                    found = True
                    break
                index = index + 1
            if found :
                saltsynonyms = med_table[index+2].string

            medicine = MedicineDetails(medicine_name, price, imgurl, saltsynonyms, side_effect, manufacturer, howtouse, description, medicine_link)
            available_searched_medicine_netmeds.append(medicine)

        print("printing details --> netmeds")
        for obj in available_searched_medicine_netmeds:
            obj.printdetails()
    return HttpResponse("netmeds link")
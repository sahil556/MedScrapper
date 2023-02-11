from django.shortcuts import render
from django.http import HttpResponse
import json 
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import re
from django.forms.models import model_to_dict
from medscrapperapp.models import Medicine
import json 
# Create your views here.



def home(request):
    return HttpResponse("Welcome to MedScrapper")


def medicine_from_1mg(request):
    medicine_name = json.loads(request.body)['name']    
    return HttpResponse("1mg link")

def medicine_from_pharmeasy(request):
    print("Requesting for pharmeasy medicine...")
    # medicine_name = request.POST['name']

    medicine_name = json.loads(request.body)['name']
 
    available_searched_medicine_model = []
    with sync_playwright () as p: 

        browser = p.chromium.launch(headless=False)
        details_link =[]
        page = browser.new_page()
        # pharmeasy scrapping starts from here
        hiturl = 'https://pharmeasy.in/search/all?name=' + medicine_name
        page.goto(hiturl)
        page.is_visible('.LHS_container__mrQkM')
        html = page.inner_html('.LHS_container__mrQkM')
        soup = BeautifulSoup (html, 'html.parser')
        links = soup.find_all('a')
   
       
        
        for link in links:
            details_link.append("https://pharmeasy.in/" + link['href'])
        
    # print(details_link)
    
    # hitting first full detail link
        i = 0
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

        
        

            medicine = Medicine(name=medicine_name, price = price, imglink = imgurl, content = saltsynonyms, sideeffect = sideeffect, manufacturer = manufacturer, howtouse = howtouse,description = description, medlink = medicine_link)
            available_searched_medicine_pharmeasy.append(model_to_dict(medicine))
            available_searched_medicine_model.append(medicine)
            if i == 0:
                break

    for obj in available_searched_medicine_model:
        obj.save()

    medicine_json = json.dumps(available_searched_medicine_pharmeasy)
    return HttpResponse(medicine_json, content_type='application/json')

def medicine_from_netmeds(request):
    print("Requesting medicine from netmeds")
    medicine_name = json.loads(request.body)['name']
    available_searched_medicine_model = []

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

        itr = 0
        terminate = 0
        available_searched_medicine_netmeds = []
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

            side_effect_node = soup.find(string = re.compile("^SIDE EFFECTS")).parent.parent
            side_effect = ""
            if side_effect_node is not None:
                node = side_effect_node.find(string = re.compile("COMMON")).parent.parent
                print(node.next_sibling)
                if node is not None:
                    temp  = node.find_all('li')
                    for index in temp:
                        side_effect += index.getText() + ", "
                node = side_effect_node.find(string = re.compile("UNCOMMON")).parent.parent
                print(node.next_sibling)
                if node is not None:
                    temp  = node.find_all('li')
                    for index in temp:
                        side_effect += index.getText() + ", "
           
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

            medicine = Medicine(name=medicine_name, price = price, imglink = imgurl, content = saltsynonyms, sideeffect = side_effect, manufacturer = manufacturer, howtouse = howtouse,description = description, medlink = medicine_link)
            available_searched_medicine_netmeds.append(model_to_dict(medicine))
            available_searched_medicine_model.append(medicine)

            if itr == terminate:
                break
        print("printing details --> netmeds")

    for obj in available_searched_medicine_model:
        obj.save()

    medicine_json = json.dumps(available_searched_medicine_netmeds)
    return HttpResponse(medicine_json, content_type='application/json')
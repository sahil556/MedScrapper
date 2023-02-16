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
# Create your views here.



def home(request):
    return HttpResponse("Welcome to MedScrapper")

def searchsuggestions(request):
    medicine_prefix = json.loads(request.body)['name']
    print(medicine_prefix)
    print(type(medicine_prefix))
    medicine_name = []
    results = MedicinePharmEasy.objects.filter(name__startswith = medicine_prefix).values('name','id')

    for result in results:
        medicine_name.append(result)
        
    results = MedicineNetMeds.objects.filter(name__startswith = medicine_prefix).values('name','id')

    for result in results:
        medicine_name.append(result)

    results = Medicine1mg.objects.filter(name__startswith = medicine_prefix).values('name','id')
    for result in results:
        medicine_name.append(result)
    print(medicine_name)
    
    return HttpResponse(json.dumps(medicine_name))

terminate = 5
def medicine_from_1mg(request):
    medicine_name = json.loads(request.body)['name']
    medicine_details = []
    medicine_details_for_save = []
    try :
        with sync_playwright () as p:

            browser = p.chromium.launch(headless=False)
            
            page = browser.new_page()
            
            page.goto('https://www.1mg.com/search/all?name=' + medicine_name)
            
            page.is_visible('#category-container > div > div.col-xs-12.col-md-10.col-sm-9.style__search-info-container___3s3zV') 
            html = page.inner_html("#category-container > div > div.col-xs-12.col-md-10.col-sm-9.style__search-info-container___3s3zV")
            
            soup = BeautifulSoup (html, 'html.parser')
            links = soup.find_all('div',{'class':'product-card-container style__sku-list-container___jSRzr'})
            if len(links) == 2:
                links = links[1]
            else :
                links = links[0]
            links = links.find_all('a')
        
            details_link = []
            for link in links:
                details_link.append("https://www.1mg.com" + link['href'])
            itr = 0
            
            for link in details_link :
                itr = itr +1
                medi = []
                medicine  = Medicine1mg()
                medicine.medlink = link
                page.goto(link)
                page.is_visible('#drug_header > div > div')
                html = page.inner_html('body')
                
                soup = BeautifulSoup(html,'html.parser')
                title = soup.find('h1', {'class' : 'DrugHeader__title-content___2ZaPo'})
                if title :
                    title = title.getText()
                else : 
                    title = soup.find('h1', {'class' : 'ProductTitle__product-title___3QMYH'})
                    if title :
                        title = title.getText()
                    else :
                        title = "Not Retrived"
            
                medicine.name = title.lower()

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
                    side_effect = side_effect.find('div',{'class':'DrugOverview__list-container___2eAr6 DrugOverview__content___22ZBX'})
                    if side_effect :
                        side_effect = side_effect.getText()
            
                medicine.sideeffect = side_effect
                medicine_details_for_save.append(medicine)
                medicine_details.append(model_to_dict(medicine))

                if itr == terminate :
                    break
        for obj in medicine_details_for_save :
            medcheck  = "NULL"
            try : 
                medcheck = Medicine1mg.objects.get(name = obj.name)
            except:
                print("Added to Database")
                obj.save()
    except :
        try :
            saltsynonyms = Medicine1mg.objects.get(name = medicine_name).content 
            print(saltsynonyms)
            saltsynonyms_temp = saltsynonyms.split('+')
            saltsynonyms = []
            for component in saltsynonyms_temp :
                if component.find('(') != -1 :
                    saltsynonyms.append(component.split('(')[0])    
                else :
                    saltsynonyms.append(component)
            
            medicine_dict = {}
            for singleContent in saltsynonyms :
                singleContent = singleContent.replace(" ","")
                print(singleContent)
                medicinenames = Medicine1mg.objects.filter(content__contains=singleContent).values('name')
                print(medicinenames)
                for medicine in medicinenames:
                    medicine = medicine['name']
                    if medicine in medicine_dict:
                        medicine_dict[str(medicine)] = medicine_dict[str(medicine)] + 1
                    else:
                        medicine_dict[str(medicine)] = 1
            sorted_medicine_dict = sorted(medicine_dict.items(), key=lambda x:-x[1])[0:10]
            for medicine_name in sorted_medicine_dict :
                medicine_details.append(model_to_dict(Medicine1mg.objects.get(name=medicine_name[0])))

        except :
            print("exception")
            return HttpResponse("Invalid Medicine Name")

    return HttpResponse(json.dumps(medicine_details))

def medicine_from_pharmeasy(request):
    print("Requesting for pharmeasy medicine...")
    # medicine_name = request.POST['name']

    medicine_name = json.loads(request.body)['name']
    available_searched_medicine_pharmeasy = []
    available_searched_medicine_model = []
    try :
        print(undef)
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
            

            itr = 0
            
            
            for link in details_link:
                itr = itr +1
                page.goto(link)
                page.is_visible('html body div#__next main.PreCheckoutLayout_mainSpacingFull__u4CD1 div.Content_wrapper__0Gx95 div.Content_container__oOxF6 div.LHS_container__mrQkM div.PDPDesktop_infoContainer__LCH8b')
                html = page.content()
                
                soup = BeautifulSoup (html, 'html.parser')
                
                medicine_name_node = soup.find('h1')
                medicine_name = medicine_name_node.get_text().lower()
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

            
            
                
                medicine = MedicinePharmEasy(name=medicine_name, price = price, imglink = imgurl, content = saltsynonyms, sideeffect = sideeffect, manufacturer = manufacturer, howtouse = howtouse,description = description, medlink = medicine_link)
                available_searched_medicine_pharmeasy.append(model_to_dict(medicine))
                available_searched_medicine_model.append(medicine)
                if itr == terminate:
                    break

        for obj in available_searched_medicine_model:
            medcheck  = "NULL"
            try : 
                medcheck = MedicinePharmEasy.objects.get(name = obj.name)
            except:
                print("Added to Database")
                obj.save()

    except :
        try :
            saltsynonyms = MedicinePharmEasy.objects.get(name = medicine_name).content 
            temp = ""
            remove = False
            for char in saltsynonyms :
                if char == '(' :
                    remove = True
                if not remove :
                    temp += char
                if char == ')' :
                    remove = False
            saltsynonyms = temp
            saltsynonyms_temp = saltsynonyms.split('+')
            saltsynonyms = []
            for component in saltsynonyms_temp :
                if component.find('/') != -1 :
                    saltsynonyms.append(component.split('/')[0])
                    saltsynonyms.append(component.split('/')[1])    
                else :
                    saltsynonyms.append(component)
            
            medicine_dict = {} 
            for singleContent in saltsynonyms :
                singleContent = singleContent.replace(" ","")
                print(singleContent)
                medicinenames = MedicinePharmEasy.objects.filter(content__contains=singleContent).values('name')
                print(medicinenames)
                for medicine in medicinenames:
                    medicine = medicine['name']
                    if medicine in medicine_dict:
                        medicine_dict[str(medicine)] = medicine_dict[str(medicine)] + 1
                    else:
                        medicine_dict[str(medicine)] = 1
            sorted_medicine_dict = sorted(medicine_dict.items(), key=lambda x:-x[1])[0:10]
            # print(sorted_medicine_dict)
            for medicine_name in sorted_medicine_dict :
                available_searched_medicine_pharmeasy.append(model_to_dict(MedicinePharmEasy.objects.get(name=medicine_name[0])))
            
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)       
            return HttpResponse("Invalid Medicine Name")

 
    
    medicine_json = json.dumps(available_searched_medicine_pharmeasy)
    return HttpResponse(medicine_json, content_type='application/json')

def medicine_from_netmeds(request):
    print("Requesting medicine from netmeds")
    medicine_name = json.loads(request.body)['name']
    available_searched_medicine_model = []
    available_searched_medicine_netmeds = []
    try :
        with sync_playwright () as p: 

            browser = p.chromium.launch(headless=False)

            page = browser.new_page()
            hiturl = 'https://www.netmeds12.com/catalogsearch/result/' + medicine_name + '/all'
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
           
            for link in details_link:
                print(link)
                itr = itr + 1
                page.goto(link)
                page.is_visible("#maincontent > div.content-section > div.product-top > div.product-right-block > div.product-detail > h1")
                html = page.content()
                soup = BeautifulSoup (html, 'html.parser')
                medicine = MedicineNetMeds()
                medicine_name = soup.find('h1',{'class':'black-txt'}).get_text().lower()
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
                    node = side_effect_node.find(string = re.compile("COMMON"))
                    if node is not None:
                        node = node.parent.parent
                        if node is not None:
                            temp  = node.find_all('li')
                            for index in temp:
                                side_effect += index.getText() + ", "
                    node = side_effect_node.find(string = re.compile("UNCOMMON"))
                    if node is not None:
                        node = node.parent.parent
                        if node is not None:
                            temp  = node.find_all('li')
                            for index in temp:
                                side_effect += index.getText() + ", "

                    node = side_effect_node.find(string = re.compile('RARE'))
                    if node is not None:
                        node = node.parent.parent
                        if node is not None:
                            temp = node.find_all('li')
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

                medicine = MedicineNetMeds(name=medicine_name, price = price, imglink = imgurl, content = saltsynonyms, sideeffect = side_effect, manufacturer = manufacturer, howtouse = howtouse,description = description, medlink = medicine_link)
                
                available_searched_medicine_netmeds.append(model_to_dict(medicine))
                available_searched_medicine_model.append(medicine)

                if itr == terminate:
                    break
        #netmeds
        for obj in available_searched_medicine_model:
            medcheck  = "NULL"
            print(obj)
            try : 
                medcheck = MedicineNetMeds.objects.get(name = obj.name)
            except:
                print("Added to Database")
                try:
                    obj.save()
                except:
                    print("Failed to save to Database")
                    
    except Exception as inst:
        # print(type(inst))    # the exception instance
        # print(inst.args)     # arguments stored in .args
        # print(inst) 
        try :
            saltsynonyms = MedicineNetMeds.objects.get(name = medicine_name).content 
           
            
            singleContent = saltsynonyms
            print(singleContent)
            medicine_dict = {} 
            if singleContent != "Not Available":
                singleContent = singleContent.replace(" ","")
                
                medicinenames = MedicineNetMeds.objects.filter(content__contains=singleContent).values('name')
                print(medicinenames)
                for medicine in medicinenames:
                    medicine = medicine['name']
                    if medicine in medicine_dict:
                        medicine_dict[str(medicine)] = medicine_dict[str(medicine)] + 1
                    else:
                        medicine_dict[str(medicine)] = 1
            sorted_medicine_dict = sorted(medicine_dict.items(), key=lambda x:-x[1])[0:10]
            print(sorted_medicine_dict)
            for medicine_name in sorted_medicine_dict :
                available_searched_medicine_netmeds.append(model_to_dict(MedicineNetMeds.objects.get(name=medicine_name[0])))
        
        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst)       
            return HttpResponse("Invalid Medicine Name")



    medicine_json = json.dumps(available_searched_medicine_netmeds)
    return HttpResponse(medicine_json, content_type='application/json')
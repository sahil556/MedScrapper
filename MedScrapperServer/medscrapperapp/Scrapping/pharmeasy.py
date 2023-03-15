from django.forms.models import model_to_dict
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from medscrapperapp.pharmeasy_models import MedicinePharmEasy
from medscrapperapp.getmedicinebycontent import get_medicinebycontent
from medscrapperapp.findmedicinebyword import get_medicine
from medscrapperapp.findcontentbymedicinename import findContentByMedicineName
import json
import re

def scrap_pharmeasy(data) :
    medicine_name = data["name"]
    available_searched_medicine_pharmeasy = []
    available_searched_medicine_model = []
    terminate = 5
    try :
        # print(undef)
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

            
            
                print("---------->", medicine_name)
                medicine = MedicinePharmEasy(name=medicine_name, price = price, imglink = imgurl, content = saltsynonyms, sideeffect = sideeffect, manufacturer = manufacturer, howtouse = howtouse,description = description, medlink = medicine_link)
                available_searched_medicine_pharmeasy.append(model_to_dict(medicine))
                available_searched_medicine_model.append(medicine)
                if itr == terminate:
                    break

        # for obj in available_searched_medicine_model:
        #     medcheck  = "NULL"
        #     try : 
        #         medcheck = MedicinePharmEasy.objects.get(name = obj.name)
        #     except:
        #         print("Added to Database")
        #         obj.save()

    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst)  
        try :
            if(data["searchby"] == "content"):
                content = []
                content.append(data["name"])
                return json.dumps(get_medicinebycontent(content,data['website']))
            elif(data["selected"] == False):
                return json.dumps(get_medicine(data['name'], data['website']))
            elif(data["website"] != "pharmeasy"):
                # find salt synonyms
                contents = findContentByMedicineName(data["name"], data["website"])
                return json.dumps(get_medicinebycontent(contents,data['website']))
                
     
            
            print(medicine_name)
            saltsynonyms = MedicinePharmEasy.objects.get(name = medicine_name).content 
            print(saltsynonyms)
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
            return "Invalid Medicine Name"

    return json.dumps(available_searched_medicine_pharmeasy)
 
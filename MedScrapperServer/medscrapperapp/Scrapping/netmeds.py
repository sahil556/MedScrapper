from django.forms.models import model_to_dict
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from medscrapperapp.netmeds_models import MedicineNetMeds
from medscrapperapp.getmedicinebycontent import get_medicinebycontent
from medscrapperapp.findmedicinebyword import get_medicine
from medscrapperapp.findcontentbymedicinename import findContentByMedicineName
import json
import re

def scrap_netmeds(data) :
    medicine_name = data["name"]
    terminate  = 5
    available_searched_medicine_model = []
    available_searched_medicine_netmeds = []
    try :
        # print(undef)
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
           
            for link in details_link:
                print(link)
                itr = itr + 1
                page.goto(link)
                page.is_visible("#maincontent > div.content-section > div.product-top > div.product-right-block > div.product-detail > h1")
                html = page.content()
                soup = BeautifulSoup (html, 'html.parser')
                medicine = MedicineNetMeds() #why should take object here?
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
                # this list used for http response (converting data to json this required)
                available_searched_medicine_netmeds.append(model_to_dict(medicine))
                # this list used for saving medicine objects in database
                available_searched_medicine_model.append(medicine)

                if itr == terminate:
                    break
        #netmeds
        for obj in available_searched_medicine_model:
            medcheck  = "NULL"
            print(obj)
            try : 
                # if medicine object not found then it will raise exception and in that part the object is saved in database
                # if medicine object found then do nothig (don't save in datase)
                medcheck = MedicineNetMeds.objects.get(name = obj.name)
            except:
                print("Added to Database")
                try:
                    obj.save()
                except:
                    print("Failed to save to Database")
                    
    except Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst) 
        try :
            if(data["searchby"] == "content"):
                # search by content not medicine name 
                content = []
                content.append(data["name"])
                return json.dumps(get_medicinebycontent(content,data['website']))
            elif(data["selected"] == False):
                # medicine name is written by user not selected from suggestion list
                return json.dumps(get_medicine(data['name'], data['website']))
            elif(data["website"] != "netmeds"):
                # medicine name is taken from suggestion list but that name is not exist in netmeds 
                # find salt synonyms
                contents = findContentByMedicineName(data["name"], data["website"])
                return json.dumps(get_medicinebycontent(contents,data['website']))
            
            # other case that medicine name is taken from suggestion list and that medicine is belongs to netmeds table
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
            return "Invalid Medicine Name"



    medicine_json = json.dumps(available_searched_medicine_netmeds)
    return medicine_json
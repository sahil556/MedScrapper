from django.forms.models import model_to_dict
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
from medscrapperapp.onemg_models import Medicine1mg
from medscrapperapp.getmedicinebycontent import get_medicinebycontent
from medscrapperapp.findmedicinebyword import get_medicine
from medscrapperapp.findcontentbymedicinename import findContentByMedicineName

undef = 0
def scrap_1mg(data) :
    medicine_name = data["name"]
    terminate = 1
    medicine_details = []
    medicine_details_for_save = []
    try :
        print(undef)
        with sync_playwright () as p:

            browser = p.chromium.launch(headless=False)
            
            page = browser.new_page()
            
            page.goto('https://www.1mg.com/search/all?name=' + medicine_name)
            html = ""
            while True :
                try :
                    page.is_visible('#category-container > div > div.col-xs-12.col-md-10.col-sm-9.style__search-info-container___3s3zV') 
                    html = page.inner_html("#category-container > div > div.col-xs-12.col-md-10.col-sm-9.style__search-info-container___3s3zV")
                    break
                except :
                    try : 
                        page.is_visible("#category-container > div > ul > li.list-suggest")
                        html = page.inner_html("#category-container > div > ul > li.list-suggest")
                        soup = BeautifulSoup(html, 'html.parser')
                        print('https://www.1mg.com' + soup.find('a')['href'])
                        page.goto('https://www.1mg.com' + soup.find('a')['href'])
                    except :
                        return []
            
            soup = BeautifulSoup (html, 'html.parser')
            links = soup.find_all('div',{'class':'product-card-container style__sku-list-container___jSRzr'})
            if len(links) == 2:
                links = links[1]
            else :
                links = links[0]
            links = links.find_all('a')
            # terminate = len(links)
            details_link_drugs = []
            details_link_otc = []
            for link in links:
                if(link['href'].startswith('/otc')) :
                    details_link_otc.append("https://www.1mg.com" + link['href'])
                else :
                    details_link_drugs.append("https://www.1mg.com" + link['href'])
            itr = 0
            # terminate = len(details_link_drugs) + len(details_link_otc)
            terminate = 5
            for link in details_link_drugs :
                itr = itr +1
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
                    medicine.imglink = img['src']
                    break
                
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
                print(itr, " Done",terminate )
                if itr == terminate :
                    break
            ite = 1
            for link in details_link_otc :
                print(link)
                itr = itr +1
                medicine  = Medicine1mg()
                medicine.medlink = link
                page.goto(link)
                page.is_visible('#container > div > div > div.row.OtcPage__top-container___2JKJ-')
                html = page.inner_html('body')
                
                soup = BeautifulSoup(html,'html.parser')
                title = soup.find('h1', {'class' : 'ProductTitle__product-title___3QMYH'})
                if title :
                    title = title.getText()
                else :
                    title = "Not Retrived"
            
                medicine.name = title.lower()
                print("Medicine name , " ,medicine.name)
                medicine.manufacturer = soup.find('div',{'class' : 'ProductTitle__manufacturer___sTfon'}).getText()
                print("menufacturrer ,", medicine.manufacturer)
                images = soup.find_all('div',{'class':'col-xs-10 ProductImage__preview-container___2oTeX'})
                images_link = []
                
                
                for img in images : 
                    images_link = img.find('img')['src']
                    break
                medicine.imglink = images_link
                print("image ,",medicine.imglink)
                
                data = soup.find('div', {'class' : 'ProductDescription__description-content___A_qCZ'})
                # print(data.find(''))
                next_take = False
                for el in data :
                    # print(el.getText(),"\n")
                    text = str(el.getText())
                    if next_take and text.replace(" ","") != "" :
                        medicine.howtouse = text
                        break
                    if text.lower().__contains__("directions for use"):
                        next_take = True
                    # else : 
                    #     #print(el.get_text())
                next_take = False
                First_take = True
                print("how to use, ",medicine.howtouse)
                medicine.description = ""
                for el in data :
                    text = str(el.getText())
                    if next_take :
                        if text.replace(" ","") != "" :
                            medicine.description = str(medicine.description) + str(",") + text
                            First_take = False
                        elif not First_take:
                            break
                    if text.__contains__('Product Specifications and Features:') or text.__contains__('Product Specifications & Features:'):
                        next_take = True
                print("medicine desc , ",medicine.description)
                next_take = False
                First_take = True
                for el in data :
                    text = str(el.getText())
                    if next_take :
                        if(text.replace(" ","") != "") :
                            medicine.content =  text
                            First_take = False
                            if el.find('br') != -1 or el.find('h') != -1 :
                                break
                        elif not First_take :
                            break
                    if text.lower().__contains__('key ingredients:'):
                        next_take = True
                print("medicine compoenets, ",medicine.content)


                next_take = False
                First_take = True
                for el in data :
                    text = str(el.getText())
                    if next_take :
                        if(text.replace(" ","") != "") :
                            medicine.sideeffect =  text
                            First_take = False
                            if el.find('br') != -1 or el.find('h') != -1 :
                                break
                        elif not First_take :
                            break
                    if text.lower().__contains__('side effects'):
                        next_take = True
                print("medicine SIde Effects, ",medicine.sideeffect)
                                       
                price_text = soup.find_all('div',{'class':'OtcPriceBox__atc-box___30PES'})
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
                print(price)
                
                medicine_details_for_save.append(medicine)
                medicine_details.append(model_to_dict(medicine))
                print(itr, " Done" )
                if itr >= terminate :
                    break    
            
        for obj in medicine_details_for_save :
            print(obj.medlink)
            medcheck  = "NULL"
            try : 
                medcheck = Medicine1mg.objects.get(name = obj.name)
            except:
                print("Added to Database")
                obj.save()
    except  Exception as inst:
        print(type(inst))    # the exception instance
        print(inst.args)     # arguments stored in .args
        print(inst) 
        try :
            if(data["searchby"] == "content"):
                content = []
                content.append(data["name"])
                return get_medicinebycontent(content,data['website'])
            elif(data["selected"] == False):
                return (get_medicine(data['name'], data['website']))
            elif(data["website"] != "1mg"):
                # find salt synonyms
                contents = findContentByMedicineName(data["name"], data["website"])
                print(contents)
                return (get_medicinebycontent(contents,data['website']))
            medicine = Medicine1mg.objects.filter(name = medicine_name)
            print(len(medicine))
            saltsynonyms = ""
            if len(medicine) > 0 : 
                saltsynonyms = medicine[0].content
            else : 
                print(medicine_name)
                medicine = Medicine1mg.objects.filter(name__startswith = medicine_name[0:2])   
                if(len(medicine) == 0) :
                    return []
                saltsynonyms = medicine[0].content    
            
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

        except Exception as inst:
            print(type(inst))    # the exception instance
            print(inst.args)     # arguments stored in .args
            print(inst) 

            return medicine_details
    print(medicine_details)
    return medicine_details
  

   
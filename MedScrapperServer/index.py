#  https://www.crummy.com/software/BeautifulSoup/bs4/doc/#contents-and-children

# https://www.skytowner.com/explore/extracting_attribute_values_in_beautiful_soup#:~:text=To%20extract%20attributes%20of%20elements,value%20of%20the%20id%20attribute.


# https://playwright.dev/docs/intro


from playwright.sync_api import sync_playwright 
from bs4 import BeautifulSoup
import re


class MedicineDetails:
    def __init__(self, name, price, imglink, content, sideeffect, manufacturer, howtouse, description, medlink):
        self.name = name
        self.price = price
        self.imglink = imglink
        self.content = content
        self.sideeffect = sideeffect
        self.manufacturer = manufacturer
        self.howtouse = howtouse
        self.description = description
        self.medlink = medlink  
    
    def printdetails(self):
        # print(f'Name: {self.name} \nPrice: {self.price} \nImage Link: {self.imglink} \nContent: {self.content} \nSide Effect: {self.sideeffect} \nManufacturer: {self.manufacturer} \nHow to use: {self.howtouse} \nDescription: {self.description} \nMedicine Link: {self.medlink}')
        print(f'Name: {self.name} \nPrice: {self.price} \nImage Link: {self.imglink is not None} \nContent: {self.content} \nSide Effect: {self.sideeffect is not None} \nManufacturer: {self.manufacturer} \nHow to use: {self.howtouse is not None} \nDescription: {self.description is not None} \nMedicine Link: {(self.medlink) is not None}')
        print()
    
    

with sync_playwright () as p:

    browser = p.chromium.launch(headless=True)

    page = browser.new_page()


    # 1mg site scrapping
    #search = input("w#hich medicine you want: ")
    
    """
    page.goto('https://www.1mg.com/search/all?name=aspirin')

    page.is_visible('#category-container > div > div.col-xs-12.col-md-10.col-sm-9.style__search-info-container___3s3zV > div:nth-child(2) > div.col-md-9 > div > div:nth-child(2) > div.row.style__grid-container___3OfcL') 
    html = page.inner_html("#category-container > div > div.col-xs-12.col-md-10.col-sm-9.style__search-info-container___3s3zV > div:nth-child(2) > div.col-md-9 > div > div:nth-child(2) > div.row.style__grid-container___3OfcL")
    """

    # pharmeasy scrapping starts from here

    page.goto('https://pharmeasy.in/search/all?name=aspirin')
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


    
    
    print("printing details --> pharmeasy")
    for obj in available_searched_medicine_pharmeasy:
        obj.printdetails()
        



    # netmeds Scappring starts from here
    page.goto('https://www.netmeds.com/catalogsearch/result/aspirin/all')
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


    

        
   



        
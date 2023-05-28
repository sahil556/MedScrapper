from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def trim_text(price) :
    temp = ""
    is_digit = False
    for c in price :
        if c.isdigit() :
            is_digit = True
            temp = temp + c
        elif c == "." and is_digit:
            temp = temp + c
        elif is_digit :
            break
    return float(temp)

def get_price_1mg(url) :
     with sync_playwright () as p:
                browser = p.chromium.launch(headless=False)
                page = browser.new_page()
                page.goto(url)        
                page.is_visible('#drug_header > div > div')
                html = page.inner_html('body')
                soup = BeautifulSoup(html,'html.parser')
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
                return price
    
def get_price_netmeds(url) :
      #will it scrap again?
      with sync_playwright () as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url)        
            page.is_visible("#maincontent > div.content-section > div.product-top > div.product-right-block > div.product-detail > h1")
            html = page.content()
            soup = BeautifulSoup (html, 'html.parser')
            price = soup.find('span',class_ = 'final-price').get_text()
            return price

def get_price_pharmeasy(url) :
    with sync_playwright () as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.goto(url)   
            page.is_visible('.LHS_container__mrQkM')
            html = page.inner_html('.LHS_container__mrQkM')
            soup = BeautifulSoup (html, 'html.parser')
            price = soup.find('div', {'class':'PriceInfo_ourPrice__jFYXr'}).getText()
            return price
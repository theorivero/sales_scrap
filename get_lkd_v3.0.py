import selenium
from selenium import webdriver
from optparse import Option
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from random import randint
from bs4 import BeautifulSoup 
import pymongo
from pymongo import MongoClient

#preciso fazer um jeito que o scroll pegue todas as empresas/ da para fazer com pgdn


cluster = MongoClient('mongodb+srv://theorivero:Intexfy1@cluster0-5wnru.mongodb.net/test?retryWrites=true&w=majority')
db = cluster['theodb']
collection = db['handles_linkedin']
options =  webdriver.ChromeOptions()
options.add_argument("--disable-notification")
driver=webdriver.Chrome("/home/theorivero/Documents/Projects/sales_scrap/chromedriver_linux64/chromedriver",chrome_options=options)
email = 'email@email.com.br'
pswd = 'senha'
industry = 32
url =f"https://www.linkedin.com/sales/search/company?geoIncluded=br%3A0&industryIncluded={industry}&page=1&searchSessionId=yF2kKErBQ5i9Xb9JGMFI%2Bg%3D%3D"



#star the browser using webdriver object
def startbrowser(driver):  
    driver.maximize_window()
    time.sleep(randint(3,5))
    driver.get("https://www.linkedin.com/uas/login?_l=pt")
    time.sleep(randint(3,5))
    return driver

def login(email,pswd, driver):
    driver.find_element_by_id("username").send_keys(email)
    driver.find_element_by_id("password").send_keys(pswd)
    time.sleep(randint(3,5))
    driver.find_element_by_tag_name("button").click()
    time.sleep(randint(3,5))

def opensales(driver):
    salesnav = driver.find_element_by_class_name("nav-item__icon")
    salesnav.click()
    time.sleep(randint(3,5))
    driver.get(url)
    time.sleep(randint(3,5))

def n_companies(driver):
    n = driver.find_element_by_class_name("artdeco-tab-primary-text").text  
    try: 
        n = n.replace('.','')
    except:
        pass
    return int(n)

def simpleget(driver,url,n_companies):
    time.sleep(5)
    driver.get(url)
    #driver.find_element_by_id("ember118").click()
    maxurl = int((n_companies/25)+ 1) 
    for c in range(1,66):
        article_list = []        
        time.sleep(randint(5,10))
        page = driver.find_element_by_tag_name("html")
        page.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        page.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        page.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        page.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        page.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        page.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
        page.send_keys(Keys.PAGE_DOWN)
        page.send_keys(Keys.PAGE_DOWN)
        page.send_keys(Keys.PAGE_DOWN)
        page.send_keys(Keys.END)
        time.sleep(randint(3,5))
        
        soup = BeautifulSoup(driver.page_source,'lxml')
        
        time.sleep(randint(7,11))

        truearticle = soup.find('ol', class_="search-results__result-list")
        nana = 1
        try:    
            for article in truearticle.find_all('article'):
                nana +=1
                try:
                    company = article.dl.dt.a.text
                    company = company.replace('            ','')
                    company = company.replace('\n\n','')
                except:
                    company = 'None'
                try:    
                    industry_type = article.find('li', class_="result-lockup__misc-item").text
                except:
                    industry_type = 'None'
                try:        
                    func_range = article.find('a', class_="result-lockup__undecorated-link ember-view").text
                    func_range = func_range.replace('                ','')
                    func_range = func_range.replace('\n','')
                except:
                    func_range = 'None' 
                try:
                    place = article.find('ul', class_="mv1 Sans-12px-black-60% result-lockup__misc-list").text
                    place = place.replace(f'\n{industry_type}\n\n                {func_range}\n \n','')
                    place = place.replace('\n','')

                except:
                    place= 'None'
                handle = article.find('a', class_="result-lockup__view-account-link ember-view")['href']
                addmongo={
                    "handle" : handle,
                    "company" :company,
                    "industry" :industry_type,
                    "number_of_employees" : func_range,
                    "address" : place

                }
                article_list.append(addmongo)

        except Exception as e:
            print(e)
            break
        print(f'page:{c}, qnt na pagina:{len(article_list)}')
        if c == 40:
            site = url.split('page=1')
            url = site[0]+"page=41"+site[1] 
            driver.get(url)
        else:       
            next_page = driver.find_element_by_class_name("search-results__pagination-next-button")
            next_page.click()
            
     

startbrowser(driver)
login(email,pswd, driver)
opensales(driver)
time.sleep(3)
n_companies = n_companies(driver)
if n_companies <= 1625:
    simpleget(driver,url,n_companies)


driver.quit()


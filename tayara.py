import requests
from bs4 import BeautifulSoup as bs
import mysql.connector
import datetime
import time
import re

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs

base_url = "https://www.tayara.tn/search/?category=Immobilier"



service = Service('./chromedriver.exe')


driver = webdriver.Chrome(service=service)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="coupedemonde2010",
    database="menzili"
)

def insert_data(title, location, chambre, price, contact):
    cursor = db.cursor()
    sql = "INSERT INTO house (title, location, chambre, price, contact, date_added) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (title, location, chambre,  price, contact, datetime.datetime.now())

    try:
        cursor.execute(sql, val)
        db.commit()
        
    except mysql.connector.Error as error:
        print("Failed to insert record into MySQL table: {}".format(error))

def delete_old_records():
    cursor = db.cursor()
    one_month_ago = datetime.datetime.now() - datetime.timedelta(days=30)
    sql = "DELETE FROM house WHERE date_added < %s"
    val = (one_month_ago,)

    try:
        cursor.execute(sql, val)
        db.commit()
        print(f"{cursor.rowcount} old records deleted.")
    except mysql.connector.Error as error:
        print("Failed to delete old records from MySQL table: {}".format(error))

def house_scrap():
  

        delete_old_records() 

        response = base_url
        url = requests.get(response)
        soup = bs(url.content, 'lxml')
        houses = soup.find_all('article', {'class': 'mx-auto'})
        contact = ""
        for house in houses:
                title = house.find("h2", {"class": "card-title"}).text.strip()
                
                locations = house.find('span', class_='line-clamp-1 truncate text-3xs md:text-xs lg:text-xs w-3/5 font-medium text-neutral-500')
                location_text = locations.text.strip()
                location = location_text.split(',')[0]

                price_element = house.find('data', {'class': 'text-red-600 font-bold font-arabic undefined'})
                if price_element is not None:
                        price = price_element.get('value')
                        
                else:
                    price=None
                    print( 'Price not found') 
                details_url = house.find('a')['href']  
              
                details_content = requests.get("https://www.tayara.tn"+str(details_url)).content
                details_soup = bs(details_content, 'lxml')
                driver.get("https://www.tayara.tn" + str(details_url))
                wait = WebDriverWait(driver, 60)  
                try:
                    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn[aria-label="Afficher numéro"]')))
                    time.sleep(15)  

                    button.click()

                   
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.w-full a[href^="tel:"]')))

                   
                    html = driver.page_source

                    
                    soup = bs(html, 'html.parser')

                  
                    phone_element = soup.find('a', href=lambda href: href and href.startswith('tel:'))

                    if phone_element:
                        contact = phone_element['href'][4:]  
                        #print('Phone number:', phone_number)
                    else:
                        print('Phone number not found.')

                except:
                    print('Button not found or element became stale. Skipping to the next house.')
                    continue

                try:
                    bedrooms_elem = details_soup.find('span', text='Chambres')
                    bedrooms_num = bedrooms_elem.find_next('span', {'class': 'text-gray-700 text-xs font-medium'}).text
                except AttributeError:
                    bedrooms_num = 'N/A'
                chambre=bedrooms_num+" Chambres"
                insert_data(title, location, chambre , price, contact)
        print(f"{len(houses)} records inserted for page ")    

if __name__=="__main__":
  while True:
    house_scrap()
    driver.quit()
    time.sleep(36000)
  
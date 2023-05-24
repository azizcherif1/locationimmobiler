import mysql.connector
import requests
from bs4 import BeautifulSoup as bs
import datetime
import time
import re

base_url = "https://www.tunisiapromo.com/recherche?page="
num_pages = 5
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
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

def house_scrap() :
    delete_old_records()
    for page_number in range(1, num_pages + 1): 
        
        response = base_url + str(page_number)
        url = requests.get(response)
        soup = bs(url.content, 'lxml')
        houses = soup.find_all('article', class_='short_ad_panel')
        for house in houses:
            
            titre_element = house.find('a',class_='headline')
            if titre_element is not None:
                title = titre_element.text
                #print(f"Titre : {titre}")
            else:
                print("Titre : None")
            prix_element = house.find('div', class_='property_price mtop')
            if prix_element is not None:
                price=prix_element.find('span',class_='price').text.strip()
                #print(f"Prix {prix}")
            else:
                 print("prix : None")
                   
            location_element = house.find('div', class_='property_location mtop')
            
            if location_element is not None:
                
                location = location_element.b.text.strip().replace(" /", ",")

                #print(f"location : {location}")
            else:
               # print("location : none")    
              pass

            details_url = house.find('a', href=True).get('href') if house.find('a', href=True) else None

            details_content = requests.get("https://www.tunisiapromo.com/"+str(details_url)).content
            details_soup = bs(details_content, 'lxml')
            
            try:    
                    
                    bedrooms_elem = details_soup.select_one('div[style="width:33%;float:left"]')
                    if bedrooms_elem:
                        chambre_num = bedrooms_elem.get_text(strip=True)
                        
                    else:
                        print("Value element not found.")
                    
            except AttributeError:
                    bedrooms_num = 'N/A'
            chambre=chambre_num+" Chambres"
            
            contact=""
            
          
            insert_data(title, location, chambre, price, contact)
        
        print(f"{len(houses)} records inserted for page {page_number}.")

            
house_scrap()
import requests
from bs4 import BeautifulSoup as bs
import mysql.connector
import datetime
import time
import re
base_url = "https://www.menzili.tn/immo/location-immobilier-tunisie?page="
num_pages = 20

# Connect to the MySQL database
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
def house_scrap() :
            
                delete_old_records()

                for page_num in range(1, num_pages + 1):
                    response = base_url + str(page_num)
                    url = requests.get(response)
                    soup = bs(url.content, 'lxml')
                    houses = soup.find_all('div', {'class': 'row li-item-list'})
                    contact = ""
                    for house in houses:
                        title = house.find("h4", {"class": "li-item-hidden"}).text.strip()
                        my_location = house.find('p').text.strip()
                        info = house.find('div', {'class': 'row li-list-item-info'})
                        
                        price_element = house.find('div', {'class': 'item-box'}).find('span', {'class': 'item-box-price pull-right'})
                        price_text = price_element.text.strip().split('/')[0].strip()
                        price = ''.join(filter(str.isdigit, price_text))
                    # price = ''.join(filter(str.isdigit, price_text))



                        contact = "" 
                        # Get the URL of the details page
                        details_url = house.find('a')['href']
                        
                        # Retrieve the HTML content of the details page
                        details_content = requests.get(details_url).content
                        details_soup = bs(details_content, 'lxml')
                        # Parse the details page content using BeautifulSoup
                        phone_element = details_soup.find('div', class_='col-md-12 col-xs-12 col-sm-12 block-2')
                        if phone_element is None:
                            continue

                        phone_element = phone_element.find('span', class_='btn')
                        if phone_element is None:
                            continue

                        contact = phone_element.get_text(strip=True)

                        chambre = info.find("span", {"class": "block-opt-2"})
                        if chambre is not None and "Chambres" in chambre.find("span", {"class": "info-text option-text"}).text:
                            chambre_text = chambre.get_text().replace(" ", "")
                            my_chambre = chambre_text.split()[0]
                        else:
                            my_chambre = None

                        if my_chambre is not None:
                            insert_data(title, my_location, my_chambre if my_chambre is not None else "not mentioned", price, contact)

                        
                        
                    
                        

                    print(f"{len(houses)} records inserted for page {page_num}.")

if __name__=="__main__":
  while True:
    house_scrap()
    time.sleep(36000)

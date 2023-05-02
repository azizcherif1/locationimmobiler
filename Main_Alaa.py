import mysql.connector
import requests
from bs4 import BeautifulSoup



db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="location_immobilier"
)

cursor = db.cursor()

url = "https://www.mubawab.tn/fr/sc/appartements-a-louer"

for i in range(1, 2):
    page_url = f"{url}:p:{i}"
    response = requests.get(page_url)
    soup = BeautifulSoup(response.content, "html.parser")
    for ad in soup.find_all(class_="listingBox w100"):
        title = ad.find(class_="listingTit").get_text().strip()
        location = ad.find(class_="listingH3").get_text().strip().replace('\n', '').replace('\t', '').split()
        location = ' '.join(location)
        price_tag = ad.find('span', class_='priceTag')
        price = price_tag.text.strip()
        price = price.replace('\xa0', ' ')
        features = [f.get_text().strip() for f in ad.find_all(class_="listingH4 floatR")]
        
        # insert data into database
        sql = "INSERT INTO table_imm (title, location, price, features) VALUES (%s, %s, %s, %s)"
        val = (title, location, price, ','.join(features))
        cursor.execute(sql, val)
        db.commit()
        
db.close()

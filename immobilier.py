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

url = "https://www.tunisiapromo.com/location"

for page_number in range(1, 801): 
    url = f"https://www.tunisiapromo.com/location?page={page_number}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    titres_elements = soup.find_all('a', class_='headline')
    for titre_element in titres_elements:
        titre = titre_element.text.strip()
        prix_element = titre_element.find_next('span', class_='price')
        prix = prix_element.text.strip() if prix_element else 'Prix non disponible'
        location_element = titre_element.find_parent().find('div', class_='property_location')
        location = location_element.find('b').text.strip() if location_element and location_element.find('b') else 'Location non disponible'
        description_element = titre_element.find_next('p', class_='listing-description')
        description = description_element.text.strip() if description_element else 'Description non disponible'
        nbchambres_element = titre_element.find_next('p', class_='listing-description')

        print(f"Titre : {titre}")
        print(f"Prix : {prix}")
        print(f"Description : {description}")
        print(f"Location : {location}\n")

        
        # insert data into database
        sql = "INSERT INTO table_imm (Titre, Prix, Description, Location) VALUES (%s, %s, %s, %s)"
        val = (Titre, Prix,nbchambres, Description, ','.join( Location))
        cursor.execute(sql, val)
        db.commit()
        
db.close()
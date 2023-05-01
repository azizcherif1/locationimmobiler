import mysql.connector
import requests
from bs4 import BeautifulSoup


# Fonction pour insérer une annonce dans la base de données
def insert_annonce(titre, adresse, prix, surface):
    # Connexion à la base de données
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="location"
    )

    # Exécution d'une requête d'insertion avec les données de l'annonce
    cursor = db.cursor()
    query = "INSERT INTO annonces (titre, adresse, prix,surface ) VALUES (%s, %s, %s, %s)"
    values = (titre, adresse, prix, surface)
    cursor.execute(query, values)

    # Validation de la transaction et fermeture de la connexion
    db.commit()
    cursor.close()
    db.close()


# URL de la page à extraire
for page in range(1, 6):
    url = f"https://www.remax.com.tn/location-appartement#mode=gallery&tt=260&cr=2&mpts=1744519&pt=1744519&cur=TND&la=All&sb=MostRecent&page={page}&sc=1048&sid=7e6fd428-3ad7-4e60-aec1-1d113cdb5f08"

    # Envoyer une requête GET au site web et obtenir le contenu de la page
    response = requests.get(url)
    html_content = response.content

    # Analyser le contenu HTML avec Beautiful Soup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Trouver toutes les annonces sur la page
    annonces = soup.find_all('div', {'class': 'gallery-item'})

    # Extraire les données de chaque annonce et les insérer dans la base de données
    for annonce in annonces:
        titre = annonce.find(
            'div', {'class': 'gallery-transtype'}).text.strip()
        adresse = annonce.find('div', {'class': 'gallery-title'}).a['title']
        prix = annonce.find('span', {'class': 'gallery-price-main'}).find('a', {'class': 'proplist_price'}).text.strip()
        surface = annonce.find('span', {'class': 'gallery-attr-item-value'})
        surface = surface.text.strip() if surface else None

        # Insérer l'annonce dans la base de données
        insert_annonce(titre, adresse, prix, surface)

import mysql.connector


def filtrer_annonces(donnees_annonces, filtres):
    annonces_filtrees = []
    for annonce in donnees_annonces:
        if "prix_min" in filtres and int(annonce["prix"].replace(",", "")) < filtres["prix_min"]:
            continue
        if "prix_max" in filtres and int(annonce["prix"].replace(",", "")) > filtres["prix_max"]:
            continue
        if "surface_min" in filtres and int(annonce["surface"].replace(" m²", "")) < filtres["surface_min"]:
            continue
        if "surface_max" in filtres and int(annonce["surface"].replace(" m²", "")) > filtres["surface_max"]:
            continue
        annonces_filtrees.append(annonce)
    return annonces_filtrees


def trier_annonces(annonces, critere_tri):
    annonces_triees = sorted(annonces, key=lambda annonce: annonce["prix"].replace(
        ",", "").replace("TND", "").strip(), reverse=True)

    return annonces_triees


# Connexion à la base de données MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="location"
)

# Récupération des annonces depuis la table "annonces"
cursor = db.cursor()
query = "SELECT titre, adresse, prix, surface FROM annonces"
cursor.execute(query)
result = cursor.fetchall()

# Stockage des annonces dans une liste de dictionnaires
donnees_annonces = []
for annonce in result:
    titre, adresse, prix, surface = annonce
    donnees_annonces.append(
        {"titre": titre, "adresse": adresse, "prix": prix, "surface": surface})

# Filtrage des annonces selon les critères
filtres = {"prix_min": 500, "prix_max": 1000,
           "surface_min": 50, "surface_max": 100}
annonces_filtrees = filtrer_annonces(donnees_annonces, filtres)

# Tri des annonces par ordre croissant de prix
annonces_triees = trier_annonces(annonces_filtrees, "prix")

# Affichage des annonces triées
for annonce in annonces_triees:
    print(
        f"Titre: {annonce['titre']}, Adresse: {annonce['adresse']}, Prix: {annonce['prix']}, Surface: {annonce['surface']}")

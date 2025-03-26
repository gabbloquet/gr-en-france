import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# URL de base
URL_BASE = "https://www.gr-infos.com/gr-fr.htm"

# Récupération de la page principale
response = requests.get(URL_BASE)
soup = BeautifulSoup(response.text, "html.parser")

# Trouver les liens vers les fiches détaillées des GR
gr_links = soup.select("a[href^='gr'][href$='.htm']")

# Stockage des données
gr_data = []

for link in gr_links:
    gr_url = "https://www.gr-infos.com/" + link["href"]
    gr_name = link.text.strip()

    # Ouvrir la page du GR
    gr_page = requests.get(gr_url)
    gr_soup = BeautifulSoup(gr_page.text, "html.parser")

    # Extraction des paragraphes contenant les infos (distance, dénivelé, etc.)
    infos = gr_soup.find_all("p")
    details = " ".join([info.text.strip() for info in infos])

    # Extraction des valeurs spécifiques avec regex
    distance_match = re.search(r"Distance[:\s]+([\d,]+)\s?km", details)
    denivele_match = re.search(r"Dénivelé cumulé montée[:\s]+([\d,]+)\s?m", details)
    location_match = re.search(r"(?i)(?:région|traverse)\s*[:\-]?\s*([A-Za-zÀ-ÿ\s\-]+)", details)

    distance = distance_match.group(1) if distance_match else ""
    denivele = denivele_match.group(1) if denivele_match else ""
    localisation = location_match.group(1).strip() if location_match else ""

    # Conversion en float et correction des nombres
    try:
        distance = float(distance.replace(",", ".")) if distance else 0
        denivele = float(denivele.replace(",", ".")) if denivele else 0

        # Calcul des km effort
        km_effort = distance + (denivele / 100)

        # Nombre de jours en supposant 25 km effort par jour
        jours = round(km_effort / 25, 1) if km_effort > 0 else ""
    except ValueError:
        distance, denivele, jours = "", "", ""

    # Ajouter aux données
    print(f"GR ajouté : {gr_name} - Distance : {distance} kms")
    gr_data.append({
        "Nom": gr_name,
        "Distance (km)": distance,
        "Dénivelé (m)": denivele,
        "Localisation": localisation,
        "Nombre de jours": jours,
        "Réalisé": "",
        "Lien PDF": "",
        "Lien": gr_url
    })

# Convertir en DataFrame Pandas
df = pd.DataFrame(gr_data)

# Suppression des lignes vides (celles qui n'ont pas de distance)
df = df[df["Distance (km)"] > 0]

# Remplacement des points par des virgules pour Google Sheets
df["Distance (km)"] = df["Distance (km)"].astype(str).str.replace(".", ",")
df["Dénivelé (m)"] = df["Dénivelé (m)"].astype(str).str.replace(".", ",")
df["Nombre de jours"] = df["Nombre de jours"].astype(str).str.replace(".", ",")

# Sauvegarde en CSV avec un séparateur `;` pour Google Sheets
df.to_csv("gr_infos.csv", index=False, encoding="utf-8", sep=";")

print("Scraping terminé pour le site GR Infos, fichier CSV formaté généré !")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import time
import pandas as pd
import re

# URL de base
URL_BASE = "https://www.mongr.fr/trouver-prochaine-randonnee/carte?duree=4-6"

service = Service('/Users/gabinbloquet/Documents/chromedriver-mac-arm64/chromedriver')
driver = webdriver.Chrome(service=service)

# Ouvrir la page
driver.get(URL_BASE)
time.sleep(1)

# Accepter les cookies
accept_button = driver.find_element(By.ID, "axeptio_btn_acceptAll")
accept_button.click()
time.sleep(1)

# Effectuer un zoom avant sur la carte
driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3);")
time.sleep(1)
zoom_in_button = driver.find_element(By.XPATH, "//div[@class='esriSimpleSliderIncrementButton' and @title='Zoom avant']")
zoom_in_button.click()
zoom_in_button.click()  # Vous pouvez ajouter plus de clics si vous voulez un zoom plus important
time.sleep(2)  # Attendre que la carte soit bien zoomée

# Chercher les éléments image avec xlink:href correspondant au GreenPin1LargeB
image_elements = driver.find_elements(By.TAG_NAME, "image")
for img in image_elements:
    print(img.get_attribute('xlink:href'))

# Afficher les éléments trouvés
print(f"Nombre d'éléments image trouvés : {len(image_elements)}")

gr_data = []

# Interagir avec chaque élément image trouvé
# Initialisation de la liste des données GR
gr_data = []

# Boucle pour interagir avec chaque élément image trouvé
for index, image in enumerate(image_elements):
    print(f"Image {index + 1} trouvée aux coordonnées x={image.get_attribute('x')} et y={image.get_attribute('y')}")

    try:
        # Cliquer sur l'image (point de repère)
        ActionChains(driver).move_to_element(image).click().perform()
        time.sleep(2)  # Attendre que le contenu se charge

        # Extraire les informations sur la randonnée
        try:
            # Nom du GR (titre de l'ancre)
            gr_name = driver.find_element(By.XPATH, "//h3[@class='title']").text.strip()

            # Départ et arrivée
            start_point = driver.find_element(By.XPATH, "//div[@class='start-point']/span").text.strip()
            end_point = driver.find_element(By.XPATH, "//div[@class='end-point']/span").text.strip()

            # Distance et durée
            distance = driver.find_element(By.XPATH, "//div[@class='distance']/span").text.strip()
            duration = driver.find_element(By.XPATH, "//div[@class='duree']/span").text.strip()

            # Ajouter les informations extraites dans la liste
            gr_data.append({
                "Nom": gr_name,
                "Départ": start_point,
                "Arrivée": end_point,
                "Distance": distance,
                "Durée": duration,
                "Lien": driver.current_url
            })

            print(f"GR trouvé: {gr_name}, Distance: {distance}, Durée: {duration}, Départ: {start_point}, Arrivée: {end_point}")

            # Revenir à la carte après avoir récupéré les informations
            ActionChains(driver).move_to_element(image).click().perform()

        except Exception as inner_e:
            print(f"Erreur lors de l'extraction des informations de la randonnée pour l'image {index + 1}: {inner_e}")
            # Fermer la fenêtre d'info si elle est ouverte (pour éviter un blocage)
            try:
                close_button = driver.find_element(By.XPATH, "//a[@class='esriPopupClose']")
                close_button.click()
                time.sleep(1)
            except Exception as close_e:
                print(f"Erreur lors de la fermeture de la fenêtre d'info: {close_e}")
            continue  # Passer à l'image suivante

    except Exception as e:
        print(f"Erreur lors de l'interaction avec l'image {index + 1}: {e}")

# Sauvegarde des données dans un fichier CSV
df = pd.DataFrame(gr_data)
df.to_csv("mon-gr.csv", index=False, encoding="utf-8", sep=";")

print("Scraping terminé, fichier CSV généré avec succès.")

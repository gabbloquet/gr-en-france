# Scraping des Informations de Randonnée GR en France

Ce projet contient des scripts Python permettant de récupérer des informations sur les randonnées GR® (sentiers de Grande Randonnée) en France depuis plusieurs sources en ligne, principalement le site **Mon GR** (https://www.mongr.fr), ainsi que d'autres informations accessibles depuis **GR Infos** (https://www.gr-infos.com/gr-fr.htm).

J'ai créé ce projet parce qu'il était fastidieux de naviguer entre plusieurs sites pour trouver facilement une randonnée GR en fonction de critères comme la distance ou le nombre de jours. Plutôt que de faire des recherches manuelles sur différents sites, l'idée ici est d'automatiser le processus pour récupérer ces informations de manière structurée et centralisée, facilitant ainsi la recherche d'une randonnée GR qui correspond aux préférences d'un utilisateur.

## Structure du Projet

Le projet contient deux scripts principaux :

1. **`scraper-mon-gr.py`** : Ce script permet de récupérer les informations des randonnées en utilisant les points affichés sur la carte du site Mon GR.
2. **`scraper-gr-infos.py`** : Ce script est utilisé pour extraire des informations supplémentaires (comme la description complète) sur les randonnées GR à partir des pages détaillées disponibles après avoir cliqué sur les points de repère sur la carte.

## Prérequis

Avant d'exécuter ces scripts, assurez-vous d'avoir installé les dépendances suivantes :

- **Python 3.x** (si ce n'est pas déjà fait, vous pouvez télécharger Python depuis [python.org](https://www.python.org/downloads/))
- **ChromeDriver** : Le pilote Selenium pour Chrome, à télécharger depuis [ici](https://sites.google.com/a/chromium.org/chromedriver/downloads) et à placer dans un dossier accessible.
- **Bibliothèques Python** :
  Vous devez installer les bibliothèques nécessaires. Vous pouvez le faire en utilisant `pip` :

  ```bash
  pip install selenium pandas
  ```

## Instructions d'Utilisation

### 1. Téléchargement de ChromeDriver

Téléchargez la version de **ChromeDriver** qui correspond à votre version de **Google Chrome**. Après l'avoir téléchargé, placez-le dans un dossier que vous pouvez facilement référencer dans votre script.

Modifiez la ligne suivante dans les scripts pour pointer vers votre ChromeDriver local :

```python
service = Service('/chemin/vers/chromedriver')  # Remplacez par le chemin correct
```

### 2. Utilisation du Script `scraper-mon-gr.py`

Ce script collecte des informations sur les randonnées affichées sur la carte Mon GR. Il détecte les points de repère sur la carte, clique dessus et récupère des informations telles que le nom de la randonnée, la durée, la distance, le départ, et l'arrivée.

#### Étapes d'exécution :
1. Ouvrez le fichier `scraper-mon-gr.py`.
2. Modifiez l'URL de base si nécessaire (`URL_BASE`).
3. Exécutez le script :

   ```bash
   python scraper-mon-gr.py
   ```

4. Le script va :
    - Accéder à la carte des randonnées.
    - Cliquer sur les points de repère pour récupérer les informations.
    - Enregistrer ces informations dans un fichier CSV appelé `mon-gr.csv`.

#### Résultats :
Un fichier CSV avec les informations des randonnées est généré, contenant les colonnes suivantes :
- **Nom** : Le nom de la randonnée.
- **Départ** : Le point de départ.
- **Arrivée** : Le point d'arrivée.
- **Distance** : La distance de la randonnée en km.
- **Durée** : Le nombre de jours de la randonnée.
- **Lien** : L'URL de la page avec les détails.

### 3. Utilisation du Script `scraper-gr-infos.py`

Ce script est utilisé pour collecter des informations supplémentaires à partir des pages détaillées des randonnées. Après avoir cliqué sur un point de repère sur la carte, ce script récupère des informations comme la description complète, les avis, et plus encore.

#### Étapes d'exécution :
1. Ouvrez le fichier `scraper-gr-infos.py`.
2. Exécutez le script :

   ```bash
   python scraper-gr-infos.py
   ```

3. Le script va extraire les informations détaillées sur chaque randonnée et les enregistrer dans un fichier CSV (par exemple, `gr-infos.csv`).

## Gestion des Erreurs

Les scripts gèrent les erreurs potentielles telles que :
- Si un point de repère n'est pas cliquable ou si l'élément est absent.
- Si certaines informations ne peuvent pas être extraites de la page.
- Les exceptions sont capturées et imprimées dans la console pour faciliter le débogage.

### 4. Format du Fichier CSV

Les fichiers CSV générés par les scripts auront les colonnes suivantes :

#### `mon-gr.csv` :
- **Nom** : Nom de la randonnée GR.
- **Départ** : Lieu de départ de la randonnée.
- **Arrivée** : Lieu d'arrivée de la randonnée.
- **Distance** : Distance en kilomètres.
- **Durée** : Durée en jours.
- **Lien** : Lien vers la page de la randonnée.

#### `gr-infos.csv` :
- **Nom** : Nom de la randonnée GR.
- **Description** : Description complète de la randonnée.
- **Avis** : Notes et avis des utilisateurs (si disponibles).
- **Détails supplémentaires** : Toute autre information extraite.

## Contribuer

Si vous souhaitez améliorer ce projet, n'hésitez pas à soumettre des pull requests ! Toute amélioration est bienvenue, que ce soit pour la gestion des erreurs, les performances du script, ou l'ajout de nouvelles fonctionnalités.

## Auteurs

- **Gabin BLOQUET** - *Créateur du projet*
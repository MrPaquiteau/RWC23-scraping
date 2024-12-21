"""
Créer l'ensemble des 40 CSV nécessaire au choix 2 dans le menu (temps d'éxécution minimum 20 minutes)
"""

# Dans la console de commande pour installer selenium :
# pip install selenium==3.141.0
# OU, de meilleur manière :
# conda install -c conda-forge selenium
# conda install -c conda-forge tabulate

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
from selenium.common.exceptions import NoSuchElementException
import urllib.request
import pandas as pd
import numpy as np
import time
from tabulate import tabulate
import platform
import os

def exec():
    """
   Crée les fichiers CSV requis pour les choix dans le menu.
   Le temps d'exécution est entre 20 et 40 minutes.

    Cette fonction rassemble les données des équipes participant à la Coupe du
    Monde de Rugby 2023 à partir du site officiel. Elle récupère les noms des
    équipes, les images, les joueurs, et leurs statistiques, puis génère des
    fichiers CSV organisés par équipes et par statistiques des joueurs.

    Dépendances,
        Assurez-vous d'avoir les bibliothèques nécessaires installées :
            - selenium==3.141.0
            - tabulate
            - beautifulsoup4
            - pandas
            - numpy

    :return: Message de complétion après l'exécution
    """
    # Prend en entrée le nom d'une équipe et ajoute à un dataframe le nom de cette équipe puis tout les urls des joueurs
    def recup_url_players(df):
        """
        Parameters
        ----------
        df : DataFrame
            DataFrame destiné a contenir les informations de l'équipe,
            et les urls des ses joueurs.

        Returns
        -------
        temp : Series
            Liste contenant l'identifiant de l'équipe, le nom de l'équipe,
            l'image de l'équipe, et la liste des URL des joueurs de l'équipe..

        """
        url = "https://www.rugbyworldcup.com/2023/teams/" + df["Name"]
        page = urllib.request.urlopen(url)
        soup = bs(page, "html.parser")
        identifier = soup.find("span", class_="widget__title--short u-show-phablet")
        identifier = identifier.text
        player_team = soup.find_all("a", {"class": "squad-list__player"})
        temp = [identifier, df["Name"], df["Image"]]
        url_players = []
        for elt in player_team:
            url_players.append("https:"+elt.get("href"))
        temp.append(url_players)
        return temp


    def cutting(dataframe, liste):
        """
        Découpe et structure les données du DataFrame en utilisant une liste de
        séparateurs.

        Parameters
        ----------
        dataframe : DataFrame
            DataFrame à traiter.
        liste : TYPE
            Liste de séparateurs pour découper les données du DataFrame..

        Returns
        -------
        temp : Liste
            Liste résultantes après le découpage.

        """
        cut = []
        for elt in dataframe:
            if any(elt in i for i in liste):
                for x in liste:
                    if elt in x:
                        cut.extend([elt, x.split(elt)[1].title()])
                        break
            else:
                cut.extend([elt, np.nan])

        temp = []
        for j in range(0, len(cut)):
            if j % 2 == 0:
                temp.append(cut[j+1])
        return temp


    options = Options()
    options.add_argument("--headless")  # ne pas afficher les pages à l'écran
    options.set_preference("permissions.default.image", 2)  # 2 pour ne pas charger les images


    if platform.system() == "Windows":
        geckodriver_path = r"geckodriver.exe"  # Spécifié le bon chemin
        options.binary_location = r"C:\Program Files\Mozilla Firefox\firefox.exe"  # Pareil
    elif platform.system() == "Darwin":
        geckodriver_path = r"usr//local//bin//geckodriver"


    profile = webdriver.FirefoxProfile()  # utiliser firefox
    profile.set_preference("intl.accept_languages", "en-US")  # Le site charge en anglais
    # -----------------------------------------------------------------------------

    # Récupération des noms des équipes
    url = "https://www.rugbyworldcup.com/2023/teams"
    page = urllib.request.urlopen(url)
    soup = bs(page, "html.parser")
    tag_team = soup.find_all("h2", {"class": "card__title article-list__title"})
    tag_image = soup.find_all("img", {"class": "article-list__image"})
    # Ecriture des noms dans un dataframe
    name_team = pd.DataFrame(columns=["Name", "Image"])
    for i in range(len(tag_team)):
        name_team.loc[len(name_team)] = [tag_team[i].text.strip().replace(" ", "-"), tag_image[i].get("data-src")]

    if not os.path.exists("CSV_files"):
        os.mkdir("CSV_files")

    # Table equipe inclus la liste de toutes les url de joueurs de l'equipe en question
    table_team = pd.DataFrame(columns=["Id", "Country", "Image", "List of URL"])
    for index, row in name_team.iterrows():
        table_team.loc[len(table_team)] = recup_url_players(row)
    
    table_team[["Id", "Country", "Image"]].to_csv("CSV_Files//country_data.csv", index=False)

    table_team["Drapeau"] = table_team["Id"].apply(lambda x: f"https://www.rugbyworldcup.com/rwc2023-resources/prod/rwc2023_v6.6.0/i/elements/team-badges/{x}.png")

    # Lancement de firefox (attention le lancement sera en arrière plan si la ligne 23 est activé)
    driver = webdriver.Firefox(executable_path=geckodriver_path, options=options, firefox_profile=profile)

    driver.get(table_team["List of URL"][0][0])

    tag_column_stats = driver.find_elements(By.CLASS_NAME, "player-stats__line-label")

    column_stats= [element.text.title().replace("\n", "").replace(":", "").replace("-", "")for element in tag_column_stats]
    column_stats = [element for element in column_stats if element != ""]
    column_stats.insert(0, "Id_Player")
    driver.close()
    # Création du dataframe pour récuperer les infos des joueurs
    table_infos_players = pd.DataFrame(columns=["Id", "Country", "Name", "Hometown", "Position",
                                                "Age", "Height", "Weight", "Photo"])

    df_stats_players = pd.DataFrame(columns=column_stats)


    # Récupération des données des joueurs et ajout au dataframe
    for index, row in table_team.iterrows():
        start_time = time.time()
        num_id = 0
        driver = webdriver.Firefox(executable_path=geckodriver_path, options=options, firefox_profile=profile)
        for url in row["List of URL"]:
            num_id += 1
            id_player = f"{row['Id']}-{num_id}"
            country = []
            country.append("Country"+row["Country"])
            name_player = []
            driver.get(url)
            time.sleep(0.8)
            # recherche/selection des éléments avec comme balise CSS : ".player-hero__player-name"
            tag_name = driver.find_element(By.CSS_SELECTOR, ".player-hero__player-name")

            # Execution d'un script jvs : "return arguments[0].textContent;", qui recupere le texte de "balise_name"
            name = driver.execute_script("return arguments[0].textContent;", tag_name).replace("\n", "")
            name_player.append("Name"+name)

            # Reherche tout les elements avec la class 'player-hero__item'
            tag_infos = driver.find_elements(By.CSS_SELECTOR, ".player-hero__item")
            infos = [element.text.title().replace("\n", "").replace(":", "").replace("-", "")for element in tag_infos]
            infos = [element for element in infos if element != ""]
            infos = name_player + infos
            infos = country + infos
            infos.insert(0, "Id" + id_player)

            tag_stats = driver.find_elements(By.CSS_SELECTOR, ".player-stats__line")
            stats = [element.text.title().replace("\n", "").replace(":", "").replace("-", "")for element in tag_stats]
            stats = [element for element in stats if element != ""]
            stats.insert(0, "Id_Player" + id_player)

            # Si l'élément est trouvé, ajoute la photo
            try:
                # le finder des balise contenant les photos de joueurs
                tag_photo = driver.find_element(By.CSS_SELECTOR, ".player-headshot__img")
                photo = driver.execute_script("return arguments[0].getAttribute('src');", tag_photo)
            # executer quand pas d'image trouvé, "NoSuchElementException" erreur renvoyer par le finder
            except NoSuchElementException:
                photo = "https://www.pngkit.com/png/full/349-3499519_person1-placeholder-imagem-de-perfil-anonimo.png"

            # découpage d'infos pour chaque joueur
            stats_players = cutting(df_stats_players, stats)
            players_infos = cutting(table_infos_players, infos)

            players_infos[-1] = photo

            df_stats_players.loc[len(df_stats_players)] = stats_players

            table_infos_players.loc[len(table_infos_players)] = players_infos
            driver.delete_all_cookies()
        end_time = time.time()
        print(f"{row['Country']} {end_time-start_time}")
        driver.close()

    table_infos_players.set_index("Id", inplace=True)
    df_stats_players.set_index("Id_Player", inplace=True)

    table_infos_players.to_csv(r"CSV_Files//all_players.csv")
    df_stats_players.to_csv(r"CSV_Files//all_players_stats.csv")

    grouped = table_infos_players.groupby("Country")
    dico_team = {f"players_{key}": group for i, (key, group) in enumerate(grouped)}

    for cle, valeur in dico_team.items():
        valeur.to_csv(fr"CSV_files//{cle}.csv")

    grouped_stats = df_stats_players.groupby(by=lambda x: x[:3])
    dico_stats = {f"Stats_{key}": group for i, (key, group) in enumerate(grouped_stats)}

    for cle, valeur in dico_stats.items():
        valeur.to_csv(fr"CSV_files//{cle}.csv")

    return "Execution completed"

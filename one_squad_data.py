"""
Créer une page HTML avec les informations de tous les joueurs d'UNE équipe
"""

# Dans la console de commande pour installer selenium :
# pip install selenium==3.141.0
# OU, de meilleur manière :
# conda install -c conda-forge selenium
# conda install -c conda-forge tabulate

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
from selenium.common.exceptions import NoSuchElementException
import urllib.request
import pandas as pd
import numpy as np
from tabulate import tabulate
import platform
import os
import create_CSS
import webbrowser


def exec():
    """
    Crée les fichiers web requis pour le site, destiné a etre executer dans le
    menu.

    Cette fonction rassemble les données d'une equipe specifique participant à
    la Coupe du Monde de Rugby 2023 à partir de fichier CSV.

    Dépendances,
        Assurez-vous d'avoir les bibliothèques nécessaires installées :
            - pandas
            - csv

    Returns
    -------
    Un message indiquant que l'exécution est terminée.
    """

    # Prend en entrée le nom d'une équipe et ajoute à un dataframe le nom de
    # cette équipe puis tout les urls des joueurs
    def recup_url_players(name_team):
        """
        Récupère l'identifiant et les URL des joueurs d'une équipe donnée.


        Parameters
        ----------
        name_team : String
            Le nom de l'équipe pour laquelle récupérer les URL.

        Returns
        -------
        temp : Series
            Une liste contenant l'identifiant, le nom de l'équipe et la liste
            des URL des joueurs.

        """
        url = "https://www.rugbyworldcup.com/2023/teams/" + name_team
        page = urllib.request.urlopen(url)
        soup = bs(page, "html.parser")
        identifier = soup.find("span", class_="widget__title--short u-show-phablet")
        identifier = identifier.text
        player_team = soup.find_all("a", {"class": "squad-list__player"})
        temp = [identifier, name_team]
        url_players = []
        for elt in player_team:
            url_players.append("https:"+elt.get("href"))
        temp.append(url_players)
        return temp

    def cutting(dataframe, list):
        """
        Découpe un dataframe en utilisant une liste de séparateurs pour
        extraire des informations.


        Parameters
        ----------
        dataframe : DataFrame
            Le dataframe à découper.
        list : list
            La liste de séparateurs.

        Returns
        -------
        temp : list
            Une liste résultante de la découpe du dataframe.

        """
        cut = []
        for elt in dataframe:
            if any(elt in i for i in list):
                for x in list:
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
    # Options pour Chrome

    if platform.system() == "Windows":
        service = Service(r"D:\Users\Documents\Selenium\126.0.6478.126\chromedriver-win64\chromedriver.exe")
        options.binary_location = r"D:\Users\Documents\Selenium\126.0.6478.126\chrome-win64\chrome.exe"

    elif platform.system() == "Darwin":
        geckodriver_path = "/usr/local/bin/geckodriver"

    # - Utiliser firefox
    driver = webdriver.Chrome(service=service, options=options)

    # -------------------------------------------------------------------------
    # ------------------------------ SCRAPPING --------------------------------
    # -------------------------------------------------------------------------

    # Récupération des noms des équipes
    url = "https://www.rugbyworldcup.com/2023/teams"
    page = urllib.request.urlopen(url)
    soup = bs(page, "html.parser")
    tag_team = soup.find_all("h2", {"class": "card__title article-list__title"})

    # Ecriture des noms dans un dataframe
    name_team = pd.DataFrame(columns=["Name"])
    for elt in tag_team:
        # Ajout d'une nouvelle ligne avec un index
        name_team.loc[len(name_team)] = elt.text.strip().replace(" ", "-")

    # - Affichage des noms d'équipes avec index pour l'input
    # - Definition du format de la table affiché :
    print(tabulate(name_team, tablefmt="youtrack"), "\n")
    choice_team = int(input("Choose a team by entering the corresponding number : "))

    # Table equipe inclus la liste des url de joueurs de l'equipe choisis
    table_team = pd.DataFrame(columns=["Id", "Country", "List of URL"])
    table_team.loc[len(table_team)] = recup_url_players(name_team["Name"][choice_team])
    table_team["Drapeau"] = table_team["Id"].apply(lambda x: f"https://www.rugbyworldcup.com/rwc2023-resources/prod/rwc2023_v6.6.0/i/elements/team-badges/{x}.png")

    # Lancement de firefox
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(table_team["List of URL"][0][0])

    tag_column_stats = driver.find_elements(By.CLASS_NAME, "player-stats__line-label")

    column_stats= [element.text.title().replace("\n", "").replace(":", "").replace("-", "")for element in tag_column_stats]
    column_stats = [element for element in column_stats if element != ""]

    # Création du dataframe pour récuperer les infos des joueurs
    table_infos_players = pd.DataFrame(columns=["Country", "Name", "Hometown",
                                                "Position", "Age", "Height",
                                                "Weight", "Photo", "Stats"])

    df_stats_players = pd.DataFrame(columns=column_stats)

    # Récupération des données des joueurs et ajout au dataframe
    for i in range(len(table_team["List of URL"])):
        country = []
        country.append("Country"+table_team["Country"][i])
        for url in table_team["List of URL"][i]:
            name_player = []
            driver.get(url)
            # Recherche/Selection des éléments par la balise CSS
            tag_name = driver.find_element(By.CSS_SELECTOR, ".player-hero__player-name")

            # Execution d"un script jvs : "return arguments[0].textContent;",
            # qui recupere le texte de "tag_name"
            name = driver.execute_script("return arguments[0].textContent;", tag_name).replace("\n", "")
            name_player.append("Name"+name)

            # Reherche tout les elements avec la class 'player-hero__item'
            tag_infos = driver.find_elements(By.CSS_SELECTOR, ".player-hero__item")
            infos = [element.text.title().replace("\n", "").replace(":", "").replace("-", "")for element in tag_infos]
            infos = [element for element in infos if element != ""]
            infos = name_player + infos
            infos = country + infos

            tag_stats = driver.find_elements(By.CSS_SELECTOR, ".player-stats__line")
            stats = [element.text.title().replace("\n", "").replace(":", "").replace("-", "")for element in tag_stats]
            stats = [element for element in stats if element != ""]

            # Si l'élément est trouvé, ajoute la photo
            try:
                # le finder des balise contenant les photos de joueurs
                tag_photo = driver.find_element(By.CSS_SELECTOR, ".player-headshot__img")
                photo = driver.execute_script("return arguments[0].getAttribute('src');", tag_photo)
                # executer wuand pas d'image trouvé, "NoSuchElementException"
                # erreur renvoyer par le finder
            except NoSuchElementException:
                photo = "https://www.pngkit.com/png/full/349-3499519_person1-placeholder-imagem-de-perfil-anonimo.png"

            # découpage d'infos pour chaque joueur
            stats_players = cutting(df_stats_players, stats)
            print(stats)
            players_infos = cutting(table_infos_players, infos)
            print(infos)

            players_infos[-2] = photo

            df_stats_players.loc[0] = stats_players

            players_infos[-1] = df_stats_players.iloc[-1]
            # ajout de la ligne dans la table
            table_infos_players.loc[len(table_infos_players)] = players_infos

    driver.close()

    # ------------------------ HTML------------------------
    if not os.path.exists("Choice_1"):
        os.mkdir("Choice_1")
    if not os.path.exists(r"Choice_1//Web_Files"):
        os.mkdir(r"Choice_1//Web_Files")

    html_code = f"""
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Team {table_team["Country"].iloc[0]}</title>
        <link rel="icon" href="{table_team["Drapeau"].iloc[0]}" type=image/x-icon>
        <link rel="stylesheet" href="style_acceuil.css">
        <script src="team.js"></script
    </head>
    <body>
    """

    html_code += """
        <label class="switch">
            <span class="sun"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><g fill="#ffd43b"><circle r="5" cy="12" cx="12"></circle><path d="m21 13h-1a1 1 0 0 1 0-2h1a1 1 0 0 1 0 2zm-17 0h-1a1 1 0 0 1 0-2h1a1 1 0 0 1 0 2zm13.66-5.66a1 1 0 0 1 -.66-.29 1 1 0 0 1 0-1.41l.71-.71a1 1 0 1 1 1.41 1.41l-.71.71a1 1 0 0 1 -.75.29zm-12.02 12.02a1 1 0 0 1 -.71-.29 1 1 0 0 1 0-1.41l.71-.66a1 1 0 0 1 1.41 1.41l-.71.71a1 1 0 0 1 -.7.24zm6.36-14.36a1 1 0 0 1 -1-1v-1a1 1 0 0 1 2 0v1a1 1 0 0 1 -1 1zm0 17a1 1 0 0 1 -1-1v-1a1 1 0 0 1 2 0v1a1 1 0 0 1 -1 1zm-5.66-14.66a1 1 0 0 1 -.7-.29l-.71-.71a1 1 0 0 1 1.41-1.41l.71.71a1 1 0 0 1 0 1.41 1 1 0 0 1 -.71.29zm12.02 12.02a1 1 0 0 1 -.7-.29l-.66-.71a1 1 0 0 1 1.36-1.36l.71.71a1 1 0 0 1 0 1.41 1 1 0 0 1 -.71.24z"></path></g></svg></span>
            <span class="moon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path d="m223.5 32c-123.5 0-223.5 100.3-223.5 224s100 224 223.5 224c60.6 0 115.5-24.2 155.8-63.4 5-4.9 6.3-12.5 3.1-18.7s-10.1-9.7-17-8.5c-9.8 1.7-19.8 2.6-30.1 2.6-96.9 0-175.5-78.8-175.5-176 0-65.8 36-123.1 89.3-153.3 6.1-3.5 9.2-10.5 7.7-17.3s-7.3-11.9-14.3-12.5c-6.3-.5-12.6-.8-19-.8z"></path></svg></span>   
            <input type="checkbox" onclick="toggleDarkMode()" id="dark-button" class="input">
            <span class="slider"></span>
        </label>"""

    html_code += f"""
        <div class="grid-container">
            <h1 class="page-title"><img class="title-icon" src="{table_team["Drapeau"].iloc[0]}" alt="Drapeau National"> {table_team["Country"].iloc[0].title()}'s players </h1>
            <div class="form-control">
                <input type="text" id="searchInput" required="" onkeyup="search()">
                <label>
                    <span style="transition-delay:0ms">P</span>
                    <span style="transition-delay:50ms">l</span>
                    <span style="transition-delay:100ms">a</span>
                    <span style="transition-delay:150ms">y</span>
                    <span style="transition-delay:200ms">e</span>
                    <span style="transition-delay:250ms">r</span>
                    <span style="transition-delay:300ms">-</span>
                    <span style="transition-delay:350ms">N</span>
                    <span style="transition-delay:400ms">a</span>
                    <span style="transition-delay:450ms">m</span>
                    <span style="transition-delay:500ms">e</span>
                </label>
            </div>
    """

    for index, row in table_infos_players.iterrows():
        html_code += f"""
            <div class="grid-item" data-name="{row["Name"]}">
            <a href="player_{index}.html"><img src="{row["Photo"]}" alt="{row["Name"]}"  loading="lazy"></a>
            <p>{row["Name"]}</p>
            <div class="container-infos">
                <div class ="line-info"><p>Position : {table_infos_players["Position"][index]}</p></div>
                <div class ="line-info"><p>Age : {table_infos_players["Age"][index]}</p></div>
            </div>
            </div>"""
    html_code += """
        </div>
        <footer>
            <div class="footer-buttons">
                <button class="ui-btn legal" id="legal" onclick="goToLegalPage()"><span>Legal Notice</span></button>
            </div>
            <div class="footer-info">
                <p>SAÉ 3.VCOD.01 Collecte automatisée de données web (2023-2024)
                <br>Website generated as part of coursework
                <br>By : Romain Troillard, Dorian Relave, Moetaz Ben Ahmed, Abder Rhaman Bouaouina</p>
            </div>
        </footer>
    </body>
</html>"""

    # Écrire le code HTML dans un fichier
    with open(os.path.join("Choice_1//Web_Files", "team_page.html"), "w", encoding="utf-8") as f:
        # Écrire le code HTML dans le fichier
        f.write(html_code)

    total_players = len(table_infos_players)

    # Pour chaque joueur, créez une nouvelle page HTML avec ses informations détaillées
    for index, row in table_infos_players.iterrows():

        prev_index = (index - 1) % total_players
        next_index = (index + 1) % total_players

        player_html_code = f"""
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="icon" href="{table_team["Drapeau"].iloc[0]}" type=image/x-icon>
        <link rel="stylesheet" href="style_joueurs.css">
        <script src="players.js"></script>
        <title>Informations de {row["Name"]}</title>
    </head>
    <body class="body-container">
        <label class="switch">
            <span class="sun"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><g fill="#ffd43b"><circle r="5" cy="12" cx="12"></circle><path d="m21 13h-1a1 1 0 0 1 0-2h1a1 1 0 0 1 0 2zm-17 0h-1a1 1 0 0 1 0-2h1a1 1 0 0 1 0 2zm13.66-5.66a1 1 0 0 1 -.66-.29 1 1 0 0 1 0-1.41l.71-.71a1 1 0 1 1 1.41 1.41l-.71.71a1 1 0 0 1 -.75.29zm-12.02 12.02a1 1 0 0 1 -.71-.29 1 1 0 0 1 0-1.41l.71-.66a1 1 0 0 1 1.41 1.41l-.71.71a1 1 0 0 1 -.7.24zm6.36-14.36a1 1 0 0 1 -1-1v-1a1 1 0 0 1 2 0v1a1 1 0 0 1 -1 1zm0 17a1 1 0 0 1 -1-1v-1a1 1 0 0 1 2 0v1a1 1 0 0 1 -1 1zm-5.66-14.66a1 1 0 0 1 -.7-.29l-.71-.71a1 1 0 0 1 1.41-1.41l.71.71a1 1 0 0 1 0 1.41 1 1 0 0 1 -.71.29zm12.02 12.02a1 1 0 0 1 -.7-.29l-.66-.71a1 1 0 0 1 1.36-1.36l.71.71a1 1 0 0 1 0 1.41 1 1 0 0 1 -.71.24z"></path></g></svg></span>
            <span class="moon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path d="m223.5 32c-123.5 0-223.5 100.3-223.5 224s100 224 223.5 224c60.6 0 115.5-24.2 155.8-63.4 5-4.9 6.3-12.5 3.1-18.7s-10.1-9.7-17-8.5c-9.8 1.7-19.8 2.6-30.1 2.6-96.9 0-175.5-78.8-175.5-176 0-65.8 36-123.1 89.3-153.3 6.1-3.5 9.2-10.5 7.7-17.3s-7.3-11.9-14.3-12.5c-6.3-.5-12.6-.8-19-.8z"></path></svg></span>
            <input type="checkbox" onclick="toggleDarkMode()" id="dark-button" class="input">
            <span class="slider"></span>
        </label>
        <div class="button-container">
            <a class="navigation-button-previous" href="player_{prev_index}.html">Previous</a>
        </div>

        <div class="home-button-container">
            <a class="home-button" href="team_page.html">Home</a>
        </div>

        <div class="button-container">
            <a class="navigation-button-next" href="player_{next_index}.html">Next</a>
        </div>

        <div class="card-container">
            <div class="card-header">
                <img src="{row["Photo"]}" alt="{row["Name"]}"  loading="lazy">
                <h1>{row["Name"]}</h1>
            </div>

            <div class="card-infos">
                <h2 class="infos-title">Personal Informations:</h2>
                <div class="grid-container-personal">"""

        for column in ['Hometown', 'Position', 'Age', 'Height', 'Weight']:
            value = str(table_infos_players[column][index])
            if value != "" and value != np.nan:
                player_html_code += f"""
                    <div class="grid-item"><strong>{column}:</strong>{value}</div>
                    """

        player_html_code += """
                </div>
            <h2 class="infos-title">Personal Statistics:</h2>
            <div class="grid-container-stats">"""

        for column in list(df_stats_players.columns):
            value = table_infos_players["Stats"][index][column]
            if value != "":
                player_html_code += f"""
                <div class="grid-item"><strong>{column}:</strong>{value}</div>
                        """
        player_html_code += """
                </div>
            </div>
        </div>
    </body>
</html>"""
        # Écrire le code HTML de chaque joueur dans un fichier séparé
        with open(os.path.join(r"Choice_1//Web_Files",f"player_{index}.html"), "w", encoding="utf-8") as f:
            f.write(player_html_code)

    create_CSS.creation_CSS_joueurs("Choice_1//Web_Files")
    create_CSS.creation_CSS_acceuil("Choice_1//Web_Files")

    chemin_absolu = os.path.abspath(r"Choice_1//Web_Files//team_page.html")
    webbrowser.open("file://" + chemin_absolu)

    return "Execution completed"

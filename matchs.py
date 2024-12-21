"""
Créer une page HTML avec les résultats de toute la compétition
"""

import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from unidecode import unidecode
import locale
import create_CSS
import webbrowser


def exec():
    """
    Fonction principale pour générer et afficher une page HTML pour la Coupe du
    Monde de Rugby 2023. Regroupant tout les matchs de la compétition.
    Destiné a etre executer depuis un menu.

    Returns
    -------
    str
        Un message indiquant que l'exécution est terminée.

    """
    locale.setlocale(locale.LC_TIME, 'fr_FR')

    def Add_matchs(tree):
        """
        Ajoute les matchs d'une phase de la compétition à un DataFrame.


        Parameters
        ----------
        tree : Object BeautifulSou^p
            Arbre HTML représentant la phase de la compétition..

        Returns
        -------
        None.

        """
        # Récupération de tout les jours de match avec ces matchs
        match_days = tree.find_all('li', {'class': "li_idalgo_content_calendar_cup_date"})

        # Parcours de chaque jour et récupération des matchs du jour
        for day in match_days:
            matchs = day.find_all("li", {"class": "li_idalgo_content_calendar_cup_date_match"})
            # On parcourt chaque match du jour et on récupére dans l'ordre :
            # Date du match / Equipe "domicile" / Score Domicile / Score Exterieur / Equipe "Exterieur" / Poule ou Phase finale)
            for m in matchs:
                row_df_matchs = []
                # Date
                row_df_matchs.append(day.find("span", {"class": "span_idalgo_content_calendar_cup_date_title_left"}).text.strip())
                # Stage
                row_df_matchs.append(m.find("div", {"class": "div_idalgo_content_calendar_cup_date_match_ctx"}).text.strip())
                # Domicile
                row_df_matchs.append(m.find("div", {"class": "div_idalgo_content_calendar_cup_date_match_local"}).text.strip())
                # Score Domicile
                row_df_matchs.append(m.find("span", {"class": "span_idalgo_score_part_left"}).text)
                # Score Exterieur
                row_df_matchs.append(m.find("span", {"class": "span_idalgo_score_part_right"}).text)
                # Exterieur
                row_df_matchs.append(m.find("div", {"class": "div_idalgo_content_calendar_cup_date_match_visitor"}).text.strip())
                stadium = m.find("div", {"class": "div_idalgo_content_calendar_cup_date_match_stadium"}).text.strip().replace("Stade : ", "")
                # Stadium
                row_df_matchs.append(re.sub(r'\([^)]*\)', '', stadium))
                # Ajout au dataframe
                df_matchs.loc[len(df_matchs)] = row_df_matchs

    # ------------------------ HTML V4 ------------------------

    # -----Récupération nom des équipes-----
    url = "https://www.rugbyrama.fr/rugby-a-xv/coupe-du-monde/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    all_name = soup.find_all("li", {"class": "navbar-sub__dropdown-item"})
    team_name = [unidecode(name.text.strip()) for name in all_name]
    team_name = pd.DataFrame({"Team Name": team_name})
    dico_traduction = {"Afrique du Sud": "South-Africa",
                       "Angleterre": "England",
                       "Argentine": "Argentina",
                       "Australie": "Australia",
                       "Chili": "Chile",
                       "Ecosse": "Scotland",
                       "Fidji": "Fiji",
                       "Georgie": "Georgia",
                       "Irlande": "Ireland",
                       "Italie": "Italy",
                       "Japon": "Japan",
                       "Namibie": "Namibia",
                       "Nouvelle-Zelande": "New-Zealand",
                       "Pays de Galles": "Wales",
                       "Roumanie": "Romania",
                       "Lundi": "Monday",
                       "Mardi": "Tuesday",
                       "Merdredi": "Wednesday",
                       "Jeudi": "Thursday",
                       "Vendredi": "Friday",
                       "Samedi": "Saturday",
                       "Dimanche": "Sunday",
                       "septembre": "September",
                       "octobre": "October",
                       "Gr.": "Pool",
                       "F.": "Final",
                       "PF": "Third-place"
                       }
    team_name["Anglais"] = team_name["Team Name"].replace(dico_traduction)
    # --------------------------------------

    # -----Récupération des classements des poules-----
    url = "https://fr.wikipedia.org/wiki/Coupe_du_monde_de_rugby_%C3%A0_XV_2023"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    pool_name = list("ABCD")
    all_pool = {}

    # On cherche à trouver dans la page Poule *lettre*
    for p in pool_name:
        element = soup.find('span', {'id': f"Poule_{p}"})
        # Si l'élément est trouvé, cherchez la table qui suit immédiatement cet élément
        if element:
            table = element.find_next('table')
            tableau_resultat = pd.read_html(str(table))[0]
            all_pool[f"Poule {p}"] = tableau_resultat
        else:
            print("Élément span non trouvé.")
    # ------------------------------------------------

    # -----Récupération de tout les matchs de la compétition-----
    df_matchs = pd.DataFrame(columns=["Date", "Stage", "Team Home", "Score Home", "Score Away", "Team Away", "Stadium"])

    url = "https://www.rugbyrama.fr/resultats/rugby/coupe-du-monde/calendrier"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    arbre = soup.find("div", {"class": "div_idalgo_content_calendar_cup"})

    Add_matchs(arbre)
    df_matchs["Team Home"], df_matchs["Team Away"] = df_matchs["Team Home"].apply(unidecode), df_matchs["Team Away"].apply(unidecode)

    df_matchs["Date"] = df_matchs["Date"].replace(r'\s+', ' ', regex=True)

    df_matchs[["Date", "Stage"]] = df_matchs[["Date", "Stage"]].replace(dico_traduction, regex=True)
    df_matchs = df_matchs.replace(dico_traduction)

    # --------------- Ajout des images de chaques equipe pour chaque matchs -------
    df_images = pd.read_csv('CSV_Files/country_data.csv')

    # Boucle pour associer les images en fonction du pays de chaque équipe
    for index, row in df_matchs.iterrows():
        team_home = str(row['Team Home']).upper()
        team_away = str(row['Team Away']).upper()
        # Trouver les liens d'image correspondants dans le DataFrame des images
        image_home = df_images.loc[df_images['Country'] == team_home, 'Image'].values
        image_away = df_images.loc[df_images['Country'] == team_away, 'Image'].values

        # Mettre à jour les colonnes 'Pic Home' et 'Pic Away' avec les liens d'image correspondants
        df_matchs.at[index, 'Pic Home'] = image_home[0] if len(image_home) > 0 else ''
        df_matchs.at[index, 'Pic Away'] = image_away[0] if len(image_away) > 0 else ''

    # -----Group by----------
    grouped = df_matchs.groupby('Stage')  # Par Phase
    dico_stage = {f'Matchs_{key}': group for i, (key, group) in enumerate(grouped)}

    matchs_by_team = {}  # par equipe
    for i in range(len(team_name)):
        nom = team_name["Anglais"][i]
        temp = (df_matchs['Team Home'] == nom) | (df_matchs['Team Away'] == nom)  # temp renvoie le dataframe avec des valeurs TRUE si la ligne à le pays dans une des 2 colonnes
        matchs_by_team[f"Matchs_{nom}"] = df_matchs[temp]

    # ------------------- HTML --------------------------
    html_code = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Rugby World Cup 2023</title>
        <link rel="stylesheet" href="style_world_cup.css">
        <link rel="icon" type="image/png" href="https://static.wikia.nocookie.net/logopedia/images/3/38/RWC2023_2018-symbol.svg/revision/latest/scale-to-width-down/250?cb=20181116103448">
    </head>
    <body>
        <h1 class="page-title"><img class="title-icon" src="https://static.wikia.nocookie.net/logopedia/images/3/38/RWC2023_2018-symbol.svg/revision/latest/scale-to-width-down/250?cb=20181116103448" alt="Rugby World cup 2023 Logo">2023's Rugby Wolrd cup Matchs</h1>
        <div class="menu-container">
            <div class="menu-item" onclick="showMatches('Matchs_Pool_A')" data-phase="Matchs_Pool_A">Group A</div>
            <div class="menu-item" onclick="showMatches('Matchs_Pool_B')" data-phase="Matchs_Pool_B">Group B</div>
            <div class="menu-item" onclick="showMatches('Matchs_Pool_C')" data-phase="Matchs_Pool_C">Group C</div>
            <div class="menu-item" onclick="showMatches('Matchs_Pool_D')" data-phase="Matchs_Pool_D">Group D</div>
            <div class="menu-item" onclick="showMatches('Quarter')" data-phase="Quarter">Quarts</div>
            <div class="menu-item" onclick="showMatches('Semi')" data-phase="Semi">Semi-final</div>
            <div class="menu-item" onclick="showMatches('Third_place')" data-phase="Third_place">Third Place</div>
            <div class="menu-item" onclick="showMatches('Final')" data-phase="Final">Final</div>
        </div>
        <div class="popup" id="popup">
            <div class="popup-content">
                <span class="close" onclick="closePopup()">&times;</span>
                <div id="matchesContainer" class="stage-container"></div>
            </div>
        </div>
        <div class="modal" id="matchesModal">
            <div class="modal-content">
                <span class="close" onclick="closeModal">&times;</span>
            </div>
        </div>
        <div class = "teams-container">"""

    # Générer la section des équipes
    for team in team_name["Anglais"]:
        team_image = df_images[df_images['Country'] == str(team).upper()]['Image'].values[0]

        html_code += f"""
            <div class="team-card" id="{team.replace(' ', '_')}">
                <h2>{team}</h2>
                <a href="#Matchs_{team.replace(' ', '_')}">
                    <div class="team-info">
                        <img src="{team_image}" alt="{team}" class="team-image">
                    </div>
                </a>
            </div>"""

    html_code += """
        </div>
        <div class="stage-matches">"""

    # Genere la section des matches par phase de la compétition
    custom_order = [2, 7, 0, 1, 3, 4, 5, 6]
    for stage_index in custom_order:
        stage = list(dico_stage.keys())[stage_index]
        matches = dico_stage[stage]
        # Determine the stage type and set the corresponding class
        stage_class = ""
        if "1/2" in stage:
            stage_class = "Semi"
        elif "1/4" in stage:
            stage_class = "Quarter"
        elif "Final" in stage:
            stage_class = "Final"
        elif "Pool" in stage:
            stage_class = str(stage.replace(" ", "_"))
        elif "Third-place" in stage:
            stage_class = "Third_place"

        html_code += f"""
            <div class="stage-container {stage_class}">
                <h2>{stage_class.replace("_", " ")}</h2>
                <div class="match-grid">"""

        for index, match in matches.iterrows():
            team_home_image = match['Pic Home']
            team_away_image = match['Pic Away']

            html_code += f"""
                    <div class="match-item">
                        <div class="team-images">
                            <img src="{team_home_image}" alt="{match['Team Home']}">
                            <img src="{team_away_image}" alt="{match['Team Away']}">
                        </div>
                        <p>{match['Date']}</p>
                        <p>{match['Team Home']} vs {match['Team Away']}</p>
                        <p>{match['Score Home']} - {match['Score Away']}</p>
                        <p>{match['Stadium']}</p>
                    </div>"""

        html_code += """
                </div>
            </div>"""

    html_code += """
        </div>
        <div class = "match-by-team">"""
    # -----------------------------------------------------------------------------

    # Générer la section des matchs par équipe
    for team, matches in matchs_by_team.items():
        html_code += f"""
            <div class="team-matches-container" id="{team.replace(' ', '_')}">
                <h2>{team.replace("_", " ").title()}</h2>
                <div class="match-grid-teams">"""
        for index, match in matches.iterrows():
            # Vérifie si l'équipe spécifiée dans 'team' est à la maison ou à l'extérieur
            team_at_home = team == ("Matchs_" + match['Team Home'])
            # Ajustement de la condition pour les matchs gagnés et perdus
            if int(match['Score Home']) > int(match['Score Away']):
                if team_at_home:
                    match_class = "won-match"
                else:
                    match_class = "lost-match"
            elif int(match['Score Home']) < int(match['Score Away']):
                if team_at_home:
                    match_class = "lost-match"
                else:
                    match_class = "won-match"
            elif int(match['Score Home']) == int(match['Score Away']):
                if team_at_home:
                    match_class = "draw-match"
                else:
                    match_class = "draw-match"

            html_code += f"""
                    <div class="cardm">
                        <div class="card {match_class}">
                            <div class="teams-info">
                                <div class="team-home pic">
                                    <img src="{match['Pic Home']}" alt="{match['Team Home']}" loading="lazy">
                                    <p>{match['Team Home']}</p>
                                </div>

                                <div class="score">{match['Score Home']} - {match['Score Away']}</div>

                                <div class="team-away pic">
                                    <img src="{match['Pic Away']}" alt="{match['Team Away']}" loading="lazy">
                                    <p>{match['Team Away']}</p>
                                </div>
                            </div>
                        </div>
                        <div class="card2">
                            <div class="upper">
                                <p class="match-date">{match['Date']}</p>
                            </div>
                            <div class="lower">
                                <p class="stadium">{match['Stadium']}</p>
                                <div class="card3">Rugby World Cup 2023</div>
                            </div>
                        </div>
                    </div>"""
        html_code += """
                </div>
            </div>
        """

    # -----------------------------------------------------------------------------

    html_code += """
        </div>
        <button onclick="scrollToTop()" id="scrollToTopBtn">Go to the top</button>

        <label class="switch">
            <span class="sun"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><g fill="#ffd43b"><circle r="5" cy="12" cx="12"></circle><path d="m21 13h-1a1 1 0 0 1 0-2h1a1 1 0 0 1 0 2zm-17 0h-1a1 1 0 0 1 0-2h1a1 1 0 0 1 0 2zm13.66-5.66a1 1 0 0 1 -.66-.29 1 1 0 0 1 0-1.41l.71-.71a1 1 0 1 1 1.41 1.41l-.71.71a1 1 0 0 1 -.75.29zm-12.02 12.02a1 1 0 0 1 -.71-.29 1 1 0 0 1 0-1.41l.71-.66a1 1 0 0 1 1.41 1.41l-.71.71a1 1 0 0 1 -.7.24zm6.36-14.36a1 1 0 0 1 -1-1v-1a1 1 0 0 1 2 0v1a1 1 0 0 1 -1 1zm0 17a1 1 0 0 1 -1-1v-1a1 1 0 0 1 2 0v1a1 1 0 0 1 -1 1zm-5.66-14.66a1 1 0 0 1 -.7-.29l-.71-.71a1 1 0 0 1 1.41-1.41l.71.71a1 1 0 0 1 0 1.41 1 1 0 0 1 -.71.29zm12.02 12.02a1 1 0 0 1 -.7-.29l-.66-.71a1 1 0 0 1 1.36-1.36l.71.71a1 1 0 0 1 0 1.41 1 1 0 0 1 -.71.24z"></path></g></svg></span>
            <span class="moon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path d="m223.5 32c-123.5 0-223.5 100.3-223.5 224s100 224 223.5 224c60.6 0 115.5-24.2 155.8-63.4 5-4.9 6.3-12.5 3.1-18.7s-10.1-9.7-17-8.5c-9.8 1.7-19.8 2.6-30.1 2.6-96.9 0-175.5-78.8-175.5-176 0-65.8 36-123.1 89.3-153.3 6.1-3.5 9.2-10.5 7.7-17.3s-7.3-11.9-14.3-12.5c-6.3-.5-12.6-.8-19-.8z"></path></svg></span>
            <input type="checkbox" onclick="darkmode()" id="dark-button" class="input">
            <span class="slider"></span>
        </label>

        <script>
            /* Script Pour le retour en haut de page */
            function scrollToTop() {
                document.body.scrollTop = 0; // Pour les navigateurs pris en charge
                document.documentElement.scrollTop = 0; // Pour les navigateurs modernes
            }

            window.onscroll = function () {
                scrollFunction();
            };

            function scrollFunction() {
                var btn = document.getElementById("scrollToTopBtn");

                if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
                    btn.style.opacity = "1";
                } else {
                    btn.style.opacity = "0";
                }
            }

            /* Script permettant d'afficher en pop-up les matchs d'une phase */
            document.addEventListener('DOMContentLoaded', function () {
                const menuItems = document.querySelectorAll('.menu-item');
                const modal = document.getElementById('matchesModal');

                menuItems.forEach(function (item) {
                    item.addEventListener('click', function () {
                        const phase = item.getAttribute('data-phase');
                        showMatches(phase);
                    });
                });

                function showMatches(phase) {
                    const modalContent = modal.querySelector('.modal-content');
                    const stageContainer = document.querySelector(`.stage-container.${phase}`);

                    if (stageContainer) {
                        const stageContent = stageContainer.innerHTML;
                        modalContent.innerHTML = stageContent;

                        // Affichage de la pop-up
                        modal.style.display = 'block';
                    }
                }

                function closeModal() {
                    modal.style.display = 'none';
                }

                modal.addEventListener('click', function (event) {
                    if (event.target === modal) {
                        closeModal();
                    }
                });

                const closeBtn = modal.querySelector('.close');
                closeBtn.addEventListener('click', closeModal);
            });

            /* Script pour passer en mode sombre */
            function darkmode() {
                var element = document.body;
                element.classList.toggle("dark-mode");
            }
            
            function goToLegalPage() {
                window.location.href = '../../legal_info.html'; // Adjust the path based on your directory structure
            }
        </script>
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
</html>
"""

    # Écrire le code HTML dans un fichier
    if not os.path.exists("Choice_3"):
        os.mkdir("Choice_3")
    if not os.path.exists(r"Choice_3//Web_Files"):
        os.mkdir(r"Choice_3//Web_Files")

    create_CSS.creation_CSS_matchs("Choice_3//Web_Files")

    with open(r"Choice_3//Web_Files//rugby_world_cup.html", "w", encoding="utf-8") as f:
        f.write(html_code)

    chemin_absolu = os.path.abspath(r"Choice_3//Web_Files//rugby_world_cup.html")
    webbrowser.open("file://" + chemin_absolu)

    return "Execution completed"

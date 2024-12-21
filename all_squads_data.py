"""
Créer une page HTML d'accueil avec toutes les équipes, et pour chaque équipe on
obtient les informations des joueurs
"""

import os
import pandas as pd
import glob
import csv
import create_CSS
import webbrowser


def exec():
    """
    Crée les fichiers web requis pour le site, destiné a etre executer dans le
    menu.

    Cette fonction rassemble les données des équipes participant à la Coupe du
    Monde de Rugby 2023 à partir de fichier CSV.

    Dépendances,
        Assurez-vous d'avoir les bibliothèques nécessaires installées :
            - pandas
            - csv

    :return: None
    """
    stats_files = glob.glob(r'CSV_Files/Stats_*.csv')

    # Créer la liste de correspondance à partir des données du CSV
    with open(r'CSV_Files/country_data.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)

    matching_list = [(row['Country'].title(), row['Id'].title()) for row in rows]

    country_data = {}
    # Merge Stats and Joueurs for each country
    for country_name, country_tag in matching_list:
        # Check if the Stats file exists for the current country
        stats_file_path = f"CSV_Files\\Stats_{country_tag}.csv"
        if stats_file_path in stats_files:
            # Read the Stats file into a dataframe
            stats_df = pd.read_csv(stats_file_path)
            # Read the Joueurs file into a dataframe
            players_df = pd.read_csv(f"CSV_Files\\players_{country_name}.csv")
            # Merge the two dataframes on the common player ID
            merged_df = pd.merge(stats_df, players_df, left_on='Id_Player', right_on='Id')
            # Store the merged dataframe in the dictionary
            country_data[country_name] = merged_df
        else:
            print(f"Stats file not found for {country_name}")

    # -------------------------------------------------------------------------
    # ---------------------------- COUNTRIES HOME PAGES -----------------------
    # -------------------------------------------------------------------------

    if not os.path.exists("Choice_2"):
        os.mkdir("Choice_2")
    if not os.path.exists(r"Choice_2//Web_Files"):
        os.mkdir(r"Choice_2//Web_Files")

    for country_name, country_df in country_data.items():
        # Create a folder for each country
        country_folder = os.path.join(r"Choice_2//Web_Files", country_name)
        os.makedirs(country_folder, exist_ok=True)

        country_df['Drapeau'] = country_df['Id_Player'].apply(lambda x: f'https://www.rugbyworldcup.com/rwc2023-resources/prod/rwc2023_v6.6.0/i/elements/team-badges/{x.upper().replace("-1", "")}.png')
        country_df['Union-emblem'] = f'https://www.rugbyworldcup.com/rwc2023-resources/prod/rwc2023_v6.6.0/i/svg-files/elements/bg/teams/union-emblem-{country_name.lower()}-alt.svg'
        country_df['Country-Draw'] = f'https://www.rugbyworldcup.com/rwc2023-resources/prod/rwc2023_v6.6.0/i/svg-files/elements/bg/teams/country-{country_name.lower()}.svg'
        country_df['Tackle Success'] = country_df['Tackle Success'].str.rstrip('%').astype('float').round(2).astype(str) + '%'

        create_CSS.creation_CSS_acceuil("Choice_2//Web_Files")
        create_CSS.creation_CSS_joueurs("Choice_2//Web_Files")

        html_code = f"""
    <!DOCTYPE html>
    <html lang="en">
        <link rel="stylesheet" href="../style_acceuil.css" />
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Team {country_name}</title>
            <link rel="icon" href="{country_df['Drapeau'].iloc[0]}" type=image/x-icon>
        </head>
        <body>
            <label class="switch">
                <span class="sun"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><g fill="#ffd43b"><circle r="5" cy="12" cx="12"></circle><path d="m21 13h-1a1 1 0 0 1 0-2h1a1 1 0 0 1 0 2zm-17 0h-1a1 1 0 0 1 0-2h1a1 1 0 0 1 0 2zm13.66-5.66a1 1 0 0 1 -.66-.29 1 1 0 0 1 0-1.41l.71-.71a1 1 0 1 1 1.41 1.41l-.71.71a1 1 0 0 1 -.75.29zm-12.02 12.02a1 1 0 0 1 -.71-.29 1 1 0 0 1 0-1.41l.71-.66a1 1 0 0 1 1.41 1.41l-.71.71a1 1 0 0 1 -.7.24zm6.36-14.36a1 1 0 0 1 -1-1v-1a1 1 0 0 1 2 0v1a1 1 0 0 1 -1 1zm0 17a1 1 0 0 1 -1-1v-1a1 1 0 0 1 2 0v1a1 1 0 0 1 -1 1zm-5.66-14.66a1 1 0 0 1 -.7-.29l-.71-.71a1 1 0 0 1 1.41-1.41l.71.71a1 1 0 0 1 0 1.41 1 1 0 0 1 -.71.29zm12.02 12.02a1 1 0 0 1 -.7-.29l-.66-.71a1 1 0 0 1 1.36-1.36l.71.71a1 1 0 0 1 0 1.41 1 1 0 0 1 -.71.24z"></path></g></svg></span>
                <span class="moon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path d="m223.5 32c-123.5 0-223.5 100.3-223.5 224s100 224 223.5 224c60.6 0 115.5-24.2 155.8-63.4 5-4.9 6.3-12.5 3.1-18.7s-10.1-9.7-17-8.5c-9.8 1.7-19.8 2.6-30.1 2.6-96.9 0-175.5-78.8-175.5-176 0-65.8 36-123.1 89.3-153.3 6.1-3.5 9.2-10.5 7.7-17.3s-7.3-11.9-14.3-12.5c-6.3-.5-12.6-.8-19-.8z"></path></svg></span>
                <input type="checkbox" onclick="toggleDarkMode()" id="dark-button" class="input">
                <span class="slider"></span>
            </label>
            <div class="button-container">
                <a class="home-button" href="../main_menu.html">Select Country</a>
            </div>
            <div class="grid-container">
                <h1 class="page-title"><img class="title-icon" src="{country_df['Drapeau'].iloc[0]}" alt="Drapeau National"> {country_name.title()}'s players </h1>
                <div class="form-control">
                    <input type="value" id="searchInput" required="" onkeyup="search()">
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
                </div>"""

        for index, row in country_df.iterrows():
            html_code += f"""
                <div class="grid-item" data-name="{row['Name']}">
                <a href="{country_name}_player_{index}.html"><img src="{country_df['Photo'][index]}" alt="{row['Name']}"  loading="lazy"></a>
                <p>{row['Name']}</p>
                <div class="container-infos">
                    <div class ="line-info" id="1"><p>Position : {row['Position']}</p></div>
                    <div class ="line-info" id="2"><p>Age : {row['Age']}</p></div>
                </div>
                </div>"""
        html_code += """
            </div>
            <script>
                function search() {
                    var input, filter, grid, items, player, txtValue;
                    input = document.getElementById("searchInput");
                    filter = input.value.toUpperCase();
                    grid = document.querySelector(".grid-container");
                    items = grid.getElementsByClassName("grid-item");

                    for (var i = 0; i < items.length; i++) {
                        player = items[i];
                        txtValue = player.textContent || player.innerText;
                        if (txtValue.toUpperCase().indexOf(filter) > -1) {
                            player.style.display = "";
                        } else {
                            player.style.display = "none";
                        }
                    }
                }

                function toggleDarkMode() {
                    var element = document.body;
                    var isDarkMode = !element.classList.contains('dark-mode');
                    var darkButton = document.getElementById('dark-button');

                    if (isDarkMode) {
                        element.classList.add('dark-mode');
                        darkButton.checked = true; // Cocher la case
                        localStorage.setItem('darkMode', 'enabled');
                    } else {
                        element.classList.remove('dark-mode');
                        darkButton.checked = false; // Décocher la case
                        localStorage.setItem('darkMode', 'disabled');
                    }
                }

                document.addEventListener('DOMContentLoaded', function () {
                var darkModeState = localStorage.getItem('darkMode');

                    // Vérifiez s'il y a un paramètre de requête pour l'état du mode sombre
                    var urlParams = new URLSearchParams(window.location.search);
                    var darkModeQueryParam = urlParams.get('darkModeState');
        
                    if (darkModeQueryParam === 'enabled') {
                        // Appliquez le mode sombre si le paramètre de requête est défini sur "enabled"
                        document.body.classList.add('dark-mode');
                        document.getElementById('dark-button').checked = true; // Check the checkbox
                        localStorage.setItem('darkMode', 'enabled');
                    } else if (darkModeQueryParam === 'disabled') {
                        // Appliquez le mode clair si le paramètre de requête est défini sur "disabled"
                        document.body.classList.remove('dark-mode');
                        document.getElementById('dark-button').checked = false; // Décocher la case
                        localStorage.setItem('darkMode', 'disabled');
                    } else if (darkModeState === 'enabled') {
                        // Appliquez le mode sombre si localStorage est défini sur "enabled" et aucun paramètre de requête
                        document.body.classList.add('dark-mode');
                        document.getElementById('dark-button').checked = true; // Cocher la case
                    }
                });

                function toggleDarkMode() {
                    var element = document.body;
                    var isDarkMode = !element.classList.contains('dark-mode');
                    var darkButton = document.getElementById('dark-button');

                    if (isDarkMode) {
                        element.classList.add('dark-mode');
                        darkButton.checked = true; // Cocher la case
                        localStorage.setItem('darkMode', 'enabled');
                    } else {
                        element.classList.remove('dark-mode');
                        darkButton.checked = false; // Décocher la case
                        localStorage.setItem('darkMode', 'disabled');
                    }
                }
                function goToLegalPage() {
                    window.location.href = '../../../legal_info.html'; // Adjust the path based on your directory structure
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
    <html>"""

        # Write the HTML code in a file inside the country folder
        country_html_file = os.path.join(country_folder, f"{country_name}_data.html")
        with open(country_html_file, "w", encoding="utf-8") as f:
            f.write(html_code)

    # -------------------------------------------------------------------------
    # ------------------------------- PLAYERS PAGES ---------------------------
    # -------------------------------------------------------------------------
        total_players = len(country_df)

        for index, row in country_df.iterrows():

            prev_index = (index - 1) % total_players
            next_index = (index + 1) % total_players

            player_html_code = f"""
<!DOCTYPE html>
<html lang="en">
    <link rel="stylesheet" href="../style_joueurs.css" />
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="icon" href="{country_df['Drapeau'].iloc[0]}" type=image/x-icon>
        <title>Informations de {row['Name']}</title>
    </head>
    <body class="body-container">
        <label class="switch">
            <span class="sun"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><g fill="#ffd43b"><circle r="5" cy="12" cx="12"></circle><path d="m21 13h-1a1 1 0 0 1 0-2h1a1 1 0 0 1 0 2zm-17 0h-1a1 1 0 0 1 0-2h1a1 1 0 0 1 0 2zm13.66-5.66a1 1 0 0 1 -.66-.29 1 1 0 0 1 0-1.41l.71-.71a1 1 0 1 1 1.41 1.41l-.71.71a1 1 0 0 1 -.75.29zm-12.02 12.02a1 1 0 0 1 -.71-.29 1 1 0 0 1 0-1.41l.71-.66a1 1 0 0 1 1.41 1.41l-.71.71a1 1 0 0 1 -.7.24zm6.36-14.36a1 1 0 0 1 -1-1v-1a1 1 0 0 1 2 0v1a1 1 0 0 1 -1 1zm0 17a1 1 0 0 1 -1-1v-1a1 1 0 0 1 2 0v1a1 1 0 0 1 -1 1zm-5.66-14.66a1 1 0 0 1 -.7-.29l-.71-.71a1 1 0 0 1 1.41-1.41l.71.71a1 1 0 0 1 0 1.41 1 1 0 0 1 -.71.29zm12.02 12.02a1 1 0 0 1 -.7-.29l-.66-.71a1 1 0 0 1 1.36-1.36l.71.71a1 1 0 0 1 0 1.41 1 1 0 0 1 -.71.24z"></path></g></svg></span>
            <span class="moon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path d="m223.5 32c-123.5 0-223.5 100.3-223.5 224s100 224 223.5 224c60.6 0 115.5-24.2 155.8-63.4 5-4.9 6.3-12.5 3.1-18.7s-10.1-9.7-17-8.5c-9.8 1.7-19.8 2.6-30.1 2.6-96.9 0-175.5-78.8-175.5-176 0-65.8 36-123.1 89.3-153.3 6.1-3.5 9.2-10.5 7.7-17.3s-7.3-11.9-14.3-12.5c-6.3-.5-12.6-.8-19-.8z"></path></svg></span>
            <input type="checkbox" onclick="toggleDarkMode()" id="dark-button" class="input">
            <span class="slider"></span>
        </label>
        <div class="button-container">
            <a class="navigation-button-previous" href="{country_name}_player_{prev_index}.html">Previous</a>
        </div>

        <div class="button-container">
            <a class="home-button" href="{country_name}_data.html">Home</a>
        </div>

        <div class="button-container">
            <a class="navigation-button-next" href="{country_name}_player_{next_index}.html">Next</a>
        </div>

        <div class="card-container">
            <div class="card-header">
                <img src="{row['Photo']}" alt="{row['Name']}"  loading="lazy">
                <h1>{row['Name']}</h1>
            </div>
            <div class="card-infos">
                <h2 class="infos-title">Personal Information:</h2>
                <div class="grid-container-personal">"""

            for column in ['Hometown', 'Position', 'Age', 'Height', 'Weight']:
                value = str(row[column])
                if value != "" and value != "nan":
                    player_html_code += f"""
                    <div class="grid-item"><strong>{column}:</strong>{value}</div>"""

            player_html_code += """
                </div>
                <h2 class="infos-title">Player Statistics:</h2>
                <div class="grid-container-stats">"""

            for column in ['Kicks From Hand', 'Runs', 'Passes', 'Offloads', 'Clean Breaks', 'Defenders Beaten', 'Yellow Cards', 'Red Cards', 'Carries', 'Metres Made', 'Tackles', 'Tackle Success', 'Handling Errors', 'Turnovers']:
                value = str(row[column])
                if value != "":
                    player_html_code += f"""
                    <div class="grid-item"><strong>{column}:</strong>{value}</div>"""

            player_html_code += """
                </div>
            </div>
        </div>
    </body>
    <script>
        function toggleDarkMode() {
            var element = document.body;
            var isDarkMode = !element.classList.contains('dark-mode');
            var darkButton = document.getElementById('dark-button');

            if (isDarkMode) {
                element.classList.add('dark-mode');
                darkButton.checked = true; // Cocher la case
                localStorage.setItem('darkMode', 'enabled');
            } else {
                element.classList.remove('dark-mode');
                darkButton.checked = false; // Décocher la case
                localStorage.setItem('darkMode', 'disabled');
            }
        }

        document.addEventListener('DOMContentLoaded', function () {
        var darkModeState = localStorage.getItem('darkMode');

            // Vérifiez s'il y a un paramètre de requête pour l'état du mode sombre
            var urlParams = new URLSearchParams(window.location.search);
            var darkModeQueryParam = urlParams.get('darkModeState');

            if (darkModeQueryParam === 'enabled') {
                // Appliquez le mode sombre si le paramètre de requête est défini sur "enabled"
                document.body.classList.add('dark-mode');
                document.getElementById('dark-button').checked = true; // Check the checkbox
                localStorage.setItem('darkMode', 'enabled');
            } else if (darkModeQueryParam === 'disabled') {
                // Appliquez le mode clair si le paramètre de requête est défini sur "disabled"
                document.body.classList.remove('dark-mode');
                document.getElementById('dark-button').checked = false; // Décocher la case
                localStorage.setItem('darkMode', 'disabled');
            } else if (darkModeState === 'enabled') {
                // Appliquez le mode sombre si localStorage est défini sur "enabled" et aucun paramètre de requête
                document.body.classList.add('dark-mode');
                document.getElementById('dark-button').checked = true; // Cocher la case
            }
        });

        function toggleDarkMode() {
            var element = document.body;
            var isDarkMode = !element.classList.contains('dark-mode');
            var darkButton = document.getElementById('dark-button');

            if (isDarkMode) {
                element.classList.add('dark-mode');
                darkButton.checked = true; // Cocher la case
                localStorage.setItem('darkMode', 'enabled');
            } else {
                element.classList.remove('dark-mode');
                darkButton.checked = false; // Décocher la case
                localStorage.setItem('darkMode', 'disabled');
            }
        }
    </script>
</html>"""
            # Write the HTML code of each player in a file inside the country folder
            player_html_file = os.path.join(country_folder, f"{country_name}_player_{index}.html")
            with open(player_html_file, "w", encoding="utf-8") as f:
                f.write(player_html_code)

    # -------------------------------------------------------------------------
    # --------------------------------- MAIN MENU -----------------------------
    # -------------------------------------------------------------------------

    # Create a new HTML file for the main menu
    main_menu_html = """
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="icon" type="image/png" href="https://static.wikia.nocookie.net/logopedia/images/3/38/RWC2023_2018-symbol.svg/revision/latest/scale-to-width-down/250?cb=20181116103448">
        <link rel="stylesheet" href="style_acceuil.css">
        <title>Rugby World Cup 2023</title>
    </head>
    <body>
        <script>
            function search() {{
                var input, filter, grid, items, player, txtValue;
                input = document.getElementById("searchInput");
                filter = input.value.toUpperCase();
                grid = document.querySelector(".grid-container");
                items = grid.getElementsByClassName("grid-item");

                for (var i = 0; i < items.length; i++) {{
                    player = items[i];
                    txtValue = player.textContent || player.innerText;
                    if (txtValue.toUpperCase().indexOf(filter) > -1) {{
                        player.style.display = "";
                    }} else {{
                        player.style.display = "none";
                    }}
                }}
            }}

            function toggleDarkMode() {
                var element = document.body;
                var isDarkMode = !element.classList.contains('dark-mode');
                var darkButton = document.getElementById('dark-button');

                if (isDarkMode) {
                    element.classList.add('dark-mode');
                    darkButton.checked = true; // Cocher la case
                    localStorage.setItem('darkMode', 'enabled');
                } else {
                    element.classList.remove('dark-mode');
                    darkButton.checked = false; // Décocher la case
                    localStorage.setItem('darkMode', 'disabled');
                }
            }

            document.addEventListener('DOMContentLoaded', function () {
            var darkModeState = localStorage.getItem('darkMode');

                // Vérifiez s'il y a un paramètre de requête pour l'état du mode sombre
                var urlParams = new URLSearchParams(window.location.search);
                var darkModeQueryParam = urlParams.get('darkModeState');

                if (darkModeQueryParam === 'enabled') {
                    // Appliquez le mode sombre si le paramètre de requête est défini sur "enabled"
                    document.body.classList.add('dark-mode');
                    document.getElementById('dark-button').checked = true; // Check the checkbox
                    localStorage.setItem('darkMode', 'enabled');
                } else if (darkModeQueryParam === 'disabled') {
                    // Appliquez le mode clair si le paramètre de requête est défini sur "disabled"
                    document.body.classList.remove('dark-mode');
                    document.getElementById('dark-button').checked = false; // Décocher la case
                    localStorage.setItem('darkMode', 'disabled');
                } else if (darkModeState === 'enabled') {
                    // Appliquez le mode sombre si localStorage est défini sur "enabled" et aucun paramètre de requête
                    document.body.classList.add('dark-mode');
                    document.getElementById('dark-button').checked = true; // Cocher la case
                }
            });

            function toggleDarkMode() {
                var element = document.body;
                var isDarkMode = !element.classList.contains('dark-mode');
                var darkButton = document.getElementById('dark-button');

                if (isDarkMode) {
                    element.classList.add('dark-mode');
                    darkButton.checked = true; // Cocher la case
                    localStorage.setItem('darkMode', 'enabled');
                } else {
                    element.classList.remove('dark-mode');
                    darkButton.checked = false; // Décocher la case
                    localStorage.setItem('darkMode', 'disabled');
                }
            }

            function goToLegalPage() {
                window.location.href = '../../legal_info.html'; // Adjust the path based on your directory structure
            }
        </script>
        <label class="switch">
            <span class="sun"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><g fill="#ffd43b"><circle r="5" cy="12" cx="12"></circle><path d="m21 13h-1a1 1 0 0 1 0-2h1a1 1 0 0 1 0 2zm-17 0h-1a1 1 0 0 1 0-2h1a1 1 0 0 1 0 2zm13.66-5.66a1 1 0 0 1 -.66-.29 1 1 0 0 1 0-1.41l.71-.71a1 1 0 1 1 1.41 1.41l-.71.71a1 1 0 0 1 -.75.29zm-12.02 12.02a1 1 0 0 1 -.71-.29 1 1 0 0 1 0-1.41l.71-.66a1 1 0 0 1 1.41 1.41l-.71.71a1 1 0 0 1 -.7.24zm6.36-14.36a1 1 0 0 1 -1-1v-1a1 1 0 0 1 2 0v1a1 1 0 0 1 -1 1zm0 17a1 1 0 0 1 -1-1v-1a1 1 0 0 1 2 0v1a1 1 0 0 1 -1 1zm-5.66-14.66a1 1 0 0 1 -.7-.29l-.71-.71a1 1 0 0 1 1.41-1.41l.71.71a1 1 0 0 1 0 1.41 1 1 0 0 1 -.71.29zm12.02 12.02a1 1 0 0 1 -.7-.29l-.66-.71a1 1 0 0 1 1.36-1.36l.71.71a1 1 0 0 1 0 1.41 1 1 0 0 1 -.71.24z"></path></g></svg></span>
            <span class="moon"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 384 512"><path d="m223.5 32c-123.5 0-223.5 100.3-223.5 224s100 224 223.5 224c60.6 0 115.5-24.2 155.8-63.4 5-4.9 6.3-12.5 3.1-18.7s-10.1-9.7-17-8.5c-9.8 1.7-19.8 2.6-30.1 2.6-96.9 0-175.5-78.8-175.5-176 0-65.8 36-123.1 89.3-153.3 6.1-3.5 9.2-10.5 7.7-17.3s-7.3-11.9-14.3-12.5c-6.3-.5-12.6-.8-19-.8z"></path></svg></span>
            <input type="checkbox" onclick="toggleDarkMode()" id="dark-button" class="input">
            <span class="slider"></span>
        </label>
        <div class="grid-container">
        <h1 class="page-title"><img class="title-icon" src="https://static.wikia.nocookie.net/logopedia/images/3/38/RWC2023_2018-symbol.svg/revision/latest/scale-to-width-down/250?cb=20181116103448" alt="Rugby World cup 2023 Logo">2023's Rugby Wolrd cup Teams</h1>
        <div class="form-control">
            <input type="text" id="searchInput" required="" onkeyup="search()">
            <label>
                <span style="transition-delay:0ms">C</span>
                <span style="transition-delay:50ms">o</span>
                <span style="transition-delay:100ms">u</span>
                <span style="transition-delay:150ms">n</span>
                <span style="transition-delay:200ms">t</span>
                <span style="transition-delay:250ms">r</span>
                <span style="transition-delay:300ms">y</span>
            </label>
        </div>"""

    # Add a card for each country
    for country_name, country_df in country_data.items():
        main_menu_html += f"""
            <div class="grid-item" data-name="{country_name}">
                <a href='{country_name}/{country_name}_data.html'><img src="{country_df['Country-Draw'].iloc[0]}" alt="{country_name}"  loading="lazy"></a>
                <p>{country_name}</p>
            </div>"""

    main_menu_html += """
        </div>
        <footer>
            <div class="footer-buttons">
                <button class="ui-btn legal" id="legal" onclick="goToLegalPage()"><span>Legal Notice</span></button>
            </div>
            <div class="footer-info">
                <p>SAÉ 3.VCOD.01 Collecte automatisée de données web (2023-2024)
                <br>Website generated as part of coursework
                <br>By : Romain Troillard, Dorian Relave, Moetaz Ben Ahmed, Abder Rahman Bouaouina</p>
            </div>
        </footer>
    </body>
</html>"""

    # Write the HTML code for the main menu
    main_menu_file = os.path.join(r"Choice_2//Web_Files", "main_menu.html")
    with open(main_menu_file, "w", encoding="utf-8") as f:
        f.write(main_menu_html)

    chemin_absolu = os.path.abspath(r"Choice_2//Web_Files/main_menu.html")
    webbrowser.open("file://" + chemin_absolu)

    return "Execution completed"

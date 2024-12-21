=========================================================
Système d'Information de la Coupe du Monde de Rugby 2023
=========================================================

===== Utilisation : =====
---------------------------------------------------------
Executer le menu via le fichier "main.py"

Observer les fichiers de sortie dans les dossier windows 
créer apres execution. 
Ceci sont nommés en fonction du choix.
---------------------------------------------------------

**Description**

Ce programme offre un système d'information interactif pour la Coupe du Monde de Rugby 2023. 
Il propose différentes fonctionnalités telles que l'affichage des informations sur les équipes, les joueurs, les matchs, ainsi que la création de fichiers CSV.

**Fichiers du Projet**

- `one_squad_data.py`: Contient le script pour afficher les informations sur une équipe.
- `all_squads_data.py`: Contient le script pour afficher les informations sur toutes les équipes.
- `matchs.py`: Contient le script pour afficher les informations sur les matchs.
- `create_CSV.py`: Contient le script pour créer les fichiers CSV nécessaires.
- `create_CSS.py`: Contient le script pour générer des fichiers CSS pour la création de pages Web.
- `main.py`: Contient le script principal avec un menu interactif.

**Dépendances**

- requests: Pour effectuer des requêtes HTTP.
- beautifulsoup4: Pour l'analyse HTML.
- selenium==3.14: Pour Une autre partie de l'Analyse HTML via les balises CSS.
- pandas: Pour la manipulation des données en tableau.
- unidecode: Pour normaliser les caractères Unicode.
- locale: Pour la gestion des formats de données locaux.
- webbrowser: Pour ouvrir des fichiers dans le navigateur.
- numpy: Pour le format des valeurs manquantes.
- tabulate: Pour l'affichage en table.
- time: Pour calculer le temps d'execution. 

Ainsi que :
- os
- glob
- csv
- platform

Ainsi que l'intallation de du navigateur Mozilla Firefox
Dans le disque dur C, chemin : C:\Program Files\Mozilla Firefox\firefox.exe
(chemin par défaut après installation)

Les fichiers web générer sont pleinement mis en forme, compatible et ont été testé avec les navigateurs Firefox, Opera et Edge

**Exécution**

Exécutez le script principal `main.py` pour accéder au menu interactif et choisir parmi les fonctionnalités disponibles.

**Instructions**

1. Sélectionnez l'option appropriée dans le menu en entrant un nombre entre 1 et 5.
2. Suivez les instructions spécifiques à chaque option pour interagir avec le système d'information.
3. Observez le résultat de votre option dans le dossier numéroté associé "Choice_{Numéro d'option}"

**Notes Importantes**

- L'option 4 (Créer les fichiers CSV) peut prendre un certain temps en raison du téléchargement de données en ligne. (Environ 40 minutes)
- Pour visualiser les informations sous forme de page Web, assurez-vous que le navigateur par défaut de votre système est correctement 
configuré et installé dans le fichier par défaut (C:\Program Files\Mozilla Firefox\firefox.exe). Les pages sont compatibles avec les 
versions les plus récentes des navigateurs cités.

**Remarque**

Veuillez consulter les fichiers python individuels pour des informations spécifiques sur chaque script.

**Credits**

Credit des éléments de design des sites créés : 

Le bouton de mode sombre : 
	lien : https://uiverse.io/andrew-demchenk0/honest-stingray-90
	Basé sur le design de "andrew-demchenk0".

Les boutons de retour à l'accueil, et de joueur suivant et précédent :
	lien : https://uiverse.io/ke1221/ancient-walrus-24
	Basé sur le design de "ke1221", et modifié. 

Le champ de recherche, de pays ou de joueurs :
	lien : https://uiverse.io/liyaxu123/warm-eel-62
	Basé sur le design de "liyaxu123".

Les cartes de match par phase :
	lien : https://uiverse.io/Praashoo7/old-dingo-81
	Basé sur le design de "Praashoo7", et largement modifier pour etre adapté à nos informations.

**Auteurs**
Ce projet a été développé par 
	Romain TROILLARD
	Dorian RELAVE
	Moetaz BENHAMED
	Abder-Rahman BOUAOUINA

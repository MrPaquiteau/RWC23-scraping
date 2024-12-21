=========================================================
Explication des fichiers Swift
=========================================================

---------------------------------------------------------
- `DataFactory.swift`
  Création d'une fonction loadCSV qui prend en parametre un fichier CSV, puis en fait une chaine de charactere
  très longue, puis on sépare les valeurs grâce aux , et on ajoute chaque valeur a la colonne associée de la
  structure appelé (Stats, Player, Matchs, Team). Donc affectation de la fonction à toute les structures.
---------------------------------------------------------

---------------------------------------------------------
- `TeamView.swift`
  Création de la vue Team (voir TeamView.JPEG pour le résultat)
  Initialisation de la variable teams qui récupére le CSV "equipe" afin de créer une liste
  de toute les équipes avec leur image (importé dans un fichier Assets avec comme nom l'id de l'équipe)
  Ajout de la possibilité de rechercher et tri par ordre alphabetique.
  NvaigationView et NavigationLink pour accéder aux pages "PlayersView"
---------------------------------------------------------   

---------------------------------------------------------
- `PlayersView.swift`
  Création de la vue Players (voir PlayersView.JPEG pour le résultat)
  Même fonctionnement que TeamView mais ici PlayersView prend en parametre forCountry qui est le
  nom du pays qui sert à afficher seulement les joueurs qui ont comme pays le même que forCountry
  NavigationLink seulement pour accéder aux stats car le NavigationView de la page précédente est affecté à 
  toute les autres pages après
---------------------------------------------------------

---------------------------------------------------------
- `StatsPlayersView.swift`
  Création de la vue StatsPlayer (voir StatsPlayersView.JPEG pour le résultat)
  Idem avec forPlayer au lieu de forCountry
  Création d'une structure "StatisticView" pour faciliter l'affichage des statistiques,
  cela marche un peu comme une fonction python.
---------------------------------------------------------

---------------------------------------------------------
- `MatchsView.swift`
  Création de la vue Matchs (voir MatchsView.JPEG pour le résultat)
  Importation des fichiers CSV "all_matchs", "equipe".
  Création de la possibilité de filtrer par poules et phases avec la variable "filteredMatches".
  Affichage des matchs selon le filtre selectionné.
  Création des sections matchs selon image, nom, score

  Structure MatchDetailsView qui affiche les détails des matchs en feuille qui s'ouvre et non pas
  dans une autre vue.
---------------------------------------------------------

---------------------------------------------------------
- `ContentView.swift`
  Permet de mettre une barre de navigation en bas dans toutes les pages.
  Lien sur les vues matchs et teams
---------------------------------------------------------

---------------------------------------------------------
- `RWC23App.swift`
  Fichier de lancement de l'appli qui est redirigé vers ContentView
---------------------------------------------------------

=========================================================
Quelques notions : 

`var` est une variable que l'on peut modifier.
`let` est une constante elle a le même role que var mais ne peut pas être modifié après initialisation.
`Hstack` permet d'empiler des éléments de texte, d'image etc de manière horizontale.
`Vstack` permet d'empiler des éléments de texte, d'image etc de manière verticale.
`Zstack` permet de superposer des éléments.
`@State` variable d'état
`private` variable utilisable seulement dans la structure dont elle fait partie






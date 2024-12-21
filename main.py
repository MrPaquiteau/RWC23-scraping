import create_CSV
import one_squad_data
import all_squads_data
import matchs


def main():
    """
    Affiche les options du menu principal pour le système d'information de la
    Coupe du Monde de Rugby 2023.

    Options :
    1. Afficher la liste des joueurs et leurs informations pour UNE équipe.
    2. Voir la liste des équipes et accéder à leurs joueurs.
    3. Voir les matchs et leurs informations.
    4. Créer les fichiers CSV nécessaires pour le choix 2. (exécution très longue)
    5. Quitter.

    Returns
    -------
    None.

    """
    print("")
    print(30 * "-", "MENU", 30 * "-")
    print("1. View the list of players and their information for ONE team.")
    print("2. View the list of teams and access their players.")
    print("3. View matches and information about them.")
    print("4. Create the CSV files necessary for choice 2. (long execution 20-40 minutes)")
    print("5. Exit.")
    print(66 * "-")
    print("")


loop = False
while not loop:
    main()
    choice = int(input("Choose from the menu (Between 1 and 5) : "))
    if choice == 1:
        one_squad_data.exec()
    elif choice == 2:
        all_squads_data.exec()
    elif choice == 3:
        matchs.exec()
    elif choice == 4:
        create_CSV.exec()
    elif choice == 5:
        print("Menu exited successfully")
        loop = True
    else:
        print("Not between 1 and 5")
    print("")

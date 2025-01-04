//
//  TeamsView.swift
//  RWC23
//
//  Created by Romain TROILLARD on 1/4/25.
//

import SwiftUI

struct TeamsView: View {
    @State private var searchText = ""
    var teams = Team.loadJSON(from: "teams_players_matches")
    
    // Filtrer et trier les équipes
    var filteredAndSortedTeams: [Team] {
        let filtered = Array(teams.values).filter {
            searchText.isEmpty || $0.country.localizedCaseInsensitiveContains(searchText)
        }
        return filtered.sorted { $0.country < $1.country }
    }
    
    var body: some View {
        NavigationView {
            List {
                ForEach(filteredAndSortedTeams, id: \.id) { team in
                    // NavigationLink pour naviguer vers PlayersView
                    NavigationLink(destination: PlayersView(team: team)) {
                        HStack {
                            // Afficher l'image du drapeau
                            AsyncImage(url: URL(string: team.images.flag)) { phase in
                                switch phase {
                                case .empty:
                                    ProgressView() // Affiche un indicateur de chargement pendant le téléchargement
                                case .success(let image):
                                    image
                                        .resizable()
                                        .scaledToFit()
                                        .frame(width: 50, height: 30) // Ajustez la taille selon vos besoins
                                case .failure:
                                    Image(systemName: "xmark.circle") // Affiche une icône d'erreur si le chargement échoue
                                        .resizable()
                                        .scaledToFit()
                                        .frame(width: 50, height: 30)
                                @unknown default:
                                    EmptyView()
                                }
                            }
                            
                            // Afficher le nom du pays
                            Text(team.country)
                                .font(.headline)
                        }
                        .padding(.vertical, 8) // Ajouter un espacement vertical entre les éléments
                    }
                }
            }
            .navigationTitle("Teams")
            .searchable(text: $searchText, prompt: "Search for a team")
        }
    }
}

struct TeamsView_Previews: PreviewProvider {
    static var previews: some View {
        TeamsView()
    }
}

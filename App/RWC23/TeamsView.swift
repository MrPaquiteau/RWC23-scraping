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
    
    // Définir la disposition de la grille
    let columns = [
        GridItem(.flexible(), spacing: 16),
        GridItem(.flexible(), spacing: 16)
    ]
    
    var body: some View {
        NavigationView {
            ScrollView {
                LazyVGrid(columns: columns, spacing: 16) {
                    ForEach(filteredAndSortedTeams, id: \.id) { team in
                        NavigationLink(destination: PlayersView(team: team)) {
                            VStack {
                                // Afficher l'image du drapeau en fonction du mode sombre ou clair
                                Image("\(team.code)-\(colorScheme == .dark ? "dark" : "light")")
                                    .resizable()
                                    .scaledToFit()
                                    .frame(width: 130, height: 80) // Agrandir l'image
                                    .cornerRadius(8)
                                
                                // Afficher le nom du pays
                                Text(team.country)
                                    .font(.headline)
                                    .foregroundColor(.primary)
                                    .multilineTextAlignment(.center)
                                    .padding(.top, 4)
                            }
                            .padding()
                            .background(Color(.systemBackground))
                            .cornerRadius(12)
                            .shadow(radius: 5)
                            .overlay(
                                RoundedRectangle(cornerRadius: 8)
                                    .stroke(borderColor, lineWidth: 2) // Bordure adaptative
                            )
                        }
                    }
                }
                .padding()
            }
            .navigationTitle("Teams")
            .searchable(text: $searchText, prompt: "Search for a team")
        }
    }
    
    // Obtenir le mode de couleur actuel
    @Environment(\.colorScheme) var colorScheme
    
    // Couleur de la bordure en fonction du mode sombre ou clair
    var borderColor: Color {
        colorScheme == .dark ? .white : .black
    }
}

struct TeamsView_Previews: PreviewProvider {
    static var previews: some View {
        TeamsView()
    }
}

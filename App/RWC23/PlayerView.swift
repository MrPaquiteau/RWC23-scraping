//
//  PlayersView.swift
//  RWC23
//
//  Created by Romain TROILLARD on 1/4/25.
//

import SwiftUI

// MARK: - PlayersView
// View to display the list of players for a selected team.
struct PlayersView: View {
    var team: Team // The selected team
    @State private var searchText = "" // State variable for search functionality
    
    var body: some View {
        // List of players in the team
        List(team.players, id: \.id) { player in
            // Navigation link to the player's stats view
            NavigationLink(destination: PlayerStatsView(player: player)) {
                VStack(alignment: .leading) {
                    Text(player.name)
                        .font(.headline) // Display the player's name
                }
                .padding(.vertical, 8)
            }
        }
        .navigationTitle(team.country) // Set the navigation title to the team's country
        .searchable(text: $searchText, prompt: "Search for a player") // Add search functionality
    }
}

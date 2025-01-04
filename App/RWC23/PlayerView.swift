//
//  PlayersView.swift
//  RWC23
//
//  Created by Romain TROILLARD on 1/4/25.
//

import SwiftUI

struct PlayersView: View {
    var team: Team // L'équipe sélectionnée
    
    var body: some View {
        List(team.players, id: \.id) { player in
            NavigationLink(destination: PlayerStatsView(player: player)) {
                VStack(alignment: .leading) {
                    Text(player.name)
                        .font(.headline)
                }
                .padding(.vertical, 8)
            }
        }
        .navigationTitle(team.country) // Titre de la vue = nom de l'équipe
    }
}

//
//  PlayersView.swift
//  TestDataframe
//
//  Created by Romain TROILLARD on 30/11/2023.
//

import SwiftUI

struct PlayersView: View {
    var forCountry: String
    
    var players = Player.loadCSV(from: "all_players")

    var body: some View {
        let team = searchTeam(forCountry: self.forCountry)
        List{
            Section(header:
                VStack {
                Image(team!.Id)
                    .resizable()
                    .frame(width: 60, height: 60)
                }
                .multilineTextAlignment(.center)
                .frame(maxWidth: .infinity)
                .padding(.bottom, 20)
            ) {
                ForEach(players.filter {$0.Country.contains(forCountry.capitalized)}
                    .sorted(by: {$0.Name < $1.Name})) {
                    player in
                        NavigationLink(destination: StatsPlayerView(forPlayer_Id: player.Id)) {
                            Text(player.Name)
                    }
                    .navigationBarTitleDisplayMode(.inline)
                    .navigationTitle(Text(team!.Country.capitalized))
                    .toolbar {
                        ToolbarItem(placement: .principal) {
                            Text(team!.Country)
                                .font(.system(size: 20))
                                .bold()
                        }
                    }
                }
            }
        }
    }
}


func searchTeam(forCountry Country: String)->Team? {
    let teams = Team.loadCSV(from: "equipe")

    if let teamIndex = teams.firstIndex(where: { $0.Country == Country}) {
        return teams[teamIndex]
    } else {
        return nil
    }
}

struct PlayersView_Preview: PreviewProvider {
    static var previews: some View {
        PlayersView(forCountry: "FRANCE")
    }
}

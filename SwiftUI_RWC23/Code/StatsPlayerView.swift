//
//  StatsPlayerView.swift
//  TestDataframe
//
//  Created by Romain TROILLARD on 01/12/2023.
//

import SwiftUI

struct StatisticView: View {
    let title: String
    let value: String

    var body: some View {
        HStack(spacing: 16) {
            VStack(alignment: .leading) {
                Text(title)
            }
            Spacer()
            VStack {
                Text(value)
            }
        }
    }
}


struct StatsPlayerView: View {
    
    var forPlayer_Id : String
    
    var stats = Stats.loadCSV(from: "all_players_stats")
    
    var body: some View {
        let player = searchPlayerID(forPlayer_Id: self.forPlayer_Id)
        List{
            ForEach(stats.filter { $0.Id_Player == forPlayer_Id }) { stat in
                StatisticView(title: "Kicks From Hand", value: stat.Kicks_From_Hand)
                StatisticView(title: "Runs", value: stat.Runs)
                StatisticView(title: "Passes", value: stat.Passes)
                StatisticView(title: "Offloads", value: stat.Offloads)
                StatisticView(title: "Clean Breaks", value: stat.Clean_Break)
                StatisticView(title: "Defenders Beaten", value: stat.Defenders_Beaten)
                StatisticView(title: "Yellow Cards", value: stat.Yellow_Cards)
                StatisticView(title: "Red Cards", value: stat.Red_Cards)
                StatisticView(title: "Carries", value: stat.Carries)
                StatisticView(title: "Metres Made", value: stat.Metres_Made)
                StatisticView(title: "Tackles", value: stat.Tackles)
                StatisticView(title: "Tackles Success", value: stat.Tackles_Success)
                StatisticView(title: "Handling Errors", value: stat.Handling_Errors)
                StatisticView(title: "Turnovers", value: stat.Turnovers)
            }
        }
        .toolbar {
            ToolbarItem(placement: .principal) {
                Text(player?.Name ?? "")
                    .font(.system(size: 20))
                    .bold()
            }
        }
    }
}



func searchPlayerID(forPlayer_Id PlayerID: String)->Player? {
    let players = Player.loadCSV(from: "all_players")
    if let playerIndex = players.firstIndex(where: { $0.Id == PlayerID}) {
        return players[playerIndex]
    } else {
        return nil
    }
}


struct StatsPlayersView_Preview: PreviewProvider {
    static var previews: some View {
        StatsPlayerView(forPlayer_Id: "Fra-15")
    }
}


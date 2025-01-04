//
//  MatchesView.swift
//  Rugby-World-Cup-23
//
//  Created by Romain TROILLARD on 05/12/2023.
//

import SwiftUI

struct MatchesView: View {
    @State private var selectedMatch: Match?
    @State private var selectedFilter: String = "All Matchs"
    
    // Charger les matchs depuis le fichier JSON
    var matchesByStage = Match.loadJSON(from: "matches_by_stage")
    
    // Charger les équipes
    var teams = Team.loadJSON(from: "teams_players_matches")
    
    // Convertir les matchs en une seule liste
    var allMatches: [Match] {
        matchesByStage.values.flatMap { $0 }
    }
    
    // Filtrer les matchs en fonction de l'étape sélectionnée
    var filteredMatches: [Match] {
        if selectedFilter == "All Matchs" {
            return allMatches
        } else {
            return matchesByStage[selectedFilter] ?? []
        }
    }
    
    var body: some View {
        NavigationView {
            Form {
                Section {
                    Picker("Filter By", selection: $selectedFilter) {
                        Text("All Matchs").tag("All Matchs")
                        Text("Pool A").tag("Pool A")
                        Text("Pool B").tag("Pool B")
                        Text("Pool C").tag("Pool C")
                        Text("Pool D").tag("Pool D")
                        Text("Quarter-Final").tag("Quarter-Final")
                        Text("Semi-Final").tag("Semi-Final")
                        Text("Bronze Final").tag("Bronze Final")
                        Text("Final").tag("Final")
                    }
                    .pickerStyle(.menu)
                    .padding()
                }
                
                List {
                    ForEach(filteredMatches) { match in
                        Section {
                            MatchRow(match: match, teams: teams)
                                .contentShape(Rectangle())
                                .onTapGesture {
                                    selectedMatch = match
                                }
                        }
                    }
                }
                .listSectionSpacing(15)
            }
            .navigationTitle("Matches")
            .sheet(item: $selectedMatch) { match in
                MatchDetailsView(match: match)
                    .presentationDetents([.height(250)])
            }
        }
    }
}

struct MatchRow: View {
    let match: Match
    let teams: [String: Team]
    
    var body: some View {
        VStack {
            TeamRow(teamName: match.home.team, score: match.home.score, teams: teams)
            TeamRow(teamName: match.away.team, score: match.away.score, teams: teams)
        }
    }
}

struct TeamRow: View {
    let teamName: String
    let score: Int
    let teams: [String: Team]
    
    var body: some View {
        if let team = teams.first(where: { $0.value.country.uppercased() == teamName.uppercased() })?.value {
            HStack {
                AsyncImage(url: URL(string: team.images.flag)) { image in
                    image
                        .resizable()
                        .frame(width: 30, height: 35)
                        .cornerRadius(5)
                } placeholder: {
                    ProgressView()
                }
                Text(teamName)
                    .bold()
                Spacer()
                Text("\(score)")
                    .bold()
            }
        } else {
            HStack {
                Image(systemName: "questionmark.circle")
                    .resizable()
                    .frame(width: 30, height: 30)
                    .cornerRadius(5)
                Text(teamName)
                    .bold()
                Spacer()
                Text("\(score)")
                    .bold()
            }
        }
    }
}

struct MatchDetailsView: View {
    let match: Match
    var teams = Team.loadJSON(from: "teams_players_matches")
    
    var body: some View {
        let homeTeam = teams.first(where: { $0.value.country.uppercased() == match.home.team.uppercased() })?.value
        let awayTeam = teams.first(where: { $0.value.country.uppercased() == match.away.team.uppercased() })?.value
        
        VStack {
            Text("Stage: \(match.stage)")
                .font(.system(size: 16))
                .bold()
                .padding()
            
            HStack {
                // Afficher l'équipe "home" avec son drapeau
                ZStack {
                    Rectangle()
                        .frame(width: 120, height: 120)
                        .opacity(0) // Rectangle invisible pour aligner le contenu
                    VStack(alignment: .center) {
                        AsyncImage(url: URL(string: homeTeam!.images.flag)) { image in
                            image
                                .resizable()
                                .frame(width: 50, height: 60)
                                .cornerRadius(5)
                        } placeholder: {
                            ProgressView() // Affiche un indicateur de chargement pendant le téléchargement
                        }
                        Text(homeTeam!.country.capitalized)
                            .bold()
                            .font(.system(size: 14))
                    }
                }
        
                Spacer()
                
                VStack {
                    Text("\(match.home.score) - \(match.away.score)")
                        .font(.system(size: 40))
                        .bold()
                }
                
                Spacer()
                
                ZStack {
                    Rectangle()
                        .frame(width: 120, height: 120)
                        .opacity(0)
                    VStack(alignment: .center) {
                        AsyncImage(url: URL(string: awayTeam!.images.flag)) { image in
                            image
                                .resizable()
                                .frame(width: 50, height: 60)
                                .cornerRadius(5)
                        } placeholder: {
                            ProgressView()
                        }
                        Text(awayTeam!.country.capitalized)
                            .bold()
                            .font(.system(size: 14))
                    }
                }
            }
            Text(match.location)
                .font(.system(size: 16))
                .bold()
            Text(match.date)
                .font(.system(size: 16))
                .bold()
        }
    }
}

struct MatchesView_Previews: PreviewProvider {
    static var previews: some View {
        MatchesView()
    }
}

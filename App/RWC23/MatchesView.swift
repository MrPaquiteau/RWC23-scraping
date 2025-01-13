//
//  MatchesView.swift
//  Rugby-World-Cup-23
//
//  Created by Romain TROILLARD on 05/12/2023.
//

import SwiftUI

// MARK: - MatchesView
// Main view to display Rugby World Cup matches.
struct MatchesView: View {
    @State private var selectedMatch: Match? // Selected match to show details
    @State private var selectedFilter: String = "All Matches" // Selected filter to display matches
    
    // Load matches from JSON file
    var matchesByStage = Match.loadJSON(from: "matches_by_stage")
    
    // Load teams from JSON file
    var teams = Team.loadJSON(from: "teams_players_matches")
    
    // Convert matches into a single list
    var allMatches: [Match] {
        matchesByStage.values.flatMap { $0 }
    }
    
    // Filter matches based on the selected stage
    var filteredMatches: [Match] {
        let matches: [Match]
        if selectedFilter == "All Matches" {
            matches = allMatches
        } else {
            matches = matchesByStage[selectedFilter] ?? []
        }
        // Order matches by date
        return matches.sorted { match1, match2 in
            let date1 = dateFormatter.date(from: match1.date) ?? Date.distantPast
            let date2 = dateFormatter.date(from: match2.date) ?? Date.distantPast
            return date1 < date2
        }
    }
    
    // Date formatter for match dates
    private let dateFormatter: DateFormatter = {
        let formatter = DateFormatter()
        formatter.dateFormat = "d MMMM yyyy"
        formatter.locale = Locale(identifier: "en_US")
        return formatter
    }()
    
    var body: some View {
        NavigationView {
            Form {
                Section {
                    // Picker to filter matches by stage
                    Picker("Filter By", selection: $selectedFilter) {
                        Text("All Matches").tag("All Matches")
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
                
                // List of filtered matches
                List {
                    ForEach(filteredMatches) { match in
                        Section {
                            // Display a match row
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
            // Show details of the selected match in a modal sheet
            .sheet(item: $selectedMatch) { match in
                MatchDetailsView(match: match)
                    .presentationDetents([.height(250)])
            }
        }
    }
}

// MARK: - MatchRow
// View to display a single match row with home and away teams.
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

// MARK: - TeamRow
// View to display a team row with flag, name, and score.
struct TeamRow: View {
    let teamName: String
    let score: Int
    let teams: [String: Team]
    
    var body: some View {
        if let team = teams.first(where: { $0.value.country.uppercased() == teamName.uppercased() })?.value {
            HStack {
                Image("\(team.code)-flag")
                    .resizable()
                    .frame(width: 30, height: 40)
                    .cornerRadius(5)
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

// MARK: - MatchDetailsView
// View to display detailed information about a selected match.
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
                // Display the home team with its flag
                ZStack {
                    Rectangle()
                        .frame(width: 120, height: 120)
                        .opacity(0) // Invisible rectangle to align content
                    VStack(alignment: .center) {
                        Image("\(homeTeam!.code)-flag")
                            .resizable()
                            .frame(width: 60, height: 80)
                            .cornerRadius(5)
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
                        Image("\(awayTeam!.code)-flag")
                            .resizable()
                            .frame(width: 60, height: 80)
                            .cornerRadius(5)
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
// MARK: - MatchesView_Previews
// Preview provider for MatchesView.
struct MatchesView_Previews: PreviewProvider {
    static var previews: some View {
        MatchesView()
    }
}

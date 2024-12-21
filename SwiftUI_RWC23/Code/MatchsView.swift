//
//  MatchsView.swift
//  Rugby-World-Cup-23
//
//  Created by Romain TROILLARD on 05/12/2023.
//

import SwiftUI

struct MatchsView: View {
    @State private var selectedMatch: Matchs?
    @State private var selectedFilter: String = "All Matchs"
    
    var matchs = Matchs.loadCSV(from: "all_matchs")
    var teams = Team.loadCSV(from: "equipe")
    
    var filteredMatches: [Matchs] {
        switch selectedFilter {
        case "Pool A":
            return matchs.filter {$0.Stage == "Pool A"}
        case "Pool B":
            return matchs.filter {$0.Stage == "Pool B"}
        case "Pool C":
            return matchs.filter {$0.Stage == "Pool C"}
        case "Pool D":
            return matchs.filter {$0.Stage == "Pool D"}
        case "Quarter-finals":
            return matchs.filter {$0.Stage == "1/4"}
        case "Semi-finals":
            return matchs.filter {$0.Stage == "1/2"}
        case "Third place":
            return matchs.filter {$0.Stage == "Third place"}
        case "Final":
            return matchs.filter {$0.Stage == "Final"}
        case "All Matchs":
            return matchs
        default:
            return matchs
        }
    }
    
    var body: some View {
        Form {
            Section {
                Picker("Filter By", selection: $selectedFilter) {
                    Text("All Matchs").tag("All Matchs")
                    Text("Pool A").tag("Pool A")
                    Text("Pool B").tag("Pool B")
                    Text("Pool C").tag("Pool C")
                    Text("Pool D").tag("Pool D")
                    Text("Quarter-finals").tag("Quarter-finals")
                    Text("Semi-finals").tag("Semi-finals")
                    Text("Third place").tag("Third place")
                    Text("Final").tag("Final")
                }
                .pickerStyle(.menu)
                .padding()
            }
            List {
                ForEach(filteredMatches) { match in
                    Section {
                        let homeTeam = teams.first(where: { $0.Country == match.Team_Home.uppercased()})
                        let awayTeam = teams.first(where: { $0.Country == match.Team_Away.uppercased()})
                        VStack {
                            HStack {
                                Image(homeTeam!.Id)
                                    .resizable()
                                    .frame(width: 30, height: 30)
                                    .cornerRadius(5)
                                Text(match.Team_Home)
                                    .bold()
                                Spacer()
                                Text(match.Score_Home)
                                    .bold()
                            }
                            HStack {
                                Image(awayTeam!.Id)
                                    .resizable()
                                    .frame(width: 30, height: 30)
                                    .cornerRadius(5)
                                Text(match.Team_Away)
                                    .bold()
                                Spacer()
                                Text(match.Score_Away)
                                    .bold()
                            }
                            
                        }
                        
                    }
                    .contentShape(Rectangle())
                    .onTapGesture {
                        selectedMatch = match
                    }
                }
                .sheet(item: $selectedMatch) { match in
                    MatchDetailsView(match: match)
                        .presentationDetents([.height(250)])
                }
            }
            .listSectionSpacing(15)
        }
    }
}


struct MatchDetailsView: View {
    let match: Matchs
    var teams = Team.loadCSV(from: "equipe")
    
    var body: some View {
        let homeTeam = teams.first(where: { $0.Country == match.Team_Home.uppercased()})
        let awayTeam = teams.first(where: { $0.Country == match.Team_Away.uppercased()})
        VStack {
            Text("Counting for \(match.Stage)")
                .font(.system(size: 16))
                .bold()
            HStack{
                ZStack {
                    Rectangle()
                        .frame(width: 120, height: 120)
                        .opacity(0)
                    VStack(alignment: .center){
                        Image(homeTeam!.Id)
                            .resizable()
                            .frame(width: 60, height: 60)
                            .cornerRadius(5)
                        Text(homeTeam!.Country.capitalized)
                            .bold()
                            .font(.system(size: 14))
                    }
                }
                Spacer()
                VStack {
                    Text("\(match.Score_Home) : \(match.Score_Away)")
                        .font(.system(size: 40))
                        .bold()
                }
                Spacer()
                ZStack {
                    Rectangle()
                        .frame(width: 120, height: 120)
                        .opacity(0)
                    VStack(alignment: .center){
                        Image(awayTeam!.Id)
                            .resizable()
                            .frame(width: 60, height: 60)
                            .cornerRadius(5)
                        Text(awayTeam!.Country.capitalized)
                            .bold()
                            .font(.system(size: 14))
                    }
                }
            }
            Text(match.Stadium)
                .font(.system(size: 16))
                .bold()
            Text(match.Date)
                .font(.system(size: 16))
                .bold()
        }
    }
}


struct MatchsView_Preview: PreviewProvider {
    static var previews: some View {
        MatchsView()
    }
}

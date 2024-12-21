//
//  TeamView.swift
//  TestDataframe
//
//  Created by Romain TROILLARD on 30/11/2023.
//

import SwiftUI

struct TeamView: View {
    @State private var searchText = ""
    var teams = Team.loadCSV(from: "equipe")
    var body: some View {
            NavigationView {
                List {
                    ForEach(teams.filter {
                        searchText.isEmpty ||
                        $0.Country.localizedCaseInsensitiveContains(searchText)
                    }
                    .sorted(by: { $0.Country < $1.Country })) { team in
                        Section {
                            NavigationLink(
                            destination: PlayersView(forCountry: team.Country)) {
                                HStack {
                                    Image(team.Id)
                                        .resizable()
                                        .frame(width: 25, height: 25)
                                        .cornerRadius(5)
                                    Text(team.Country)
                                        .bold()
                                }
                                .frame(height: 45)
                            }
                        }
                    }
                }
                .listSectionSpacing(15)
                .searchable(text: $searchText)
                .navigationTitle("Teams")
            }
        }
    }

struct TeamView_Preview: PreviewProvider {
    static var previews: some View {
        TeamView()
    }
}

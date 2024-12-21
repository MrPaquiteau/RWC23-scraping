//
//  ContentView.swift
//  Rugby-World-Cup-23
//
//  Created by Romain TROILLARD on 07/12/2023.
//

import SwiftUI

struct ContentView: View {
    @State private var selection = 1
    
    var body: some View {
        TabView(selection: $selection) {
            TeamView()
                .tabItem {
                    Label("Teams", systemImage: "person.3.sequence")
            }
                .tag(1)
                .transition(.slide)
            MatchsView()
                .tabItem {
                    Label("Matchs", systemImage: "sportscourt")
                }
                .tag(2)
                .transition(.slide)
        }
        .accentColor(Color.blue)
    }
}


struct ContentView_Preview: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

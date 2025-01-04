//
//  ContentView.swift
//  RWC23
//
//  Created by Romain TROILLARD on 1/4/25.
//

import SwiftUI

struct ContentView: View {
    @State private var selection = 1
    
    var body: some View {
        TabView(selection: $selection) {
            TeamsView()
                .tabItem {
                    Label("Teams", systemImage: "person.3.sequence")
            }
                .tag(1)
                .transition(.slide)
            MatchesView()
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


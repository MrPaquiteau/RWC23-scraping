//
//  ContentView.swift
//  RWC23
//
//  Created by Romain TROILLARD on 1/4/25.
//

import SwiftUI

// MARK: - ContentView
// Main view that serves as the entry point for the app, containing a tab view for navigation.
struct ContentView: View {
    @State private var selection = 1 // State variable to track the selected tab
    
    var body: some View {
        // TabView to switch between different views
        TabView(selection: $selection) {
            // Teams tab
            TeamsView()
                .tabItem {
                    Label("Teams", systemImage: "person.3.sequence")
                }
                .tag(1) // Unique identifier for the tab
                .transition(.slide) // Slide transition when switching tabs
            
            // Matches tab
            MatchesView()
                .tabItem {
                    Label("Matchs", systemImage: "sportscourt")
                }
                .tag(2) // Unique identifier for the tab
                .transition(.slide) // Slide transition when switching tabs
        }
        .accentColor(Color.blue) // Set the accent color for the tab view
    }
}

// MARK: - ContentView_Preview
// Preview provider for ContentView.
struct ContentView_Preview: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

//
//  DataFactory.swift
//  RWC23
//
//  Created by Romain TROILLARD on 1/4/25.
//

import Foundation
import UIKit

// MARK: - Team Structure
// Represents a rugby team with identifiable and codable properties.
struct Team: Identifiable, Codable {
    var id: String? // Optional unique identifier for the team
    var code: String // Team code (e.g., "FRA" for France)
    var country: String // Country name of the team
    var images: TeamImages // Images associated with the team (flag, shape, logo)
    var players: [Player] // List of players in the team
}

// MARK: - TeamImages Structure
// Represents the images associated with a team.
struct TeamImages: Codable {
    var flag: String // URL or path to the team's flag image
    var shape: String // URL or path to the team's shape image
    var logo: TeamLogo // Team logo with light and dark variants
}

// MARK: - TeamLogo Structure
// Represents the team's logo with light and dark variants.
struct TeamLogo: Codable {
    var light: String // URL or path to the light version of the logo
    var dark: String // URL or path to the dark version of the logo
}

// MARK: - Player Structure
// Represents a rugby player with identifiable and codable properties.
struct Player: Identifiable, Codable {
    var id: String // Unique identifier for the player
    var name: String // Player's name
    var age: Int? // Optional age of the player
    var position: String? // Optional position of the player (e.g., "Flyhalf")
    var height: Int? // Optional height of the player in centimeters
    var weight: Int? // Optional weight of the player in kilograms
    var hometown: String? // Optional hometown of the player
    var photo: String? // URL or path to the player's photo
    var stats: PlayerStats // Player's statistics
}

// MARK: - PlayerStats Structure
// Represents the statistics of a rugby player.
struct PlayerStats: Codable {
    var kickFromHand: Int // Number of kicks from hand
    var runs: Int // Number of runs
    var passes: Int // Number of passes
    var offload: Int // Number of offloads
    var tackles: String // Number of tackles (stored as a string)
    var carries: Int // Number of carries
    var metresMade: Int // Metres made by the player
    var defendersBeaten: Int // Number of defenders beaten
    var cleanBreaks: Int // Number of clean breaks
    var handlingError: Int // Number of handling errors
    var redCards: Int // Number of red cards received
    var yellowCards: Int // Number of yellow cards received

    // Custom coding keys to map JSON keys to Swift properties
    enum CodingKeys: String, CodingKey {
        case kickFromHand = "Kick from hand"
        case runs = "Runs"
        case passes = "Passes"
        case offload = "Offload"
        case tackles = "Tackles"
        case carries = "Carries"
        case metresMade = "Metres made"
        case defendersBeaten = "Defenders beaten"
        case cleanBreaks = "Clean breaks"
        case handlingError = "Handling error"
        case redCards = "Red cards"
        case yellowCards = "Yellow cards"
    }
}

// MARK: - Match Structure
// Represents a rugby match with identifiable and codable properties.
struct Match: Identifiable, Codable {
    var id: String // Unique identifier for the match
    var stage: String // Stage of the match (e.g., "Group Stage")
    var date: String // Date of the match
    var location: String // Location of the match
    var home: TeamScore // Home team's score
    var away: TeamScore // Away team's score
}

// MARK: - TeamScore Structure
// Represents the score of a team in a match.
struct TeamScore: Codable {
    var team: String // Team name or code
    var score: Int // Team's score in the match
}

// MARK: - Team Extension
// Extension to provide methods for loading team data from JSON.
extension Team {
    // Loads team data from a JSON file in the app bundle.
    static func loadJSON(from jsonName: String) -> [String: Team] {
        // 1. Locate the JSON file in the bundle
        guard let url = Bundle.main.url(forResource: jsonName, withExtension: "json") else {
            print("JSON file not found: \(jsonName)")
            return [:]
        }
        
        do {
            // 2. Load the data from the JSON file
            let data = try Data(contentsOf: url)
            
            // 3. Decode the JSON data using JSONDecoder
            let decoder = JSONDecoder()
            let teams = try decoder.decode([String: Team].self, from: data)
            
            return teams
        } catch {
            print("Error decoding JSON: \(error)")
            return [:]
        }
    }
    
    // Loads team data from a remote URL.
    static func loadJSONURL(from url: URL, completionHandler: @escaping ([Team]?, Error?) -> Void) {
        URLSession.shared.dataTask(with: url) { data, response, error in
            if let error = error {
                completionHandler(nil, error)
                return
            }
            
            guard let data = data else {
                completionHandler(nil, NSError(domain: "NoData", code: 400, userInfo: nil))
                return
            }
            
            do {
                let decoder = JSONDecoder()
                let teams = try decoder.decode([Team].self, from: data)
                completionHandler(teams, nil)
            } catch {
                completionHandler(nil, error)
            }
        }.resume()
    }
}

// MARK: - Match Extension
// Extension to provide methods for loading match data from JSON.
extension Match {
    // Loads match data from a JSON file in the app bundle.
    static func loadJSON(from jsonName: String) -> [String: [Match]] {
        // 1. Locate the JSON file in the bundle
        guard let url = Bundle.main.url(forResource: jsonName, withExtension: "json") else {
            print("JSON file not found: \(jsonName)")
            return [:]
        }
        
        do {
            // 2. Load the data from the JSON file
            let data = try Data(contentsOf: url)
            
            // 3. Decode the JSON data using JSONDecoder
            let decoder = JSONDecoder()
            let matchesByStage = try decoder.decode([String: [Match]].self, from: data)
            
            return matchesByStage
        } catch {
            print("Error decoding JSON: \(error)")
            return [:]
        }
    }
}

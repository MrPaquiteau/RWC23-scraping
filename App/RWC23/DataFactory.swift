//
//  DataFactory.swift
//  RWC23
//
//  Created by Romain TROILLARD on 1/4/25.
//

import Foundation
import UIKit

struct Team: Identifiable, Codable {
    var id: String?
    var code: String
    var country: String
    var images: TeamImages
    var players: [Player]
}

struct TeamImages: Codable {
    var flag: String
    var shape: String
    var logo: TeamLogo
}

struct TeamLogo: Codable {
    var light: String
    var dark: String
}

struct Player: Identifiable, Codable {
    var id: String
    var name: String
    var age: Int?
    var position: String?
    var height: Int?
    var weight: Int?
    var hometown: String?
    var photo: String?
    var stats: PlayerStats
}

struct PlayerStats: Codable {
    var kickFromHand: Int
    var runs: Int
    var passes: Int
    var offload: Int
    var tackles: String
    var carries: Int
    var metresMade: Int
    var defendersBeaten: Int
    var cleanBreaks: Int
    var handlingError: Int
    var redCards: Int
    var yellowCards: Int

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

// Structure pour représenter un match
struct Match: Identifiable, Codable {
    var id: String
    var stage: String
    var date: String
    var location: String
    var home: TeamScore
    var away: TeamScore
}

// Structure pour représenter le score d'une équipe dans un match
struct TeamScore: Codable {
    var team: String
    var score: Int
}

extension Team {
    static func loadJSON(from jsonName: String) -> [String: Team] {
        // 1. Localiser le fichier JSON dans le bundle
        guard let url = Bundle.main.url(forResource: jsonName, withExtension: "json") else {
            print("Fichier JSON introuvable : \(jsonName)")
            return [:]
        }
        
        do {
            // 2. Charger les données du fichier JSON
            let data = try Data(contentsOf: url)
            
            // 3. Décoder les données JSON en utilisant JSONDecoder
            let decoder = JSONDecoder()
            let teams = try decoder.decode([String: Team].self, from: data)
            
            return teams
        } catch {
            print("Erreur lors du décodage JSON : \(error)")
            return [:]
        }
    }
    
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


extension Match {
    static func loadJSON(from jsonName: String) -> [String: [Match]] {
        // 1. Localiser le fichier JSON dans le bundle
        guard let url = Bundle.main.url(forResource: jsonName, withExtension: "json") else {
            print("Fichier JSON introuvable : \(jsonName)")
            return [:]
        }
        
        do {
            // 2. Charger les données du fichier JSON
            let data = try Data(contentsOf: url)
            
            // 3. Décoder les données JSON en utilisant JSONDecoder
            let decoder = JSONDecoder()
            let matchesByStage = try decoder.decode([String: [Match]].self, from: data)
            
            return matchesByStage
        } catch {
            print("Erreur lors du décodage JSON : \(error)")
            return [:]
        }
    }
}

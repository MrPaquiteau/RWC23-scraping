//
//  DataFactory.swift
//  TestDataframe
//
//  Created by Romain TROILLARD on 30/11/2023.
//

import Foundation

protocol CSVLoadable {
    init?(raw: [String])
}

struct Team: Identifiable, CSVLoadable {
    var Id: String = ""
    var Country: String = ""
    var id = UUID()

    init?(raw: [String]) {
        Id = raw[0]
        Country = raw[1].trimmingCharacters(in: .whitespacesAndNewlines)
    }
}

struct Player: Identifiable, CSVLoadable {
    var Id: String = ""
    var Country: String = ""
    var Name: String = ""
    var Hometown: String = ""
    var Position: String = ""
    var Age: String = ""
    var Height: String = ""
    var Weight: String = ""
    var Photo: String = ""
    var id = UUID()

    init?(raw: [String]) {
        Id = raw[0]
        Country = raw[1].capitalized
        Name = raw[2]
        Hometown = raw[3]
        Position = raw[4]
        Age = raw[5]
        Height = raw[6]
        Weight = raw[7]
        Photo = raw[8]
    }
}

struct Stats: Identifiable, CSVLoadable {
    var Id_Player: String = ""
    var Kicks_From_Hand: String = ""
    var Runs: String = ""
    var Passes: String = ""
    var Offloads: String = ""
    var Clean_Break: String = ""
    var Defenders_Beaten: String = ""
    var Yellow_Cards: String = ""
    var Red_Cards: String = ""
    var Carries: String = ""
    var Metres_Made: String = ""
    var Tackles: String = ""
    var Tackles_Success: String = ""
    var Handling_Errors: String = ""
    var Turnovers: String = ""
    var id = UUID()
    
    init?(raw: [String]){
        Id_Player = raw[0]
        Kicks_From_Hand = raw[1]
        Runs = raw[2]
        Passes = raw[3]
        Offloads = raw[4]
        Clean_Break = raw[5]
        Defenders_Beaten = raw[6]
        Yellow_Cards = raw[7]
        Red_Cards = raw[8]
        Carries = raw[9]
        Metres_Made = raw[10]
        Tackles = raw[11]
        Tackles_Success = raw[12]
        Handling_Errors = raw[13]
        Turnovers = raw[14].trimmingCharacters(in: .whitespacesAndNewlines)
    }
}

struct Matchs: Identifiable, CSVLoadable {
    var Date: String = ""
    var Stage: String = ""
    var Team_Home: String = ""
    var Score_Home: String = ""
    var Score_Away: String = ""
    var Team_Away: String = ""
    var Stadium: String = ""
    var id = UUID()
    
    init?(raw: [String]){
        Date = raw[0]
        Stage = raw[1]
        Team_Home = raw[2]
        Score_Home = raw[3]
        Score_Away = raw[4]
        Team_Away = raw[5]
        Stadium = raw[6].trimmingCharacters(in: .whitespacesAndNewlines)
    }
}


extension CSVLoadable {
    static func loadCSV(from csvName: String) -> [Self] {
        var csvToStruct = [Self]()
        
        //locate the csv file
        guard let filePath = Bundle.main.path(forResource: csvName, ofType: "csv") else {
            return []
        }
        // Convert the content of the csvfile into one very long string
        var data = ""
        do {
            data = try String(contentsOfFile: filePath)
        } catch {
            print(error)
            return []
        }
        
        //split the long string into an arraw of "rows" of data. Each row is a string
        //detect "/n" carriage return, then split
        var rows = data.components(separatedBy: "\n")
        
        //remove header rows
        rows.removeFirst()
        
        //now loop aroud each row and slit into columns
        for row in rows {
            let csvColumns = row.components(separatedBy: ",")
            if csvColumns.count > 1 {
                let genericStruct = Self.init(raw: csvColumns)
                csvToStruct.append(genericStruct!)
            }
        }
        return csvToStruct
    }
}

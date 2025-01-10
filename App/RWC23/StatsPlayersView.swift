//
//  PlayerStatsView.swift
//  RWC23
//
//  Created by Romain TROILLARD on 1/4/25.
//

import SwiftUI

// MARK: - PlayerStatsView
// View to display detailed statistics for a selected player.
struct PlayerStatsView: View {
    var player: Player // The selected player

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // Section 1: Player photo and general information
                HStack(alignment: .top, spacing: 20) {
                    // Player photo (top left)
                    if let photoURL = URL(string: player.photo ?? "") {
                        AsyncImage(url: photoURL) { phase in
                            switch phase {
                            case .empty:
                                ProgressView()
                                    .frame(width: 100) // Show a loading indicator
                            case .success(let image):
                                image
                                    .resizable()
                                    .scaledToFill()
                                    .clipped()
                                    .frame(width: 100)
                                    .cornerRadius(10) // Display the player's photo
                            case .failure:
                                Image(systemName: "person.crop.circle.fill")
                                    .resizable()
                                    .scaledToFill()
                                    .frame(width: 100)
                                    .clipped()
                                    .cornerRadius(10) // Fallback image if photo fails to load
                            @unknown default:
                                EmptyView()
                            }
                        }
                    } else {
                        // Fallback image if no photo URL is provided
                        Image(systemName: "person.crop.circle.fill")
                            .resizable()
                            .scaledToFill()
                            .frame(width: 100, height: 100)
                            .clipped()
                            .cornerRadius(10)
                            .overlay(
                                RoundedRectangle(cornerRadius: 10)
                                    .stroke(Color.primary, lineWidth: 1)
                            )
                    }

                    // General information (right of the photo)
                    VStack(alignment: .leading, spacing: 8) {
                        Text(player.name)
                            .font(.title)
                            .fontWeight(.bold) // Display the player's name

                        if let age = player.age {
                            InfoRow(label: "Age", value: "\(age)") // Display age if available
                        }
                        if let position = player.position {
                            InfoRow(label: "Position", value: position) // Display position if available
                        }
                        if let height = player.height {
                            InfoRow(label: "Height", value: "\(height) cm") // Display height if available
                        }
                        if let weight = player.weight {
                            InfoRow(label: "Weight", value: "\(weight) kg") // Display weight if available
                        }
                    }
                }

                // Section 2: Player statistics (bottom section)
                VStack(alignment: .leading, spacing: 10) {
                    Text("Statistics")
                        .font(.title2)
                        .fontWeight(.bold) // Section title

                    // List of statistics
                    VStack(alignment: .leading, spacing: 8) {
                        StatRow(label: "Kick from hand", value: "\(player.stats.kickFromHand)")
                        StatRow(label: "Runs", value: "\(player.stats.runs)")
                        StatRow(label: "Passes", value: "\(player.stats.passes)")
                        StatRow(label: "Offload", value: "\(player.stats.offload)")
                        StatRow(label: "Tackles", value: player.stats.tackles)
                        StatRow(label: "Carries", value: "\(player.stats.carries)")
                        StatRow(label: "Metres made", value: "\(player.stats.metresMade)")
                        StatRow(label: "Defenders beaten", value: "\(player.stats.defendersBeaten)")
                        StatRow(label: "Clean breaks", value: "\(player.stats.cleanBreaks)")
                        StatRow(label: "Handling error", value: "\(player.stats.handlingError)")
                        StatRow(label: "Red cards", value: "\(player.stats.redCards)")
                        StatRow(label: "Yellow cards", value: "\(player.stats.yellowCards)")
                    }
                    .padding()
                    .background(Color(.systemBackground))
                    .cornerRadius(10)
                    .overlay(
                        RoundedRectangle(cornerRadius: 10)
                            .stroke(Color.primary, lineWidth: 0.5)
                    )
                    .shadow(radius: 5)
                }
            }
            .padding()
        }
    }
}

// MARK: - InfoRow
// View to display a row of general information (e.g., age, position).
struct InfoRow: View {
    var label: String
    var value: String

    var body: some View {
        HStack {
            Text(label)
                .font(.headline)
                .foregroundColor(.secondary) // Label text
            Spacer()
            Text(value)
                .font(.body)
                .fontWeight(.medium) // Value text
        }
        .padding(.vertical, 4)
        .overlay(
            Rectangle()
                .frame(height: 1)
                .foregroundColor(Color.primary.opacity(0.1)),
            alignment: .bottom
        )
    }
}

// MARK: - StatRow
// View to display a row of statistics (e.g., runs, tackles).
struct StatRow: View {
    var label: String
    var value: String

    var body: some View {
        HStack {
            Text(label)
                .font(.body)
                .foregroundColor(.primary) // Label text
            Spacer()
            Text(value)
                .font(.body)
                .fontWeight(.medium) // Value text
        }
        .padding(.vertical, 4)
        .overlay(
            Rectangle()
                .frame(height: 1)
                .foregroundColor(Color.primary.opacity(0.1)),
            alignment: .bottom
        )
    }
}

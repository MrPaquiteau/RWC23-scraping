//
//  PlayerStatsView.swift
//  RWC23
//
//  Created by Romain TROILLARD on 1/4/25.
//

import SwiftUI

struct PlayerStatsView: View {
    var player: Player // Le joueur sélectionné

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 20) {
                // Section 1 : Photo et informations générales
                HStack(alignment: .top, spacing: 20) {
                    // Photo du joueur (en haut à gauche)
                    if let photoURL = URL(string: player.photo ?? "") {
                        AsyncImage(url: photoURL) { phase in
                            switch phase {
                            case .empty:
                                ProgressView()
                                    .frame(width: 100)
                            case .success(let image):
                                image
                                    .resizable()
                                    .scaledToFill()
                                    .clipped()
                                    .frame(width: 100)
                                    .cornerRadius(10)
                            case .failure:
                                Image(systemName: "person.crop.circle.fill")
                                    .resizable()
                                    .scaledToFill()
                                    .frame(width: 100)
                                    .clipped()
                                    .cornerRadius(10)
                            @unknown default:
                                EmptyView()
                            }
                        }
                    } else {
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

                    // Informations générales (à droite de la photo)
                    VStack(alignment: .leading, spacing: 8) {
                        Text(player.name)
                            .font(.title)
                            .fontWeight(.bold)

                        if let age = player.age {
                            InfoRow(label: "Age", value: "\(age)")
                        }
                        if let position = player.position {
                            InfoRow(label: "Position", value: position)
                        }
                        if let height = player.height {
                            InfoRow(label: "Height", value: "\(height) cm")
                        }
                        if let weight = player.weight {
                            InfoRow(label: "Weight", value: "\(weight) kg")
                        }
                    }
                }

                // Section 2 : Statistiques (en bas)
                VStack(alignment: .leading, spacing: 10) {
                    Text("Statistiques")
                        .font(.title2)
                        .fontWeight(.bold)

                    // Liste des statistiques
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
//        .navigationTitle(player.name)
//        .navigationBarTitleDisplayMode(.inline)
    }
}

// Vue pour afficher une ligne d'information
struct InfoRow: View {
    var label: String
    var value: String

    var body: some View {
        HStack {
            Text(label)
                .font(.headline)
                .foregroundColor(.secondary)
            Spacer()
            Text(value)
                .font(.body)
                .fontWeight(.medium)
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

// Vue pour afficher une ligne de statistique
struct StatRow: View {
    var label: String
    var value: String

    var body: some View {
        HStack {
            Text(label)
                .font(.body)
                .foregroundColor(.primary)
            Spacer()
            Text(value)
                .font(.body)
                .fontWeight(.medium)
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

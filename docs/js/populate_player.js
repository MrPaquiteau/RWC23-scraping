// Charger les données du joueur
document.addEventListener("DOMContentLoaded", () => {
    const urlParams = new URLSearchParams(window.location.search);
    const teamName = urlParams.get('team'); // Récupérer le nom de l'équipe à partir de l'URL
    const playerId = urlParams.get('player'); // Récupérer le nom du joueur à partir de l'URL

    const playerPhoto = document.getElementById("player-photo");
    const playerNameElement = document.getElementById("player-name");
    const infoSection = document.getElementById("info-section");
    const statsSection = document.getElementById("stats-section");
    const teamNavList = document.getElementById('team-nav-list');


    fetch("data/teams_players_matches.json")
        .then(response => response.json())
        .then(data => {
            const teamData = data[teamName];
            const playerData = teamData.players.find(player => player.id === playerId);
            
            if (playerData) {
                // Photo et nom du joueur
                playerPhoto.src = playerData.photo;
                playerNameElement.textContent = playerData.name;
                const fallbackImage = "https://www.pngkit.com/png/full/349-3499519_person1-placeholder-imagem-de-perfil-anonimo.png";
                playerPhoto.onerror = () => {
                    playerPhoto.src = fallbackImage;
                };
                
                // Informations générales
                const infoKeys = {
                    age: "Age",
                    height: "Height (cm)",
                    weight: "Weight (kg)",
                    hometown: "Hometown"
                };
                Object.entries(infoKeys).forEach(([key, label]) => {
                    if (playerData[key]) {
                        const infoItem = document.createElement("div");
                        infoItem.classList.add("info-item");
                        infoItem.innerHTML = `
                            <span class="label">${label}:</span>
                            <span>${playerData[key]}</span>
                        `;
                        infoSection.appendChild(infoItem);
                    }
                });

                // Statistiques
                Object.entries(playerData.stats).forEach(([label, value]) => {
                    const statCard = document.createElement("div");
                    statCard.classList.add("stat-card");
                    statCard.innerHTML = `
                        <div class="value">${value}</div>
                        <div class="label">${label}</div>
                    `;
                    statsSection.appendChild(statCard);
                });
            } else {
                console.error("Joueur non trouvé dans les données de l'équipe.");
            }
        })
        .catch(error => {
            console.error("Erreur lors du chargement des données:", error);
        });
});
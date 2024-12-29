// Charger les données de l'équipe
document.addEventListener("DOMContentLoaded", () => {
    const urlParams = new URLSearchParams(window.location.search);
    const teamName = urlParams.get('team'); // Récupérer le nom de l'équipe à partir de l'URL
    const playerGrid = document.getElementById("player-grid");
    const teamTitle = document.getElementById('teamTitle');
    const favicon = document.getElementById('favicon');
    document.title = `Team ${teamName}`;

    fetch("../../data/teams_players_api.json")
        .then(response => response.json())
        .then(data => {
            const teamData = data[teamName];

            // Ajouter les informations de l'équipe
            teamTitle.innerHTML = `<img class="title-icon" src="${teamData.flag}" alt="Drapeau National"> ${teamName}'s players`;
            favicon.href = teamData.flag;
            console.log("Image path:", teamData.flag); // Debugging line to check the image path

            // Ajouter les joueurs
            teamData.players.forEach(player => {
                const playerCard = document.createElement("div");
                playerCard.className = "grid-item";
                playerCard.dataset.name = player.name;
                
                playerCard.innerHTML = `
                    <img src="${player.photo}" alt="${player.name}">
                    <p>${player.name}</p>
                `;

                playerGrid.appendChild(playerCard);
            });
        })
        .catch(error => {
            console.error("Erreur lors du chargement des données:", error);
        });
});

// Fonction pour rechercher les joueurs
function searchPlayers() {
    const input = document.getElementById("searchInput");
    const filter = input.value.toUpperCase();
    const gridItems = document.querySelectorAll(".grid-item");

    gridItems.forEach(item => {
        const playerName = item.dataset.name.toUpperCase();
        item.style.display = playerName.includes(filter) ? "" : "none";
    });
}
// Charger les données de l'équipe
document.addEventListener("DOMContentLoaded", () => {
    const urlParams = new URLSearchParams(window.location.search);
    const teamName = urlParams.get('team'); // Récupérer le nom de l'équipe à partir de l'URL
    const playerGrid = document.getElementById("player-grid");
    const teamTitle = document.getElementById('teamTitle');
    const favicon = document.getElementById('favicon');
    const teamNavList = document.getElementById('team-nav-list');
    document.title = `Team ${teamName}`;

    fetch("../../data/teams_players_api.json")
        .then(response => response.json())
        .then(data => {
            const teamData = data[teamName];

            // Ajouter les informations de l'équipe
            teamTitle.innerHTML = `<img class="title-icon" src="${teamData['images']['flag']}" alt="Drapeau National"> ${teamName}'s players`;
            favicon.href = teamData['images']['flag'];

            // Ajouter les liens de navigation pour chaque équipe
            Object.keys(data).forEach(team => {
                const navItem = document.createElement("li");
                navItem.innerHTML = `<a href="team.html?team=${team}">${team}</a>`;
                teamNavList.appendChild(navItem);
            });

            // Ajouter les joueurs
            teamData.players.forEach(player => {
                const playerCard = document.createElement("div");
                playerCard.className = "grid-item";
                playerCard.dataset.name = player.name;
            
                // Chemin de l'image de substitution
                const fallbackImage = "https://www.pngkit.com/png/full/349-3499519_person1-placeholder-imagem-de-perfil-anonimo.png";
            
                playerCard.innerHTML = `
                    <div>
                        <a href="player.html?team=${teamName}&player=${player.id}">
                            <img src="${player.photo}" alt="${player.name}" onerror="this.src='${fallbackImage}'">
                        </a>
                        <p>${player.name}</p>
                    </div>
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
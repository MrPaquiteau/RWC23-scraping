document.addEventListener("DOMContentLoaded", () => {
    const gridContainer = document.querySelector(".grid-container");

    // Charger le fichier JSON
    fetch("./data.json")
        .then(response => {
            if (!response.ok) {
                throw new Error("Erreur lors du chargement du fichier JSON");
            }
            return response.json();
        })
        .then(data => {
            // Parcourir les équipes du JSON
            Object.entries(data).forEach(([teamName, teamData]) => {
                // Créer un élément pour chaque équipe
                const teamCard = document.createElement("div");
                teamCard.className = "grid-item";
                teamCard.dataset.name = teamName;

                // Ajouter le contenu HTML
                teamCard.innerHTML = `
                    <a href="${teamName}/${teamName}_data.html">
                        <img src="${teamData.image}" alt="${teamName}" loading="lazy">
                    </a>
                    <p>${teamName}</p>
                `;

                // Ajouter l'élément à la grille
                gridContainer.appendChild(teamCard);
            });
        })
        .catch(error => {
            console.error("Erreur :", error);
        });
});

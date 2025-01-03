function search() {{
var input, filter, grid, items, player, txtValue;
input = document.getElementById("searchInput");
filter = input.value.toUpperCase();
grid = document.querySelector(".grid-container");
items = grid.getElementsByClassName("grid-item");

for (var i = 0; i < items.length; i++) {{
    player = items[i];
    txtValue = player.textContent || player.innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {{
        player.style.display = "";
    }} else {{
        player.style.display = "none";
    }}
}}
}}

function goBack() {
    window.history.back();
}

function toggleDarkMode() {
    var element = document.body;
    var isDarkMode = !element.classList.contains('dark-mode');
    var darkButton = document.getElementById('dark-button');

    if (isDarkMode) {
        element.classList.add('dark-mode');
        darkButton.checked = true; // Cocher la case
        localStorage.setItem('darkMode', 'enabled');
    } else {
        element.classList.remove('dark-mode');
        darkButton.checked = false; // Décocher la case
        localStorage.setItem('darkMode', 'disabled');
    }

    // Mettre à jour les images dynamiquement
    updateLogos();
}

function updateLogos() {
    const isDarkMode = document.body.classList.contains('dark-mode');
    const darkLogos = document.querySelectorAll(".darkLogo");
    const lightLogos = document.querySelectorAll(".lightLogo");

    if (isDarkMode) {
        darkLogos.forEach(img => {
            img.style.display = "block";
        });
        lightLogos.forEach(img => {
            img.style.display = "none";
        });
    } else {
        darkLogos.forEach(img => {
            img.style.display = "none";
        });
        lightLogos.forEach(img => {
            img.style.display = "block";
        });
    }
}

document.addEventListener('DOMContentLoaded', function () {
    var darkModeState = localStorage.getItem('darkMode');

    // Vérifiez s'il y a un paramètre de requête pour l'état du mode sombre
    var urlParams = new URLSearchParams(window.location.search);
    var darkModeQueryParam = urlParams.get('darkModeState');

    if (darkModeQueryParam === 'enabled') {
        // Appliquez le mode sombre si le paramètre de requête est défini sur "enabled"
        document.body.classList.add('dark-mode');
        document.getElementById('dark-button').checked = true; // Check the checkbox
        localStorage.setItem('darkMode', 'enabled');
    } else if (darkModeQueryParam === 'disabled') {
        // Appliquez le mode clair si le paramètre de requête est défini sur "disabled"
        document.body.classList.remove('dark-mode');
        document.getElementById('dark-button').checked = false; // Décocher la case
        localStorage.setItem('darkMode', 'disabled');
    } else if (darkModeState === 'enabled') {
        // Appliquez le mode sombre si localStorage est défini sur "enabled" et aucun paramètre de requête
        document.body.classList.add('dark-mode');
        document.getElementById('dark-button').checked = true; // Cocher la case
    }

    // Mettre à jour les logos après le chargement de la page
    updateLogos();
});
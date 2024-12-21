/* Script pour passer en mode sombre */
document.addEventListener('DOMContentLoaded', function () {
var darkModeState = localStorage.getItem('darkMode');

// Appliquez le mode sombre si localStorage est défini sur "enabled"
if (darkModeState === 'enabled') {
    document.body.classList.add('dark-mode');
        // Coche le bouton (passe le bouton sur la position dark)
    document.getElementById('dark-button').checked = true;
}
});

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
});

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
}

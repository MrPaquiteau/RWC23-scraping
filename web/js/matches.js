/* Script Pour le retour en haut de page */
function scrollToTop() {
    document.body.scrollTop = 0; // Pour les navigateurs pris en charge
    document.documentElement.scrollTop = 0; // Pour les navigateurs modernes
}

window.onscroll = function () {
    scrollFunction();
};

function scrollFunction() {
    var btn = document.getElementById("scrollToTopBtn");

    if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
        btn.style.opacity = "1";
    } else {
        btn.style.opacity = "0";
    }
}

/* Script permettant d'afficher en pop-up les matchs d'une phase */
document.addEventListener('DOMContentLoaded', function () {
    const menuItems = document.querySelectorAll('.menu-item');
    const modal = document.getElementById('matchesModal');

    menuItems.forEach(function (item) {
        item.addEventListener('click', function () {
            const phase = item.getAttribute('data-phase');
            showMatches(phase);
        });
    });

    function showMatches(phase) {
        const modalContent = modal.querySelector('.modal-content');
        const stageContainer = document.querySelector(`.stage-container.${phase}`);

        if (stageContainer) {
            const stageContent = stageContainer.innerHTML;
            modalContent.innerHTML = stageContent;

            // Affichage de la pop-up
            modal.style.display = 'block';
        }
    }

    function closeModal() {
        modal.style.display = 'none';
    }

    modal.addEventListener('click', function (event) {
        if (event.target === modal) {
            closeModal();
        }
    });

    const closeBtn = modal.querySelector('.close');
    closeBtn.addEventListener('click', closeModal);
});

/* Script pour passer en mode sombre */
function darkmode() {
    var element = document.body;
    element.classList.toggle("dark-mode");
}

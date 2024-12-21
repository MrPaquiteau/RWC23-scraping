"""
Créer les fichiers CSS nécessaires aux différentes pages
"""


def creation_CSS_acceuil(path):
    """
    Crée un fichier CSS pour la page d'accueil du site avec des
    styles prédéfinis.

    Parameters
    ----------
    path : String
        Chemin du répertoire où le fichier CSS sera enregistré.

    Returns
    -------
    None.

    """
    style_css_acceuil = """


body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    background-color: #f4f4f4;
}

.page-title {
    text-align: center;
    padding: 20px;
    font-size: 4vw;
    color: #333;
    grid-column: 1 / -1;
    display: flex;
    align-items: center;
    justify-content: center;
}

.title-icon {
    height: 4vw;
    margin-right: 10px;
}

.grid-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    padding: 20px;
    justify-content: center;
}

.grid-item {
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
    transition: transform 0.3s, box-shadow 0.3s;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.grid-item:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.grid-item p {
    text-align: center;
    font-size: 18px;
    font-weight: bold;
    margin: 15px 0;
    color: #333;
}

.grid-item a {
    display: block;
    overflow: hidden;
    border-bottom: 1px solid #ddd;
}

.grid-item img {
    width: 100%;
    height: auto;
    transition: transform 0.3s;
}

.grid-item:hover img {
    transform: scale(1.1);
}

.container-infos {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
}

.form-control {
    grid-column: 1 / -1;
    position: relative;
    margin: 0px auto 40px;
    width: 250px;
}

.form-control input {
  background-color: transparent;
  border: 0;
  border-bottom: 2px #525252 solid;
  display: block;
  width: 100%;
  padding: 15px 0;
  font-size: 28px;
  color: #363636;
}

.form-control input:focus,
.form-control input:valid {
  outline: 0;
}

.form-control label {
  position: absolute;
  top: 15px;
  left: 0;
  pointer-events: none;
}

.form-control label span {
  display: inline-block;
  font-size: 28px;
  min-width: 5px;
  color: #000000;
  transition: 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

.form-control input:focus+label span,
.form-control input:valid+label span {
  transform: translateY(-45px);
}
/* ------------------------------------ */
.home-button:hover, .navigation-button-previous:hover, .navigation-button-next:hover {
    box-shadow: none;
    color: #292929;
}

.home-button:active, .navigation-button-previous:active, .navigation-button-next:active {
    color: #666;
    box-shadow: inset 4px 4px 12px #c5c5c5, inset -4px -4px 12px #ffffff;
}

.home-button {
    color: #111;
    padding: 0.7em 1.7em;
    font-size: 18px;
    border-radius: 0.5em;
    background: #fff;
    border: 1px solid #e8e8e8;
    box-shadow: 6px 6px 12px #c5c5c5, -6px -6px 12px #ffffff;
    position: absolute;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
    text-decoration: none;
    transition: all 0.3s;
    z-index: 2;
}

.dark-mode .home-button {
    color: #fff;
    background: #1a1a1a;
    border: 1px solid #292929;
    box-shadow: 10px 10px 20px #0d0d0d, -10px -10px 20px #272727;
}

.dark-mode .home-button:hover {
    color: #fff;
    box-shadow: none;
}

.dark-mode .home-button:active {
    color: #aaa;
    box-shadow: inset 6px 6px 12px #0d0d0d, inset -6px -6px 12px #272727;
}
/* ---------- Style DARKMODE ---------- */
.dark-mode  {
    background-color: rgb(16, 16, 16);
}


.dark-mode, .dark-mode .modal-content {
    background-color: rgb(16, 16, 16);
}

.dark-mode h2, .dark-mode .page-title,
.dark-mode .form-control span, .dark-mode .form-control input,
.dark-mode .grid-item p {
    color: #f4f4f4;
}

.dark-mode .grid-item {
    border: none;
    background-color: #001225;
}
/* ------------------------------------ */

/* --------- BOUTONS DARKMODE --------- */
.switch {
    position: fixed;
    top: 30px;
    right: 40px;
    z-index: 6;
    font-size: 17px;
    display: inline-block;
    width: 64px;
    height: 34px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #73C0FC;
  transition: .4s;
  border-radius: 30px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 30px;
  width: 30px;
  border-radius: 20px;
  left: 2px;
  bottom: 2px;
  z-index: 2;
  background-color: #e8e8e8;
  transition: .4s;
}

.sun svg {
  position: absolute;
  top: 6px;
  left: 36px;
  z-index: 1;
  width: 24px;
  height: 24px;
}

.moon svg {
  fill: #73C0FC;
  position: absolute;
  top: 5px;
  left: 5px;
  z-index: 1;
  width: 24px;
  height: 24px;
}

/* .switch:hover */.sun svg {
  animation: rotate 15s linear infinite;
}

@keyframes rotate {

  0% {
    transform: rotate(0);
  }

  100% {
    transform: rotate(360deg);
  }
}

/* .switch:hover */.moon svg {
  animation: tilt 5s linear infinite;
}

@keyframes tilt {

  0% {
    transform: rotate(0deg);
  }

  25% {
    transform: rotate(-10deg);
  }

  75% {
    transform: rotate(10deg);
  }

  100% {
    transform: rotate(0deg);
  }
}

.input:checked + .slider {
  background-color: #183153;
}

.input:focus + .slider {
  box-shadow: 0 0 1px #183153;
}

.input:checked + .slider:before {
  transform: translateX(30px);
}
/* ------------------------------------ */

/* ----------- STYLE FOOTER ----------- */
footer {
  background-color: #0d1b2a;
  color: white;
  padding: 20px;
  text-align: center;
  box-shadow: 0px -5px 15px rgba(0, 0, 0, 0.2);
}

.footer-info {
  max-width: 800px;
  margin: 0 auto;
  font-size: 0.8em;
  line-height: 1.2;
}

.footer-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.ui-btn {
  --btn-default-bg: rgb(41, 41, 41);
  --btn-padding: 15px 20px;
  --btn-hover-bg: rgb(51, 51, 51);
  --btn-transition: .3s;
  --btn-letter-spacing: .1rem;
  --btn-animation-duration: 1.2s;
  --btn-shadow-color: rgba(0, 0, 0, 0.137);
  --btn-shadow: 0 2px 10px 0 var(--btn-shadow-color);
  --hover-btn-color: #FAC921;
  --default-btn-color: #fff;
  --font-size: 16px;
  --font-weight: 600;
  --font-family: Menlo, Roboto Mono, monospace;
}

.ui-btn {
  box-sizing: border-box;
  padding: var(--btn-padding);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--default-btn-color);
  font: var(--font-weight) var(--font-size) var(--font-family);
  background: var(--btn-default-bg);
  border: none;
  cursor: pointer;
  transition: var(--btn-transition);
  overflow: hidden;
  box-shadow: var(--btn-shadow);
}

.ui-btn span {
  letter-spacing: var(--btn-letter-spacing);
  transition: var(--btn-transition);
  box-sizing: border-box;
  position: relative;
  background: inherit;
}

.ui-btn span::before {
  box-sizing: border-box;
  position: absolute;
  content: "";
  background: inherit;
}

.ui-btn:hover, .ui-btn:focus {
  background: var(--btn-hover-bg);
}

.ui-btn:hover span, .ui-btn:focus span {
  color: var(--hover-btn-color);
}

.ui-btn.legal:hover span::before, .ui-btn.legal:focus span::before {
  animation: legalAnimation linear both var(--btn-animation-duration);
}

@keyframes legalAnimation {
  0% {
    content: "#";
  }

  5% {
    content: "-.";
  }

  10% {
    content: "^{";
  }

  15% {
    content: "-!6";
  }

  20% {
    content: "#$_è";
  }

  25% {
    content: "№*:$x";
  }

  30% {
    content: "r#{*";
  }

  35% {
    content: "@}0-?z";
  }

  40% {
    content: "?{4@%";
  }

  45% {
    content: "=.,^!6";
  }

  50% {
    content: "?ù2_@%";
  }

  55% {
    content: ")^;1}]";
  }

  60% {
    content: "?{-%:%";
    right: 0;
  }

  65% {
    content: "|{f[4";
    right: 0;
  }

  70% {
    content: "{4%0%";
    right: 0;
  }

  75% {
    content: "'1_0<";
    right: 0;
  }

  80% {
    content: "{0%";
    right: 0;
  }

  85% {
    content: "]>'";
    right: 0;
  }

  90% {
    content: "4/";
    right: 0;
  }

  95% {
    content: "2";
    right: 0;
  }

  100% {
    content: "";
    right: 0;
  }
}"""
    with open(fr"{path}//style_acceuil.css", "w", encoding="utf-8", newline="\r\n") as f:
        # Écrire le code HTML dans le fichier
        f.write(style_css_acceuil)


def creation_CSS_joueurs(path):
    """
    Crée un fichier CSS pour les pages de chaque joueurs du site avec des
    styles prédéfinis.

    Parameters
    ----------
    path : String
        Chemin du répertoire où le fichier CSS sera enregistré.

    Returns
    -------
    None.

    """
    style_css_joueurs = """

.body-container {
    font-family: 'Arial', sans-serif;
    background-color: #f4f4f4;
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.card-container {
    display: flex;
    padding: 20px;
    border-radius: 2%;
    width: 90%;
    max-width: 800px;
    transition: transform 0.3s, box-shadow 0.3s;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background: linear-gradient(120deg, #fff 30%, #e5e5e5 38%,
                                #e5e5e5 40%, #fff 48%);
    background-size: 200% 100%;
    animation: reflect 2s infinite;
    align-items: center;
}

@keyframes reflect {
    0% {
        background-position: 100% 0;
    }
    100% {
        background-position: -100% 0;
    }
}

.card-header {
    flex: 1;
}

.card-header img {
    width: 100%;
    max-width: 100%;
    border-radius: 8px;
    margin-bottom: 15px;
    transition: transform 0.3s, box-shadow 0.3s;
}

.card-header img:hover {
    transform: scale(1.15);
}

.card-header h1 {
    color: #333;
    text-align: center;
}

.card-infos {
    flex: 1;
    padding: 20px;
}

.infos-title {
    text-align: center;
}

.grid-container-stats, .grid-container-personal {
    display: grid;
    gap: 20px;
    grid-template-columns: repeat(7, 2fr);
}

.grid-item {
    margin-bottom: 1em;
    align-items: center;
    justify-content: center;
}

.grid-item strong {
    display: block;
    font-weight: bold;
}

/* ------------- BUTTTON ------------- */

.home-button:hover, .navigation-button-previous:hover,
.navigation-button-next:hover {
    box-shadow: none;
    color: #292929;
}

.home-button:active, .navigation-button-previous:active,
.navigation-button-next:active {
    color: #666;
    box-shadow: inset 4px 4px 12px #c5c5c5, inset -4px -4px 12px #ffffff;
}

.home-button {
    color: #111;
    padding: 0.7em 1.7em;
    font-size: 18px;
    border-radius: 0.5em;
    background: #fff;
    border: 1px solid #e8e8e8;
    box-shadow: 6px 6px 12px #c5c5c5, -6px -6px 12px #ffffff;
    position: absolute;
    top: 10px;
    left: 50%;
    transform: translateX(-50%);
    text-decoration: none;
    transition: all 0.3s;
    z-index: 2;
}

.navigation-button-previous {
    color: #111;
    padding: 0.7em 1.7em;
    font-size: 18px;
    border-radius: 0.5em;
    background: #fff;
    border: 1px solid #e8e8e8;
    box-shadow: 6px 6px 12px #c5c5c5, -6px -6px 12px #ffffff;
    position: absolute;
    top: 10px;
    left: 30%;
    transform: translateX(-50%);
    text-decoration: none;
    transition: all 0.3s;
    z-index: 2;
}

.navigation-button-next {
    color: #111;
    padding: 0.7em 1.7em;
    font-size: 18px;
    border-radius: 0.5em;
    background: #fff;
    border: 1px solid #e8e8e8;
    box-shadow: 6px 6px 12px #c5c5c5, -6px -6px 12px #ffffff;
    position: absolute;
    top: 10px;
    left: 70%;
    transform: translateX(-50%);
    text-decoration: none;
    transition: all 0.3s;
    z-index: 2;
}

/* Media query pour les écrans plus petits */
@media only screen and (max-width: 1000px) {

    .body-container {
        font-family: 'Arial', sans-serif;
        background-color: #f4f4f4;
        margin-top: 200px;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .card-container {
        margin: auto;
        text-align: left;
        padding: 20px;
        border-radius: 8px;
        width: 90%;
        max-width: 400px;
        transition: transform 0.3s, box-shadow 0.3s;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    @keyframes reflect {
        0% {
            background-position: 0 0;
        }
    }

    .card-header img {
        width: 100%;
        max-width: 200px;
        height: auto;
        border-radius: 8px;
        margin-bottom: 15px;
        transition: transform 0.3s, box-shadow 0.3s;
    }

    .card-header img:hover {
        transform: scale(1.15);
    }

    .infos-title {
        text-align: center;
    }

    h1 {
        color: #333;
    }

    .grid-container-personal, .grid-container-stats {
        display: grid;
        gap: 15px;
    }

    .grid-container-personal {
        grid-template-columns: repeat(3, 1fr);
    }

    .grid-container-stats {
        grid-template-columns: repeat(3, 2fr);
    }

    .grid-item {
        margin-bottom: 1em;
    }

    .grid-item strong {
        display: block;
        font-weight: bold;
    }

    .card-container {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .home-button:hover, .navigation-button-previous:hover,
    .navigation-button-next:hover {
        box-shadow: none;
        color: #292929;
    }

    .home-button:active, .navigation-button-previous:active,
    .navigation-button-next:active {
        color: #666;
        box-shadow: inset 4px 4px 12px #c5c5c5, inset -4px -4px 12px #ffffff;
    }

    .home-button {
        color: #111;
        padding: 0.7em 1.7em;
        font-size: 18px;
        border-radius: 0.5em;
        background: #fff;
        border: 1px solid #e8e8e8;
        box-shadow: 6px 6px 12px #c5c5c5, -6px -6px 12px #ffffff;
        position: absolute;
        top: 80px;
        transform: translateX(-50%);
        text-decoration: none;
        transition: all 0.3s;
        z-index: 2;
    }

    .navigation-button-previous {
        color: #111;
        padding: 0.7em 1.7em;
        font-size: 18px;
        border-radius: 0.5em;
        background: #fff;
        border: 1px solid #e8e8e8;
        box-shadow: 6px 6px 12px #c5c5c5, -6px -6px 12px #ffffff;
        position: absolute;
        top: 10px;
        left: 50%;
        transform: translateX(-50%);
        text-decoration: none;
        transition: all 0.3s;
        z-index: 2;
    }

    .navigation-button-next {
        color: #111;
        padding: 0.7em 1.7em;
        font-size: 18px;
        border-radius: 0.5em;
        background: #fff;
        border: 1px solid #e8e8e8;
        box-shadow: 6px 6px 12px #c5c5c5, -6px -6px 12px #ffffff;
        position: absolute;
        top: 160px;
        left: 50%;
        transform: translateX(-50%);
        text-decoration: none;
        transition: all 0.3s;
        z-index: 2;
    }
}
/* ------------------------------------ */

/* ---------- Style DARKMODE ---------- */
.dark-mode {
    background-color: rgb(16, 16, 16);
}

.dark-mode .grid-item, .dark-mode .card-infos h2, .dark-mode .card-header h1 {
    color: #f4f4f4;
}

.dark-mode .card-container {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
    background: linear-gradient(120deg, rgb(29, 43, 58) 30%, #001225 40%, #001225 48%, rgb(29, 43, 58) 58%);
    transition: transform 0.3s, box-shadow 0.3s;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background-size: 200% 100%;
    animation: reflect 2s infinite;
}

/* Styles des boutons pour le mode sombre */
.dark-mode .home-button,
.dark-mode .navigation-button-previous,
.dark-mode .navigation-button-next {
    color: #fff;
    background: #1a1a1a;
    border: 1px solid #292929;
    box-shadow: 10px 10px 20px #0d0d0d, -10px -10px 20px #272727;
}

.dark-mode .home-button:hover,
.dark-mode .navigation-button-previous:hover,
.dark-mode .navigation-button-next:hover {
    color: #fff;
    box-shadow: none;
}

.dark-mode .home-button:active,
.dark-mode .navigation-button-previous:active,
.dark-mode .navigation-button-next:active {
    color: #aaa;
    box-shadow: inset 6px 6px 12px #0d0d0d, inset -6px -6px 12px #272727;
}
/* ------------------------------------ */

/* --------- BOUTONS DARKMODE --------- */
.switch {
    position: fixed;
    top: 30px;
    right: 40px;
    z-index: 6;
    font-size: 17px;
    display: inline-block;
    width: 64px;
    height: 34px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #73C0FC;
  transition: .4s;
  border-radius: 30px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 30px;
  width: 30px;
  border-radius: 20px;
  left: 2px;
  bottom: 2px;
  z-index: 2;
  background-color: #e8e8e8;
  transition: .4s;
}

.sun svg {
  position: absolute;
  top: 6px;
  left: 36px;
  z-index: 1;
  width: 24px;
  height: 24px;
}

.moon svg {
  fill: #73C0FC;
  position: absolute;
  top: 5px;
  left: 5px;
  z-index: 1;
  width: 24px;
  height: 24px;
}

.sun svg {
  animation: rotate 15s linear infinite;
}

@keyframes rotate {

  0% {
    transform: rotate(0);
  }

  100% {
    transform: rotate(360deg);
  }
}

.moon svg {
  animation: tilt 5s linear infinite;
}

@keyframes tilt {

  0% {
    transform: rotate(0deg);
  }

  25% {
    transform: rotate(-10deg);
  }

  75% {
    transform: rotate(10deg);
  }

  100% {
    transform: rotate(0deg);
  }
}

.input:checked + .slider {
  background-color: #183153;
}

.input:focus + .slider {
  box-shadow: 0 0 1px #183153;
}

.input:checked + .slider:before {
  transform: translateX(30px);
}
/* ------------------------------------ */

/* ----------- STYLE FOOTER ----------- */
footer {
  background-color: #0d1b2a;
  color: white;
  padding: 20px;
  text-align: center;
  box-shadow: 0px -5px 15px rgba(0, 0, 0, 0.2);
}

.footer-info {
  max-width: 800px;
  margin: 0 auto;
  font-size: 0.8em;
  line-height: 1.2;
}

.footer-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.ui-btn {
  --btn-default-bg: rgb(41, 41, 41);
  --btn-padding: 15px 20px;
  --btn-hover-bg: rgb(51, 51, 51);
  --btn-transition: .3s;
  --btn-letter-spacing: .1rem;
  --btn-animation-duration: 1.2s;
  --btn-shadow-color: rgba(0, 0, 0, 0.137);
  --btn-shadow: 0 2px 10px 0 var(--btn-shadow-color);
  --hover-btn-color: #FAC921;
  --default-btn-color: #fff;
  --font-size: 16px;
  --font-weight: 600;
  --font-family: Menlo, Roboto Mono, monospace;
}

.ui-btn {
  box-sizing: border-box;
  padding: var(--btn-padding);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--default-btn-color);
  font: var(--font-weight) var(--font-size) var(--font-family);
  background: var(--btn-default-bg);
  border: none;
  cursor: pointer;
  transition: var(--btn-transition);
  overflow: hidden;
  box-shadow: var(--btn-shadow);
}

.ui-btn span {
  letter-spacing: var(--btn-letter-spacing);
  transition: var(--btn-transition);
  box-sizing: border-box;
  position: relative;
  background: inherit;
}

.ui-btn span::before {
  box-sizing: border-box;
  position: absolute;
  content: "";
  background: inherit;
}

.ui-btn:hover, .ui-btn:focus {
  background: var(--btn-hover-bg);
}

.ui-btn:hover span, .ui-btn:focus span {
  color: var(--hover-btn-color);
}

.ui-btn.legal:hover span::before, .ui-btn.legal:focus span::before {
  animation: legalAnimation linear both var(--btn-animation-duration);
}

@keyframes legalAnimation {
  0% {
    content: "#";
  }

  5% {
    content: "-.";
  }

  10% {
    content: "^{";
  }

  15% {
    content: "-!6";
  }

  20% {
    content: "#$_è";
  }

  25% {
    content: "№*:$x";
  }

  30% {
    content: "r#{*";
  }

  35% {
    content: "@}0-?z";
  }

  40% {
    content: "?{4@%";
  }

  45% {
    content: "=.,^!6";
  }

  50% {
    content: "?ù2_@%";
  }

  55% {
    content: "^/;1}]";
  }

  60% {
    content: "?{-%:%";
    right: 0;
  }

  65% {
    content: "|{f[4";
    right: 0;
  }

  70% {
    content: "{4%0%";
    right: 0;
  }

  75% {
    content: "'1_0<";
    right: 0;
  }

  80% {
    content: "{0%";
    right: 0;
  }

  85% {
    content: "]>'";
    right: 0;
  }

  90% {
    content: "4/";
    right: 0;
  }

  95% {
    content: "2";
    right: 0;
  }

  100% {
    content: "";
    right: 0;
  }
}"""
    with open(fr"{path}//style_joueurs.css", "w", encoding="utf-8", newline="\r\n") as f:
        # Écrire le code HTML dans le fichier
        f.write(style_css_joueurs)


def creation_CSS_matchs(path):
    """
    Crée un fichier CSS pour la page présentant touts les matchs de la coupe
    du monde du site avec des styles prédéfinis.

    Parameters
    ----------
    path : String
        Chemin du répertoire où le fichier CSS sera enregistré.

    Returns
    -------
    None.

    """
    style_css_matchs = """


body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f4f4f4;
    padding: 15px;
}

h2 {
    color: #333;
    border-bottom: 2px solid #333;
    padding-bottom: 5px;
    margin-left: 10px;
}

/* ---------- Icon et Titre ---------- */
.page-title {
    text-align: center;
    padding: 30px;
    font-size: 4vw;
    color: #333;
    display: flex;
    align-items: center;
    justify-content: center;
}

.title-icon {
    width: 60px;
    margin-right: 10px;
}
/* ----------------------------------- */

/* ----------- Menu Phases ----------- */
.menu-container {
    display: flex;
    justify-content: center;
    background-color: #0470fe; /* Couleur du cercle */
    padding: 10px;
    border-radius: 25px; /* Bordure arrondie pour le cercle */
    margin: 25px;
}

.menu-item {
    cursor: pointer;
    font-size: 24px;
    color: #fff; /* Couleur du texte */
    text-decoration: none;
    padding: 5px 20px;
    display: inline-flex;
    font-weight: 700;
    transition: 0.5s;
    position: relative;
}

.menu-container:hover .menu-item {
    color: #0002;
    border-radius: 25px;
}

.menu-container .menu-item:hover {
    color: #000;
    background: transparent;
}

.menu-container .menu-item:nth-child(1):hover {
    background-color: #04fe64; /* Couleur au survol pour le premier élément */
}

.menu-container .menu-item:nth-child(2):hover {
    background-color: #ff7675; /* Couleur au survol pour le deuxième élément */
}

.menu-container .menu-item:nth-child(3):hover {
    background-color: #fe8615; /* Couleur au survol pour le troisième élément */
}

.menu-container .menu-item:nth-child(4):hover {
    background-color: #a29bfe; /* Couleur au survol pour le quatrième élément */
}

.menu-container .menu-item:nth-child(5):hover {
    background-color: #fd79a8; /* Couleur au survol pour le cinquième élément */
}

.menu-container .menu-item:nth-child(6):hover {
    background-color: #ffeaa7; /* Couleur au survol pour le sixième élément */
}

.menu-container .menu-item:nth-child(7):hover {
    background-color: #ffa7e5; /* Couleur au survol pour le sixième élément */
}

.menu-container .menu-item:nth-child(8):hover {
    background-color: #ffa7a7; /* Couleur au survol pour le sixième élément */
}

@media (max-width: 950px) {
    .menu-container {
        flex-direction: column;
        align-items: center;
    }

    .menu-item {
        margin-top: 10px;
    }
}
/* ----------------------------------- */

/* ---------- POP-UP Phases ---------- */
.modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.7);
    overflow: auto;
    z-index: 5;
}

.modal-content {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #f4f4f4;
    padding: 25px;
    border-radius: 25px;
    width: 900px; /* Fixed width */
    max-width: 80%;
    max-height: 80%; /* Adjusted max-height */
    overflow: auto; /* Added overflow for small screens */
    justify-content: center;
    align-items: center;
    text-align: center;
}

.popup {
    display: none;
}

.popup-content {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: #fff;
    padding: 20px;
    border-radius: 5px;
    width: 400px; /* Fixed width */
    max-height: 80%; /* Adjusted max-height */
    overflow: auto; /* Added overflow for small screens */
    display: flex;
    text-align: center;
    justify-content: center;
}
/* ----------------------------------- */

/* -------- Icones des EQUIPE -------- */
.teams-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
    padding: 20px;
    justify-content: center;
}

.team-card {
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
    transition: transform 0.3s, box-shadow 0.3s;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    text-align: center;
}

.team-card h2 {
    font-size: 18px;
    font-weight: bold;
    margin: 15px 0;
    color: #333;
}

.team-info {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.team-image {
    max-width: 100%;
    height: auto;
    margin-top: 10px;
}

.team-card:hover {
    transform: scale(1.1);
}
/* ----------------------------------- */

/* -------- Matchs par PHASES -------- */
.stage-container,
.team-matches-container {
    margin-bottom: 30px;
}

.stage-matches {
    display: grid;
    grid-template-columns: repeat(4, minmax(250px, 1fr));
    gap: 20px;
    text-align: center;
}

.Final .match-item {
    background-color: rgb(184, 162, 40);
}

.team-images img {
    width: 80px;
    height: auto;
    border-radius: 50%;
    margin: 5px; /* Ajustez l'espacement entre les images */
}

.match-item p {
    margin: 5px;
}

/* Ajout de flex pour aligner le contenu */
.match-item .team-images,
.match-item p {
    flex: 1;
}

@media screen and (max-width: 1200px) {
    .stage-matches {
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    }
}
/* ----------------------------------- */

/* ----- BOUTON de retour en HAUT ----- */
#scrollToTopBtn {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: #007BFF;
    color: #fff;
    border: none;
    border-radius: 15px;
    padding: 20px;
    font-size: 28px;
    cursor: pointer;
    transition: 0.3s;
    opacity: 0;
    transition: opacity 0.3s ease-in-out;
    z-index: 6;
}

#scrollToTopBtn:hover {
    background-color: #0056b3;
}
/* ----------------------------------- */

/* -------- Formes des Matchs -------- */
.match-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 15px;
    padding: 10px;
}

.match-item {
    border: none;
    padding: 10px;
    border-radius: 8px;
    background-color: #ffffff;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: all 0.25s ease-in-out;
}

.match-item:hover {
    transform: scale(1.08);
}
/* ------------------------------------ */

/* -------- Matchs par EQUIPES -------- */
.match-grid-teams {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
    gap: 15px;
    padding: 10px;
}

.match-item-teams {
    border: none;
    padding: 10px;
    border-radius: 8px;
    background-color: #fff;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
/* ------------------------------------ */

/* ----- Cards Matchs par EQUIPES ----- */

/* Positionnement central du conteneur principal */
.cardm {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    padding-bottom: 100px;
}

/* Styles de la carte principale */
.card {
    position: relative;
    width: 400px;
    height: auto;
    border-radius: 25px;
    background: whitesmoke;
    color: black;
    z-index: 4;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: .4s ease-in-out;
}

/* Styles du score */
.score {
    font-size: 3em;
    text-align: center;
    padding-top: 50px;
}

/* Styles des informations d'équipe */
.teams-info {
    display: flex;
    justify-content: space-around;
}

/* Styles au survol de la carte principale */
.card:hover {
    background-color: rgb(255, 255, 155);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card.won-match:hover {
    background-color: #8fd367;
}

.card.lost-match:hover {
    background-color: #d36264;
}

.card.won-match {
    border-top: 3px solid #8fd367;
}

.card.lost-match {
    border-top: 3px solid #d36264;
}

/* Styles des images d'équipe */
.pic img {
    width: 80px;
    height: auto;
    border-radius: 50%;
    padding-top: 25px;
}

/* Styles des équipes (home et away) */
.team-home, .team-away {
    display: flex;
    flex-direction: column;
    align-items: center;
    font-size: 1em;
    margin-top: 0.5em;
}

/* Styles de la deuxième carte et son effet au survol de la première carte */
.card2,
.card2:hover {
    position: absolute;
    display: flex;
    flex-direction: column;
    width: 398px;
    height: 80px;
    border-radius: 25px;
    background: #ebebeb;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    z-index: 3;
    transition: .4s ease-in-out;
}

.card:hover + .card2 {
    height: 300px;
    border-bottom-left-radius: 0px;
    border-bottom-right-radius: 0px;
}

/* Styles de la partie supérieure de la deuxième carte */
.upper {
    display: flex;
    flex-direction: row;
    position: relative;
    color: black;
    left: 1.8em;
    top: 0.5em;
    gap: 4em;
}

/* Styles de la partie inférieure de la deuxième carte et son effet au survol */
.lower,
.lower.stadium {
    display: flex;
    flex-direction: row;
    position: absolute;
    text-align: center;
    color: black;
    left: 3em;
    top: 1em;
    font-size: 0.7em;
    padding-top: 10px;
    transition: .4s ease-in-out;
}

.stadium, .match-date {
    font-size: large;
}

.card:hover + .card2 .lower {
    top: 20.2em;
}

/* Styles de la troisième carte et son effet au survol de la deuxième carte */
.card3,
.card3:hover {
    position: absolute;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    width: 398px;
    height: auto;
    padding-top: 5px;
    padding-bottom: 5px;
    top: 4.1em;
    left: -1.8em;
    font-size: 1.65em;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    border-bottom-left-radius: 25px;
    border-bottom-right-radius: 25px;
    background: rgb(50, 53, 205);
    color: #f4f4f4;
    transition: .4s ease-in-out;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
/* ------------------------------------ */

/* ---------- Style DARKMODE ---------- */
.dark-mode, .dark-mode .modal-content {
    background-color: rgb(16, 16, 16);
}

.dark-mode .modal h2 {
    color: #f4f4f4;
}

.dark-mode .card, .dark-mode .card2,
.dark-mode .match-item, .dark-mode .team-card {
    background-color: rgb(80, 80, 80);
}

.dark-mode .team-card {
    border: none;
}

.dark-mode p, .dark-mode .stage-container h2, .dark-mode .page-title,
.dark-mode .team-card h2, .dark-mode .card .score,
.dark-mode .match-by-team h2, .dark-mode .modal-content {
    color: #f4f4f4;
}

.dark-mode .card3 {
    background-color: #002f61;
}
/* ------------------------------------ */

/* --------- BOUTTON DARKMODE --------- */
.switch {
    position: fixed;
    top: 30px;
    right: 40px;
    z-index: 6;
    font-size: 17px;
    display: inline-block;
    width: 64px;
    height: 34px;
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #73C0FC;
  transition: .4s;
  border-radius: 30px;
}

.slider:before {
  position: absolute;
  content: "";
  height: 30px;
  width: 30px;
  border-radius: 20px;
  left: 2px;
  bottom: 2px;
  z-index: 2;
  background-color: #e8e8e8;
  transition: .4s;
}

.sun svg {
  position: absolute;
  top: 6px;
  left: 36px;
  z-index: 1;
  width: 24px;
  height: 24px;
}

.moon svg {
  fill: #73C0FC;
  position: absolute;
  top: 5px;
  left: 5px;
  z-index: 1;
  width: 24px;
  height: 24px;
}

/* .switch:hover */.sun svg {
  animation: rotate 15s linear infinite;
}

@keyframes rotate {

  0% {
    transform: rotate(0);
  }

  100% {
    transform: rotate(360deg);
  }
}

/* .switch:hover */.moon svg {
  animation: tilt 5s linear infinite;
}

@keyframes tilt {

  0% {
    transform: rotate(0deg);
  }

  25% {
    transform: rotate(-10deg);
  }

  75% {
    transform: rotate(10deg);
  }

  100% {
    transform: rotate(0deg);
  }
}

.input:checked + .slider {
  background-color: #183153;
}

.input:focus + .slider {
  box-shadow: 0 0 1px #183153;
}

.input:checked + .slider:before {
  transform: translateX(30px);
}
/* ------------------------------------ */

/* ----------- STYLE FOOTER ----------- */
footer {
  background-color: #0d1b2a;
  color: white;
  padding: 20px;
  text-align: center;
  box-shadow: 0px -5px 15px rgba(0, 0, 0, 0.2);
}

.footer-info {
  max-width: 800px;
  margin: 0 auto;
  font-size: 0.8em;
  line-height: 1.2;
}

.footer-buttons {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.ui-btn {
  --btn-default-bg: rgb(41, 41, 41);
  --btn-padding: 15px 20px;
  --btn-hover-bg: rgb(51, 51, 51);
  --btn-transition: .3s;
  --btn-letter-spacing: .1rem;
  --btn-animation-duration: 1.2s;
  --btn-shadow-color: rgba(0, 0, 0, 0.137);
  --btn-shadow: 0 2px 10px 0 var(--btn-shadow-color);
  --hover-btn-color: #FAC921;
  --default-btn-color: #fff;
  --font-size: 16px;
  --font-weight: 600;
  --font-family: Menlo, Roboto Mono, monospace;
}

.ui-btn {
  box-sizing: border-box;
  padding: var(--btn-padding);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--default-btn-color);
  font: var(--font-weight) var(--font-size) var(--font-family);
  background: var(--btn-default-bg);
  border: none;
  cursor: pointer;
  transition: var(--btn-transition);
  overflow: hidden;
  box-shadow: var(--btn-shadow);
}

.ui-btn span {
  letter-spacing: var(--btn-letter-spacing);
  transition: var(--btn-transition);
  box-sizing: border-box;
  position: relative;
  background: inherit;
}

.ui-btn span::before {
  box-sizing: border-box;
  position: absolute;
  content: "";
  background: inherit;
}

.ui-btn:hover, .ui-btn:focus {
  background: var(--btn-hover-bg);
}

.ui-btn:hover span, .ui-btn:focus span {
  color: var(--hover-btn-color);
}

.ui-btn.legal:hover span::before, .ui-btn.legal:focus span::before {
  animation: legalAnimation linear both var(--btn-animation-duration);
}

@keyframes legalAnimation {
  0% {
    content: "#";
  }

  5% {
    content: "-.";
  }

  10% {
    content: "^{";
  }

  15% {
    content: "-!6";
  }

  20% {
    content: "#$_è";
  }

  25% {
    content: "№*:$x";
  }

  30% {
    content: "r#{*";
  }

  35% {
    content: "@}0-?z";
  }

  40% {
    content: "?{4@%";
  }

  45% {
    content: "=.,^!6";
  }

  50% {
    content: "?ù2_@%";
  }

  55% {
    content: "$^;1}]";
  }

  60% {
    content: "?{-%:%";
    right: 0;
  }

  65% {
    content: "|{f[4";
    right: 0;
  }

  70% {
    content: "{4%0%";
    right: 0;
  }

  75% {
    content: "'1_0<";
    right: 0;
  }

  80% {
    content: "{0%";
    right: 0;
  }

  85% {
    content: "]>'";
    right: 0;
  }

  90% {
    content: "4/";
    right: 0;
  }

  95% {
    content: "2";
    right: 0;
  }

  100% {
    content: "";
    right: 0;
  }
}"""
    with open(fr"{path}//style_world_cup.css", "w", encoding="utf-8") as f:
        # Écrire le code HTML dans le fichier
        f.write(style_css_matchs)

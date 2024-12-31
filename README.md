<h1 align="center"> 🏉 RWC23 - WebScraping & Vizualisation

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Project Overview](#project-overview)
  - [Features](#features)
  - [Technology stack](#technology-stack)
  - [Project Structure](#project-structure)
- [Installation](#installation)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Install Dependencies](#2-install-dependencies)
  - [3. Install ChromeDriver and Chrome](#3-install-chromedriver-and-chrome)
- [Utilisation](#utilisation)
  - [1. Run the Program](#1-run-the-program)
  - [2. Fetch Data or Generate HTML](#2-fetch-data-or-generate-html)
  - [3. View the Results](#3-view-the-results)
- [Upcoming Features](#upcoming-features)
- [Contributing](#contributing)
- [Author](#author)
- [Contributors](#contributors)
- [License](#license)

## Project Overview
This project is a Python-based web scraping tool designed to provide detailed insights into the 2023 Rugby World Cup. The program allows users to easily visualize key aspects of the tournament through dynamically generated HTML pages. Data is collected from the official 2023 Rugby World Cup website using Selenium or private 'APIs'. This data is then used to create interactive web pages that display match results, team compositions, and detailed player information, including their statistics.

### Features

Knockout Stage

Visualization of the knockout stage progression (quarter-finals, semi-finals, final).

- **Team Details**
    - Displays team compositions.
    - Detailed player information (name, position, age, etc.).
    - Player statistics (tries, passes, points scored, etc.).
  
- **Match Results**
    - Displays the results of all matches in the tournament.
    - Presents scores and match details (date, place, stage)

- **Competition Progression**
    - Displays the advancement of teams from the pool stage to the final.
    - Provides visual representation of every stage (Pools, Quarters, etc.).

### Technology stack
- **Frontend**:
  - HTML
  - CSS
  - JavaScript

- **Backend**:
  - Python

- **Libraries**:
  - Selenium
  - Requests
  - Jinja2

- **Data Storage**:
  - JSON

### Project Structure

```
📦RWC23
 ┣ 📂data
 ┃ ┣ 📜matches_by_stage.json
 ┃ ┗ 📜teams_players_matches.json
 ┣ 📂src
 ┃ ┣ 📂utils
 ┃ ┃ ┣ 🐍__init__.py
 ┃ ┃ ┣ 🐍api_fetcher.py
 ┃ ┃ ┣ 🐍data_io.py
 ┃ ┃ ┣ 🐍images_builder.py
 ┃ ┃ ┣ 🐍make_html.py
 ┃ ┃ ┣ 🐍models.py
 ┃ ┃ ┗ 🐍web_driver.py
 ┃ ┣ 🐍__init__.py
 ┃ ┣ 🐍fetch_matches_api.py
 ┃ ┣ 🐍fetch_matches_selenium.py
 ┃ ┣ 🐍fetch_players_api.py
 ┃ ┣ 🐍fetch_players_selenium.py
 ┃ ┣ 🐍fetch_teams_api.py
 ┃ ┗ 🐍fetch_teams_selenium.py
 ┣ 📂web
 ┃ ┣ 📂css
 ┃ ┃ ┣ 🎨matches.css
 ┃ ┃ ┣ 🎨player.css
 ┃ ┃ ┣ 🎨switch.css
 ┃ ┃ ┣ 🎨team.css
 ┃ ┃ ┗ 🎨teams.css
 ┃ ┣ 📂js
 ┃ ┃ ┣ 📝matches.js
 ┃ ┃ ┣ 📝populate_player.js
 ┃ ┃ ┣ 📝populate_team.js
 ┃ ┃ ┗ 📝script.js
 ┃ ┣ 📂templates
 ┃ ┃ ┣ 🌐template_matches.html
 ┃ ┃ ┗ 🌐template_teams.html
 ┃ ┣ 🌐player.html
 ┃ ┗ 🌐team.html
 ┣ 📜.gitignore
 ┣ 📜LICENSE
 ┣ 📜README.md
 ┣ 📜instructions.pdf
 ┗ 🐍main.py
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/MrPaquiteau/RWC23-scraping.git
cd RWC23-scraping
```

### 2. Install Dependencies

Make sure you have Python installed (here 3.12), then install the required dependencies:
```bash
pip install -r requirements.txt
```

### 3. Install ChromeDriver and Chrome

To use Selenium for web scraping, you need to have Chrome and ChromeDriver installed.

- Visit the [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/) website to download Chrome and ChromeDriver. Make sure to select a stable version, currently 131.0.6778.204.

If Chrome or ChromeDriver are not installed in the default location, you need to add them to your PATH. You can also modify the paths directly in `src/utils/web_driver.py`.

To add ChromeDriver to your PATH, use the following command:
```bash
export PATH=$PATH:/path/to/chromedriver
```

To add Chrome to your PATH, use the following command:
```bash
export PATH=$PATH:/path/to/chrome
```

Alternatively, you can edit the `src/utils/web_driver.py` file to specify the paths directly:
```python
service = Service("/path/to/chromedriver")
options.binary_location = "/path/to/chrome"
```

## Utilisation
### 1. Run the Program
To run the program, execute the main.py:
```bash
python main.py
```
### 2. Fetch Data or Generate HTML
When you run the program, you will be prompted to choose one of the following options:
1. Fetch data using Selenium (Almost 20min).
2. Fetch data from the API (Almost 2min).
3. Generate HTML files (once the data is stored).

### 3. View the Results
Once the HTML pages are generated, you can view them in your browser. You will be prompted to choose which page to view (Teams or Matches).

## Upcoming Features
- **iOS Application**
    - Develop a little iOS application using Swift.
    - Display match results, team details, and player statistics.
  
## Contributing
If you would like to contribute to this project, please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## Author
Romain TROILLARD | [MrPaquiteau](https://github.com/MrPaquiteau)

## Contributors
- Dorian RELAVE | [Legolaswash](https://github.com/Legolaswash) - Contributed to the first commit (v1.0)
- Moetaz BEN-AMHED - Contributed to the first commit (v1.0)
- Abder-Rahman BOUAOUINA - Contributed to the first commit (v1.0)

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

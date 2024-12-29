import requests


BASE_URL = "https://www.rugbyworldcup.com/2023"
TEAM_FLAG_URL_PATTERN = "https://www.rugbyworldcup.com/rwc2023-resources/prod/rwc2023_v6.8.0/i/svg-files/elements/bg/teams/flag-{}.png"
TEAM_SHAPE_URL_PATTERN = "https://www.rugbyworldcup.com/rwc2023-resources/prod/rwc2023_v6.8.0/i/svg-files/elements/bg/teams/country-{}.svg"
TEAM_LOGO_URL_PATTERN = "https://www.rugbyworldcup.com/rwc2023-resources/prod/rwc2023_v6.8.0/i/svg-files/elements/bg/teams/union-emblem-{}.svg"

def build_team_url(country):
    """Construit l'URL de la page de l'équipe."""
    return f"{BASE_URL}/teams/{country.replace(' ', '-').lower()}"

def build_flag_url(code):
    """Construit l'URL du drapeau de l'équipe."""
    return TEAM_FLAG_URL_PATTERN.format(code.lower()) if code else None

def build_shape_url(country):
    """Construit l'URL de l'image de l'équipe."""
    return TEAM_SHAPE_URL_PATTERN.format(country.replace(' ', '-').lower())

def build_logo_url(country):
    """Construit l'URL du logo de l'équipe."""
    return TEAM_LOGO_URL_PATTERN.format(country.replace(' ', '-').lower()), TEAM_LOGO_URL_PATTERN.format(f"{country.replace(' ', '-').lower()}-alt")

def is_url_valid(url):
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False
import requests
import json
from concurrent.futures import ThreadPoolExecutor
import time

# Configuration
BASE_URL = "https://api.wr-rims-prod.pulselive.com/rugby/v3/"
TEAM_FLAG_URL_PATTERN = "https://www.rugbyworldcup.com/rwc2023-resources/prod/rwc2023_v6.6.0/i/elements/team-badges/{}.png"
TEAM_IMAGE_URL_PATTERN = "https://www.rugbyworldcup.com/rwc2023-resources/prod/rwc2023_v6.8.0/i/svg-files/elements/bg/teams/country-{}.svg"

def fetch_teams():
    """
    Fetches the list of teams participating in the 2023 World Cup.

    Returns
    -------
    list
        A list of teams.
    """
    url = f"{BASE_URL}event/1893/teams"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["teams"]

def fetch_team_squad(team_id):
    """
    Fetches the list of players for a team.

    Parameters
    ----------
    team_id : int
        The ID of the team.

    Returns
    -------
    list
        A list of players.
    """
    url = f"{BASE_URL}event/1893/squad/{team_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["players"]

def fetch_player_stats(player_id):
    """
    Fetches statistics for a player.

    Parameters
    ----------
    player_id : int
        The ID of the player.

    Returns
    -------
    dict
        A dictionary containing the player's statistics.
    """
    url = f"{BASE_URL}stats/player/{player_id}/EVENT?event=1893"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def extract_player_info(player_data):
    """
    Extracts basic information for a player.

    Parameters
    ----------
    player_data : dict
        The data of the player.

    Returns
    -------
    dict
        A dictionary containing the player's basic information.
    """
    player = player_data["player"]
    return {
        'id': player['id'],
        'name': player['name']['display'],
        'age': player['age']['years'],
        'height': player['height'],
        'weight': player['weight'],
        'hometown': player['pob'],
        'photo': f'https://www.rugbyworldcup.com/rwc2023/person-images-site/player-profile/{player['id']}.png'
    }

def extract_player_stats(player_data):
    """
    Extracts statistics for a player.

    Parameters
    ----------
    player_data : dict
        The data of the player.

    Returns
    -------
    dict
        A dictionary containing the player's statistics.
    """
    player_stats = player_data['extendedStats']
    stats = {
        'Kick from hand': player_stats['KicksFromHand'],
        'Runs': player_stats['Runs'],
        'Passes': player_stats['Passes'],
        'Offload': player_stats['Offload'],
        'Tackles': f"{player_stats['Tackles']} ({player_stats['TackleSuccess']*100}%)",
        'Carries': player_stats['Carries'],
        'Metres made': player_stats['Metres'],
        'Defenders beaten': player_stats['DefendersBeaten'],
        'Clean breaks': player_stats['CleanBreaks'],
        'Handling error': player_stats['HandlingError'],
        'Red cards': player_data['stats']['RedCards'],
        'Yellow cards': player_data['stats']['YellowCards'],
    }
    return {k: str(int(v)) if isinstance(v, (int, float)) else v for k, v in stats.items()}


def process_team(team):
    """
    Processes data for a team.

    Parameters
    ----------
    team : dict
        The data of the team.

    Returns
    -------
    dict
        A dictionary containing the team's data and player statistics.
    """
    team_name = team['name']
    team_id = team['id']
    team_code = team['abbreviation']
    team_flag_url = TEAM_FLAG_URL_PATTERN.format(team_code)
    team_image_url = TEAM_IMAGE_URL_PATTERN.format(team_name.replace(' ', '-').lower())

    squad = fetch_team_squad(team_id)
    player_ids = [player['player']['id'] for player in squad]

    with ThreadPoolExecutor(max_workers=5) as executor:
        player_stats_futures = {executor.submit(fetch_player_stats, player_id): player_id for player_id in player_ids}
        players = []
        for future in player_stats_futures:
            player_id = player_stats_futures[future]
            try:
                data = future.result()
                player_info = extract_player_info(data)
                player_info['stats'] = extract_player_stats(data)
                players.append(player_info)
                # print(f"Données pour le joueur {player_id} récupérées.")
            except Exception as e:
                print(f"Erreur pour le joueur {player_id} : {e}")

    return {
        'name': team_name,
        'id': team_id,
        'code': team_code,
        'flag': team_flag_url,
        'image': team_image_url,
        'players': players
    }

def main():
    """
    Main function to fetch and process team data, then save it to a JSON file.
    """
    teams = fetch_teams()
    with ThreadPoolExecutor(max_workers=5) as executor:
        team_futures = {executor.submit(process_team, team): team['name'] for team in teams}
        teams_data = {}
        for future in team_futures:
            start = time.time()
            team_name = team_futures[future]
            try:
                teams_data[team_name] = future.result()
            except Exception as e:
                print(f"Error for team {team_name}: {e}")
            end = time.time()
            print(f"Data for team {team_name} fetched. ({end-start:.2f})")

    with open("data.json", "w") as f:
        json.dump(teams_data, f, indent=4)

if __name__ == '__main__':
    main()
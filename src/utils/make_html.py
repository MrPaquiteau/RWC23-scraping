from jinja2 import Environment, FileSystemLoader
import json
import os

def make_teams_html(env, data):
    template = env.get_template('template_teams.html')
    output = template.render(teams=data)

    with open('web/teams.html', 'w') as f:
        f.write(output)
    print("Teams HTML created")

def make_matches_html(env, data):
    with open('data/matches_by_stage.json') as f:
        matches_by_stage = json.load(f)

    template = env.get_template('template_matches.html')
    output = template.render(matches_by_stage=matches_by_stage, teams_matches=data)

    with open('web/matches.html', 'w') as f:
        f.write(output)
    print("Matches HTML created")

def build():
    env = Environment(loader=FileSystemLoader('web/templates'))
    if os.path.exists('data/teams_players_matches.json'):
        with open('data/teams_players_matches.json') as f:
            data = json.load(f)
        make_teams_html(env, data)
        make_matches_html(env, data)
    else:
        print("Data file not found. Run fetch_data_from_api() or fetch_data_from_selenium() first.")
        return
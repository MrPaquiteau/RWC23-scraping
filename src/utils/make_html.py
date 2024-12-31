from jinja2 import Environment, FileSystemLoader
import json


env = Environment(loader=FileSystemLoader('web/templates'))
with open('data/teams_players_matches.json') as f:
    data = json.load(f)

def make_teams_html():
    template = env.get_template('template_teams.html')
    output = template.render(teams=data)

    with open('web/teams.html', 'w') as f:
        f.write(output)
    print("Teams HTML created")

def make_matches_html():
    with open('data/matches_by_stage.json') as f:
        matches_by_stage = json.load(f)

    template = env.get_template('template_matches.html')
    output = template.render(matches_by_stage=matches_by_stage, teams_matches=data)

    with open('web/matches.html', 'w') as f:
        f.write(output)
    print("Matches HTML created")


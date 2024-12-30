from jinja2 import Environment, FileSystemLoader
import json

with open('../data/teams_api.json') as f:
    teams = json.load(f)

env = Environment(loader=FileSystemLoader('../templates'))
template = env.get_template('template_teams.html')

output = template.render(teams=teams)

with open('../web/teams.html', 'w') as f:
    f.write(output)
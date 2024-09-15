import requests
from bs4 import BeautifulSoup
import random

base_url = "https://www.procyclingstats.com/"
url = 'https://www.procyclingstats.com/teams.php'

def random_player():
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    #teams = [team.text for team in soup.select('ul.list li div a')]
    team_links = [a['href'] for a in soup.select('ul.list li div a') if 'href' in a.attrs]

    #cycling_teams = [i for i in teams if i != ""]

    #random_team = random.choice(cycling_teams)

    #print(f'Randomly selected team: {random_team}')

    random_team_link = random.choice(team_links)
    new_url = base_url + random_team_link

    team_response = requests.get(new_url)
    team_soup = BeautifulSoup(team_response.content, "html.parser")

    title_tag = team_soup.find('title')
    title_text = title_tag.get_text(strip=True) if title_tag else 'No title found'
    team_name = title_text.split(' 2024')[0] if ' 2024' in title_text else title_text

    rider_names = [span.get_text(strip=True) for span in team_soup.select('ul.photos li span')]

    #print("team:", team_name)
    #print("number of riders:", len(rider_names))

    random_rider = random.choice(rider_names)
    #print("random rider:", random_rider)

    return team_name, random_rider



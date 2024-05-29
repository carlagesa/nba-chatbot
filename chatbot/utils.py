# chatbot/utils.py
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder, playercareerstats
import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def get_team_id(team_name):
    all_teams = teams.get_teams()
    for team in all_teams:
        if team_name.lower() in team['full_name'].lower():
            return team['id']
    return None

def get_live_score(team_name):
    team_id = get_team_id(team_name)
    if not team_id:
        return "Team not found."

    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id)
    games = gamefinder.get_dict()['resultSets'][0]['rowSet']
    if not games:
        return "No games found for this team."

    latest_game = games[0]
    return f"{latest_game[4]} vs {latest_game[6]}: {latest_game[21]} - {latest_game[22]}"

def get_player_stats(player_name):
    from nba_api.stats.static import players
    player_dict = players.get_players()
    player = [p for p in player_dict if player_name.lower() in p['full_name'].lower()]
    if not player:
        return "Player not found."

    player_id = player[0]['id']
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    career_stats = career.get_dict()
    latest_stats = career_stats['resultSets'][0]['rowSet'][-1]
    stats = {
        "points_per_game": latest_stats[3],
        "rebounds_per_game": latest_stats[5],
        "assists_per_game": latest_stats[6]
    }
    return stats

def get_openai_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

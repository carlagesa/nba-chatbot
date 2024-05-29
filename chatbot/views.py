# chatbot/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .utils import get_openai_response, get_live_score, get_player_stats

def chatbot_view(request):
    return render(request, 'chatbot/chat.html')

def get_response(request):
    user_message = request.GET.get('message')

    if "score" in user_message.lower():
        team = user_message.split()[-1]  # Simplistic extraction; improve as needed
        score = get_live_score(team)
        bot_response = f"The current score for {team} is {score}."
    elif "stats" in user_message.lower():
        player = ' '.join(user_message.split()[3:])  # Simplistic extraction; improve as needed
        stats = get_player_stats(player)
        bot_response = (f"The latest stats for {player} are: "
                        f"Points per game: {stats['points_per_game']}, "
                        f"Rebounds per game: {stats['rebounds_per_game']}, "
                        f"Assists per game: {stats['assists_per_game']}.")
    else:
        bot_response = get_openai_response(f"User: {user_message}\nBot:")

    return JsonResponse({'response': bot_response})

import requests
import os
from django.http import JsonResponse
from music_suggester.settings import CLIENT_ID, CLIENT_SECRET


def get_spotify_token():
    # Faz uma requisição para gerar um token do spotify
    global spotify_token
    try:
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
            },
        )
        response.raise_for_status()
        token_info = response.json()
        spotify_token = token_info["access_token"]  # Salva o token na variável global
        return spotify_token
    except requests.exceptions.RequestException as e:
        return JsonResponse(
            {"error": "Failed to retrieve Spotify token", "details": f"{e}"}, status=500
        )

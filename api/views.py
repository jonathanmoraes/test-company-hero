import requests
import dotenv
import os
from django.http import JsonResponse
from services.weather_service import get_temperature
from services.spotify_service import get_spotify_token
from rest_framework.decorators import api_view
from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, this is the home page!")

# Utilizando Dotenv para manipular dados sensíveis
dotenv.load_dotenv(dotenv.find_dotenv())

# Variavel global para salvar o token do spotify
spotify_token = None

@api_view(['GET'])
def get_playlist(request, city):
    global spotify_token
    client_id = os.getenv("spotify_client_id")
    client_secret = os.getenv("spotify_client_secret")

    if spotify_token is None:
        spotify_token = get_spotify_token(client_id, client_secret)
        if spotify_token is None:
            return JsonResponse({"error": "Failed to obtain Spotify token"}, status=500)

    try:
        temperature = get_temperature(city)
        # Verifica se a resposta é um JsonResponse (erro)
        if isinstance(temperature, JsonResponse):
            return temperature

        genre = def_genre(temperature)

        # Tenta obter a playlist da API do Spotify
        spotify_response = requests.get(
            f"https://api.spotify.com/v1/browse/categories/{genre}/playlists",
            headers={"Authorization": f"Bearer {spotify_token}"},
        )

        # Verifica se o token é inválido
        if spotify_response.status_code == 401:  # Token inválido
            spotify_token = get_spotify_token(client_id, client_secret)
            if spotify_token is None:
                return JsonResponse(
                    {"error": "Failed to obtain Spotify token"}, status=500
                )

            # Tenta a requisição novamente com o novo token
            # Esse codigo existe por conta do tempo que um token do spotify fica valido
            spotify_response = requests.get(
                f"https://api.spotify.com/v1/browse/categories/{genre}/playlists",
                headers={"Authorization": f"Bearer {spotify_token}"},
            )
            spotify_response.raise_for_status()
        return extract_playlist_data(spotify_response.json())

    # tratamento de possiveis exceções
    except requests.exceptions.RequestException as e:
        return JsonResponse(
            {"error": "Failed to retrieve playlist from Spotify", "details": str(e)},
            status=500,
        )
    except (KeyError, IndexError) as e:
        return JsonResponse(
            {
                "error": "Unexpected data format received from Spotify",
                "details": str(e),
            },
            status=500,
        )
    except Exception as e:
        return JsonResponse(
            {"error": "An unexpected error occurred", "details": str(e)}, status=500
        )


def def_genre(temperature):
    # Define o genero da musica de acordo com a temperatura
    if temperature > 25:
        genre = "pop"
    elif 10 <= temperature <= 25:
        genre = "rock"
    else:
        genre = "classical"
    return genre


def extract_playlist_data(spotify_data):
    # Formata os dados da playlist para retornar apenas as informações relevantes a principio.
    spotify_playlist = spotify_data["playlists"]["items"][0]

    playlist_data = {
        "name": spotify_playlist["name"],
        "description": spotify_playlist.get("description", "No description available"),
        "spotify_external_url": spotify_playlist["external_urls"]["spotify"],
        "album_image_url": spotify_playlist["images"][0]["url"]
        if spotify_playlist["images"]
        else None,
    }
    return JsonResponse(playlist_data)

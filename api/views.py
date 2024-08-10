import requests
import dotenv
import os
from django.http import JsonResponse

# Utilizando Dotenv para manipular dados sensíveis
dotenv.load_dotenv(dotenv.find_dotenv())
# Variavel global para salvar o token do spotify
spotify_token = None


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
            spotify_response = requests.get(
                f"https://api.spotify.com/v1/browse/categories/{genre}/playlists",
                headers={"Authorization": f"Bearer {spotify_token}"},
            )
            spotify_response.raise_for_status()
        return extract_playlist_data(spotify_response.json())
    
    #tratamento de possiveis exceções 
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


def get_temperature(city):
    # Tenta obter a temperatura da cidade
    openweathermap_app_id = os.getenv("openweathermap_app_id")
    try:
        weather_response = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&limit=1&appid={openweathermap_app_id}&units=metric"
        )
        weather_data = weather_response.json()

        # Verifica se a cidade não foi encontrada
        if weather_data.get("cod") == "404":
            return JsonResponse(
                {
                    "error": f"City '{city}' not found.",
                    "details": weather_data.get("message"),
                },
                status=404,
            )

        # Se a cidade for encontrada, retorna a temperatura
        temperature = weather_data["main"]["temp"]
        return temperature
    
    except requests.exceptions.RequestException as e:
        return JsonResponse(
            {
                "error": f"Failed to retrieve temperature for {city} from OpenWeatherMap.",
                "details": str(e),
            },
            status=500,
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


def get_spotify_token(client_id, client_secret):
    # Faz uma requisição para gerar um token do spotify
    global spotify_token
    try:
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
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

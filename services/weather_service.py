import requests
import os
from django.http import JsonResponse


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

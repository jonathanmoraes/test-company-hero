import unittest
import os
import django
import requests
from unittest.mock import patch, MagicMock
from django.http import JsonResponse
from services.weather_service import get_temperature

# Configure o Django para rodar testes
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_suggester.settings')
django.setup()

class TestWeatherService(unittest.TestCase):

    @patch('requests.get')
    def test_get_temperature_success(self, mock_get):
        # Configura o mock da resposta do OpenWeatherMap
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "main": {"temp": 25}
        }
        mock_get.return_value = mock_response

        # Chama a função
        temperature = get_temperature('London')

        # Verifica o resultado
        self.assertEqual(temperature, 25)

    @patch('requests.get')
    def test_get_temperature_city_not_found(self, mock_get):
        # Configura o mock da resposta do OpenWeatherMap para cidade não encontrada
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {"cod": "404", "message": "city not found"}
        mock_get.return_value = mock_response

        # Chama a função
        response = get_temperature('UnknownCity')

        # Verifica o resultado
        self.assertEqual(response.status_code, 404)
        # Usa o atributo content para verificar o JSON retornado
        self.assertEqual(response.content.decode('utf-8'), '{"error": "City \'UnknownCity\' not found.", "details": "city not found"}')

    @patch('requests.get')
    def test_get_temperature_request_exception(self, mock_get):
        # Configura o mock para lançar uma exceção de RequestException
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        # Chama a função
        response = get_temperature('London')

        # Verifica o resultado
        self.assertEqual(response.status_code, 500)
        # Usa o atributo content para verificar o JSON retornado
        self.assertEqual(response.content.decode('utf-8'), '{"error": "Failed to retrieve temperature for London from OpenWeatherMap.", "details": "Network error"}')

if __name__ == '__main__':
    unittest.main()

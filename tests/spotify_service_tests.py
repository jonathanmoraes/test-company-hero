import unittest
import requests
import os
import django
from unittest.mock import patch, MagicMock
from django.http import JsonResponse
from services.spotify_service import get_spotify_token

# Configura o Django para rodar testes
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_suggester.settings')
django.setup()

class TestSpotifyService(unittest.TestCase):

    @patch('requests.post')
    def test_get_spotify_token_success(self, mock_post):
        # Configura o mock da resposta do Spotify token
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'access_token': 'mock_token'}
        mock_post.return_value = mock_response

        # Chama a função
        token = get_spotify_token('mock_client_id', 'mock_client_secret')

        # Verifica o resultado
        self.assertEqual(token, 'mock_token')

    @patch('requests.post')
    def test_get_spotify_token_request_exception(self, mock_post):
        # Configura o mock para lançar uma exceção de RequestException
        mock_post.side_effect = requests.exceptions.RequestException("Network error")

        # Chama a função
        response = get_spotify_token('mock_client_id', 'mock_client_secret')

        # Verifica o resultado
        self.assertEqual(response.status_code, 500)
        # Usa o atributo content para verificar o JSON retornado
        self.assertEqual(response.content.decode('utf-8'), '{"error": "Failed to retrieve Spotify token", "details": "Network error"}')

if __name__ == '__main__':
    unittest.main()

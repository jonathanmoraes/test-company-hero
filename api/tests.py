import unittest
import os
import django
import requests
from unittest.mock import patch, MagicMock
from django.http import JsonResponse
import json

from .views import get_playlist, get_temperature, def_genre, get_spotify_token, extract_playlist_data

# Configure o Django para rodar testes
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_suggester.settings')
django.setup()

class TestMusicSuggester(unittest.TestCase):

    @patch('api.views.get_temperature')
    @patch('api.views.get_spotify_token')
    @patch('requests.get')
    def test_get_playlist_success(self, mock_requests_get, mock_get_spotify_token, mock_get_temperature):
        # Configura o mock do token
        mock_get_spotify_token.return_value = 'mock_token'
        
        # Configura o mock da temperatura
        mock_get_temperature.return_value = 30
        
        # Configura o mock da resposta do Spotify
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'playlists': {
                'items': [{
                    'name': 'Summer Hits',
                    'description': 'Hot hits for a hot day!',
                    'external_urls': {'spotify': 'https://spotify.com/playlist'},
                    'images': [{'url': 'https://image.url'}]
                }]
            }
        }
        mock_requests_get.return_value = mock_response
        
        # Cria uma requisição mock
        request = MagicMock()
        
        # Chama a função
        response = get_playlist(request, 'city_name')
        
        # Decodifique o conteúdo da resposta JSON
        response_content = json.loads(response.content)
        
        # Verifica o resultado
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_content, {
            'name': 'Summer Hits',
            'description': 'Hot hits for a hot day!',
            'spotify_external_url': 'https://spotify.com/playlist',
            'album_image_url': 'https://image.url'
        })

    @patch('requests.get')
    def test_get_temperature_city_not_found(self, mock_requests_get):
        # Configura o mock da resposta do OpenWeatherMap para cidade não encontrada
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {'cod': '404', 'message': 'city not found'}
        mock_requests_get.return_value = mock_response
        
        # Chama a função
        response = get_temperature('unknown_city')
        
        # Decodifique o conteúdo da resposta JSON
        response_content = json.loads(response.content)
        
        # Verifica o resultado
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_content, {
            'error': "City 'unknown_city' not found.",
            'details': 'city not found'
        })

    @patch('requests.post')
    def test_get_spotify_token_success(self, mock_requests_post):
        # Configura o mock da resposta do Spotify token
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'access_token': 'mock_token'}
        mock_requests_post.return_value = mock_response
        
        # Chama a função
        token = get_spotify_token('client_id', 'client_secret')
        
        # Verifica o resultado
        self.assertEqual(token, 'mock_token')

    def test_def_genre(self):
        # Testa a função def_genre com diferentes temperaturas
        self.assertEqual(def_genre(30), 'pop')
        self.assertEqual(def_genre(20), 'rock')
        self.assertEqual(def_genre(5), 'classical')

if __name__ == '__main__':
    unittest.main()

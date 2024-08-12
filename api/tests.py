import unittest
import os
import django
from unittest.mock import patch, MagicMock
from django.http import JsonResponse
from django.test import RequestFactory
import json

from .views import get_playlist, def_genre

# Configure o Django para rodar testes
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'music_suggester.settings')
django.setup()

class TestMusicSuggester(unittest.TestCase):

    def setUp(self):
        self.factory = RequestFactory()

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
        
        # Cria uma requisição real usando RequestFactory
        request = self.factory.get('/playlist/city_name/')
        
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

    def test_def_genre(self):
        # Testa a função def_genre com diferentes temperaturas
        self.assertEqual(def_genre(30), 'pop')
        self.assertEqual(def_genre(20), 'rock')
        self.assertEqual(def_genre(5), 'classical')

if __name__ == '__main__':
    unittest.main()

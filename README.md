
# Music Suggester

Music Suggester é uma aplicação Django que sugere playlists do Spotify com base na temperatura atual de uma cidade. A aplicação utiliza a API do OpenWeatherMap para obter a temperatura e a API do Spotify para buscar playlists apropriadas.

## Funcionalidades

- **Obter Playlist:** Baseado na temperatura da cidade, a aplicação sugere uma playlist do Spotify.

## Pré-requisitos

- Python 3.11 ou superior
- Django
- Requests
- python-dotenv

## Configuração

  **1. Clone o repositório:**

    git clone https://github.com/yourusername/music-suggester.git
    cd music-suggester

  **2. Crie um ambiente virtual e ative-o:**

    Copiar código
    python -m venv venv
    source venv/bin/activate  # Para Windows use: venv\Scripts\activate

  **3. Instale as dependências:**

    Copiar código
    pip install -r requirements.txt

  **4. Configure variáveis de ambiente:**

  Crie um arquivo .env na raiz do projeto e adicione suas credenciais da API:

    dotenv
    Copiar código
    spotify_client_id=YOUR_SPOTIFY_CLIENT_ID
    spotify_client_secret=YOUR_SPOTIFY_CLIENT_SECRET
    openweathermap_app_id=YOUR_OPENWEATHERMAP_APP_ID
  
## Estrutura
* API: onde esta localizado o view pricipal do enpoint e os testes do mesmo.
* Music_suggester o projeto em si onde esta localizado as cofigurações e a url do endpoint.
* Services: estão localizadas as views de cada service externo utlizado no projeto no caso Spotify e OpenWeatherMap.
* Tests: Onde estão localizados os testes de cada service separados.
## Executar o Projeto
**1. Crie o arquivo dotenv **
  variáveis necessarias
    spotify_client_id = "your spotify_client_id" 
    spotify_client_secret = "your spotify_client_secret"
    openweathermap_app_id = "your openweathermap_app_id"

**2. Execute as migrações:**

    Copiar código
    python manage.py migrate

**3. Inicie o servidor Django:**

    Copiar código
    python manage.py runserver
    A aplicação estará disponível em http://localhost:8000/.

## Testes
Para rodar os testes, certifique-se de que as variáveis de ambiente estão configuradas corretamente e então execute:

    Roda os testes do service spotify_service.py:
    'python -m unittest .\tests\spotify_service_tests.py'

    Roda os testes do service weather_service.py:
    'python -m unittest .\tests\weather_service_tests.py'
    
    Roda os testes do view pricipal que faz o tratamento dos dados da requisição 
    pricipal do music_suggester:
    'python manage.py test'

    
Estrutura do Código

    views.py: Contém as funções principais para obter playlists.
    tests.py: Contém testes unitários para garantir o correto funcionamento das funções.
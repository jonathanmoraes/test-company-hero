# test-company-hero
Test for the development of a music suggestion api based on the temperature of a city

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

    ```bash
    git clone https://github.com/yourusername/music-suggester.git
    cd music-suggester

  **2. Crie um ambiente virtual e ative-o:**

    ```bash
    Copiar código
    python -m venv venv
    source venv/bin/activate  # Para Windows use: venv\Scripts\activate

  **3. Instale as dependências:**

    ```bash
    Copiar código
    pip install -r requirements.txt

  **4. Configure variáveis de ambiente:**

  Crie um arquivo .env na raiz do projeto e adicione suas credenciais da API:

    dotenv
    Copiar código
    spotify_client_id=YOUR_SPOTIFY_CLIENT_ID
    spotify_client_secret=YOUR_SPOTIFY_CLIENT_SECRET
    openweathermap_app_id=YOUR_OPENWEATHERMAP_APP_ID
  
## Executar o Projeto

**1. Execute as migrações:**

    ```bash
    Copiar código
    python manage.py migrate

**2. Inicie o servidor Django:**

    ```bash
    Copiar código
    python manage.py runserver
    A aplicação estará disponível em http://localhost:8000/.

## Testes
Para rodar os testes, certifique-se de que as variáveis de ambiente estão configuradas corretamente e então execute:

    ```bash
    Copiar código
    python -m unittest discover -s api/tests
    
Estrutura do Código

    views.py: Contém as funções principais para obter playlists, temperatura, determinar gênero musical e gerar tokens do Spotify.
    tests.py: Contém testes unitários para garantir o correto funcionamento das funções.
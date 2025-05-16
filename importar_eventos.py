import os
import django
from dotenv import load_dotenv

# Carregar as variáveis de ambiente
load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

import requests
from requests.auth import HTTPBasicAuth
from django.utils import timezone
from eventos.models import Eventos

# Suas credenciais OAuth
CLIENT_ID = os.getenv('TICKETMASTER_CLIENT_ID')       # seu Consumer Key
CLIENT_SECRET = os.getenv('TICKETMASTER_CLIENT_SECRET')  # seu Consumer Secret

def obter_access_token(client_id, client_secret):
    url_token = 'https://oauth.ticketmaster.com/oauth/token'
    auth = HTTPBasicAuth(client_id, client_secret)
    data = {'grant_type': 'client_credentials'}

    response = requests.post(url_token, auth=auth, data=data)
    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print(f"Erro ao obter token: {response.status_code} - {response.text}")
        return None

def importar_eventos():
    token = obter_access_token(CLIENT_ID, CLIENT_SECRET)
    if not token:
        print("Não foi possível obter o token de acesso. Abortando importação.")
        return

    headers = {
        'Authorization': f'Bearer {token}'
    }

    params = {
        'countryCode': 'BR',
        'size': 100
    }

    response = requests.get('https://app.ticketmaster.com/discovery/v2/events.json', headers=headers, params=params)

    if response.status_code != 200:
        print(f"Erro ao buscar eventos: {response.status_code} - {response.text}")
        return

    data = response.json()
    eventos = data.get('_embedded', {}).get('events', [])

    for evento in eventos:
        nome = evento.get('name')
        data_hora = evento.get('dates', {}).get('start', {}).get('dateTime')
        imagem_url = evento.get('images', [])[0].get('url') if evento.get('images') else ''
        legenda = evento.get('info', 'Sem descrição')

        Eventos.objects.update_or_create(
            nome=nome,
            defaults={
                'data': timezone.make_aware(timezone.datetime.fromisoformat(data_hora)) if data_hora else None,
                'imagem': imagem_url,
                'legenda': legenda
            }
        )

    print(f"{len(eventos)} eventos importados com sucesso!")

if __name__ == '__main__':
    importar_eventos()
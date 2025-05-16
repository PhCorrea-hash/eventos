import os
import requests
import django
from dotenv import load_dotenv
from django.utils import timezone

# Carregar as variáveis de ambiente
load_dotenv()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from eventos.models import Eventos

API_KEY = os.getenv('TICKETMASTER_API_KEY')
BASE_URL = 'https://app.ticketmaster.com/discovery/v2/events.json'


def importar_eventos():
    params = {
        'apikey': API_KEY,
        'countryCode': 'BR',  # Apenas eventos no Brasil
        'size': 100  # Quantidade máxima de eventos por página
    }

    response = requests.get(BASE_URL, params=params)
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

        # Criar ou atualizar o evento no banco de dados
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
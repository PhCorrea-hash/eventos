import requests
from eventos.models import Eventos
from django.conf import settings
from django.utils import timezone

def buscar_eventos_ticketmaster():
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        'apikey': settings.IMPORT_KEY,  # Alterado para usar IMPORT_KEY
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        eventos_data = response.json()['_embedded']['events']
        return eventos_data
    else:
        raise Exception(f"Erro ao buscar eventos: {response.status_code}")

def salvar_eventos(eventos_data):
    for evento_data in eventos_data:
        # Verifica se o evento já existe no banco de dados
        evento, created = Eventos.objects.get_or_create(
            nome=evento_data['name'],  # Assumindo que 'name' é o nome do evento
            defaults={
                'descricao': evento_data.get('description', ''),
                'data': timezone.datetime.strptime(evento_data['dates']['start']['localDate'], '%Y-%m-%d'),
                'imagem': evento_data['_embedded']['images'][0]['url'] if evento_data.get('_embedded') else '',
                'link': evento_data['url'],
                'publicada': True,
            }
        )
        if created:
            print(f"Evento '{evento.nome}' criado com sucesso.")
        else:
            print(f"Evento '{evento.nome}' já existe.")

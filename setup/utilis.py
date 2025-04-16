import requests
from eventos.models import Eventos

def buscar_eventos_ticketmaster():
    url = 'https://app.ticketmaster.com/discovery/v2/events.json'
    params = {
        'apikey': 'SUA_API_KEY',
        'countryCode': 'BR',
        'size': 20
    }

    response = requests.get(url, params=params)
    data = response.json()

    eventos = data.get('_embedded', {}).get('events', [])
    return eventos

def salvar_eventos(eventos):
    for evento in eventos:
        nome = evento['name']
        data = evento['dates']['start'].get('localDate', '')
        url = evento.get('url', '')

        Eventos.objects.update_or_create(
            nome=nome,
            defaults={'data': data, 'url': url}
        )

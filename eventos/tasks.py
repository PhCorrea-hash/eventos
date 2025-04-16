from celery import shared_task
from setup.utilis import buscar_eventos_ticketmaster, salvar_eventos

@shared_task
def importar_eventos_ticketmaster():
    eventos = buscar_eventos_ticketmaster()
    salvar_eventos(eventos)
from django.shortcuts import render
from eventos.models import Eventos
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Q
from django.utils.timezone import localtime
import requests
from django.conf import settings
from .tasks import importar_eventos_ticketmaster

def index(request):

    eventos = Eventos.objects.order_by("data").filter(publicada=True)
    eventos_destaque = Eventos.objects.filter(publicada=True, destaque=True).order_by('data')[:3]
    return render(request, 'index.html', {
        "cards": eventos, 
        "cards_destaque": eventos_destaque
                   })

def cloudinary_webhook(request):
    if request.method == 'POST':
        # Lógica para processar os dados do webhook
        # Você pode acessar os dados do webhook com request.body ou request.POST
        # Por exemplo:
        data = request.body
        print("Webhook recebido:", data)

        # Responda com um status HTTP 200 (OK)
        return JsonResponse({'status': 'ok'}, status=200)

    # Se o método não for POST, retornar um erro
    return JsonResponse({'error': 'Método não permitido'}, status=405)

def eventos_api(request):
    eventos = Eventos.objects.all().values('nome', 'descricao', 'imagem')
    data = [
        {
            'nome': e['nome'],
            'descricao': e['descricao'],
            'imagem': request.build_absolute_uri(e['imagem']),
        }
        for e in eventos
    ]
    return JsonResponse(data, safe=False)

def buscar_eventos(request):
    termo = request.GET.get('q', '')
    resultados = Eventos.objects.filter(
        Q(nome__icontains=termo) | Q(descricao__icontains=termo)
    ) if termo else Eventos.objects.filter(publicada=True)

    data = []
    for evento in resultados:
        data.append({
            'nome': evento.nome,
            'descricao': evento.descricao,
            'legenda': evento.legenda,
            'data': localtime(evento.data).strftime('%d/%m/%Y'),  # formata a data
            'link': evento.link,
            'imagem': evento.imagem.url if evento.imagem else '',
        })

    return JsonResponse(data, safe=False)

@csrf_exempt
def webhook_importar_eventos(request):
    token = request.headers.get("Authorization")

    if token != f"Token {settings.IMPORT_TOKEN}":
        return JsonResponse({"error": "Unauthorized"}, status=401)

    importar_eventos_ticketmaster.delay()
    return JsonResponse({"status": "Importação iniciada"})
